import Foundation
import Observation

struct Curriculum: Codable {
    let version: Int
    let updatedAt: String
    let language: String
    let nodes: [PatternNode]
    let problems: [StudyProblem]
    let catalog: [CatalogProblem]
    var roots: [PatternNode] { nodes.filter { $0.parentId == nil } }
    var patterns: [PatternNode] { nodes.filter { $0.kind == "pattern" } }
    func children(of id: String) -> [PatternNode] { nodes.filter { $0.parentId == id } }
    func node(_ id: String) -> PatternNode? { nodes.first { $0.id == id } }
    func descendants(of id: String) -> Set<String> {
        var found: Set<String> = [id]
        var queue = [id]
        var index = 0
        while index < queue.count {
            for child in children(of: queue[index]) where !found.contains(child.id) {
                found.insert(child.id); queue.append(child.id)
            }
            index += 1
        }
        return found
    }
    func problems(for id: String) -> [StudyProblem] {
        let ids = descendants(of: id)
        return problems.filter { !Set($0.patternIds + ($0.collectionIds ?? [])).isDisjoint(with: ids) }
    }
}
extension Curriculum {
    func entries(for id: String? = nil) -> [CatalogProblem] {
        guard let id else { return catalog }
        let scope = descendants(of: id)
        var included = Set(problems(for: id).map(\.id))
        for node in nodes where scope.contains(node.id) { included.formUnion(node.problemIds ?? []) }
        return catalog.filter { included.contains($0.id) }
    }
}
struct CatalogTag: Codable, Hashable { let name: String; let slug: String }
struct CatalogProblem: Codable, Identifiable, Hashable {
    let id: String; let title: String; let slug: String; let difficulty: String; let premium: Bool
    let tags: [CatalogTag]?
}
enum ProblemOrder: String, CaseIterable {
    case difficulty, difficultyDescending, number, numberDescending, title
    var label: String { switch self {
    case .difficulty: "Difficulty: easy to hard"
    case .difficultyDescending: "Difficulty: hard to easy"
    case .number: "Number: ascending"
    case .numberDescending: "Number: descending"
    case .title: "Title: A–Z"
    } }
    func sorted(_ entries: [CatalogProblem]) -> [CatalogProblem] {
        let ranks = ["Easy": 0, "Medium": 1, "Hard": 2]
        return entries.sorted { a, b in
            let numberAscending = a.id.compare(b.id, options: .numeric) == .orderedAscending
            switch self {
            case .number: return numberAscending
            case .numberDescending: return a.id.compare(b.id, options: .numeric) == .orderedDescending
            case .title: return a.title == b.title ? numberAscending : a.title.localizedStandardCompare(b.title) == .orderedAscending
            case .difficulty, .difficultyDescending:
                let x = ranks[a.difficulty, default: 0], y = ranks[b.difficulty, default: 0]
                return x == y ? numberAscending : (self == .difficulty ? x < y : x > y)
            }
        }
    }
}
struct PatternNode: Codable, Identifiable, Hashable {
    let id: String
    let parentId: String?
    let title: String
    let kind: String
    let level: String
    let priority: String
    let description: String
    let approach: String
    let pseudocode: TechniquePseudocode?
    let tips: [String]
    let why: String
    let sourceUrls: [String]
    let references: [ReferenceSection]
    let problemIds: [String]?
    let sourceTitle: String?
}
struct TechniquePseudocode: Codable, Hashable {
    let code: String
    let example: String?
}
struct ReferenceSection: Codable, Hashable {
    let title: String
    let url: String
    let problemIds: [String]
}
struct StudyProblem: Codable, Identifiable, Hashable {
    let origin: String?
    let collectionIds: [String]?
    let id: String
    let title: String
    let slug: String
    let difficulty: String
    let premium: Bool
    let description: String
    let constraints: String
    let examples: [Example]
    let patternIds: [String]
    let solutions: [CanonicalSolution]
    let starter: String
    let sourceUrl: String
}
struct Example: Codable, Hashable { let input: String; let output: String; let note: String }
struct SolutionAttribution: Codable, Hashable {
    let author: String; let license: String; let url: String; let commit: String; let sha256: String
}
struct CanonicalSolution: Codable, Hashable {
    let attribution: SolutionAttribution?
    let patternId: String
    let title: String
    let language: String
    let approach: String
    let code: String
    let time: String
    let space: String
}
enum RecallRating: String, Codable, CaseIterable { case again, hard, good, easy
    var label: String { rawValue.capitalized }
    var intervalLabel: String { switch self { case .again: "10 min"; case .hard: "1+ day"; case .good: "3+ days"; case .easy: "7+ days" } }
}
struct Review: Codable {
    let repetitions: Int
    let lapses: Int
    let interval: Double
    let due: String
    let lastReviewed: String
    let rating: RecallRating
    static func schedule(_ previous: Review?, rating: RecallRating, now: Date = .now) -> Review {
        let old = previous?.interval ?? 0
        let interval: Double
        switch rating {
        case .again: interval = 10.0 / 1440
        case .hard: interval = max(1, (old * 1.2).rounded())
        case .good: interval = max(3, (old * 2.3).rounded())
        case .easy: interval = max(7, (old * 3.2).rounded())
        }
        return Review(repetitions: rating == .again ? 0 : (previous?.repetitions ?? 0) + 1,
                      lapses: (previous?.lapses ?? 0) + (rating == .again ? 1 : 0), interval: interval,
                      due: iso(now.addingTimeInterval(interval * 86400)), lastReviewed: iso(now), rating: rating)
    }
}
func iso(_ date: Date) -> String {
    let formatter = ISO8601DateFormatter(); formatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
    return formatter.string(from: date)
}
func dateFromISO(_ string: String) -> Date? {
    let formatter = ISO8601DateFormatter(); formatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
    return formatter.date(from: string) ?? ISO8601DateFormatter().date(from: string)
}
func cardKey(_ problem: String, _ pattern: String) -> String { "\(problem):\(pattern)" }
struct StudyProgress: Codable {
    var leetcode: LeetCodeHistory?
    var visits: PageVisits?
    var version = 1
    var cards: [String: Review] = [:]
    var drafts: [String: String] = [:]
    var bookmarks: [String] = []
    var activity: [String: Int] = [:]
    static func decode(_ data: Data) throws -> StudyProgress {
        guard data.count <= 10_000_000 else { throw StudyError.invalidBackup }
        let value = try JSONDecoder().decode(StudyProgress.self, from: data)
        guard value.version == 1,
              value.cards.values.allSatisfy({ $0.repetitions >= 0 && $0.lapses >= 0 && $0.interval >= 0 && $0.interval.isFinite && dateFromISO($0.due) != nil && dateFromISO($0.lastReviewed) != nil }),
              value.drafts.values.allSatisfy({ $0.count <= 200_000 }),
              value.activity.allSatisfy({ $0.key.range(of: #"^\d{4}-\d{2}-\d{2}$"#, options: .regularExpression) != nil && $0.value >= 0 }) else { throw StudyError.invalidBackup }
        guard value.leetcode?.valid ?? true, validVisits(value.visits ?? [:]) else { throw StudyError.invalidBackup }
        return value
    }
}
enum StudyError: LocalizedError {
    case missingCurriculum, invalidBackup
    var errorDescription: String? { switch self { case .missingCurriculum: "The bundled curriculum could not be opened."; case .invalidBackup: "This backup is invalid or unsupported. Your existing progress has been kept." } }
}
struct ReviewCard: Identifiable {
    let problem: StudyProblem
    let patternId: String
    var id: String { cardKey(problem.id, patternId) }
}
@MainActor @Observable final class StudyStore {
    var curriculum: Curriculum?
    var loadError: String?
    var message: String?
    var progress = StudyProgress()
    let defaults: UserDefaults
    private let key = "pattern-atlas.progress.v1"
    init(defaults: UserDefaults = .standard, bundle: Bundle = .main) {
        self.defaults = defaults
        if let data = defaults.data(forKey: key) {
            do { progress = try StudyProgress.decode(data) }
            catch { message = "Saved progress could not be read. A recovery copy was preserved."; defaults.set(data, forKey: key + ".recovery") }
        }
        do {
            guard let url = bundle.url(forResource: "curriculum", withExtension: "json") else { throw StudyError.missingCurriculum }
            curriculum = try JSONDecoder().decode(Curriculum.self, from: Data(contentsOf: url))
        } catch { loadError = error.localizedDescription }
    }
    func save() {
        do { defaults.set(try JSONEncoder().encode(progress), forKey: key) }
        catch { message = "The change could not be saved. Please export a backup." }
    }
    func draft(for problem: StudyProblem) -> String { progress.drafts[problem.id] ?? problem.starter }
    func setDraft(_ text: String, for id: String) { progress.drafts[id] = text; save() }
    func toggleBookmark(_ id: String) {
        if progress.bookmarks.contains(id) { progress.bookmarks.removeAll { $0 == id } }
        else { progress.bookmarks.append(id) }
        save()
    }
    func rate(_ key: String, _ rating: RecallRating, now: Date = .now) {
        progress.cards[key] = Review.schedule(progress.cards[key], rating: rating, now: now)
        let formatter = DateFormatter(); formatter.locale = Locale(identifier: "en_US_POSIX"); formatter.dateFormat = "yyyy-MM-dd"
        let day = formatter.string(from: now)
        progress.activity[day, default: 0] += 1
        save()
    }
    func learned(_ problem: StudyProblem) -> Bool { problem.patternIds.contains { (progress.cards[cardKey(problem.id, $0)]?.repetitions ?? 0) >= 2 } }
    var dueCount: Int { progress.cards.values.filter { (dateFromISO($0.due) ?? .distantFuture) <= .now }.count }
    func queue(nodeId: String? = nil, limit: Int = 10, now: Date = .now) -> [ReviewCard] {
        guard let data = curriculum else { return [] }
        let ids = nodeId.map { data.descendants(of: $0) }
        let cards = data.problems.flatMap { p in p.patternIds.filter { (ids?.contains($0) ?? true) || (ids.map { !Set(p.collectionIds ?? []).isDisjoint(with: $0) } ?? false) }.map { ReviewCard(problem: p, patternId: $0) } }
        return Array(cards.filter { progress.cards[$0.id].map { (dateFromISO($0.due) ?? .distantFuture) <= now } ?? true }.enumerated().sorted { a, b in
            let x = progress.cards[a.element.id]; let y = progress.cards[b.element.id]
            if let x, let y { return x.due == y.due ? a.offset < b.offset : x.due < y.due }
            if x != nil { return true }; if y != nil { return false }; return a.offset < b.offset
        }.prefix(limit).map(\.element))
    }
    func exportData() throws -> Data { let encoder = JSONEncoder(); encoder.outputFormatting = [.prettyPrinted, .sortedKeys]; return try encoder.encode(progress) }
    func mergeBackup(_ data: Data) throws {
        let incoming = try StudyProgress.decode(data)
        let history = try incoming.leetcode.map { try progress.leetcode?.merging($0) ?? $0 } ?? progress.leetcode
        for (key, review) in incoming.cards where progress.cards[key] == nil || review.lastReviewed > progress.cards[key]!.lastReviewed { progress.cards[key] = review }
        for (key, draft) in incoming.drafts where progress.drafts[key] == nil { progress.drafts[key] = draft }
        progress.bookmarks = Array(Set(progress.bookmarks + incoming.bookmarks)).sorted()
        for (day, count) in incoming.activity { progress.activity[day] = max(progress.activity[day] ?? 0, count) }
        progress.leetcode = history
        progress.visits = mergeVisits(progress.visits ?? [:], incoming.visits ?? [:])
        save(); message = "Backup merged. Existing local drafts were kept."
    }
}
