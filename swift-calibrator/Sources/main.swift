import Cocoa
import Foundation



// MARK: - Drag Area Delegate Protocol
protocol DragAreaDelegate: AnyObject {
    func dragAreaDidFinishDragging(withRect rect: NSRect)
}


// MARK - Recntangle Drawing
class RectangleView: NSView {
    override func draw(_ dirtyRect: NSRect) {
        super.draw(dirtyRect)

        // Define the rectangle
        let rectangle = NSRect(x: 20, y: 20, width: 100, height: 100)

        // Create the bezier path for the rectangle
        let path = NSBezierPath(rect: rectangle)

        // Set the fill color (optional)
        NSColor.red.setFill()
        path.fill()

        // Set the stroke color (optional)
        NSColor.black.setStroke()
        path.lineWidth = 2
        path.stroke()
    }
}

// MARK: - Main Script Implementation
class MainScript: NSObject, DragAreaDelegate, NSWindowDelegate {
    var cliFlags: [String] = []
    
    var savedRectCoords: [Any] = []
    

    init(flags: [String]) {
        self.cliFlags = flags
        
    }
    
    struct BoundingBox : Codable {
        let width: Double
        let height: Double
        let x: Double
        let y: Double
    }
    
    func dragAreaDidFinishDragging(withRect rect: NSRect) {
        //print("Dragged Area: \(rect)")
        
        
        // Calculate topLeft and bottomRight
        let jsonDict = ["x": rect.origin.x, "width": rect.size.width, "y": rect.origin.y , "height": rect.size.height]
        savedRectCoords.append(jsonDict)
        
        do {
            // Step 3: Convert your dictionary to JSON Data
            let jsonData = try JSONSerialization.data(withJSONObject: savedRectCoords, options: [])

            // Step 4: Create a file URL
            let fileURL = URL(fileURLWithPath: FileManager.default.currentDirectoryPath).appendingPathComponent("Coordinates.json")
            
            // Step 5: Write the data to the file
            try jsonData.write(to: fileURL, options: [])
            print("Coordinate was written to the file successfully!")
        } catch {
            print("Error: \(error)")
        }

        // Convert the dictionary to JSON data
        if let jsonData = try? JSONSerialization.data(withJSONObject: jsonDict, options: .prettyPrinted),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            print(jsonString)
        }

        if(self.cliFlags.count > 1 && self.cliFlags[1] == "--onerun"){
            exit(0)
        }
        
    }
    
    func readAndDecodeJSONFromFileAtPath<T: Codable>(filePath: String, modelType: T.Type) -> T? {
        let fileURL = URL(fileURLWithPath: filePath)

        do {
            let data = try Data(contentsOf: fileURL)
            let decoder = JSONDecoder()
            let decodedData = try decoder.decode(T.self, from: data)
            return decodedData
        } catch {
            print("Error reading or decoding JSON: \(error.localizedDescription)")
            return nil
        }
    }
    
    func extractBoxes(filename: String) -> [NSRect]{
    
        if let fileURL = Bundle.main.url(forResource: filename, withExtension: "json") {
            do {
                let data = try Data(contentsOf: fileURL)
                    print("In here")
                if let jsonObject = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                    // Now `jsonObject` is a dictionary with your JSON data
                    print(jsonObject)
                }
            } catch {
                print("Error reading or serializing JSON: \(error.localizedDescription)")
            }
        }
        
        return [NSRect]()
    }
    
    // finds the path after the --pos-path var
    func boxFilePath() -> String{
        if(self.cliFlags.count > 1 && self.cliFlags[1] == "--pos-path"){
            return self.cliFlags[2]
        }else{
            return ""
        }
    }
    

    func run() {
        let screenFrame = NSScreen.main?.visibleFrame ?? NSRect.zero
        print(screenFrame)
        let app = NSApplication.shared
        let viewController = NSViewController()
        let dragAreaView = DragAreaView()
        

        dragAreaView.frame = screenFrame
        dragAreaView.delegate = self
        viewController.view = dragAreaView

        let window = NSWindow(contentRect: screenFrame,
                              styleMask: [.titled, .closable, .miniaturizable, .resizable],
                              backing: .buffered, defer: false)
        
        window.delegate = self
        window.titleVisibility = .hidden
        window.titlebarAppearsTransparent = true
        window.title = "Custom Drag Area"
        window.contentViewController = viewController
        window.makeKeyAndOrderFront(nil)
        window.isOpaque = false // Make window non-opaque
        window.backgroundColor = NSColor.clear // Set background color to clear

        
        app.setActivationPolicy(.regular)
        app.activate(ignoringOtherApps: true)
        
        let boxPath: String = boxFilePath()
        var boxArrayAsNSRect: [NSRect] = [NSRect]()
        
        // Subroutine to load boxes in from coordinates
        if boxPath != "" {

            print(boxPath)
            if let boxArray: [BoundingBox] = readAndDecodeJSONFromFileAtPath(filePath: boxPath, modelType: [BoundingBox].self) {
                
                for box in boxArray{
                    boxArrayAsNSRect.append(NSMakeRect(box.x, box.y, box.width, box.height))
                }
                
                print(boxArrayAsNSRect)
                dragAreaView.addRectangleArray(boxArrayAsNSRect)
                
            } else {
                // Failed to decode JSON
                print("Failed to read or decode JSON from the specified path")
            }
        }

        
        app.run()
        
    }
}

// Run the script
let arguments = CommandLine.arguments
let mainScript = MainScript(flags: arguments)
mainScript.run()



