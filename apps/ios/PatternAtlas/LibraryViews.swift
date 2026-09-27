import SwiftUI

struct LibraryView: View {
    let data: Curriculum
    @State private var search = ""
    @State private var level = "All levels"
    var filtered: [PatternNode] {
        data.nodes.filter { $0.kind != "category" && (level == "All levels" || $0.level == level) && (search.isEmpty || "\($0.title) \($0.description) \($0.id)".localizedCaseInsensitiveContains(search)) }
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
        }.navigationTitle("Pattern library").trackPage("/library").searchable(text: $search, prompt: "Find a pattern or technique")
    }
}
struct NodeDetailView: View {
    let data: Curriculum
    let node: PatternNode
    @State private var review = false
    var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 14) {
                    HStack { LevelBadge(text: node.level); LevelBadge(text: node.priority + " priority") }
                    Text(node.title).font(.title2.weight(.bold))
                    Text(node.description).font(.subheadline).foregroundStyle(.secondary)
                }.padding(.vertical, 7)
            }
            Section { NavigationLink("Assess familiarity with this topic") { DiagnosticSetupView(data: data, nodeId: node.id) } }
            Section("The general approach") {
                Text(node.approach).font(.subheadline).lineSpacing(5).padding(.vertical, 5)
                if let pseudocode = node.pseudocode {
                    VStack(alignment: .leading, spacing: 12) {
                        Eyebrow(text: "Pseudocode")
                        ScrollView(.horizontal) {
                            Text(pseudocode.code).font(.system(.caption, design: .monospaced))
                                .lineSpacing(5).textSelection(.enabled).padding(16)
                        }.foregroundStyle(Color(red: 0.84, green: 0.89, blue: 0.98))
                            .background(AtlasStyle.forest, in: RoundedRectangle(cornerRadius: 6))
                            .accessibilityIdentifier("approachPseudocode")
                        if let example = pseudocode.example, !example.isEmpty {
                            Eyebrow(text: "Trace an example")
                            Text(example).font(.system(.caption, design: .monospaced))
                                .lineSpacing(5).textSelection(.enabled)
                        }
                    }.padding(.vertical, 8)
                }
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
            }
            ProblemCollectionSection(data: data, nodeId: node.id)
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
        }.trackPage("/library/\(node.id)").navigationTitle(node.kind == "pattern" ? "Pattern" : "Topic").navigationBarTitleDisplayMode(.inline)
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
    var body: some View {
        List {
            ProblemCollectionSection(data: data, query: query)
            Section { Text("\(data.problems.count.formatted()) problems with offline Python solutions. Official statements and reference-only entries open on LeetCode.").font(.caption).foregroundStyle(.secondary) }
        }.navigationTitle("Problem index").trackPage("/catalog").searchable(text: $query, prompt: "Title or exact problem number")
    }
}

struct ProblemCollectionSection: View {
    let data: Curriculum
    var nodeId: String? = nil
    var query = ""
    @State private var search = ""
    @State private var difficulty = "All"
    @State private var availability = "All problems"
    @State private var limit = 50
    @AppStorage private var orderRaw: String
    init(data: Curriculum, nodeId: String? = nil, query: String = "") {
        self.data = data; self.nodeId = nodeId; self.query = query
        self._orderRaw = AppStorage(wrappedValue: ProblemOrder.difficulty.rawValue, "pattern-atlas.sort.\(nodeId ?? "all")")
    }
    var body: some View {
        let worked = Dictionary(uniqueKeysWithValues: data.problems.map { ($0.id, $0) })
        let text = (nodeId == nil ? query : search).trimmingCharacters(in: .whitespacesAndNewlines)
        let entries = data.entries(for: nodeId).filter { p in
            let card = worked[p.id]
            let matchesText = text.isEmpty || (text.allSatisfy(\.isNumber) ? p.id == text : p.title.localizedCaseInsensitiveContains(text) || (p.tags ?? []).contains { $0.name.localizedCaseInsensitiveContains(text) })
            let available = availability == "All problems" || (availability == "With solutions" ? card != nil : availability == "Authored lessons" ? card?.origin == "authored" : card == nil)
            return matchesText && available && (difficulty == "All" || p.difficulty == difficulty)
        }
        let results = (ProblemOrder(rawValue: orderRaw) ?? .difficulty).sorted(entries)
        Section("Problem filters") {
            if nodeId != nil { TextField("Search title or number", text: $search).accessibilityIdentifier("collectionSearch") }
            Picker("Difficulty", selection: $difficulty) { ForEach(["All", "Easy", "Medium", "Hard"], id: \.self) { Text($0) } }
            Picker("Content", selection: $availability) { ForEach(["All problems", "With solutions", "Authored lessons", "Reference only"], id: \.self) { Text($0) } }
            Picker("Sort problems", selection: $orderRaw) { ForEach(ProblemOrder.allCases, id: \.rawValue) { Text($0.label).tag($0.rawValue) } }.accessibilityIdentifier("sortProblems")
        }
        Section("\(results.count.formatted()) problems · \(results.filter { worked[$0.id] != nil }.count.formatted()) with solutions") {
            if let nodeId, data.node(nodeId)?.kind == "pattern" {
                Text("Authored lessons demonstrate this pattern. Related practice comes from the guide’s surrounding sections and may use neighboring techniques.").font(.caption).foregroundStyle(.secondary)
            }
            ForEach(Array(results.prefix(limit))) { p in
                if let card = worked[p.id] {
                    NavigationLink { ProblemDetailView(data: data, problem: card, initialPattern: card.patternIds.contains(nodeId ?? "") ? nodeId : nil) } label: { CatalogProblemRow(problem: p, kind: card.origin == "community" ? "Community solution" : "Authored lesson") }
                } else if let url = URL(string: "https://leetcode.com/problems/\(p.slug)/") {
                    Link(destination: url) { CatalogProblemRow(problem: p, kind: p.premium ? "Premium reference ↗" : "Reference only ↗") }
                }
            }
            if results.isEmpty { Text("No matching problems. Try another filter.").font(.caption).foregroundStyle(.secondary) }
            if results.count > limit { Button("Show 50 more · \(limit) of \(results.count)") { limit += 50 }.font(.caption) }
        }
    }
}
struct CatalogProblemRow: View {
    let problem: CatalogProblem
    let kind: String
    var body: some View {
        VStack(alignment: .leading, spacing: 9) {
            Text("\(problem.id). \(problem.title)").font(.subheadline.weight(.medium)).foregroundStyle(.primary)
            HStack { LevelBadge(text: problem.difficulty); Text(kind).font(.caption2).foregroundStyle(.secondary) }
        }.padding(.vertical, 5)
    }
}
