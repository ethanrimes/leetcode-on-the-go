import SwiftUI

struct FamiliarityTotalsView: View {
    let summary: FamiliaritySummary
    var body: some View {
        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 18) {
            StatView(value: "\(summary.definitely)", label: "Definitely got it")
            StatView(value: "\(summary.probably)", label: "Probably got it")
            StatView(value: "\(summary.notYet)", label: "Did not get it")
            StatView(value: "\(summary.unassessed)", label: "Unassessed")
        }.padding(.vertical, 12)
    }
}
struct FamiliarityBarView: View {
    let summary: FamiliaritySummary
    var body: some View {
        GeometryReader { geometry in
            let unit = geometry.size.width / Double(max(1, summary.total))
            HStack(spacing: 0) {
                AtlasStyle.green.frame(width: unit * Double(summary.definitely))
                Color.orange.opacity(0.7).frame(width: unit * Double(summary.probably))
                Color(red: 0.71, green: 0.36, blue: 0.4).frame(width: unit * Double(summary.notYet))
                Color.secondary.opacity(0.18).frame(width: unit * Double(summary.unassessed))
            }.clipShape(RoundedRectangle(cornerRadius: 3))
        }.frame(height: 14).accessibilityLabel("\(summary.definitely) definitely, \(summary.probably) probably, \(summary.notYet) did not get it, \(summary.unassessed) unassessed")
    }
}
struct FamiliarityDashboardSection: View {
    let data: Curriculum
    @Environment(StudyStore.self) private var store
    var body: some View {
        let summary = FamiliaritySummary(diagnosticCards(data), progress: store.progress)
        Section {
            FamiliarityTotalsView(summary: summary)
            NavigationLink { DiagnosticSetupView(data: data) } label: { Label("Start diagnostic test", systemImage: "checklist") }.accessibilityIdentifier("startDiagnostic")
            NavigationLink("Familiarity by concept & pattern") { FamiliarityReportView(data: data) }
            Text("\(summary.assessed) of \(summary.total) authored solution sets assessed").font(.caption).foregroundStyle(.secondary)
        } header: { Text("Diagnostic familiarity") } footer: { Text("Open solutions and flag how well you understand them. Self-assessments are separate from submissions, recall, and practice freshness. Unassessed means unknown.") }
    }
}
struct FamiliarityReportView: View {
    let data: Curriculum
    @Environment(StudyStore.self) private var store
    @State private var options = DiagnosticOptions()
    @State private var leaves = false
    @State private var uncertain = false
    @State private var query = ""
    var body: some View {
        let rows = familiarityByNode(data, progress: store.progress, options: options, leaves: leaves).filter { row in
            (query.isEmpty || row.node.title.localizedCaseInsensitiveContains(query)) && (!uncertain || row.summary.notYet + row.summary.probably > 0)
        }
        List {
            Section {
                Picker("Category", selection: $options.nodeId) { Text("All concepts").tag(""); ForEach(data.nodes.filter { $0.kind == "category" }) { Text($0.title).tag($0.id) } }
                Toggle("Individual patterns & collections", isOn: $leaves)
                Toggle("Include community collections", isOn: $options.includeCommunity)
                Toggle("Uncertain ratings only", isOn: $uncertain)
            }
            Section {
                FamiliarityTotalsView(summary: FamiliaritySummary(diagnosticCards(data, options: options), progress: store.progress))
            } footer: { Text("Each solution set is a problem paired with one mapped approach. Community collections are broad groupings, not exact authored patterns.") }
            ForEach(rows) { row in
                Section {
                    NavigationLink { NodeDetailView(data: data, node: row.node) } label: { Text(row.node.title).font(.subheadline.weight(.semibold)) }
                    FamiliarityBarView(summary: row.summary)
                    Text("\(row.summary.definitely) definitely · \(row.summary.probably) probably · \(row.summary.notYet) did not get it").font(.caption).foregroundStyle(.secondary)
                    Text("\(row.summary.assessed)/\(row.summary.total) assessed").font(.caption2).foregroundStyle(.secondary)
                    if let date = row.summary.lastAssessed.flatMap(dateFromISO) { Text("Last assessed \(date.formatted(date: .abbreviated, time: .omitted))").font(.caption2).foregroundStyle(.secondary) }
                    NavigationLink("Assess this group") { DiagnosticSetupView(data: data, nodeId: row.id, mode: uncertain ? .uncertain : .unassessed, includeCommunity: options.includeCommunity) }
                }
            }
            if rows.isEmpty { Text("No familiarity results match these filters.").font(.caption) }
        }.navigationTitle("Familiarity").searchable(text: $query, prompt: "Concept or pattern").trackPage("/progress/familiarity")
    }
}
struct DiagnosticSetupView: View {
    let data: Curriculum
    @Environment(StudyStore.self) private var store
    @State private var options: DiagnosticOptions
    @State private var cards: [DiagnosticCard] = []
    @State private var running = false
    init(data: Curriculum, nodeId: String = "", mode: DiagnosticMode = .unassessed, includeCommunity: Bool = false) {
        self.data = data
        _options = State(initialValue: DiagnosticOptions(nodeId: nodeId, includeCommunity: includeCommunity || data.node(nodeId)?.kind == "collection", mode: mode))
    }
    var body: some View {
        let eligible = diagnosticQueue(data, progress: store.progress, options: DiagnosticOptions(nodeId: options.nodeId, difficulty: options.difficulty, includeCommunity: options.includeCommunity, mode: options.mode, limit: Int.max))
        Form {
            Section { Text("Open the solutions. Follow the reasoning. Flag your confidence—no answer or code required.").font(.subheadline).lineSpacing(4) }
            Section("Choose your diagnostic") {
                Picker("Category", selection: $options.nodeId) { Text("Entire curriculum").tag(""); ForEach(data.nodes) { Text($0.title).tag($0.id) } }
                    .onChange(of: options.nodeId) { _, id in if data.node(id)?.kind == "collection" { options.includeCommunity = true } }
                Picker("Problem difficulty", selection: $options.difficulty) { Text("All difficulties").tag(""); ForEach(["Easy", "Medium", "Hard"], id: \.self) { Text($0).tag($0) } }
                Toggle("Include community collections", isOn: $options.includeCommunity)
                Picker("Include", selection: $options.mode) { ForEach(DiagnosticMode.allCases, id: \.self) { Text($0.label).tag($0) } }
                Picker("Test length", selection: $options.limit) { ForEach([10,20,50,10000], id: \.self) { Text($0 == 10000 ? "All eligible sets" : "\($0) solution sets").tag($0) } }
            }
            Section {
                Button { cards = Array(eligible.prefix(options.limit)); running = true } label: { Label("Start diagnostic test", systemImage: "checklist") }.disabled(eligible.isEmpty).accessibilityIdentifier("beginDiagnostic")
                Text("\(eligible.count) eligible solution sets").font(.caption).foregroundStyle(.secondary)
                if eligible.isEmpty { Text("Change the filters or choose All to reassess saved ratings.").font(.caption) }
            } footer: { Text("Samples spread across concepts and patterns. Ratings save immediately. Return to Unassessed only to continue where you left off.") }
        }.navigationTitle("Diagnostic test").trackPage("/diagnostic")
            .navigationDestination(isPresented: $running) { DiagnosticSessionView(data: data, cards: cards) }
    }
}
struct DiagnosticSessionView: View {
    let data: Curriculum
    let cards: [DiagnosticCard]
    @Environment(StudyStore.self) private var store
    @State private var index = 0
    @State private var finished = false
    var body: some View {
        Group {
            if finished { summary }
            else if cards.indices.contains(index) {
                ScrollViewReader { proxy in
                    ScrollView {
                        VStack(alignment: .leading, spacing: 20) {
                            Text("Set \(index + 1) of \(cards.count) · \(FamiliaritySummary(cards, progress: store.progress).assessed) assessed").font(.caption).foregroundStyle(.secondary).id("diagnosticTop")
                            DiagnosticCardView(card: cards[index]).id(cards[index].id)
                            HStack {
                                Button("Previous set") { index -= 1; proxy.scrollTo("diagnosticTop", anchor: .top) }.disabled(index == 0).buttonStyle(.bordered)
                                Spacer()
                                Button(index + 1 == cards.count ? "View summary" : store.progress.familiarity?[cards[index].id] == nil ? "Skip for now" : "Next set") {
                                    if index + 1 == cards.count { finished = true } else { index += 1; proxy.scrollTo("diagnosticTop", anchor: .top) }
                                }.buttonStyle(.borderedProminent).accessibilityIdentifier("nextDiagnostic")
                            }
                        }.padding(20).frame(maxWidth: 850)
                    }.background(AtlasStyle.paper)
                }
            }
        }.navigationTitle("Solution familiarity").navigationBarTitleDisplayMode(.inline).trackPage("/diagnostic/session")
            .toolbar { if !finished { Button("Finish") { finished = true }.accessibilityIdentifier("finishDiagnostic") } }
    }
    private var summary: some View {
        List {
            Section("Your familiarity snapshot") {
                FamiliarityTotalsView(summary: FamiliaritySummary(cards, progress: store.progress))
                Text("Your latest ratings for this selection are saved. Skipped sets remain unassessed unless they had an earlier rating.").font(.caption).foregroundStyle(.secondary)
                NavigationLink("View familiarity dashboard") { FamiliarityReportView(data: data) }
                Button("Review these ratings") { index = 0; finished = false }
            }
            ForEach(Array(cards.enumerated()), id: \.element.id) { i, card in
                Button { index = i; finished = false } label: {
                    VStack(alignment: .leading, spacing: 5) {
                        Text("\(card.problem.id). \(card.problem.title)").font(.subheadline)
                        Text(card.node.title).font(.caption).foregroundStyle(.secondary)
                        Text(store.progress.familiarity?[card.id]?.rating.label ?? "Unassessed").font(.caption.weight(.semibold))
                    }
                }
            }
        }.accessibilityIdentifier("diagnosticSummary")
    }
}
struct DiagnosticCardView: View {
    let card: DiagnosticCard
    @Environment(StudyStore.self) private var store
    @State private var revealed = false
    var body: some View {
        VStack(alignment: .leading, spacing: 18) {
            HStack { LevelBadge(text: card.problem.difficulty); LevelBadge(text: card.node.level) }
            Text("\(card.problem.id). \(card.problem.title)").font(.title2.weight(.bold))
            Text(card.node.title).font(.subheadline).foregroundStyle(AtlasStyle.green)
            Text(card.problem.description).font(.subheadline).lineSpacing(4)
            Link("Read full problem on LeetCode ↗", destination: URL(string: card.problem.sourceUrl)!).font(.caption)
            Button { revealed.toggle() } label: { Label(revealed ? "Hide solution set" : "Open solution set", systemImage: "eye").frame(maxWidth: .infinity) }.buttonStyle(.borderedProminent).accessibilityIdentifier("openDiagnosticSolutions")
            Text("\(card.solutions.count) implementations for this approach").font(.caption).foregroundStyle(.secondary)
            if revealed { ForEach(Array(card.solutions.enumerated()), id: \.offset) { _, solution in DiagnosticSolutionView(solution: solution) } }
            Text("How well do you understand this solution set?").font(.headline)
            ForEach(FamiliarityRating.allCases, id: \.self) { rating in
                Button { store.assess(card.id, rating) } label: {
                    VStack(alignment: .leading, spacing: 7) {
                        HStack { Text(rating.label).font(.subheadline.weight(.semibold)); Spacer(); if store.progress.familiarity?[card.id]?.rating == rating { Image(systemName: "checkmark.circle.fill") } }
                        Text(rating.detail).font(.caption).foregroundStyle(.secondary)
                    }.padding(16).frame(maxWidth: .infinity, alignment: .leading).background(store.progress.familiarity?[card.id]?.rating == rating ? AtlasStyle.green.opacity(0.13) : Color(uiColor: .secondarySystemGroupedBackground), in: RoundedRectangle(cornerRadius: 6))
                }.buttonStyle(.plain).disabled(!revealed).opacity(revealed ? 1 : 0.5).accessibilityIdentifier("familiarity_" + rating.rawValue)
            }
            Text(store.progress.familiarity?[card.id].map { "Saved: \($0.rating.label). Open the solutions to change your rating." } ?? (revealed ? "Choose a rating to save your familiarity." : "Open the solution set to enable ratings.")).font(.caption).foregroundStyle(.secondary).accessibilityIdentifier("familiarityStatus")
        }
    }
}
struct DiagnosticSolutionView: View {
    let solution: CanonicalSolution
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Divider(); Text(solution.title).font(.headline)
            Text(solution.approach).font(.subheadline).lineSpacing(4)
            if let credit = solution.attribution {
                Link("By \(credit.author) ↗", destination: URL(string: credit.url)!).font(.caption)
                Link("MIT license", destination: URL(string: "https://github.com/walkccc/LeetCode/blob/\(credit.commit)/LICENSE")!).font(.caption)
            }
            ScrollView(.horizontal) { Text(solution.code).font(.system(size: 12, design: .monospaced)).lineSpacing(5).textSelection(.enabled).padding(16) }
                .foregroundStyle(Color(red: 0.84, green: 0.89, blue: 0.98)).background(AtlasStyle.forest, in: RoundedRectangle(cornerRadius: 6)).accessibilityIdentifier("diagnosticSolutionCode")
            Text("Time: \(solution.time) · Space: \(solution.space)").font(.caption).foregroundStyle(.secondary)
        }
    }
}
