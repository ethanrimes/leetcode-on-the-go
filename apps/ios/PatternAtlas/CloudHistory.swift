import Foundation
import Security

private let cloudEndpoint = URL(string: "https://blue-sea-0c03ac51e.3.azurestaticapps.net/api/history")!
private let keychainService = "com.ethanrimes.patternatlas.cloud-history"

private func storedCloudKey() -> String? {
    let query: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                kSecAttrService as String: keychainService,
                                kSecAttrAccount as String: "owner",
                                kSecReturnData as String: true,
                                kSecMatchLimit as String: kSecMatchLimitOne]
    var result: CFTypeRef?
    guard SecItemCopyMatching(query as CFDictionary, &result) == errSecSuccess,
          let data = result as? Data else { return nil }
    return String(data: data, encoding: .utf8)
}

private func storeCloudKey(_ value: String) -> Bool {
    let match: [String: Any] = [kSecClass as String: kSecClassGenericPassword,
                                kSecAttrService as String: keychainService,
                                kSecAttrAccount as String: "owner"]
    SecItemDelete(match as CFDictionary)
    var item = match
    item[kSecValueData as String] = Data(value.utf8)
    item[kSecAttrAccessible as String] = kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
    return SecItemAdd(item as CFDictionary, nil) == errSecSuccess
}

extension StudyStore {
    func installStagedCloudKey() {
        guard let folder = try? FileManager.default.url(for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: true) else { return }
        let source = folder.appendingPathComponent("Cloud Sync Key.txt")
        guard let key = try? String(contentsOf: source, encoding: .utf8).trimmingCharacters(in: .whitespacesAndNewlines),
              !key.isEmpty, storeCloudKey(key) else { return }
        try? FileManager.default.removeItem(at: source)
    }

    func configureCloudSync(_ key: String) {
        cloudStatus = storeCloudKey(key) ? "Sync key saved securely. Connecting to Azure…" : "The sync key could not be saved."
    }

    func syncCloudHistory() async {
        guard let key = storedCloudKey(), !key.isEmpty else { return }
        cloudStatus = "Loading history from Azure…"
        do {
            var request = URLRequest(url: cloudEndpoint)
            request.setValue(key, forHTTPHeaderField: "x-pattern-atlas-sync-key")
            request.cachePolicy = .reloadIgnoringLocalCacheData
            let (remoteData, response) = try await URLSession.shared.data(for: request)
            guard let http = response as? HTTPURLResponse else { throw CloudHistoryError.unavailable }
            guard http.statusCode == 200 || http.statusCode == 204 else { throw CloudHistoryError.http(http.statusCode) }
            if http.statusCode == 200 {
                let remote = try LeetCodeHistory.decodeExport(remoteData)
                progress.leetcode = try progress.leetcode?.merging(remote) ?? remote
                save()
            }
            if let history = progress.leetcode {
                let packet = SubmissionExport(calendars: history.calendars, completions: history.completions, through: history.through,
                                              format: "pattern-atlas-leetcode", version: 1,
                                              account: history.account, exportedAt: history.exportedAt,
                                              complete: history.complete, submissions: Array(history.submissions.values))
                var update = URLRequest(url: cloudEndpoint)
                update.httpMethod = "POST"
                update.setValue(key, forHTTPHeaderField: "x-pattern-atlas-sync-key")
                update.setValue("application/json", forHTTPHeaderField: "Content-Type")
                update.httpBody = try JSONEncoder().encode(packet)
                let (_, uploaded) = try await URLSession.shared.data(for: update)
                guard let result = uploaded as? HTTPURLResponse, result.statusCode == 200 else {
                    throw CloudHistoryError.http((uploaded as? HTTPURLResponse)?.statusCode ?? 0)
                }
                cloudStatus = "Connected to Azure · \(history.completions?.slugs.count ?? 0) completed · \(history.submissions.count) submissions"
            } else {
                cloudStatus = "Connected to Azure. Import LeetCode history to start."
            }
        } catch {
            cloudStatus = "Cloud history could not sync: \(error.localizedDescription)"
        }
    }
}

private enum CloudHistoryError: LocalizedError {
    case unavailable, http(Int)
    var errorDescription: String? {
        switch self {
        case .unavailable: "The server did not return a response."
        case .http(401): "The sync key was not recognized."
        case .http(let code): "Azure returned \(code). Try again later."
        }
    }
}
