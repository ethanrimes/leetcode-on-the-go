import Foundation

struct LeetCodeSubmission: Codable, Identifiable {
    let id: String
    let slug: String
    let title: String
    let timestamp: String
    let status: String
    let language: String
    var accepted: Bool { status.lowercased() == "accepted" }
    var valid: Bool {
        id.range(of: #"^\d{1,30}$"#, options: .regularExpression) != nil &&
        slug.range(of: #"^[a-z0-9]+(?:-[a-z0-9]+)*$"#, options: .regularExpression) != nil && slug.count <= 300 &&
        dateFromISO(timestamp) != nil && !status.isEmpty && [title, status, language].allSatisfy { $0.count <= 500 }
    }
}
struct LeetCodeHistory: Codable {
    var through: String? = nil
    let account: String
    let exportedAt: String
    let complete: Bool
    var submissions: [String: LeetCodeSubmission]
    var valid: Bool { (through == nil || through!.range(of: #"^\d{4}-\d{2}-\d{2}$"#, options: .regularExpression) != nil) && !account.isEmpty && account.count <= 300 && !["__proto__", "constructor", "prototype"].contains(account) && dateFromISO(exportedAt) != nil && submissions.allSatisfy { $0.key == $0.value.id && $0.value.valid } }
    func merging(_ incoming: LeetCodeHistory) throws -> LeetCodeHistory {
        guard account.lowercased() == incoming.account.lowercased() else { throw HistoryError.differentAccount }
        let newer = (dateFromISO(incoming.exportedAt) ?? .distantPast) >= (dateFromISO(exportedAt) ?? .distantPast)
        var result = newer ? incoming : self
        result.submissions = submissions.merging(incoming.submissions) { newer ? $1 : $0 }
        return result
    }
    static func decodeExport(_ data: Data) throws -> LeetCodeHistory {
        guard data.count <= 10_000_000 else { throw StudyError.invalidBackup }
        let packet = try JSONDecoder().decode(SubmissionExport.self, from: data)
        guard packet.format == "pattern-atlas-leetcode", packet.version == 1 else { throw HistoryError.invalidExport }
        var records: [String: LeetCodeSubmission] = [:]
        for submission in packet.submissions { guard submission.valid else { throw HistoryError.invalidExport }; records[submission.id] = submission }
        let result = LeetCodeHistory(through: packet.through, account: packet.account, exportedAt: packet.exportedAt, complete: packet.complete, submissions: records)
        guard result.valid else { throw HistoryError.invalidExport }; return result
    }
}
struct SubmissionExport: Codable {
    var through: String? = nil
    let format: String
    let version: Int
    let account: String
    let exportedAt: String
    let complete: Bool
    let submissions: [LeetCodeSubmission]
}
enum HistoryError: LocalizedError {
    case differentAccount, invalidExport
    var errorDescription: String? { switch self {
    case .differentAccount: "This export belongs to a different LeetCode account. Existing history was kept."
    case .invalidExport: "Choose the JSON file downloaded by the Pattern Atlas LeetCode exporter."
    } }
}
struct PageVisit: Codable {
    var count: Int
    var lastVisited: String
}
typealias PageVisits = [String: [String: PageVisit]]
func validVisits(_ visits: PageVisits) -> Bool {
    visits.allSatisfy { device, pages in
        !device.isEmpty && device.count <= 300 && !["__proto__", "constructor", "prototype"].contains(device) && pages.allSatisfy { page, visit in
            page.count <= 500 && page.range(of: #"^/[a-zA-Z0-9/_-]*$"#, options: .regularExpression) != nil && visit.count >= 0 && dateFromISO(visit.lastVisited) != nil
        }
    }
}
func mergeVisits(_ current: PageVisits, _ incoming: PageVisits) -> PageVisits {
    var result = current
    for (device, pages) in incoming { for (page, visit) in pages {
        let old = result[device]?[page]
        result[device, default: [:]][page] = PageVisit(count: max(old?.count ?? 0, visit.count), lastVisited: max(old?.lastVisited ?? "", visit.lastVisited))
    } }
    return result
}
func totalVisits(_ visits: PageVisits) -> [String: PageVisit] {
    var result: [String: PageVisit] = [:]
    for pages in visits.values { for (page, visit) in pages {
        result[page] = PageVisit(count: (result[page]?.count ?? 0) + visit.count, lastVisited: max(result[page]?.lastVisited ?? "", visit.lastVisited))
    } }
    return result
}
extension StudyStore {
    func importHistory(_ data: Data) throws {
        let incoming = try LeetCodeHistory.decodeExport(data)
        progress.leetcode = try progress.leetcode?.merging(incoming) ?? incoming
        save(); message = "Merged \(incoming.submissions.count) submissions. Duplicate IDs were kept once."
    }
    func visit(_ page: String, now: Date = .now) {
        let key = "pattern-atlas.device"
        let device = defaults.string(forKey: key) ?? UUID().uuidString
        defaults.set(device, forKey: key)
        var visits = progress.visits ?? [:]
        let count = visits[device]?[page]?.count ?? 0
        visits[device, default: [:]][page] = PageVisit(count: count + 1, lastVisited: iso(now))
        progress.visits = visits; save()
    }
}
struct CoverageStats: Identifiable {
    let node: PatternNode
    let total: Int
    let solved: Int
    let attempted: Int
    let visits: Int
    let fresh: Int
    let practiced: Int
    let lastPracticed: String?
    let due: Int
    var id: String { node.id }
    var unseen: Int { total - solved - attempted }
    var accessibilitySummary: String { "\(node.title): \(solved) accepted, \(attempted) attempted, \(total) problems, \(fresh) fresh, \(practiced - fresh) need refresh, \(visits) category entries" }
}
struct AnalyticsFilter {
    var scope = ""
    var depth = 1
    var difficulty = ""
    var level = ""
    var query = ""
    var period = 0
    var freshDays = 30
}
struct CurriculumAnalytics {
    let data: Curriculum
    let membership: [String: Set<String>]
    let children: [String: [PatternNode]]
    init(_ data: Curriculum) {
        self.data = data
        children = Dictionary(grouping: data.nodes, by: { $0.parentId ?? "" })
        var direct = Dictionary(uniqueKeysWithValues: data.nodes.map { ($0.id, Set($0.problemIds ?? [])) })
        for problem in data.problems { for id in problem.patternIds + (problem.collectionIds ?? []) { direct[id, default: []].insert(problem.id) } }
        var result: [String: Set<String>] = [:]
        func collect(_ id: String, _ trail: Set<String> = []) -> Set<String> {
            if let cached = result[id] { return cached }
            var ids = direct[id] ?? []
            if trail.contains(id) { return ids }
            for child in data.nodes where child.parentId == id { ids.formUnion(collect(child.id, trail.union([id]))) }
            result[id] = ids; return ids
        }
        for node in data.nodes { _ = collect(node.id) }
        membership = result
    }
    func snapshot(_ progress: StudyProgress, filter: AnalyticsFilter, now: Date = .now) -> AnalyticsSnapshot {
        let pages = totalVisits(progress.visits ?? [:])
        let all = Array(progress.leetcode?.submissions.values ?? [:].values)
        let submissions = all.filter { filter.period == 0 || (dateFromISO($0.timestamp) ?? .distantPast) >= now.addingTimeInterval(-Double(filter.period) * 86400) }
        let solved = Set(submissions.filter(\.accepted).map(\.slug)), attempted = Set(submissions.map(\.slug))
        let eligible = Dictionary(uniqueKeysWithValues: data.catalog.filter { filter.difficulty.isEmpty || $0.difficulty == filter.difficulty }.map { ($0.id, $0) })
        let bySlug = Dictionary(uniqueKeysWithValues: data.catalog.map { ($0.slug, $0.id) })
        var practice: [String: Date] = [:]; var due = Set<String>()
        for s in all { if let id = bySlug[s.slug], let date = dateFromISO(s.timestamp) { practice[id] = max(practice[id] ?? .distantPast, date) } }
        for (key, review) in progress.cards {
            let id = String(key.split(separator: ":").first ?? "")
            if let date = dateFromISO(review.lastReviewed) { practice[id] = max(practice[id] ?? .distantPast, date) }
            if (dateFromISO(review.due) ?? .distantFuture) <= now { due.insert(id) }
        }
        let cutoff = now.addingTimeInterval(-Double(filter.freshDays) * 86400)
        func stats(_ node: PatternNode) -> CoverageStats {
            let problems = (membership[node.id] ?? []).compactMap { eligible[$0] }
            let dates = problems.compactMap { practice[$0.id] }.sorted()
            let branch = data.descendants(of: node.id)
            return CoverageStats(node: node, total: problems.count, solved: problems.filter { solved.contains($0.slug) }.count,
                attempted: problems.filter { attempted.contains($0.slug) && !solved.contains($0.slug) }.count,
                visits: branch.reduce(0) { $0 + (pages["/library/\($1)"]?.count ?? 0) },
                fresh: dates.filter { $0 >= cutoff }.count, practiced: dates.count,
                lastPracticed: dates.last.map(iso), due: problems.filter { problem in
                    if node.kind == "pattern" { return progress.cards[cardKey(problem.id, node.id)].map { (dateFromISO($0.due) ?? .distantFuture) <= now } ?? false }
                    return due.contains(problem.id)
                }.count)
        }
        func frontier(_ id: String, _ depth: Int) -> [PatternNode] {
            (children[id] ?? []).flatMap { node in depth > 1 && !(children[node.id] ?? []).isEmpty ? frontier(node.id, depth - 1) : [node] }
        }
        var nodes = frontier(filter.scope, filter.depth)
        if nodes.isEmpty, let node = data.node(filter.scope) { nodes = [node] }
        let visibleNodes = nodes.filter { (filter.level.isEmpty || $0.level == filter.level) && (filter.query.isEmpty || $0.title.localizedCaseInsensitiveContains(filter.query)) }
        let tileStats: [CoverageStats] = visibleNodes.map(stats)
        let tiles = tileStats.filter { $0.total > 0 }.sorted { a, b in a.total == b.total ? a.id < b.id : a.total > b.total }
        let scope = filter.scope.isEmpty ? Set(data.catalog.map(\.id)) : membership[filter.scope] ?? []
        let problems = eligible.values.filter { scope.contains($0.id) }; let slugs = Set(problems.map(\.slug))
        let branch = filter.scope.isEmpty ? Set(data.nodes.map(\.id)) : data.descendants(of: filter.scope)
        let candidates: [CoverageStats] = data.patterns.filter { branch.contains($0.id) }.map(stats)
        let needingPractice = candidates.filter { $0.total > 0 && ($0.fresh < $0.total || $0.due > 0) }
        let focus = needingPractice.sorted { a, b in
            if a.due != b.due { return a.due > b.due }
            if a.practiced - a.fresh != b.practiced - b.fresh { return a.practiced - a.fresh > b.practiced - b.fresh }
            if (a.practiced > 0) != (b.practiced > 0) { return a.practiced > 0 }
            if (a.node.priority == "Core") != (b.node.priority == "Core") { return a.node.priority == "Core" }
            return Double(a.solved) / Double(a.total) < Double(b.solved) / Double(b.total)
        }
        return AnalyticsSnapshot(tiles: tiles, focus: Array(focus.prefix(6)), total: problems.count, solved: problems.filter { solved.contains($0.slug) }.count,
            attempted: problems.filter { attempted.contains($0.slug) && !solved.contains($0.slug) }.count,
            submissions: submissions.filter { (filter.scope.isEmpty && filter.difficulty.isEmpty) || slugs.contains($0.slug) }.sorted { $0.timestamp > $1.timestamp },
            unmapped: all.filter { bySlug[$0.slug] == nil }.count, pages: pages)
    }
}
struct AnalyticsSnapshot {
    let tiles: [CoverageStats]; let focus: [CoverageStats]; let total: Int; let solved: Int; let attempted: Int
    let submissions: [LeetCodeSubmission]; let unmapped: Int; let pages: [String: PageVisit]
}
struct TileRectangle: Identifiable {
    let id: Int; let x: Double; let y: Double; let width: Double; let height: Double
}
func treemap(_ weights: [Int], width: Double, height: Double) -> [TileRectangle] {
    var result: [TileRectangle] = []
    func split(_ items: [(Int, Double)], _ x: Double, _ y: Double, _ w: Double, _ h: Double) {
        guard let first = items.first else { return }
        if items.count == 1 { result.append(TileRectangle(id: first.0, x: x, y: y, width: w, height: h)); return }
        let total = items.reduce(0) { $0 + $1.1 }; var sum = first.1; var k = 1
        while k < items.count - 1 && abs(total / 2 - (sum + items[k].1)) < abs(total / 2 - sum) { sum += items[k].1; k += 1 }
        let ratio = sum / total
        if w >= h { split(Array(items.prefix(k)), x, y, w * ratio, h); split(Array(items.dropFirst(k)), x + w * ratio, y, w * (1 - ratio), h) }
        else { split(Array(items.prefix(k)), x, y, w, h * ratio); split(Array(items.dropFirst(k)), x, y + h * ratio, w, h * (1 - ratio)) }
    }
    split(weights.enumerated().filter { $0.element > 0 }.map { ($0.offset, Double($0.element)) }, 0, 0, width, height)
    return result
}
