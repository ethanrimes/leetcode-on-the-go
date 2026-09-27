import SwiftUI

@main struct PatternAtlasApp: App {
    @State private var store = StudyStore()
    var body: some Scene {
        WindowGroup {
            AppRootView().environment(store).tint(AtlasStyle.green)
        }
    }
}
enum AtlasStyle {
    static let green = Color(red: 0.19, green: 0.37, blue: 0.83)
    static let forest = Color(red: 0.09, green: 0.11, blue: 0.15)
    static let lime = Color(red: 0.85, green: 0.90, blue: 1.0)
    static let paper = Color(uiColor: .systemGroupedBackground)
}
struct AppRootView: View {
    @Environment(StudyStore.self) private var store
    var body: some View {
        Group {
            if let data = store.curriculum {
                TabView {
                    NavigationStack { HomeView(data: data) }.tabItem { Label("Today", systemImage: "square.grid.2x2") }
                    NavigationStack { LibraryView(data: data) }.tabItem { Label("Library", systemImage: "point.3.connected.trianglepath.dotted") }
                    NavigationStack { ProblemLibraryView(data: data) }.tabItem { Label("Problems", systemImage: "chevron.left.forwardslash.chevron.right") }
                    NavigationStack { ProgressViewScreen(data: data) }.tabItem { Label("Progress", systemImage: "chart.bar.xaxis") }
                }
            } else {
                ContentUnavailableView("Library unavailable", systemImage: "books.vertical", description: Text(store.loadError ?? "Please reinstall the app to restore the bundled curriculum."))
            }
        }
        .alert("Pattern Atlas", isPresented: Binding(get: { store.message != nil }, set: { if !$0 { store.message = nil } })) {
            Button("OK") { store.message = nil }
        } message: { Text(store.message ?? "") }
    }
}
struct LevelBadge: View {
    let text: String
    private var color: Color {
        switch text { case "Hard", "Advanced": .purple; case "Medium", "Intermediate": .orange; default: AtlasStyle.green }
    }
    var body: some View {
        Text(text).font(.caption2.weight(.medium)).padding(.horizontal, 8).padding(.vertical, 5)
            .foregroundStyle(color).background(color.opacity(0.09), in: RoundedRectangle(cornerRadius: 5))
    }
}
struct Eyebrow: View {
    let text: String
    var body: some View { Text(text.uppercased()).font(.system(size: 9, weight: .semibold)).tracking(1.8).foregroundStyle(.secondary) }
}
struct HomeView: View {
    let data: Curriculum
    @Environment(StudyStore.self) private var store
    @State private var review = false
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 25) {
                HStack(spacing: 10) {
                    Image(systemName: "square.3.layers.3d").font(.title2).foregroundStyle(AtlasStyle.green)
                    Text("Pattern Atlas").font(.headline)
                    Spacer()
                    Image(systemName: "chevron.left.forwardslash.chevron.right").foregroundStyle(AtlasStyle.green)
                }
                VStack(alignment: .leading, spacing: 10) {
                    Eyebrow(text: "Algorithms / Systematic practice")
                    Text("Algorithm practice,\norganized.").font(.system(.largeTitle, design: .default, weight: .bold)).tracking(-1.1)
                    Text("A structured library of techniques, problems, and reference implementations.").font(.subheadline).foregroundStyle(.secondary).lineSpacing(4)
                }
                VStack(alignment: .leading, spacing: 17) {
                    Label("RECALL SESSION", systemImage: "square.stack").font(.system(size: 9, weight: .semibold)).tracking(1.4).foregroundStyle(AtlasStyle.lime)
                    HStack(alignment: .top) {
                        Text("Test your understanding.").font(.system(.title2, design: .default, weight: .semibold)).foregroundStyle(.white)
                        Spacer(minLength: 10)
                        Image(systemName: "point.3.connected.trianglepath.dotted").font(.system(size: 48, weight: .ultraLight)).foregroundStyle(AtlasStyle.lime.opacity(0.7))
                    }
                    Text("Recall the approach before revealing the solution.").font(.caption).foregroundStyle(.white.opacity(0.65))
                    Button { review = true } label: {
                        HStack { Text("Start a study session"); Spacer(); Image(systemName: "arrow.right") }
                            .font(.subheadline.weight(.semibold)).padding(14).foregroundStyle(AtlasStyle.forest).background(AtlasStyle.lime, in: RoundedRectangle(cornerRadius: 5))
                    }.accessibilityIdentifier("startReview")
                    Label("10 cards · at your own pace", systemImage: "clock").font(.caption2).foregroundStyle(.white.opacity(0.55))
                }.padding(23).background(AtlasStyle.forest, in: RoundedRectangle(cornerRadius: 6))
                HStack(spacing: 0) {
                    StatView(value: "\(data.patterns.count)", label: "Patterns")
                    Divider().frame(height: 30)
                    StatView(value: "\(data.problems.count)", label: "Study cards")
                    Divider().frame(height: 30)
                    StatView(value: "\(store.dueCount)", label: "Due for review")
                }.padding(.vertical, 19).background(.background, in: RoundedRectangle(cornerRadius: 6))
                VStack(alignment: .leading, spacing: 7) {
                    Eyebrow(text: "CURRICULUM INDEX")
                    Text("Topics and techniques").font(.title2.weight(.bold))
                }
                ForEach(data.roots) { node in
                    NavigationLink { NodeDetailView(data: data, node: node) } label: { TopicCard(data: data, node: node) }.buttonStyle(.plain)
                }
                Text("Available offline. Your drafts and recall history stay on this device.").font(.caption).foregroundStyle(.secondary).padding(.vertical)
            }.padding(22).frame(maxWidth: 800)
        }.trackPage("/").background(AtlasStyle.paper).toolbar(.hidden, for: .navigationBar)
            .sheet(isPresented: $review) { NavigationStack { ReviewSessionView(data: data) } }
    }
}
struct StatView: View {
    let value: String
    let label: String
    var body: some View { VStack(spacing: 6) { Text(value).font(.title2.weight(.semibold)); Text(label).font(.system(size: 9)).foregroundStyle(.secondary) }.frame(maxWidth: .infinity) }
}
struct TopicCard: View {
    let data: Curriculum
    let node: PatternNode
    private var patternCount: Int { let ids = data.descendants(of: node.id); return data.patterns.filter { ids.contains($0.id) }.count }
    var body: some View {
        VStack(alignment: .leading, spacing: 13) {
            HStack { Image(systemName: "point.3.connected.trianglepath.dotted").font(.title3).foregroundStyle(AtlasStyle.green).padding(10).background(AtlasStyle.green.opacity(0.07), in: RoundedRectangle(cornerRadius: 10)); Spacer(); LevelBadge(text: node.level) }
            Text(node.title).font(.headline)
            Text(node.description).font(.caption).foregroundStyle(.secondary).lineSpacing(3)
            Divider()
            HStack { Text("\(patternCount) patterns · \(data.entries(for: node.id).count.formatted()) problems").font(.caption2).foregroundStyle(.secondary); Spacer(); Image(systemName: "arrow.up.right").font(.caption).foregroundStyle(AtlasStyle.green) }
        }.padding(19).background(.background, in: RoundedRectangle(cornerRadius: 6))
            .overlay(RoundedRectangle(cornerRadius: 6).stroke(.primary.opacity(0.04)))
    }
}
