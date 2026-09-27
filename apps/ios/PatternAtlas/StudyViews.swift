import SwiftUI

struct ProblemDetailView: View {
    let data: Curriculum
    let problem: StudyProblem
    var initialPattern: String? = nil
    var reviewMode = false
    var onRate: ((RecallRating) -> Void)? = nil
    @Environment(StudyStore.self) private var store
    @State private var revealed = false
    @State private var showHint = false
    @State private var selected = 0
    @State private var tab = 0
    @State private var rated: RecallRating?
    @FocusState private var editing: Bool
    private var solution: CanonicalSolution { problem.solutions[selected] }
    private var pattern: PatternNode? { data.node(solution.patternId) }
    var body: some View {
        ScrollViewReader { proxy in
            ScrollView {
                VStack(alignment: .leading, spacing: 22) {
                    VStack(alignment: .leading, spacing: 12) {
                        HStack { Eyebrow(text: "Problem \(problem.id)"); LevelBadge(text: problem.difficulty); if problem.premium { LevelBadge(text: "Premium") } }
                        Text(problem.title).font(.system(.title, design: .rounded, weight: .bold))
                        if !reviewMode || revealed, let pattern {
                            NavigationLink { NodeDetailView(data: data, node: pattern) } label: { Label(pattern.title, systemImage: "point.3.connected.trianglepath.dotted").font(.caption) }
                        }
                    }
                    VStack(alignment: .leading, spacing: 17) {
                        Eyebrow(text: "The challenge · original study summary")
                        Text(problem.description).font(.subheadline).lineSpacing(5)
                        ForEach(Array(problem.examples.enumerated()), id: \.offset) { _, example in
                            VStack(alignment: .leading, spacing: 10) {
                                Eyebrow(text: "Arguments")
                                Text(example.input).font(.system(.caption, design: .monospaced)).textSelection(.enabled)
                                Eyebrow(text: "Result")
                                Text(example.output).font(.system(.caption, design: .monospaced)).textSelection(.enabled)
                            }.frame(maxWidth: .infinity, alignment: .leading).padding(16).background(AtlasStyle.green.opacity(0.055), in: RoundedRectangle(cornerRadius: 9))
                        }
                        DisclosureGroup("Input notes") {
                            Text(problem.constraints + " Study functions use solve(...). Trees and linked lists use LeetCode-style node objects.").font(.caption).foregroundStyle(.secondary).padding(.top, 10)
                        }.font(.caption.weight(.medium))
                        Divider()
                        Label("Name the state. State the invariant. Estimate the complexity.", systemImage: "sparkles").font(.caption).foregroundStyle(AtlasStyle.green)
                        Button { showHint.toggle() } label: { Label(showHint ? "Hide hint" : "Need a small hint?", systemImage: "lightbulb").font(.caption) }
                        if showHint, let pattern { Text(pattern.description + "\n\n" + pattern.tips.joined(separator: " ")).font(.caption).foregroundStyle(.secondary).lineSpacing(4) }
                    }.padding(20).background(.background, in: RoundedRectangle(cornerRadius: 14))
                    VStack(alignment: .leading, spacing: 16) {
                        Picker("Workspace", selection: $tab) { Text("Your draft").tag(0); if revealed { Text("Solution").tag(1) } }.pickerStyle(.segmented)
                        if tab == 0 {
                            HStack { Label("Saved on this device", systemImage: "checkmark.circle"); Spacer(); Text("Python 3") }.font(.caption2).foregroundStyle(.secondary)
                            TextEditor(text: Binding(get: { store.draft(for: problem) }, set: { store.setDraft($0, for: problem.id) }))
                                .font(.system(.callout, design: .monospaced)).autocorrectionDisabled().textInputAutocapitalization(.never)
                                .scrollContentBackground(.hidden).padding(12).frame(minHeight: 270)
                                .background(Color(uiColor: .secondarySystemBackground), in: RoundedRectangle(cornerRadius: 10))
                                .focused($editing).accessibilityLabel("Solution draft").accessibilityIdentifier("solutionDraft")
                            HStack {
                                Text("Execution lives on LeetCode.").font(.caption2).foregroundStyle(.secondary)
                                Spacer()
                                Button("Copy draft") { UIPasteboard.general.string = store.draft(for: problem); store.message = "Draft copied." }.font(.caption)
                            }
                        } else {
                            if problem.solutions.count > 1 && !reviewMode {
                                Picker("Approach", selection: $selected) { ForEach(problem.solutions.indices, id: \.self) { Text(problem.solutions[$0].title).tag($0) } }.font(.caption)
                                    .onChange(of: selected) { _, _ in rated = nil }
                            }
                            Text(solution.approach).font(.subheadline).lineSpacing(5)
                            ScrollView(.horizontal) {
                                Text(solution.code).font(.system(size: 12, design: .monospaced)).lineSpacing(5).textSelection(.enabled).padding(17)
                            }.foregroundStyle(Color(red: 0.83, green: 0.9, blue: 0.76)).background(AtlasStyle.forest, in: RoundedRectangle(cornerRadius: 10))
                                .accessibilityIdentifier("canonicalSolution")
                            VStack(alignment: .leading, spacing: 9) {
                                Label("Time: " + solution.time, systemImage: "clock")
                                Label("Space: " + solution.space, systemImage: "square.stack.3d.up")
                            }.font(.caption).foregroundStyle(.secondary)
                            if let pattern { Text("Watch for this: " + pattern.tips.joined(separator: " ")).font(.caption).lineSpacing(4).foregroundStyle(.secondary) }
                        }
                    }.padding(18).background(.background, in: RoundedRectangle(cornerRadius: 14)).id("workspace")
                    if !revealed {
                        Button {
                            editing = false; revealed = true; tab = 1
                            withAnimation { proxy.scrollTo("workspace", anchor: .top) }
                        } label: { Label("Reveal solution", systemImage: "eye").font(.subheadline.weight(.semibold)).frame(maxWidth: .infinity).padding(8) }
                            .buttonStyle(.borderedProminent).accessibilityIdentifier("revealSolution")
                    } else {
                        VStack(alignment: .leading, spacing: 14) {
                            Text(rated == nil ? "How well did you recall the approach?" : "Review saved").font(.subheadline.weight(.semibold))
                            Text("Your next review follows your recall rating.").font(.caption).foregroundStyle(.secondary)
                            HStack(spacing: 7) {
                                ForEach(RecallRating.allCases, id: \.self) { rating in
                                    Button {
                                        guard rated == nil else { return }
                                        rated = rating
                                        if let onRate { onRate(rating) }
                                        else { store.rate(cardKey(problem.id, solution.patternId), rating) }
                                    } label: {
                                        VStack(spacing: 6) { Text(rating.label).font(.caption.weight(.semibold)); Text(rating.intervalLabel).font(.system(size: 9)) }.frame(maxWidth: .infinity).padding(.vertical, 13)
                                            .background(rated == rating ? AtlasStyle.lime : Color(uiColor: .systemBackground), in: RoundedRectangle(cornerRadius: 8))
                                    }.disabled(rated != nil).accessibilityIdentifier("rate_" + rating.rawValue)
                                }
                            }
                        }.padding(18).background(AtlasStyle.green.opacity(0.07), in: RoundedRectangle(cornerRadius: 13))
                    }
                    if let url = URL(string: problem.sourceUrl) {
                        Link(destination: url) { Label("Read full statement & run on LeetCode", systemImage: "arrow.up.right.square").font(.caption).frame(maxWidth: .infinity) }.padding(.vertical, 7)
                    }
                }.padding(20).frame(maxWidth: 850)
            }.background(AtlasStyle.paper)
        }
        .navigationTitle(reviewMode ? "Recall practice" : "Problem study").navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                Button { store.toggleBookmark(problem.id) } label: { Image(systemName: store.progress.bookmarks.contains(problem.id) ? "bookmark.fill" : "bookmark") }
                    .accessibilityLabel(store.progress.bookmarks.contains(problem.id) ? "Unsave problem" : "Save problem")
            }
            ToolbarItemGroup(placement: .keyboard) { Spacer(); Button("Done") { editing = false } }
        }
        .onAppear { selected = problem.solutions.firstIndex { $0.patternId == initialPattern } ?? 0 }
    }
}
struct ReviewSessionView: View {
    let data: Curriculum
    var nodeId: String? = nil
    @Environment(StudyStore.self) private var store
    @Environment(\.dismiss) private var dismiss
    @State private var cards: [ReviewCard] = []
    @State private var index = 0
    @State private var started = false
    var body: some View {
        Group {
            if index < cards.count {
                VStack(spacing: 0) {
                    HStack { Label("\(index + 1) / \(cards.count)", systemImage: "square.stack.3d.up").font(.caption); ProgressView(value: Double(index), total: Double(cards.count)).tint(AtlasStyle.green) }.padding(.horizontal, 22).padding(.vertical, 14)
                    ProblemDetailView(data: data, problem: cards[index].problem, initialPattern: cards[index].patternId, reviewMode: true) { rating in
                        store.rate(cards[index].id, rating); index += 1
                    }.id(cards[index].id)
                }
            } else if started {
                VStack(spacing: 21) {
                    Image(systemName: "checkmark.seal").font(.system(size: 55)).foregroundStyle(AtlasStyle.green)
                    Text(cards.isEmpty ? "All caught up" : "A little better, one pattern at a time.").font(.title2.bold()).multilineTextAlignment(.center)
                    Text(cards.isEmpty ? "No new or due cards in this topic. Explore another branch of the library." : "You reviewed \(cards.count) cards. The next reviews are scheduled from your recall ratings.").font(.subheadline).foregroundStyle(.secondary).multilineTextAlignment(.center)
                    Button("Back to the library") { dismiss() }.buttonStyle(.borderedProminent)
                }.padding(30).frame(maxWidth: 650, maxHeight: .infinity)
            } else { ProgressView("Preparing your deck…") }
        }.toolbar { ToolbarItem(placement: .topBarLeading) { Button("Close") { dismiss() } } }
            .onAppear { if !started { cards = store.queue(nodeId: nodeId); started = true } }
    }
}
