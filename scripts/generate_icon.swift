import CoreGraphics
import ImageIO
import UniformTypeIdentifiers
import Foundation

let size = 1024
let context = CGContext(data: nil, width: size, height: size, bitsPerComponent: 8, bytesPerRow: size * 4, space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
context.setFillColor(CGColor(red: 0.09, green: 0.11, blue: 0.15, alpha: 1))
context.fill(CGRect(x: 0, y: 0, width: size, height: size))
context.setStrokeColor(CGColor(red: 0.60, green: 0.72, blue: 1.0, alpha: 1))
context.setLineWidth(35)
context.setLineJoin(.round)
context.setLineCap(.round)
for offset in [0.0, -115.0, -230.0] {
    context.move(to: CGPoint(x: 250, y: 610 + offset))
    context.addLine(to: CGPoint(x: 512, y: 740 + offset))
    context.addLine(to: CGPoint(x: 774, y: 610 + offset))
    context.addLine(to: CGPoint(x: 512, y: 480 + offset))
    context.closePath()
    context.strokePath()
}
let image = context.makeImage()!
let url = URL(fileURLWithPath: CommandLine.arguments[1])
let destination = CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(destination, image, nil)
precondition(CGImageDestinationFinalize(destination))
