// On-screen text reader for ad videos (macOS Vision).
// Build: swiftc -O scripts/ad-copy-check/ocr.swift -o ~/.local/bin/hg-vision-ocr
// Usage: hg-vision-ocr <dir of .jpg frames>  ->  prints "frame.jpg<TAB>text" per line.
// Language correction is OFF on purpose, so typos in captions are not auto-fixed.
import Vision
import AppKit

let dir = CommandLine.arguments[1]
let files = try! FileManager.default.contentsOfDirectory(atPath: dir).filter { $0.hasSuffix(".jpg") }.sorted()
for f in files {
    guard let img = NSImage(contentsOfFile: dir + "/" + f),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    for o in (req.results ?? []) {
        if let t = o.topCandidates(1).first, t.confidence > 0.3 { print("\(f)\t\(t.string)") }
    }
}
