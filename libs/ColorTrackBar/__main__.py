import ColorTrackBar
import cv2

choice = {"bgr": ColorTrackBar.HSVFilter}

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    _, img = cap.read()
    
    window = choice["bgr"](img)

    window.show()
    cv2.destroyAllWindows()