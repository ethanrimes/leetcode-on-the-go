import XCTest

final class StudyFlowTests: XCTestCase {
    func testRevealAndReviewNativeCard() {
        let app = XCUIApplication()
        app.launch()
        let start = app.buttons["startReview"]
        XCTAssertTrue(start.waitForExistence(timeout: 10))
        start.tap()
        let reveal = app.buttons["revealSolution"]
        for _ in 0..<6 { if reveal.isHittable { break }; app.swipeUp() }
        XCTAssertTrue(reveal.waitForExistence(timeout: 5))
        reveal.tap()
        let solution = app.descendants(matching: .any)["canonicalSolution"].firstMatch
        XCTAssertTrue(solution.waitForExistence(timeout: 5))
        let good = app.buttons["rate_good"]
        for _ in 0..<6 { if good.isHittable { break }; app.swipeUp() }
        XCTAssertTrue(good.isHittable)
        let screenshot = XCTAttachment(screenshot: app.screenshot())
        screenshot.name = "Native solution reveal and recall controls"; screenshot.lifetime = .keepAlways; add(screenshot)
        good.tap()
        XCTAssertTrue(app.staticTexts["2 / 10"].waitForExistence(timeout: 5))
    }
    func testCommunityProblemSearchAndAttribution() {
        let app = XCUIApplication()
        app.launch()
        app.tabBars.buttons["Problems"].tap()
        let search = app.searchFields.firstMatch
        XCTAssertTrue(search.waitForExistence(timeout: 10))
        search.tap(); search.typeText("13")
        let row = app.staticTexts["13. Roman to Integer"]
        XCTAssertTrue(row.waitForExistence(timeout: 5)); row.tap()
        XCTAssertTrue(app.staticTexts["COMMUNITY STUDY CARD"].waitForExistence(timeout: 5))
        let reveal = app.buttons["revealSolution"]
        for _ in 0..<8 { if reveal.isHittable { break }; app.swipeUp() }
        XCTAssertTrue(reveal.isHittable); reveal.tap()
        let solution = app.descendants(matching: .any)["canonicalSolution"].firstMatch
        XCTAssertTrue(solution.waitForExistence(timeout: 5))
        XCTAssertTrue(app.links["By Peng-Yu Chen (walkccc) ↗"].exists || app.buttons["By Peng-Yu Chen (walkccc) ↗"].exists)
        let screenshot = XCTAttachment(screenshot: app.screenshot())
        screenshot.name = "Community solution attribution"; screenshot.lifetime = .keepAlways; add(screenshot)
    }
    func testNativeProgressDashboardAndCharts() {
        let app = XCUIApplication(); app.launch()
        app.tabBars.buttons["Progress"].tap()
        XCTAssertTrue(app.buttons["importLeetCode"].waitForExistence(timeout: 10))
        let map = app.descendants(matching: .any)["coverageTreemap"].firstMatch
        for _ in 0..<12 { if map.isHittable { break }; app.swipeUp() }
        XCTAssertTrue(map.exists)
        let bars = app.buttons["Stacked bars"]
        XCTAssertTrue(bars.isHittable); bars.tap()
        let screenshot = XCTAttachment(screenshot: app.screenshot())
        screenshot.name = "Native progress stacked bars"; screenshot.lifetime = .keepAlways; add(screenshot)
        app.buttons["Treemap"].tap()
        XCTAssertTrue(map.exists)
    }
    func testDiagnosticRevealFlagAndSummary() {
        let app = XCUIApplication(); app.launch()
        app.tabBars.buttons["Progress"].tap()
        let start = app.buttons["startDiagnostic"]
        for _ in 0..<5 { if start.isHittable { break }; app.swipeUp() }
        XCTAssertTrue(start.waitForExistence(timeout: 10)); start.tap()
        let begin = app.buttons["beginDiagnostic"]
        for _ in 0..<5 { if begin.isHittable { break }; app.swipeUp() }
        XCTAssertTrue(begin.isHittable); begin.tap()
        let open = app.buttons["openDiagnosticSolutions"]
        XCTAssertTrue(open.waitForExistence(timeout: 10))
        for _ in 0..<5 { if open.isHittable { break }; app.swipeUp() }
        open.tap()
        let code = app.descendants(matching: .any)["diagnosticSolutionCode"].firstMatch
        XCTAssertTrue(code.waitForExistence(timeout: 5))
        let flag = app.buttons["familiarity_probably"]
        for _ in 0..<12 { if flag.isHittable { break }; app.swipeUp() }
        XCTAssertTrue(flag.isHittable); flag.tap()
        let status = app.staticTexts["familiarityStatus"]
        for _ in 0..<3 { if status.isHittable { break }; app.swipeUp() }
        XCTAssertTrue(status.label.contains("Saved: Probably got it"))
        let screenshot = XCTAttachment(screenshot: app.screenshot()); screenshot.name = "Diagnostic familiarity rating"; screenshot.lifetime = .keepAlways; add(screenshot)
        app.buttons["finishDiagnostic"].tap()
        XCTAssertTrue(app.staticTexts["Your familiarity snapshot"].exists || app.staticTexts["YOUR FAMILIARITY SNAPSHOT"].exists)
        XCTAssertTrue(app.buttons["View familiarity dashboard"].exists)
    }
}
