import SwiftUI

struct PageEntryModifier: ViewModifier {
    let page: String
    @Environment(StudyStore.self) private var store
    @State private var visible = false
    func body(content: Content) -> some View {
        content.onAppear { if !visible { visible = true; store.visit(page) } }.onDisappear { visible = false }
    }
}
extension View { func trackPage(_ page: String) -> some View { modifier(PageEntryModifier(page: page)) } }

struct AnalyticsDashboardSections: View {
    let data: Curriculum
    @Environment(StudyStore.self) private var store
    @State private var engine: CurriculumAnalytics?
    @State private var filter = AnalyticsFilter()
    @State private var chart = "Treemap"
    @State private var freshness = false
    @State private var selected: String?
    @State private var importing = false
    var body: some View {
        Group {
            connection
            if let engine {
                let snapshot = engine.snapshot(store.progress, filter: filter)
                Section {
                    HStack {
                        StatView(value: "\(snapshot.solved)", label: "Accepted")
                        StatView(value: "\(snapshot.attempted)", label: "Attempted")
                        StatView(value: "\(snapshot.total)", label: "In scope")
                    }.padding(.vertical, 12)
                }
                focusSection(snapshot)
                filterSection
                chartSection(snapshot)
                Section("History & activity") {
                    NavigationLink { SubmissionHistoryView(data: data, submissions: snapshot.submissions) } label: { Label("Submission history · \(snapshot.submissions.count)", systemImage: "clock.arrow.circlepath") }
                    NavigationLink { PageEntriesView(data: data) } label: { Label("Page entries · \(snapshot.pages.values.reduce(0) { $0 + $1.count })", systemImage: "rectangle.on.rectangle") }
                    if snapshot.unmapped > 0 { Text("\(snapshot.unmapped) submission records are outside this catalog. They remain visible in unfiltered history.").font(.caption).foregroundStyle(.secondary) }
                }
            }
        }
        .onAppear { if engine == nil { engine = CurriculumAnalytics(data) } }
        .fileImporter(isPresented: $importing, allowedContentTypes: [.json]) { result in
            do {
                let url = try result.get(); let access = url.startAccessingSecurityScopedResource()
                defer { if access { url.stopAccessingSecurityScopedResource() } }
                try store.importHistory(Data(contentsOf: url))
            } catch { store.message = error.localizedDescription }
        }
    }
    private var connection: some View {
        Section {
            if let history = store.progress.leetcode {
                Label(history.account, systemImage: "person.crop.circle").font(.headline)
                Text("\(history.submissions.count) submissions · exported \(dateFromISO(history.exportedAt)?.formatted(date: .abbreviated, time: .shortened) ?? history.exportedAt)").font(.caption).foregroundStyle(.secondary)
                if let snapshot = history.completions {
                    Text("LeetCode reports \(snapshot.slugs.count) completed problems as of \(dateFromISO(snapshot.observedAt)?.formatted(date: .abbreviated, time: .omitted) ?? snapshot.observedAt). The snapshot contributes to all-time coverage only; unknown submission dates stay unknown.").font(.caption).foregroundStyle(.secondary)
                }
                if let through = history.through { Text("Latest export includes submissions through \(through).").font(.caption2).foregroundStyle(.secondary) }
                Text(history.complete ? "Latest export reached the oldest available record." : "Latest export is partial. Previously imported records are kept.").font(.caption2).foregroundStyle(.secondary)
            } else { Text("Bring your LeetCode history into your study workspace.").font(.subheadline) }
            Button { importing = true } label: { Label("Import LeetCode history", systemImage: "square.and.arrow.down") }.accessibilityIdentifier("importLeetCode")
            NavigationLink("How to export or update") { LeetCodeExportHelpView() }
        } header: { Text("LeetCode history") } footer: { Text("Import the same JSON on web and iOS. Submission IDs are merged once; no automatic background sync.") }
    }
    private func focusSection(_ snapshot: AnalyticsSnapshot) -> some View {
        Section {
            Picker("Refresh after", selection: $filter.freshDays) { ForEach([7,14,30,60,90], id: \.self) { Text("\($0) days").tag($0) } }
            ForEach(snapshot.recommendations) { item in
                VStack(alignment: .leading, spacing: 9) {
                    HStack { Text(item.kind).font(.caption.weight(.semibold)).foregroundStyle(AtlasStyle.green); Spacer(); Text(item.node.level).font(.caption2).foregroundStyle(.secondary) }
                    Text(item.topic).font(.caption2).foregroundStyle(.secondary)
                    NavigationLink { NodeDetailView(data: data, node: item.node) } label: { Text(item.node.title).font(.subheadline.weight(.semibold)) }
                    Text(item.reason).font(.caption).foregroundStyle(.secondary)
                    NavigationLink { ProblemDetailView(data: data, problem: item.problem, initialPattern: item.node.id) } label: {
                        Text("Practice #\(item.problem.id) · \(item.problem.title)").font(.caption.weight(.medium)).foregroundStyle(AtlasStyle.green)
                    }
                }.padding(.vertical, 8)
            }
            if snapshot.recommendations.isEmpty { Text("No practice is due for these filters. Broaden the category or difficulty to explore more patterns.").font(.caption) }
        } header: { Text("Recommended practice") } footer: { Text("A varied set based on all available history: due reviews, unsuccessful attempts, uncertain solutions, older practice, then gaps. Category, difficulty, and pattern level filters apply. Missing dates stay unknown; completion does not prove mastery.") }
    }

    private var filterSection: some View {
        Section("Explore coverage") {
            Picker("Category", selection: $filter.scope) {
                Text("Entire curriculum").tag("")
                ForEach(data.nodes.filter { $0.kind == "category" }) { Text($0.title).tag($0.id) }
            }
            Picker("Map detail", selection: $filter.depth) { Text("Overview").tag(1); Text("Grouped detail").tag(2); Text("Fine detail").tag(3); Text("All patterns & collections").tag(99) }
            Picker("Problem difficulty", selection: $filter.difficulty) { Text("All difficulties").tag(""); ForEach(["Easy","Medium","Hard"], id: \.self) { Text($0).tag($0) } }
            Picker("Pattern level", selection: $filter.level) { Text("All levels").tag(""); ForEach(["Foundation","Intermediate","Advanced"], id: \.self) { Text($0).tag($0) } }
            Picker("Submission period", selection: $filter.period) { Text("All imported history").tag(0); Text("Last 30 days").tag(30); Text("Last 90 days").tag(90) }
            TextField("Find a category or pattern tile", text: $filter.query)
            Toggle("Show practice freshness", isOn: $freshness)
        }
    }
    private func chartSection(_ snapshot: AnalyticsSnapshot) -> some View {
        Section {
            Picker("Chart view", selection: $chart) { Text("Treemap").tag("Treemap"); Text("Stacked bars").tag("Stacked bars") }.pickerStyle(.segmented)
            HStack(spacing: 12) {
                legend(freshness ? "Fresh" : "Accepted", AtlasStyle.green)
                legend(freshness ? "Needs refresh" : "Attempted", .orange)
                legend(freshness ? "No dated practice" : "No attempt", .gray.opacity(0.4))
            }
            if !filter.scope.isEmpty { Button("Back to all topics") { filter.scope = ""; selected = nil } }
            if snapshot.tiles.isEmpty { Text("No categories match these filters.").font(.caption) }
            else if chart == "Treemap" { CoverageTreemap(tiles: snapshot.tiles, freshness: freshness, selected: $selected).frame(height: 400) }
            else {
                ScrollView { LazyVStack(spacing: 14) { ForEach(snapshot.tiles) { item in
                    Button { selected = item.id } label: { CoverageBar(item: item, freshness: freshness) }.buttonStyle(.plain).accessibilityLabel(item.accessibilitySummary)
                } }.padding(.vertical, 10) }.frame(height: 400)
            }
            if let item = snapshot.tiles.first(where: { $0.id == selected }) {
                VStack(alignment: .leading, spacing: 8) {
                    Text(item.node.title).font(.headline)
                    Text("\(item.solved) accepted · \(item.attempted) attempted · \(item.unseen) no recorded attempt").font(.caption)
                    Text("\(item.fresh) fresh · \(item.practiced - item.fresh) need refresh · \(item.visits) category entries").font(.caption).foregroundStyle(.secondary)
                    if !data.children(of: item.id).isEmpty { Button("Drill into category") { filter.scope = item.id; selected = nil } }
                    NavigationLink("Open study page") { NodeDetailView(data: data, node: item.node) }
                }.padding(.vertical, 8)
            }
            NavigationLink("View all \(snapshot.tiles.count) tiles as a list") {
                List(snapshot.tiles) { item in NavigationLink { NodeDetailView(data: data, node: item.node) } label: { CoverageBar(item: item, freshness: freshness) } }
                    .navigationTitle("Coverage details").trackPage("/progress/tiles")
            }
        } footer: { Text("Area represents problem memberships. Blue fill shows the selected metric. Problems can appear in multiple tiles; totals count each problem once. Acceptance does not prove a particular technique was used. Freshness uses all recorded practice, independent of the submission-period filter. Category entries include child category pages.") }
    }
    private func legend(_ text: String, _ color: Color) -> some View { HStack(spacing: 4) { Circle().fill(color).frame(width: 6, height: 6); Text(text).font(.system(size: 9)).foregroundStyle(.secondary) } }
}
struct CoverageTreemap: View {
    let tiles: [CoverageStats]
    let freshness: Bool
    @Binding var selected: String?
    var body: some View {
        GeometryReader { geometry in
            let rectangles = treemap(tiles.map(\.total), width: geometry.size.width, height: geometry.size.height)
            ZStack(alignment: .topLeading) {
                ForEach(rectangles) { rect in
                    let tile = tiles[rect.id]
                    let value = freshness ? tile.fresh : tile.solved
                    Button { selected = tile.id } label: {
                        ZStack(alignment: .bottomLeading) {
                            Color(uiColor: .secondarySystemGroupedBackground)
                            AtlasStyle.green.opacity(0.32).frame(height: max(0, rect.height - 2) * Double(value) / Double(tile.total))
                            VStack(alignment: .leading, spacing: 5) {
                                if rect.width > 48 && rect.height > 30 { Text(tile.node.title).font(.system(size: rect.width > 110 ? 12 : 9, weight: .semibold)).lineLimit(rect.height > 80 ? 3 : 1) }
                                Spacer(minLength: 0)
                                if rect.width > 42 && rect.height > 40 { Text("\(value)/\(tile.total)").font(.system(size: 10, weight: .medium)).lineLimit(1).minimumScaleFactor(0.6) }
                            }.padding(6).frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
                        }.frame(width: max(0, rect.width - 2), height: max(0, rect.height - 2)).clipped()
                            .overlay(Rectangle().stroke(selected == tile.id ? AtlasStyle.green : Color.secondary.opacity(0.2), lineWidth: selected == tile.id ? 2 : 0.5))
                    }.buttonStyle(.plain).position(x: rect.x + rect.width / 2, y: rect.y + rect.height / 2).accessibilityLabel(tile.accessibilitySummary)
                }
            }
        }.accessibilityIdentifier("coverageTreemap")
    }
}
struct CoverageBar: View {
    let item: CoverageStats
    let freshness: Bool
    var body: some View {
        let first = freshness ? item.fresh : item.solved
        let second = freshness ? item.practiced - item.fresh : item.attempted
        VStack(alignment: .leading, spacing: 7) {
            HStack { Text(item.node.title).font(.caption.weight(.medium)); Spacer(); Text("\(first)/\(item.total)").font(.caption2).foregroundStyle(.secondary) }
            GeometryReader { geometry in HStack(spacing: 0) {
                AtlasStyle.green.frame(width: geometry.size.width * Double(first) / Double(item.total))
                Color.orange.opacity(0.7).frame(width: geometry.size.width * Double(second) / Double(item.total))
                Color.secondary.opacity(0.18)
            } }.frame(height: 14).clipShape(RoundedRectangle(cornerRadius: 3))
            Text("\(item.visits) entries · \(item.fresh) fresh · \(item.practiced - item.fresh) need refresh").font(.caption2).foregroundStyle(.secondary)
        }
    }
}
struct LeetCodeExportHelpView: View {
    var body: some View {
        List {
            Section("Export on a desktop browser") {
                Text("1. Sign in on the LeetCode progress page.\n\n2. Open Pattern Atlas on the web, go to Your progress, and copy the exporter script. Paste it into the developer console on LeetCode.\n\n3. Choose Export all available history the first time. Use Update · last 30 days for regular refreshes, or a full export after longer gaps.\n\n4. Save the downloaded JSON in Files or AirDrop it to your iPhone. Return here and choose Import LeetCode history.").font(.subheadline).lineSpacing(4)
                Link("Open web exporter instructions", destination: URL(string: "https://blue-sea-0c03ac51e.3.azurestaticapps.net/#/progress")!)
                Link("LeetCode progress", destination: URL(string: "https://leetcode.com/progress/")!)
            }
            Section("Easy repeat updates") { Text("For headless updates from your computer, run npm run history:login once in the repository, then npm run history:export. Install the browser script in a userscript manager to keep an export button on LeetCode. Reimporting is safe: submissions are merged by ID. Exports contain metadata only; passwords, cookies, and solution code are excluded. Both apps store your history locally.").font(.caption).foregroundStyle(.secondary) }
        }.navigationTitle("Update history").trackPage("/progress/export-help")
    }
}
struct SubmissionHistoryView: View {
    let data: Curriculum
    let submissions: [LeetCodeSubmission]
    @State private var query = ""
    @State private var result = "All"
    @State private var limit = 50
    private var filtered: [LeetCodeSubmission] { submissions.filter { (query.isEmpty || "\($0.title) \($0.language)".localizedCaseInsensitiveContains(query)) && (result == "All" || (result == "Accepted" ? $0.accepted : !$0.accepted)) } }
    var body: some View {
        List {
            Section { Picker("Result", selection: $result) { Text("All results").tag("All"); Text("Accepted").tag("Accepted"); Text("Other results").tag("Other") }; Text("\(filtered.count) records · category, difficulty, and period from dashboard").font(.caption).foregroundStyle(.secondary) }
            ForEach(Array(filtered.prefix(limit))) { submission in
                VStack(alignment: .leading, spacing: 7) {
                    if let problem = data.problems.first(where: { $0.slug == submission.slug }) { NavigationLink { ProblemDetailView(data: data, problem: problem) } label: { Text(submission.title).font(.subheadline.weight(.medium)) } }
                    else { Link(submission.title, destination: URL(string: "https://leetcode.com/problems/\(submission.slug)/")!).font(.subheadline.weight(.medium)) }
                    HStack { Text(submission.status).foregroundStyle(submission.accepted ? AtlasStyle.green : .orange); Spacer(); Text(submission.language).foregroundStyle(.secondary) }.font(.caption)
                    HStack { Text(dateFromISO(submission.timestamp)?.formatted(date: .abbreviated, time: .shortened) ?? submission.timestamp).font(.caption2).foregroundStyle(.secondary); Spacer(); Link("Submission ↗", destination: URL(string: "https://leetcode.com/submissions/detail/\(submission.id)/")!).font(.caption2) }
                }.padding(.vertical, 5)
            }
            if filtered.isEmpty { Text("No submissions match. Import a history file on the dashboard.").font(.caption).foregroundStyle(.secondary) }
            if filtered.count > limit { Button("Show more submissions") { limit += 100 } }
        }.navigationTitle("Submission history").searchable(text: $query, prompt: "Problem or language").trackPage("/progress/submissions")
    }
}
struct PageEntriesView: View {
    let data: Curriculum
    @Environment(StudyStore.self) private var store
    @State private var query = ""
    private func name(_ page: String) -> String {
        let parts = page.split(separator: "/").map(String.init)
        if parts.count == 2, parts[0] == "library" { return data.node(parts[1])?.title ?? page }
        if parts.count == 2, parts[0] == "problem" { return data.problems.first { $0.id == parts[1] }?.title ?? page }
        return ["/":"Overview", "/catalog":"All problems", "/library":"Pattern library", "/progress":"Your progress", "/review":"Practice deck", "/about":"Curriculum notes"][page] ?? page
    }
    var body: some View {
        let visits = totalVisits(store.progress.visits ?? [:]).filter { query.isEmpty || name($0.key).localizedCaseInsensitiveContains(query) }.sorted { $0.value.count == $1.value.count ? $0.key < $1.key : $0.value.count > $1.value.count }
        List {
            Section { Text("Entries count when a page opens or you return to it. Editing and revealing solutions do not add entries. Tracking begins with this update; backups carry the counts between devices.").font(.caption).foregroundStyle(.secondary) }
            ForEach(visits, id: \.key) { page, visit in
                VStack(alignment: .leading, spacing: 6) {
                    HStack { Text(name(page)).font(.subheadline); Spacer(); Text("\(visit.count)").font(.headline.monospacedDigit()) }
                    Text(page).font(.caption2).foregroundStyle(.secondary)
                    if let date = dateFromISO(visit.lastVisited) { Text("Last opened \(date.formatted())").font(.caption2).foregroundStyle(.secondary) }
                }
            }
        }.navigationTitle("Page entries").searchable(text: $query, prompt: "Page or pattern name").trackPage("/progress/visits")
    }
}
