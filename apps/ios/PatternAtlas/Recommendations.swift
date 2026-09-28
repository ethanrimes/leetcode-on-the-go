import Foundation

struct PracticeRecommendation: Identifiable {
    let node: PatternNode
    let problem: StudyProblem
    let rootId: String
    let topic: String
    let kind: String
    let reason: String
    let score: Double
    var id: String { node.id }
}

// Keep priorities and topic diversification aligned with packages/core/recommendations.ts.
func practiceRecommendations(_ data: Curriculum, progress: StudyProgress, filter: AnalyticsFilter, now: Date = .now) -> [PracticeRecommendation] {
    let branch = filter.selectedScopes.isEmpty ? nil : filter.selectedScopes.reduce(into: Set<String>()) { $0.formUnion(data.descendants(of: $1)) }
    var latest: [String: LeetCodeSubmission] = [:]
    var completed = Set(progress.leetcode?.completions?.slugs ?? [])
    for submission in progress.leetcode?.submissions.values ?? [:].values {
        guard let date = dateFromISO(submission.timestamp), date <= now else { continue }
        if submission.accepted { completed.insert(submission.slug) }
        let previous = latest[submission.slug]
        if previous == nil || submission.timestamp > previous!.timestamp || (submission.timestamp == previous!.timestamp && submission.id.compare(previous!.id, options: .numeric) == .orderedDescending) { latest[submission.slug] = submission }
    }
    var candidates: [PracticeRecommendation] = []
    for node in data.patterns {
        if let branch, !branch.contains(node.id) { continue }
        if !filter.selectedLevels.isEmpty && !filter.selectedLevels.contains(node.level) { continue }
        var root = node; var seen = Set<String>()
        while let parentId = root.parentId, let parent = data.node(parentId), seen.insert(parentId).inserted { root = parent }
        for problem in data.problems where problem.solutions.contains(where: { $0.patternId == node.id }) {
            if !filter.selectedDifficulties.isEmpty && !filter.selectedDifficulties.contains(problem.difficulty) { continue }
            let key = cardKey(problem.id, node.id), review = progress.cards[key]
            let rating = progress.familiarity?[key]?.rating, submission = latest[problem.slug]
            let submissionDate = submission.flatMap { dateFromISO($0.timestamp) }, reviewDate = review.flatMap { dateFromISO($0.lastReviewed) }
            let practiceDates = [submissionDate, reviewDate].compactMap { $0 }
            let age = practiceDates.max().map { max(0, Int(now.timeIntervalSince($0) / 86400)) }
            var kind: String; var reason: String; var score: Double
            if let review, (dateFromISO(review.due) ?? .distantFuture) <= now {
                kind = "Review due"; reason = "Your saved recall review is due."; score = 500
            } else if let submission, !submission.accepted, (reviewDate ?? .distantPast) < (submissionDate ?? .distantPast) {
                kind = "Retry a problem"; reason = "Latest recorded submission: \(submission.status). Revisit the approach."; score = 450
            } else if rating == .notYet || rating == .probably {
                kind = "Revisit the solution"; reason = rating == .notYet ? "You marked this approach “Did not get it.”" : "You marked this approach “Probably got it.”"; score = rating == .notYet ? 420 : 380
            } else if let age, age >= filter.freshDays {
                kind = "Refresh recall"; reason = "Last practiced \(age) days ago. Try recalling the pattern first."; score = 250 + Double(min(age, 120)) / 4
            } else if age == nil && completed.contains(problem.slug) {
                kind = "Check your recall"; reason = "Completed on LeetCode; its practice date is unavailable."; score = 160
            } else if age == nil && !completed.contains(problem.slug) {
                kind = "Build coverage"; reason = "No completion or practice recorded for this worked example."; score = 100
            } else { continue }
            score += node.priority == "Core" ? 20 : node.priority == "Useful" ? 10 : 0
            if node.level == "Foundation" { score += 3 }
            candidates.append(PracticeRecommendation(node: node, problem: problem, rootId: root.id, topic: root.title, kind: kind, reason: reason, score: score))
        }
    }
    var chosen: [PracticeRecommendation] = [], usedProblems = Set<String>(), usedNodes = Set<String>(), topics: [String: Int] = [:]
    while chosen.count < 6 {
        let ranked = candidates.filter { !usedProblems.contains($0.problem.id) && !usedNodes.contains($0.node.id) }.sorted { a, b in
            let x = a.score - Double(topics[a.rootId, default: 0] * 120), y = b.score - Double(topics[b.rootId, default: 0] * 120)
            if x != y { return x > y }
            if a.node.id != b.node.id { return a.node.id < b.node.id }
            return a.problem.id.compare(b.problem.id, options: .numeric) == .orderedAscending
        }
        guard let next = ranked.first else { break }
        chosen.append(next); usedProblems.insert(next.problem.id); usedNodes.insert(next.node.id); topics[next.rootId, default: 0] += 1
    }
    return chosen
}
