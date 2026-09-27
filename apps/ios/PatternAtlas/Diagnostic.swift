import Foundation

enum FamiliarityRating: String, Codable, CaseIterable {
    case definitely, probably, notYet = "not-yet"
    var label: String { switch self { case .definitely: "Definitely got it"; case .probably: "Probably got it"; case .notYet: "Did not get it" } }
    var detail: String { switch self { case .definitely: "I understand the approach and could explain it."; case .probably: "The idea makes sense, but I am unsure of some steps."; case .notYet: "I need to study this approach again." } }
    var rank: Int { switch self { case .notYet: 0; case .probably: 1; case .definitely: 2 } }
}
struct FamiliarityAssessment: Codable { let rating: FamiliarityRating; let assessedAt: String }
typealias Familiarity = [String: FamiliarityAssessment]
func validFamiliarity(_ records: Familiarity) -> Bool {
    records.allSatisfy { key, value in key.count <= 500 && key.range(of: #"^[A-Za-z0-9_-]+:[A-Za-z0-9_-]+$"#, options: .regularExpression) != nil && dateFromISO(value.assessedAt) != nil }
}
func mergeFamiliarity(_ current: Familiarity, _ incoming: Familiarity) -> Familiarity {
    var result = current
    for (key, item) in incoming {
        let old = result[key], date = dateFromISO(item.assessedAt) ?? .distantPast
        let previous = old.flatMap { dateFromISO($0.assessedAt) } ?? .distantPast
        if old == nil || date > previous || (date == previous && item.rating.rank < old!.rating.rank) { result[key] = item }
    }
    return result
}
extension StudyStore {
    func assess(_ key: String, _ rating: FamiliarityRating, now: Date = .now) {
        var records = progress.familiarity ?? [:]
        records[key] = FamiliarityAssessment(rating: rating, assessedAt: iso(now))
        progress.familiarity = records; save()
    }
}
struct DiagnosticCard: Identifiable {
    let problem: StudyProblem; let node: PatternNode; let solutions: [CanonicalSolution]
    var id: String { cardKey(problem.id, node.id) }
}
enum DiagnosticMode: String, CaseIterable {
    case unassessed, uncertain, all
    var label: String { switch self { case .unassessed: "Unassessed only"; case .uncertain: "Probably / did not get it"; case .all: "All · reassess previous ratings" } }
}
struct DiagnosticOptions {
    var nodeId = "", difficulty = ""
    var includeCommunity = false
    var mode: DiagnosticMode = .unassessed
    var limit = 20
}
func diagnosticCards(_ data: Curriculum, options: DiagnosticOptions = DiagnosticOptions()) -> [DiagnosticCard] {
    let nodes = Dictionary(uniqueKeysWithValues: data.nodes.map { ($0.id, $0) })
    let scope = options.nodeId.isEmpty ? nil : data.descendants(of: options.nodeId)
    return data.problems.flatMap { problem -> [DiagnosticCard] in
        if !options.difficulty.isEmpty && problem.difficulty != options.difficulty { return [] }
        var seen = Set<String>()
        return problem.solutions.compactMap { solution in
            guard seen.insert(solution.patternId).inserted, let node = nodes[solution.patternId],
                  (options.includeCommunity || node.kind == "pattern"), (scope?.contains(node.id) ?? true) else { return nil }
            return DiagnosticCard(problem: problem, node: node, solutions: problem.solutions.filter { $0.patternId == node.id })
        }
    }
}
func diagnosticQueue(_ data: Curriculum, progress: StudyProgress, options: DiagnosticOptions) -> [DiagnosticCard] {
    let nodes = Dictionary(uniqueKeysWithValues: data.nodes.map { ($0.id, $0) })
    func root(_ start: PatternNode) -> String {
        var node = start, seen = Set<String>()
        while let parent = node.parentId.flatMap({ nodes[$0] }), seen.insert(node.id).inserted { node = parent }
        return node.id
    }
    let cards = diagnosticCards(data, options: options).filter { card in
        let record = progress.familiarity?[card.id]
        switch options.mode { case .unassessed: return record == nil; case .uncertain: return record != nil && record?.rating != .definitely; case .all: return true }
    }
    func before(_ a: DiagnosticCard, _ b: DiagnosticCard) -> Bool {
        let x = progress.familiarity?[a.id], y = progress.familiarity?[b.id]
        if (x == nil) != (y == nil) { return x == nil }
        if let x, let y {
            if x.rating.rank != y.rating.rank { return x.rating.rank < y.rating.rank }
            let dx = dateFromISO(x.assessedAt) ?? .distantPast, dy = dateFromISO(y.assessedAt) ?? .distantPast
            if dx != dy { return dx < dy }
        }
        let ranks = ["Easy":0, "Medium":1, "Hard":2], ra = ranks[a.problem.difficulty, default:0], rb = ranks[b.problem.difficulty, default:0]
        if ra != rb { return ra < rb }
        if a.problem.id != b.problem.id { return a.problem.id.compare(b.problem.id, options: .numeric) == .orderedAscending }
        return a.id < b.id
    }
    var rootOrder: [String] = [], groups: [String: [String: [DiagnosticCard]]] = [:]
    for card in cards {
        let id = root(card.node)
        if groups[id] == nil { rootOrder.append(id) }
        groups[id, default: [:]][card.node.id, default: []].append(card)
    }
    var buckets: [[DiagnosticCard]] = rootOrder.map { id in
        var patterns = (groups[id] ?? [:]).values.map { $0.sorted(by: before) }.sorted { before($0[0], $1[0]) }
        var ordered: [DiagnosticCard] = []
        while patterns.contains(where: { !$0.isEmpty }) { for i in patterns.indices where !patterns[i].isEmpty { ordered.append(patterns[i].removeFirst()) } }
        return ordered
    }
    var result: [DiagnosticCard] = []
    while result.count < options.limit && buckets.contains(where: { !$0.isEmpty }) {
        for i in buckets.indices where !buckets[i].isEmpty { result.append(buckets[i].removeFirst()); if result.count >= options.limit { break } }
    }
    return result
}
struct FamiliaritySummary {
    var total = 0, definitely = 0, probably = 0, notYet = 0, unassessed = 0
    var lastAssessed: String?
    var assessed: Int { definitely + probably + notYet }
    init(_ cards: [DiagnosticCard], progress: StudyProgress) {
        total = cards.count
        for card in cards {
            guard let record = progress.familiarity?[card.id] else { unassessed += 1; continue }
            switch record.rating { case .definitely: definitely += 1; case .probably: probably += 1; case .notYet: notYet += 1 }
            if (dateFromISO(record.assessedAt) ?? .distantPast) > (lastAssessed.flatMap(dateFromISO) ?? .distantPast) { lastAssessed = record.assessedAt }
        }
    }
}
struct FamiliarityRow: Identifiable {
    let node: PatternNode; let summary: FamiliaritySummary
    var id: String { node.id }
}
func familiarityByNode(_ data: Curriculum, progress: StudyProgress, options: DiagnosticOptions, leaves: Bool) -> [FamiliarityRow] {
    let cards = diagnosticCards(data, options: options)
    let scope = options.nodeId.isEmpty ? nil : data.descendants(of: options.nodeId)
    var nodes = data.nodes.filter { node in
        leaves ? node.kind == "pattern" || (options.includeCommunity && node.kind == "collection") : node.parentId == (options.nodeId.isEmpty ? nil : options.nodeId)
    }
    if !leaves && nodes.isEmpty, let node = data.node(options.nodeId) { nodes = [node] }
    return nodes.filter { scope?.contains($0.id) ?? true }.compactMap { node in
        let branch = data.descendants(of: node.id)
        let summary = FamiliaritySummary(cards.filter { branch.contains($0.node.id) }, progress: progress)
        return summary.total > 0 ? FamiliarityRow(node: node, summary: summary) : nil
    }
}
