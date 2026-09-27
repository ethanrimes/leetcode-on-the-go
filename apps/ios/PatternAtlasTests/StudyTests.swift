import XCTest
@testable import PatternAtlas

final class StudyTests: XCTestCase {
    func testReviewScheduleMatchesWebIntervals() throws {
        let now = try XCTUnwrap(dateFromISO("2026-09-27T12:00:00.000Z"))
        let again = Review.schedule(nil, rating: .again, now: now)
        XCTAssertEqual(again.due, "2026-09-27T12:10:00.000Z")
        XCTAssertEqual(again.repetitions, 0)
        XCTAssertEqual(again.lapses, 1)
        let good = Review.schedule(nil, rating: .good, now: now)
        XCTAssertEqual(good.due, "2026-09-30T12:00:00.000Z")
        XCTAssertEqual(Review.schedule(good, rating: .easy, now: now).interval, 10)
    }
    func testBackupRoundTripAndInvalidData() throws {
        var progress = StudyProgress()
        progress.drafts["1"] = "def solve():\n    return 42"
        progress.bookmarks = ["1"]
        let decoded = try StudyProgress.decode(JSONEncoder().encode(progress))
        XCTAssertEqual(decoded.drafts, progress.drafts)
        XCTAssertEqual(decoded.bookmarks, progress.bookmarks)
        XCTAssertThrowsError(try StudyProgress.decode(Data("{\"version\":2}".utf8)))
    }
    @MainActor func testBundledCurriculumQueueAndDraftPersistence() throws {
        let suite = "PatternAtlas.Tests.\(UUID().uuidString)"
        let defaults = try XCTUnwrap(UserDefaults(suiteName: suite))
        defer { defaults.removePersistentDomain(forName: suite) }
        let store = StudyStore(defaults: defaults)
        let data = try XCTUnwrap(store.curriculum)
        XCTAssertGreaterThan(data.patterns.count, 150)
        let card = try XCTUnwrap(store.queue(nodeId: "dynamic-programming-knapsack").first)
        XCTAssertTrue(data.descendants(of: "dynamic-programming-knapsack").contains(card.patternId))
        store.setDraft("my retained draft", for: card.problem.id)
        store.rate(card.id, .good)
        XCTAssertFalse(store.queue(limit: 1000).contains { $0.id == card.id })
        let reloaded = StudyStore(defaults: defaults)
        XCTAssertEqual(reloaded.draft(for: card.problem), "my retained draft")
        XCTAssertEqual(reloaded.progress.cards[card.id]?.rating, .good)
    }
    @MainActor func testMergeDoesNotEraseExistingDraft() throws {
        let suite = "PatternAtlas.Tests.\(UUID().uuidString)"
        let defaults = try XCTUnwrap(UserDefaults(suiteName: suite))
        defer { defaults.removePersistentDomain(forName: suite) }
        let store = StudyStore(defaults: defaults)
        store.setDraft("local", for: "1")
        var incoming = StudyProgress(); incoming.drafts = ["1": "imported", "2": "new"]
        try store.mergeBackup(JSONEncoder().encode(incoming))
        XCTAssertEqual(store.progress.drafts["1"], "local")
        XCTAssertEqual(store.progress.drafts["2"], "new")
    }
}
