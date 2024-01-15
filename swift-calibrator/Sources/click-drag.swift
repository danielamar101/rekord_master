import Cocoa

// MARK: - Custom Drag Area View
class DragAreaView: NSView {
    weak var delegate: DragAreaDelegate?
    private var startPoint: NSPoint?
    private var dragRect: NSRect?
    
    private var actualRect: NSRect?
    

    // Array to store rectangles
    var rectangles: [NSRect] = []

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
        let windowPoint = convert(event.locationInWindow, from: nil)
        
        // Convert the coordinates to the absolute screen coordinates
        var currentPoint = window?.convertPoint(toScreen: windowPoint) ?? NSPoint.zero
        
        
        // To make the coordinates match up with ocr screenreader
//        if let screen = window?.screen {
//            let screenHeight = screen.frame.size.height
//            currentPoint.y = screenHeight - currentPoint.y
//        }
        
        

        dragRect = NSRect(x: min(start.x, windowPoint.x),
                          y: min(start.y, windowPoint.y),
                          width: abs(windowPoint.x - start.x),
                          height: abs(windowPoint.y - start.y))
        
        self.actualRect = NSRect(x: start.x,
                          y: start.y,
                          width: abs(currentPoint.x - start.x),
                          height: abs(currentPoint.y - start.y))
        
        //print("Relative Rect:" + NSStringFromRect(dragRect ?? NSRect(x: 0, y: 0, width: 0, height: 0)))
    //print("Absolute Rect:" + NSStringFromRect(self.actualRect ?? NSRect(x: 0, y: 0, width: 0, height: 0)))
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
