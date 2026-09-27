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
}
