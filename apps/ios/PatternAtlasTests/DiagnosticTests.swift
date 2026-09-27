import XCTest
@testable import PatternAtlas

final class DiagnosticTests: XCTestCase {
    private let now = dateFromISO("2026-09-27T12:00:00.000Z")!
    @MainActor func testDiagnosticQueueAndExactApproachAttribution() throws {
        let suite = "Atlas.Diagnostic.\(UUID().uuidString)"
        let defaults = try XCTUnwrap(UserDefaults(suiteName: suite))
        defer { defaults.removePersistentDomain(forName: suite) }
        let store = StudyStore(defaults: defaults), data = try XCTUnwrap(store.curriculum)
        let cards = diagnosticCards(data)
        XCTAssertEqual(cards.count, 200)
        let queue = diagnosticQueue(data, progress: store.progress, options: DiagnosticOptions(limit: 12))
        func root(_ node: PatternNode) -> String { if let parent = node.parentId.flatMap(data.node) { return root(parent) }; return node.id }
        XCTAssertEqual(Set(queue.map { root($0.node) }).count, 12)
        XCTAssertTrue(queue.allSatisfy { card in card.solutions.allSatisfy { $0.patternId == card.node.id } })
        let card = try XCTUnwrap(cards.first)
        store.assess(card.id, .probably, now: now)
        XCTAssertEqual(FamiliaritySummary([card], progress: store.progress).probably, 1)
        XCTAssertTrue(store.progress.cards.isEmpty); XCTAssertTrue(store.progress.activity.isEmpty); XCTAssertNil(store.progress.leetcode)
        let uncertain = diagnosticQueue(data, progress: store.progress, options: DiagnosticOptions(mode: .uncertain))
        XCTAssertEqual(uncertain.map(\.id), [card.id])
        let summary = familiarityByNode(data, progress: store.progress, options: DiagnosticOptions(), leaves: true)
        XCTAssertEqual(summary.filter { $0.summary.assessed > 0 }.count, 1)
        XCTAssertEqual(summary.first { $0.id == card.node.id }?.summary.probably, 1)
        store.assess(card.id, .definitely, now: now.addingTimeInterval(1))
        XCTAssertTrue(diagnosticQueue(data, progress: store.progress, options: DiagnosticOptions(mode: .uncertain)).isEmpty)
        let reloaded = StudyStore(defaults: defaults)
        XCTAssertEqual(reloaded.progress.familiarity?[card.id]?.rating, .definitely)
        let all = diagnosticCards(data, options: DiagnosticOptions(includeCommunity: true))
        XCTAssertGreaterThan(all.count, 2800)
        let community = try XCTUnwrap(all.first { $0.node.kind == "collection" })
        store.assess(community.id, .definitely, now: now)
        XCTAssertEqual(FamiliaritySummary(cards, progress: store.progress).assessed, 1)
        XCTAssertEqual(FamiliaritySummary(all, progress: store.progress).assessed, 2)
    }
    @MainActor func testDiagnosticBackupsMergeAndKeepPracticeSeparate() throws {
        let suite = "Atlas.Diagnostic.Backup.\(UUID().uuidString)"
        let defaults = try XCTUnwrap(UserDefaults(suiteName: suite))
        defer { defaults.removePersistentDomain(forName: suite) }
        let store = StudyStore(defaults: defaults), data = try XCTUnwrap(store.curriculum), card = try XCTUnwrap(diagnosticCards(data).first)
        store.setDraft("local", for: card.problem.id); store.assess(card.id, .definitely, now: now)
        var incoming = StudyProgress(); incoming.familiarity = [card.id: FamiliarityAssessment(rating: .notYet, assessedAt: iso(now.addingTimeInterval(1)))]; incoming.drafts[card.problem.id] = "incoming"
        try store.mergeBackup(JSONEncoder().encode(incoming))
        XCTAssertEqual(store.progress.familiarity?[card.id]?.rating, .notYet); XCTAssertEqual(store.progress.drafts[card.problem.id], "local")
        let engine = CurriculumAnalytics(data), snapshot = engine.snapshot(store.progress, filter: AnalyticsFilter(scope: card.node.id), now: now)
        XCTAssertEqual(snapshot.tiles.first?.fresh, 0)
        let roundtrip = try StudyProgress.decode(store.exportData()); XCTAssertEqual(roundtrip.familiarity?[card.id]?.rating, .notYet)
        let invalid = Data(#"{"version":1,"cards":{},"drafts":{},"bookmarks":[],"activity":{},"familiarity":{"1:pattern":{"rating":"invalid","assessedAt":"2026-09-27T12:00:00.000Z"}}}"#.utf8)
        XCTAssertThrowsError(try StudyProgress.decode(invalid))
        XCTAssertNil(try StudyProgress.decode(Data(#"{"version":1,"cards":{},"drafts":{},"bookmarks":[],"activity":{}}"#.utf8)).familiarity)
        let a = [card.id: FamiliarityAssessment(rating: .definitely, assessedAt: iso(now))], b = [card.id: FamiliarityAssessment(rating: .probably, assessedAt: iso(now))]
        XCTAssertEqual(mergeFamiliarity(a,b)[card.id]?.rating, mergeFamiliarity(b,a)[card.id]?.rating)
    }
}
