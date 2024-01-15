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
    
    init(flags: [String]) {
        self.cliFlags = flags
        
    }
    
    func dragAreaDidFinishDragging(withRect rect: NSRect) {
        //print("Dragged Area: \(rect)")
        
        
        // Calculate topLeft and bottomRight
        let topLeft = [rect.origin.x, rect.origin.y + rect.size.height]
        let bottomRight = [rect.origin.x + rect.size.width, rect.origin.y]

        // Create the dictionary
        let jsonDict: [String: [CGFloat]] = [
            "topLeft": topLeft,
            "bottomRight": bottomRight
        ]

        // Convert the dictionary to JSON data
        if let jsonData = try? JSONSerialization.data(withJSONObject: jsonDict, options: .prettyPrinted),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            print(jsonString)
        }
        
        

        if(self.cliFlags.count > 1 && self.cliFlags[1] == "--onerun"){
            exit(0)
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
        app.run()
        
    }
}

// Run the script
let arguments = CommandLine.arguments
let mainScript = MainScript(flags: arguments)
mainScript.run()



