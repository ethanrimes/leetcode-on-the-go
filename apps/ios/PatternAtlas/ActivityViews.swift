import SwiftUI

private func activityKey(_ date: Date) -> String {
    let parts = Calendar.current.dateComponents([.year, .month, .day], from: date)
    return String(format: "%04d-%02d-%02d", parts.year ?? 0, parts.month ?? 0, parts.day ?? 0)
}

struct LeetCodeActivitySection: View {
    let data: Curriculum
    let history: LeetCodeHistory
    @State private var year = Calendar.current.component(.year, from: .now)
    @State private var selectedDay: String?

    private var byDay: [String: [LeetCodeSubmission]] {
        Dictionary(grouping: history.submissions.values.compactMap { submission -> (String, LeetCodeSubmission)? in
            guard let date = dateFromISO(submission.timestamp) else { return nil }
            return (activityKey(date), submission)
        }, by: { $0.0 }).mapValues { $0.map(\.1) }
    }
    private var years: [Int] {
        Set([Calendar.current.component(.year, from: .now)] + byDay.keys.compactMap { Int($0.prefix(4)) }).sorted(by: >)
    }
    private var keys: [String] { byDay.keys.sorted() }
    private var currentStreak: Int {
        guard let last = keys.last else { return 0 }
        let today = activityKey(.now), yesterday = activityKey(Calendar.current.date(byAdding: .day, value: -1, to: .now) ?? .now)
        guard last == today || last == yesterday else { return 0 }
        var count = 1
        for index in stride(from: keys.count - 1, to: 0, by: -1) {
            guard let earlier = dayDate(keys[index - 1]), let later = dayDate(keys[index]),
                  Calendar.current.dateComponents([.day], from: earlier, to: later).day == 1 else { break }
            count += 1
        }
        return count
    }
    private var longestStreak: Int {
        var longest = 0, run = 0, previous: Date?
        for key in keys {
            guard let date = dayDate(key) else { continue }
            run = previous.map { Calendar.current.dateComponents([.day], from: $0, to: date).day == 1 } == true ? run + 1 : 1
            longest = max(longest, run); previous = date
        }
        return longest
    }
    private func dayDate(_ key: String) -> Date? {
        let parts = key.split(separator: "-").compactMap { Int($0) }
        guard parts.count == 3 else { return nil }
        return Calendar.current.date(from: DateComponents(year: parts[0], month: parts[1], day: parts[2], hour: 12))
    }
    private var weeks: [[Date]] {
        let calendar = Calendar.current
        guard let start = calendar.date(from: DateComponents(year: year, month: 1, day: 1)),
              let end = calendar.date(from: DateComponents(year: year + 1, month: 1, day: 1)) else { return [] }
        let weekday = (calendar.component(.weekday, from: start) + 5) % 7
        var cursor = calendar.date(byAdding: .day, value: -weekday, to: start) ?? start
        var result: [[Date]] = []
        while cursor < end {
            result.append((0..<7).compactMap { calendar.date(byAdding: .day, value: $0, to: cursor) })
            cursor = calendar.date(byAdding: .day, value: 7, to: cursor) ?? end
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
        let current = byDay.filter { $0.key.hasPrefix(String(year)) }
        Section {
            Picker("Year", selection: $year) { ForEach(years, id: \.self) { Text(String($0)).tag($0) } }
            HStack {
                StatView(value: "\(current.values.reduce(0) { $0 + $1.count })", label: "Submissions")
                StatView(value: "\(current.count)", label: "Active days")
                StatView(value: "\(currentStreak)", label: "Day streak")
                StatView(value: "\(longestStreak)", label: "Best streak")
            }.padding(.vertical, 8)
            ScrollView(.horizontal) {
                HStack(alignment: .top, spacing: 3) {
                    ForEach(weeks.indices, id: \.self) { week in
                        VStack(spacing: 3) {
                            ForEach(weeks[week], id: \.self) { day in
                                let key = activityKey(day), count = byDay[key]?.count ?? 0
                                Button { selectedDay = key } label: { RoundedRectangle(cornerRadius: 2).fill(color(count)).frame(width: 12, height: 12) }
                                    .buttonStyle(.plain)
                                    .disabled(Calendar.current.component(.year, from: day) != year)
                                    .accessibilityLabel("\(day.formatted(date: .abbreviated, time: .omitted)): \(count) submissions")
                            }
                        }
                    }
                }.padding(.vertical, 5)
            }.scrollIndicators(.hidden)
            Text("Select a day to see its LeetCode submissions. Undated completions do not create activity or streaks.").font(.caption).foregroundStyle(.secondary)
        } header: { Text("Your activity") }
            .sheet(isPresented: Binding(get: { selectedDay != nil }, set: { if !$0 { selectedDay = nil } })) {
                NavigationStack {
                    List {
                        let entries = (byDay[selectedDay ?? ""] ?? []).sorted { $0.timestamp > $1.timestamp }
                        if entries.isEmpty { Text("No recorded submissions on this day.").foregroundStyle(.secondary) }
                        ForEach(entries) { submission in
                            VStack(alignment: .leading, spacing: 6) {
                                if let problem = data.problems.first(where: { $0.slug == submission.slug }) {
                                    NavigationLink(submission.title) { ProblemDetailView(data: data, problem: problem) }
                                } else { Link(submission.title, destination: URL(string: "https://leetcode.com/problems/\(submission.slug)/")!) }
                                Text("\(submission.status) · \(submission.language) · \(dateFromISO(submission.timestamp)?.formatted(date: .omitted, time: .shortened) ?? "")")
                                    .font(.caption).foregroundStyle(submission.accepted ? .blue : .orange)
                                Link("View submission ↗", destination: URL(string: "https://leetcode.com/submissions/detail/\(submission.id)/")!).font(.caption)
                            }.padding(.vertical, 4)
                        }
                    }.navigationTitle(dayDate(selectedDay ?? "")?.formatted(date: .abbreviated, time: .omitted) ?? "Activity")
                        .toolbar { Button("Done") { selectedDay = nil } }
                }
            }
    }
}
