import SwiftUI

struct LibraryView: View {
    let data: Curriculum
    @State private var search = ""
    @State private var level = "All levels"
    var filtered: [PatternNode] {
        data.patterns.filter { (level == "All levels" || $0.level == level) && (search.isEmpty || "\($0.title) \($0.description) \($0.id)".localizedCaseInsensitiveContains(search)) }
    }
    var body: some View {
        List {
            Section {
                Picker("Pattern level", selection: $level) { ForEach(["All levels", "Foundation", "Intermediate", "Advanced"], id: \.self) { Text($0) } }
            }
            if search.isEmpty && level == "All levels" {
                Section("Browse the hierarchy") {
                    ForEach(data.roots) { node in
                        NavigationLink { NodeDetailView(data: data, node: node) } label: {
                            VStack(alignment: .leading, spacing: 7) { Text(node.title).font(.headline); Text(node.description).font(.caption).foregroundStyle(.secondary) }.padding(.vertical, 6)
                        }
                    }
                }
            } else {
                Section("\(filtered.count) patterns") {
                    ForEach(filtered) { node in
                        NavigationLink { NodeDetailView(data: data, node: node) } label: {
                            VStack(alignment: .leading, spacing: 7) { Text(node.title).font(.subheadline.weight(.medium)); LevelBadge(text: node.level); Text(node.description).font(.caption).foregroundStyle(.secondary) }.padding(.vertical, 5)
                        }
                    }
                }
                if filtered.isEmpty { ContentUnavailableView.search(text: search) }
            }
        }.navigationTitle("Pattern library").searchable(text: $search, prompt: "Find a pattern or technique")
    }
}
struct NodeDetailView: View {
    let data: Curriculum
    let node: PatternNode
    @State private var review = false
    @State private var difficulty = "All"
    var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 14) {
                    HStack { LevelBadge(text: node.level); LevelBadge(text: node.priority + " priority") }
                    Text(node.title).font(.title2.weight(.bold))
                    Text(node.description).font(.subheadline).foregroundStyle(.secondary)
                }.padding(.vertical, 7)
            }
            Section("The general approach") {
                Text(node.approach).font(.subheadline).lineSpacing(5).padding(.vertical, 5)
                ForEach(node.tips, id: \.self) { tip in Label { Text(tip).font(.caption).lineSpacing(4) } icon: { Image(systemName: "lightbulb").foregroundStyle(AtlasStyle.green) } }
            }
            Section("Why learn this?") { Text(node.why).font(.caption).foregroundStyle(.secondary).lineSpacing(4) }
            if !data.children(of: node.id).isEmpty {
                Section("Go one level deeper") {
                    ForEach(data.children(of: node.id)) { child in
                        NavigationLink { NodeDetailView(data: data, node: child) } label: {
                            VStack(alignment: .leading, spacing: 8) { Text(child.title).font(.subheadline.weight(.medium)); HStack { LevelBadge(text: child.level); Text(child.kind == "pattern" ? "Pattern" : "Technique family").font(.caption2).foregroundStyle(.secondary) } }.padding(.vertical, 4)
                        }
                    }
                }
            }
            Section {
                Button { review = true } label: { Label("Study this topic", systemImage: "square.stack.3d.up").font(.subheadline.weight(.semibold)) }.accessibilityIdentifier("studyTopic")
                Picker("Problem difficulty", selection: $difficulty) { ForEach(["All", "Easy", "Medium", "Hard"], id: \.self) { Text($0) } }
            }
            Section("Worked problems") {
                let problems = data.problems(for: node.id).filter { difficulty == "All" || $0.difficulty == difficulty }
                ForEach(problems) { problem in
                    NavigationLink { ProblemDetailView(data: data, problem: problem, initialPattern: node.kind == "pattern" ? node.id : nil) } label: { ProblemRow(problem: problem) }
                }
                if problems.isEmpty { Text("No worked problems at this difficulty. Try another filter.").font(.caption).foregroundStyle(.secondary) }
            }
            Section("Reference reading") {
                ForEach(Array(node.sourceUrls.enumerated()), id: \.element) { index, raw in
                    if let url = URL(string: raw) { Link(index == 0 ? "LeetCode reference ↗" : "EndlessCheng guide ↗", destination: url).font(.caption) }
                }
                ForEach(Array(node.references.enumerated()), id: \.offset) { _, section in
                    if let url = URL(string: section.url) {
                        Link(destination: url) { VStack(alignment: .leading, spacing: 5) { Text(section.title); Text("\(section.problemIds.count) additional problem references in this source section").foregroundStyle(.secondary) } }.font(.caption)
                    }
                }
            }
        }.navigationTitle(node.kind == "pattern" ? "Pattern" : "Topic").navigationBarTitleDisplayMode(.inline)
            .sheet(isPresented: $review) { NavigationStack { ReviewSessionView(data: data, nodeId: node.id) } }
    }
}
struct ProblemRow: View {
    let problem: StudyProblem
    @Environment(StudyStore.self) private var store
    var body: some View {
        HStack(spacing: 10) {
            Image(systemName: store.learned(problem) ? "checkmark.circle.fill" : "chevron.left.forwardslash.chevron.right").font(.caption).foregroundStyle(AtlasStyle.green)
            VStack(alignment: .leading, spacing: 7) { Text("\(problem.id). \(problem.title)").font(.subheadline.weight(.medium)); HStack { LevelBadge(text: problem.difficulty); if store.progress.bookmarks.contains(problem.id) { Image(systemName: "bookmark.fill").font(.caption2).foregroundStyle(AtlasStyle.green) } } }
        }.padding(.vertical, 5)
    }
}
struct ProblemLibraryView: View {
    let data: Curriculum
    @State private var query = ""
    @State private var difficulty = "All"
    var results: [StudyProblem] {
        data.problems.filter { (difficulty == "All" || $0.difficulty == difficulty) && (query.isEmpty || $0.title.localizedCaseInsensitiveContains(query) || $0.id == query || $0.solutions.contains { $0.title.localizedCaseInsensitiveContains(query) }) }
    }
    var body: some View {
        List {
            Section { Picker("Difficulty", selection: $difficulty) { ForEach(["All", "Easy", "Medium", "Hard"], id: \.self) { Text($0) } } }
            Section("\(results.count) worked study cards") {
                ForEach(results) { problem in NavigationLink { ProblemDetailView(data: data, problem: problem) } label: { ProblemRow(problem: problem) } }
            }
            if results.isEmpty { ContentUnavailableView.search(text: query) }
            Section { Text("All worked cards are available offline. The complete LeetCode reference catalog is available in the web app.").font(.caption).foregroundStyle(.secondary) }
        }.navigationTitle("Problems").searchable(text: $query, prompt: "Title, number, or pattern")
    }
}
