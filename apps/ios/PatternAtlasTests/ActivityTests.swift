import XCTest
@testable import PatternAtlas

final class ActivityTests: XCTestCase {
    func testSourceCalendarTotalsUTCAndSelectedYearStreak() throws {
        let source = ActivityCalendar(year: 2025, observedAt: "2026-09-28T01:00:00Z", days: ["2025-05-01": 10, "2025-05-02": 20, "2025-12-03": 2])
        let detail = LeetCodeSubmission(id: "1", slug: "two-sum", title: "Two Sum", timestamp: "2025-05-01T00:30:00Z", status: "Accepted", language: "python3")
        let packet = SubmissionExport(calendars: ["2025": source], format: "pattern-atlas-leetcode", version: 1, account: "demo", exportedAt: source.observedAt, complete: false, submissions: [detail])
        let history = try LeetCodeHistory.decodeExport(JSONEncoder().encode(packet))
        let result = leetCodeActivity(history, year: 2025, now: dateFromISO("2026-09-28T02:00:00Z")!)
        XCTAssertEqual(result.total, 32); XCTAssertEqual(result.imported, 1); XCTAssertEqual(result.accepted, 1)
        XCTAssertEqual(result.activeDays, 3); XCTAssertEqual(result.longest, 2); XCTAssertEqual(result.current, 0)
        XCTAssertEqual(result.byDay["2025-05-01"]?.count, 1); XCTAssertNil(result.byDay["2025-12-03"])
        var oldClient = history; oldClient.calendars = nil
        XCTAssertEqual(try history.merging(oldClient).calendars?["2025"]?.days, source.days)
        XCTAssertFalse(ActivityCalendar(year: 2025, observedAt: source.observedAt, days: ["2025-02-30": 1]).valid)
        XCTAssertFalse(ActivityCalendar(year: 2025, observedAt: source.observedAt, days: ["2025-05-01": -1]).valid)
    }
    func testNewDetailsExtendSourceCountsOnceAndExcludeFutureActivity() {
        let source = ActivityCalendar(year: 2026, observedAt: "2026-01-02T01:00:00Z", days: ["2026-01-01": 2, "2026-01-02": 1])
        let dates = ["2025-12-31T23:59:59Z", "2026-01-02T00:00:00Z", "2026-01-02T02:00:00Z", "2026-01-03T00:00:00Z", "2026-01-04T00:00:00Z"]
        let entries = dates.enumerated().map { index, date in LeetCodeSubmission(id: String(index), slug: "two-sum", title: "Two Sum", timestamp: date, status: "Accepted", language: "python3") }
        let history = LeetCodeHistory(calendars: ["2026": source], account: "demo", exportedAt: source.observedAt, complete: false, submissions: Dictionary(uniqueKeysWithValues: entries.map { ($0.id, $0) }))
        let result = leetCodeActivity(history, year: 2026, now: dateFromISO("2026-01-03T01:00:00Z")!)
        XCTAssertEqual(result.total, 5); XCTAssertEqual(result.imported, 3)
        XCTAssertEqual(result.longest, 3); XCTAssertEqual(result.current, 3)
        XCTAssertEqual(result.counts["2026-01-02"], 2); XCTAssertNil(result.counts["2026-01-04"])
    }
}
