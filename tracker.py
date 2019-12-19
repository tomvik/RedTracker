import libs.ColorTrackBar.ColorTrackBar as ColorTrackBar
import numpy as np
import cv2

# Initializes the video capturing from the webcam (0)
# From a file, just write string in there.
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera didn't open. Something went wrong")
    exit

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640*.7)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480*.7)

# Define the codec and create VideoWriter object.
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# False the last one if it's going to be on gray scale.
# The size of the window must be correct otherwise, trouble.
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

# Take a picture and modify the filter values.
ret, frame = cap.read()
window = ColorTrackBar.HSVTrackBar(frame)
lower_values = window.showAndGetValues()
print(lower_values)
positions = [lower_values['H'], lower_values['S'], lower_values['V']]
red_bounds = np.array([[lower_values['H'][0], lower_values['S'][0], lower_values['V'][0]],
                           [lower_values['H'][1], lower_values['S'][1], lower_values['V'][1]]])

while(cap.isOpened()):
    ret, frame = cap.read()
    # If ret is false, means there was an issue and there's no frame.
    if ret==True:
        # Convert to HSV scale, since with the H one we can get a better red filter.
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        circle_frame = frame.copy()

        mask = cv2.inRange(hsv_frame, red_bounds[0], red_bounds[1])
        red_frame = cv2.bitwise_and(frame, frame, mask=mask)

        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(contours) > 0:
            max_contour = max(contours, key=cv2.contourArea)
            ((x,y), r) = cv2.minEnclosingCircle(max_contour)
            if r > 2:
                M = cv2.moments(max_contour)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(circle_frame, (int(x), int(y)), int(r),(0, 255, 255), 2)
                cv2.circle(circle_frame, center, 3, (0, 0, 255), -1)
                cv2.putText(circle_frame,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                cv2.putText(circle_frame,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)

        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        red_hor = np.concatenate((mask, red_frame), axis=1)
        # Concatenate on the horizontal axis the original frame and the gray one.
        # Vertical axis: 0 instead of 1.
        original_and_circle = np.concatenate((frame, circle_frame), axis=1)
        final_complete = np.concatenate((original_and_circle, red_hor), axis=0)


        # Show the frame on the screen.
        cv2.imshow('Final complete', final_complete)

        # Write the frame.
        out.write(final_complete)

        # Ends when q has been pressed.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
