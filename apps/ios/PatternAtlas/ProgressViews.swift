import SwiftUI
import UniformTypeIdentifiers

struct BackupDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.json] }
    var data: Data
    init(data: Data = Data()) { self.data = data }
    init(configuration: ReadConfiguration) throws { data = configuration.file.regularFileContents ?? Data() }
    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper { FileWrapper(regularFileWithContents: data) }
}
struct ProgressViewScreen: View {
    let data: Curriculum
    @Environment(StudyStore.self) private var store
    @State private var importing = false
    @State private var exporting = false
    @State private var document = BackupDocument()
    @State private var enteredSyncKey = ""
    var body: some View {
        List {
            Section {
                Text(store.cloudStatus).font(.caption).foregroundStyle(.secondary)
                SecureField("Private sync key", text: $enteredSyncKey)
                    .textInputAutocapitalization(.never).autocorrectionDisabled()
                Button("Connect and load history") {
                    let key = enteredSyncKey.trimmingCharacters(in: .whitespacesAndNewlines)
                    guard !key.isEmpty else { return }
                    store.configureCloudSync(key)
                    enteredSyncKey = ""
                    Task { await store.syncCloudHistory() }
                }.disabled(enteredSyncKey.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                Button("Refresh from Azure") { Task { await store.syncCloudHistory() } }
            } header: { Text("Azure history") } footer: { Text("Completions and submissions sync with your private Azure history. Drafts, ratings, and page visits stay on this device.") }
            if let history = store.progress.leetcode {
                Section("Your LeetCode progress") {
                    let solved = Set((history.completions?.slugs ?? []) + history.submissions.values.filter(\.accepted).map(\.slug))
                    HStack {
                        StatView(value: "\(solved.count)", label: "Completed")
                        StatView(value: "\(history.submissions.count)", label: "Submissions")
                    }.padding(.vertical, 12)
                    Text(history.account).font(.caption).foregroundStyle(.secondary)
                    NavigationLink("Coverage & freshness") { List { AnalyticsDashboardSections(data: data) }.navigationTitle("LeetCode progress").trackPage("/progress/leetcode") }
                }
                LeetCodeActivitySection(data: data, history: history)
            }
            Section {
                HStack {
                    StatView(value: "\(store.progress.cards.count)", label: "Reviewed")
                    StatView(value: "\(data.problems.filter { store.learned($0) }.count)", label: "Recalled twice")
                    StatView(value: "\(store.dueCount)", label: "Due now")
                }.padding(.vertical, 12)
            }
            AnalyticsDashboardSections(data: data)
            FamiliarityDashboardSection(data: data)
            Section("Saved for later") {
                let saved = data.problems.filter { store.progress.bookmarks.contains($0.id) }
                ForEach(saved) { problem in NavigationLink { ProblemDetailView(data: data, problem: problem) } label: { ProblemRow(problem: problem) } }
                if saved.isEmpty { Text("Bookmark a problem to return to it here.").font(.caption).foregroundStyle(.secondary) }
            }
            Section {
                Button { do { document = BackupDocument(data: try store.exportData()); exporting = true } catch { store.message = error.localizedDescription } } label: { Label("Export progress & drafts", systemImage: "square.and.arrow.up") }
                Button { importing = true } label: { Label("Import a backup", systemImage: "square.and.arrow.down") }
            } header: { Text("Your work travels with you") } footer: { Text("Backups work in both apps. Import merges newer reviews and preserves existing local drafts.") }
            Section {
                NavigationLink("Sources & curriculum notes") { CurriculumNotesView(data: data) }
            }
        }.navigationTitle("Your progress").trackPage("/progress")
            .fileExporter(isPresented: $exporting, document: document, contentType: .json, defaultFilename: "pattern-atlas-backup") { result in
                if case .failure(let error) = result { store.message = error.localizedDescription }
            }
            .fileImporter(isPresented: $importing, allowedContentTypes: [.json]) { result in
                do {
                    let url = try result.get(); let access = url.startAccessingSecurityScopedResource()
                    defer { if access { url.stopAccessingSecurityScopedResource() } }
                    try store.mergeBackup(Data(contentsOf: url))
                } catch { store.message = error.localizedDescription }
            }
    }
}
struct CurriculumNotesView: View {
    let data: Curriculum
    var body: some View {
        List {
            Section("The study loop") { Text("Recognize the pattern, state its invariant, draft a solution, reveal the explanation, and rate your recall. Pattern levels describe learning complexity; LeetCode difficulty describes the problem.").font(.subheadline).lineSpacing(5) }
            Section("Source audit") {
                Text("The curriculum draws on all 12 EndlessCheng guide outlines, labuladong’s full algorithm directory and learning plans, and official LeetCode topic tags. The core lessons are independently authored. Additional Python implementations are imported from walkccc under MIT, with attribution and source links on every solution.").font(.caption).lineSpacing(4)
                Link("EndlessCheng’s algorithm directory", destination: URL(string: "https://github.com/EndlessCheng/codeforces-go")!)
                Link("labuladong’s learning plan", destination: URL(string: "https://labuladong.online/en/algo/intro/quick-learning-plan/")!)
                Link("Community solutions · walkccc · MIT", destination: URL(string: "https://github.com/walkccc/LeetCode")!)
                Link("LeetCode problem catalog", destination: URL(string: "https://leetcode.com/problemset/")!)
            }
            Section("Coverage") {
                Text("\(data.patterns.count) worked patterns · \(data.problems.count) study cards · updated \(data.updatedAt)").font(.caption)
                Text("This edition focuses on algorithmic problems. The repository tracks source coverage and specialist extension topics. SQL, shell, concurrency, and language-specific tracks are separate domains. A reference catalog entry is not a completed study lesson.").font(.caption).foregroundStyle(.secondary).lineSpacing(4)
                Link("Repository & coverage audit", destination: URL(string: "https://github.com/ethanrimes/leetcode-on-the-go")!)
            }
            Section("Your private notebook") { Text("The complete worked curriculum is bundled for offline study. Drafts and review history remain on this device. The app does not execute your code. Open LeetCode to run or submit solutions. This app is independent of LeetCode and the referenced educators.").font(.caption).foregroundStyle(.secondary).lineSpacing(4) }
        }.navigationTitle("Curriculum notes").trackPage("/about").navigationBarTitleDisplayMode(.inline)
    }
}
