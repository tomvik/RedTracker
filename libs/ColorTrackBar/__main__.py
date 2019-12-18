import ColorTrackBar
import cv2

choice = {"bgr": ColorTrackBar.HSVTrackBar}

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    _, img = cap.read()
    
    window = choice["bgr"](img)

    window.showAndGetValues()
    cv2.destroyAllWindows()