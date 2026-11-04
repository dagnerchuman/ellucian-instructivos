// Uso (solo macOS): swiftc -O herramientas/diagramas/ocr_capturas.swift -o /tmp/ocr && /tmp/ocr captura1.png captura2.png > ocr.json
// Sirve para ubicar los cuadros de las capturas de TEST (anotar_capturas.py, C195): da la posición de cada texto.
// OCR de capturas con Vision: imprime JSON {archivo: [{t, x, y, w, h}]} en píxeles, origen arriba a la izquierda.
import Foundation
import Vision
import AppKit

var salida: [String: [[String: Any]]] = [:]
for ruta in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: ruta),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
    let W = Double(cg.width), H = Double(cg.height)
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.recognitionLanguages = ["es-ES", "en-US"]
    req.usesLanguageCorrection = false
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    var lista: [[String: Any]] = []
    for obs in req.results ?? [] {
        guard let cand = obs.topCandidates(1).first else { continue }
        let b = obs.boundingBox
        lista.append(["t": cand.string,
                      "x": Int((b.minX * W).rounded()), "y": Int(((1 - b.maxY) * H).rounded()),
                      "w": Int((b.width * W).rounded()), "h": Int((b.height * H).rounded())])
    }
    salida[(ruta as NSString).lastPathComponent] = lista
}
let datos = try! JSONSerialization.data(withJSONObject: salida, options: [.prettyPrinted, .sortedKeys])
print(String(data: datos, encoding: .utf8)!)
