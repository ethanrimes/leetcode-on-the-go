import XCTest
@testable import PatternAtlas

final class AnalyticsTests: XCTestCase {
    private let now = dateFromISO("2026-09-27T12:00:00.000Z")!
    private func exportData(account: String = "demo") throws -> Data {
        let entries = [
            LeetCodeSubmission(id: "1", slug: "two-sum", title: "Two Sum", timestamp: "2026-08-01T00:00:00.000Z", status: "Accepted", language: "python3"),
            LeetCodeSubmission(id: "2", slug: "two-sum", title: "Two Sum", timestamp: "2026-09-26T00:00:00.000Z", status: "Wrong Answer", language: "python3"),
            LeetCodeSubmission(id: "3", slug: "valid-anagram", title: "Valid Anagram", timestamp: "2026-07-01T00:00:00.000Z", status: "Wrong Answer", language: "python3")
        ]
        return try JSONEncoder().encode(SubmissionExport(format: "pattern-atlas-leetcode", version: 1, account: account, exportedAt: iso(now), complete: true, submissions: entries))
    }
    @MainActor func testImportsAreIdempotentAndKeepAccountsSeparate() throws {
        let suite = "Atlas.Analytics.\(UUID().uuidString)"; let defaults = try XCTUnwrap(UserDefaults(suiteName: suite))
        defer { defaults.removePersistentDomain(forName: suite) }
        let store = StudyStore(defaults: defaults)
        let packet = try exportData()
        try store.importHistory(packet); try store.importHistory(packet)
        XCTAssertEqual(store.progress.leetcode?.submissions.count, 3)
        XCTAssertThrowsError(try store.importHistory(exportData(account: "other")))
        XCTAssertEqual(store.progress.leetcode?.account, "demo")
        store.setDraft("keep", for: "1"); store.visit("/problem/1", now: now); store.visit("/problem/1", now: now)
        let backup = try store.exportData(); try store.mergeBackup(backup)
        XCTAssertEqual(totalVisits(store.progress.visits ?? [:])["/problem/1"]?.count, 2)
        XCTAssertEqual(store.progress.drafts["1"], "keep")
        XCTAssertEqual(try StudyProgress.decode(backup).leetcode?.submissions.count, 3)
        let old = Data(#"{"version":1,"cards":{},"drafts":{},"bookmarks":[],"activity":{}}"#.utf8)
        XCTAssertNil(try StudyProgress.decode(old).leetcode)
    }
    @MainActor func testCoverageFreshnessAndOverlap() throws {
        let defaults = try XCTUnwrap(UserDefaults(suiteName: "Atlas.Analytics.Content"))
        defer { defaults.removePersistentDomain(forName: "Atlas.Analytics.Content") }
        let store = StudyStore(defaults: defaults), data = try XCTUnwrap(store.curriculum)
        try store.importHistory(exportData())
        let engine = CurriculumAnalytics(data)
        let snapshot = engine.snapshot(store.progress, filter: AnalyticsFilter(), now: now)
        XCTAssertEqual(snapshot.solved, 1); XCTAssertEqual(snapshot.attempted, 1)
        var filter = AnalyticsFilter(); filter.depth = 99
        let leaves = engine.snapshot(store.progress, filter: filter, now: now)
        let frequency = try XCTUnwrap(leaves.tiles.first { $0.node.title == "Frequency signatures" })
        XCTAssertEqual(frequency.fresh, 0) // A visit cannot refresh the old anagram attempt.
        store.visit("/library/\(frequency.id)", now: now)
        let after = engine.snapshot(store.progress, filter: filter, now: now)
        XCTAssertEqual(after.tiles.first { $0.id == frequency.id }?.fresh, 0)
        XCTAssertEqual(after.tiles.first { $0.id == frequency.id }?.visits, 1)
        filter.period = 30
        XCTAssertEqual(engine.snapshot(store.progress, filter: filter, now: now).solved, 0)
    }
    func testInvalidRecordsAndTreemapGeometry() throws {
        XCTAssertThrowsError(try LeetCodeHistory.decodeExport(Data(#"{"format":"other"}"#.utf8)))
        let bad = PageVisit(count: -1, lastVisited: iso(now))
        XCTAssertFalse(validVisits(["web": ["/": bad]]))
        let one = ["web": ["/": PageVisit(count: 2, lastVisited: iso(now))]]
        let two = ["ios": ["/": PageVisit(count: 3, lastVisited: iso(now))]]
        let merged = mergeVisits(one, two)
        XCTAssertEqual(totalVisits(mergeVisits(merged, merged))["/"]?.count, 5)
        let weights = [100,50,40,10,1,0]
        let rectangles = treemap(weights, width: 800, height: 500)
        XCTAssertEqual(rectangles.count, 5)
        for rect in rectangles { XCTAssertEqual(rect.width * rect.height / 400000, Double(weights[rect.id]) / 201, accuracy: 0.000001) }
    }
}
