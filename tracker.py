import libs.ColorTrackBar.ColorTrackBar as ColorTrackBar
import numpy as np
import cv2

ORIGINAL_HEIGHT = 640
ORIGINAL_WIDTH = 480
RESIZE_FACTOR = 1

HEIGHT = int(ORIGINAL_HEIGHT*RESIZE_FACTOR)
WIDTH = int(ORIGINAL_WIDTH*RESIZE_FACTOR)

# Initializes the video capturing from the webcam (0)
# From a file, just write string in there.
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera didn't open. Something went wrong")
    exit

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)

# Define the codec and create VideoWriter object.
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

# False the last one if it's going to be on gray scale.
# The size of the window must be correct otherwise, trouble.
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (HEIGHT*2,WIDTH*2))

# Take a picture and get the filter values.
ret, frame = cap.read()
window = ColorTrackBar.HSVTrackBar(frame)
values = window.showAndGetValues()
positions = [values['H'], values['S'], values['V']]
red_bounds = np.array([[values['H'][0], values['S'][0], values['V'][0]],
                           [values['H'][1], values['S'][1], values['V'][1]]])

while(cap.isOpened()):
    ret, frame = cap.read()
    # If ret is false, means there was an issue and there's no frame.
    if ret==True:
        # Get a copy for the frame where the circle will be drawn.
        circle_frame = frame.copy()

        # Convert to HSV scale, since with the H one we can get a better red filter.
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get the mask according to the filters and get only the inRange part of the original frame.
        mask = cv2.inRange(hsv_frame, red_bounds[0], red_bounds[1])
        red_frame = cv2.bitwise_and(frame, frame, mask=mask)

        # Get the contours of the image [-2] are the contours.
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(contours) > 0:
            # Get the max contour and from that the minimum enclosing circle.
            max_contour = max(contours, key=cv2.contourArea)
            ((x,y), r) = cv2.minEnclosingCircle(max_contour)
            if r > 5:
                # More about moments on: https://en.wikipedia.org/wiki/Image_moment
                M = cv2.moments(max_contour)
                # Must be an int, for the pixels and handles the division by 0.
                center = [int(np.divide(M["m10"], M["m00"])), int(np.divide(M["m01"], M["m00"]))]
                center[:] = [x if x != np.inf else 0 for x in center]
                center = tuple(center)

                # Draw the circle and centroid on the frame
                cv2.circle(circle_frame, (int(x), int(y)), int(r),(0, 255, 255), 2)
                cv2.circle(circle_frame, center, 3, (0, 0, 255), -1)
                cv2.putText(circle_frame,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                cv2.putText(circle_frame,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)

        # Convert mask to BGR so it's on the same scale as all the others and can be concatenated and saved on the video.
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        
        # Concatenate on the horizontal axis the original frame and the gray one.
        # Vertical axis: 0 instead of 1.
        red_hor = np.concatenate((mask, red_frame), axis=1)
        original_and_circle = np.concatenate((frame, circle_frame), axis=1)
        final_complete = np.concatenate((original_and_circle, red_hor), axis=0)


        # Show the frame on the screen.
        cv2.imshow('Result', final_complete)

        # Write the frame.
        out.write(final_complete)

        # Ends when q has been pressed.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything when the job is finished.
cap.release()
out.release()
cv2.destroyAllWindows()
