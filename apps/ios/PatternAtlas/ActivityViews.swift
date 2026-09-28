import SwiftUI

private struct ActivityDaySelection: Identifiable { let id: String }
struct LeetCodeActivitySection: View {
    let data: Curriculum
    let history: LeetCodeHistory
    @State private var year = activityCalendar.component(.year, from: .now)
    @State private var selectedDay: ActivityDaySelection?
    private var years: [Int] {
        Set([activityCalendar.component(.year, from: .now)] + (history.calendars ?? [:]).keys.compactMap(Int.init) + history.submissions.values.compactMap { dateFromISO($0.timestamp).map { activityCalendar.component(.year, from: $0) } }).sorted(by: >)
    }
    private var weeks: [[Date]] {
        let calendar = activityCalendar
        guard let start = calendar.date(from: DateComponents(year: year, month: 1, day: 1)),
              let end = calendar.date(from: DateComponents(year: year + 1, month: 1, day: 1)) else { return [] }
        var cursor = calendar.date(byAdding: .day, value: -(calendar.component(.weekday, from: start) + 5) % 7, to: start) ?? start
        var result: [[Date]] = []
        while cursor < end {
            result.append((0..<7).map { cursor.addingTimeInterval(Double($0) * 86400) })
            cursor = cursor.addingTimeInterval(7 * 86400)
        }
        return result
    }
    private func color(_ count: Int) -> Color {
        switch count {
        case 0: Color.gray.opacity(0.16)
        case 1: Color.blue.opacity(0.28)
        case 2...3: Color.blue.opacity(0.5)
        case 4...7: Color.blue.opacity(0.72)
        default: Color.blue
        }
    }
    var body: some View {
        let summary = leetCodeActivity(history, year: year)
        Section {
            Picker("Year", selection: $year) { ForEach(years, id: \.self) { Text(String($0)).tag($0) } }
            HStack {
                StatView(value: "\(summary.total)", label: summary.source == nil ? "Imported submissions" : "Submissions")
                StatView(value: "\(summary.activeDays)", label: "Active days")
                StatView(value: "\(summary.longest)", label: "Best streak in \(String(year))")
            }.padding(.vertical, 8)
            if year == activityCalendar.component(.year, from: .now) { Text("Current streak in \(String(year)): \(summary.current) days").font(.subheadline) }
            Text("\(summary.accepted) accepted in imported details").font(.caption).foregroundStyle(.secondary)
            if let source = summary.source {
                Text("LeetCode calendar: \(summary.total) submissions. \(summary.imported) details imported\(summary.total == summary.imported ? " — totals match." : ". Some individual results may be unavailable.") Refreshed \(dateFromISO(source.observedAt)?.formatted() ?? source.observedAt).")
                    .font(.caption).foregroundStyle(.secondary)
            } else { Text("LeetCode’s yearly calendar has not been imported. Totals and streaks use available details and may be incomplete. Run a history update to reconcile them.").font(.caption).foregroundStyle(.secondary) }
            ScrollView(.horizontal) {
                HStack(alignment: .top, spacing: 3) {
                    ForEach(weeks.indices, id: \.self) { week in
                        VStack(spacing: 3) {
                            ForEach(weeks[week], id: \.self) { day in
                                let key = activityDay(day), count = summary.counts[key, default: 0]
                                Button { selectedDay = ActivityDaySelection(id: key) } label: { RoundedRectangle(cornerRadius: 2).fill(color(count)).frame(width: 12, height: 12) }
                                    .buttonStyle(.plain)
                                    .disabled(activityCalendar.component(.year, from: day) != year)
                                    .accessibilityLabel("\(key): \(count) submissions (UTC)")
                            }
                        }
                    }
                }.padding(.vertical, 5)
            }.scrollIndicators(.hidden)
            Text("Select a day to inspect its submissions. Days use LeetCode’s UTC boundary. Activity and longest streak use the selected year; undated completions contribute to coverage only.").font(.caption).foregroundStyle(.secondary)
        } header: { Text("Your activity") }
            .sheet(item: $selectedDay) { selection in
                NavigationStack {
                    List {
                        let entries = (summary.byDay[selection.id] ?? []).sorted { $0.timestamp > $1.timestamp }
                        let total = summary.counts[selection.id, default: 0]
                        Text("\(total) submissions · \(entries.count) details imported · \(entries.filter(\.accepted).count) known accepted").font(.subheadline)
                        if total > entries.count { Text("\(total - entries.count) submission details have not been imported for this day. The calendar total comes from LeetCode.").font(.caption).foregroundStyle(.secondary) }
                        if entries.isEmpty && total == 0 { Text(summary.source == nil ? "No submission details imported for this day." : "No submissions reported by LeetCode on this day.").foregroundStyle(.secondary) }
                        ForEach(entries) { submission in
                            VStack(alignment: .leading, spacing: 6) {
                                if let problem = data.problems.first(where: { $0.slug == submission.slug }) {
                                    NavigationLink(submission.title) { ProblemDetailView(data: data, problem: problem) }
                                } else { Link(submission.title, destination: URL(string: "https://leetcode.com/problems/\(submission.slug)/")!) }
                                Text("\(submission.status) · \(submission.language)")
                                    .font(.caption).foregroundStyle(submission.accepted ? .blue : .orange)
                                Link("View submission ↗", destination: URL(string: "https://leetcode.com/submissions/detail/\(submission.id)/")!).font(.caption)
                            }.padding(.vertical, 4)
                        }
                    }.navigationTitle(selection.id + " · UTC")
                        .toolbar { Button("Done") { selectedDay = nil } }
                }
            }
    }
}
