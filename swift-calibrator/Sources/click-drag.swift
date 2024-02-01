import Cocoa


// MARK: - Custom Drag Area View
class DragAreaView: NSView {
    weak var delegate: DragAreaDelegate?
    private var startPoint: NSPoint?
    private var dragRect: NSRect?
    
    private var actualRect: NSRect?
    

    // Array to store rectangles
    var rectangles: [NSRect] = []
    
    // Add rectangles from file
    public func addRectangleArray(_ boundBoxArray: [NSRect]){
        for rectangle in boundBoxArray{
            addRectangleAndConvert(rectangle: rectangle)
            //addRectangle(rectangle)
        }
    }
    
    func addRectangleAndConvert(rectangle: NSRect){
        
        var screenHeight = CGFloat(0)
        if let screen = window?.screen {
            screenHeight = screen.frame.size.height

        }
        
        // Step 1: Get the NSWindow from the DragAreaView
        if let window = self.window {
            
            // Convert the y coordinate
            let convertedY = screenHeight - rectangle.origin.y

            // Adjust for the rectangle's height to get the top-left origin in the top-down system
            let adjustedY = convertedY - rectangle.height
            
            // Convert the screenRect to the window's coordinate system
            let yConvertedRect = NSRect(x: rectangle.origin.x, y: adjustedY, width: rectangle.width, height: rectangle.height)

            let windowRect = window.convertFromScreen(yConvertedRect)
            rectangles.append(windowRect)
            self.setNeedsDisplay(windowRect)
            
        } else{
            print("Rectangle was not printed")
        }
    }
    
    // Function to add a new rectangle
    func addRectangle(_ rectangle: NSRect) {
        rectangles.append(rectangle)
        self.setNeedsDisplay(rectangle)  // Request redraw of the view
    }

    override func mouseDown(with event: NSEvent) {
        startPoint = convert(event.locationInWindow, from: nil)
    }

    override func mouseDragged(with event: NSEvent) {
        guard let start = startPoint else { return }
        let actual_start = window?.convertPoint(toScreen: start) ?? NSPoint.zero
        
        let windowPoint = convert(event.locationInWindow, from: nil)
        
        // Convert the coordinates to the absolute screen coordinates
        let currentPoint = window?.convertPoint(toScreen: windowPoint) ?? NSPoint.zero
        
        var screenHeight = CGFloat(0)
        // To make the coordinates match up with ocr screenreader
        if let screen = window?.screen {
            screenHeight = screen.frame.size.height

        }
        
        //Rectangle relative to the view window
        dragRect = NSRect(x: min(start.x, windowPoint.x),
                          y: min(start.y, windowPoint.y),
                          width: abs(windowPoint.x - start.x),
                          height: abs(windowPoint.y - start.y))
        
        //Rectangle relative to the whole screen
        self.actualRect = NSRect(x: actual_start.x,
                          y: screenHeight - actual_start.y,
                          width: abs(currentPoint.x - actual_start.x),
                          height: abs(currentPoint.y - actual_start.y))
        
//        print("Relative Rect:" + NSStringFromRect(dragRect ?? NSRect(x: 0, y: 0, width: 0, height: 0)))
//        print("Absolute Rect:" + NSStringFromRect(self.actualRect ?? NSRect(x: 0, y: 0, width: 0, height: 0)))
        needsDisplay = true
    }

    override func mouseUp(with event: NSEvent) {
        if let dragRect = dragRect {
            delegate?.dragAreaDidFinishDragging(withRect: self.actualRect ?? dragRect)
        }
        addRectangle(dragRect ?? NSRect(x: 0, y: 0, width: 0, height: 0))
        dragRect = nil
        needsDisplay = true
    }

    override func draw(_ dirtyRect: NSRect) {
        super.draw(dirtyRect)
        
        if let rect = dragRect {
            NSColor.selectedControlColor.setStroke()
            let path = NSBezierPath(rect: rect)
            NSColor.red.setStroke()
            path.stroke()

        }
        
        for saved_rect in rectangles{
            NSColor.selectedControlColor.setStroke()
            let path = NSBezierPath(rect: saved_rect)
            NSColor.red.setStroke()
            path.stroke()
            
        }
    }


}
