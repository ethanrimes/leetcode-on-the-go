import AppKit
import Foundation

let size = 1024
let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: size, pixelsHigh: size, bitsPerSample: 8, samplesPerPixel: 3, hasAlpha: false, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
NSColor(calibratedRed: 0.09, green: 0.19, blue: 0.15, alpha: 1).setFill()
NSBezierPath(rect: NSRect(x: 0, y: 0, width: size, height: size)).fill()
NSColor(calibratedRed: 0.83, green: 0.93, blue: 0.67, alpha: 1).setStroke()
for offset in [0.0, -115.0, -230.0] {
    let path = NSBezierPath()
    path.lineWidth = 35; path.lineJoinStyle = .round; path.lineCapStyle = .round
    path.move(to: NSPoint(x: 250, y: 610 + offset))
    path.line(to: NSPoint(x: 512, y: 740 + offset))
    path.line(to: NSPoint(x: 774, y: 610 + offset))
    path.line(to: NSPoint(x: 512, y: 480 + offset))
    path.close(); path.stroke()
}
NSGraphicsContext.restoreGraphicsState()
let destination = CommandLine.arguments[1]
try bitmap.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: destination))
