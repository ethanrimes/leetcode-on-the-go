import Foundation

var activityCalendar: Calendar {
    var calendar = Calendar(identifier: .gregorian)
    calendar.timeZone = TimeZone(secondsFromGMT: 0)!
    return calendar
}
func activityDay(_ date: Date) -> String {
    let parts = activityCalendar.dateComponents([.year, .month, .day], from: date)
    return String(format: "%04d-%02d-%02d", parts.year ?? 0, parts.month ?? 0, parts.day ?? 0)
}
func activityDate(_ day: String) -> Date? { dateFromISO(day + "T00:00:00Z") }

struct ActivityCalendar: Codable {
    let year: Int
    let observedAt: String
    let days: [String: Int]
    var valid: Bool {
        year >= 1000 && year <= 9999 && dateFromISO(observedAt) != nil && days.count <= 366 && days.allSatisfy { day, count in
            guard day.hasPrefix("\(year)-"), day.count == 10, let date = activityDate(day) else { return false }
            return activityDay(date) == day && day <= String(observedAt.prefix(10)) && count > 0 && count <= 1_000_000
        }
    }
}
struct LeetCodeActivity {
    var counts: [String: Int] = [:]
    var byDay: [String: [LeetCodeSubmission]] = [:]
    var source: ActivityCalendar?
    var longest = 0
    var current = 0
    var total: Int { counts.values.reduce(0, +) }
    var imported: Int { byDay.values.reduce(0) { $0 + $1.count } }
    var accepted: Int { byDay.values.reduce(0) { $0 + $1.filter(\.accepted).count } }
    var activeDays: Int { counts.values.filter { $0 > 0 }.count }
}
func leetCodeActivity(_ history: LeetCodeHistory, year: Int, now: Date = .now) -> LeetCodeActivity {
    let today = activityDay(now), snapshot = history.calendars?[String(year)]
    var result = LeetCodeActivity(source: snapshot)
    if let snapshot { result.counts = snapshot.days.filter { $0.key <= today } }
    for submission in history.submissions.values {
        guard let date = dateFromISO(submission.timestamp), date <= now, activityCalendar.component(.year, from: date) == year else { continue }
        let day = activityDay(date)
        result.byDay[day, default: []].append(submission)
        if snapshot == nil || date > (dateFromISO(snapshot!.observedAt) ?? .distantPast) { result.counts[day, default: 0] += 1 }
    }
    var run = 0, previous: Date?
    for day in result.counts.keys.sorted() {
        guard result.counts[day, default: 0] > 0, let date = activityDate(day) else { continue }
        run = previous.map { date.timeIntervalSince($0) == 86400 } == true ? run + 1 : 1
        result.longest = max(result.longest, run); previous = date
    }
    if year == activityCalendar.component(.year, from: now), let start = activityDate(today) {
        var cursor = result.counts[today, default: 0] > 0 ? start : start.addingTimeInterval(-86400)
        while activityCalendar.component(.year, from: cursor) == year && result.counts[activityDay(cursor), default: 0] > 0 {
            result.current += 1; cursor = cursor.addingTimeInterval(-86400)
        }
    }
    return result
}
