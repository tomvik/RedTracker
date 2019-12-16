import numpy as np
import cv2

# Initializes the video capturing from the webcam (0)
# From a file, just write string in there.
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object.
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# False the last one if it's going to be on gray scale.
# The size of the window must be correct otherwise, trouble.
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640*2,480*2))

while(cap.isOpened()):
    ret, frame = cap.read()
    # If ret is false, means there was an issue and there's no frame.
    if ret==True:
        # Convert to gray scale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Make the gray scale image have three channels.
        gray_3_channel = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        # Concatenate on the horizontal axis the original frame and the gray one.
        # Vertical axis: 0 instead of 1.
        original_and_gray_horizontal = np.concatenate((frame, gray_3_channel), axis=1)

        # Convert to HSV scale, since with the H one we can get a better red filter.
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Red filters
        lower_bound_red = np.array([[0, 120, 70], [10, 255, 255]])
        upper_bound_red = np.array([[170, 120, 70], [180, 255, 255]])

        mask_1 = cv2.inRange(hsv_frame, lower_bound_red[0], lower_bound_red[1])
        mask_2 = cv2.inRange(hsv_frame, upper_bound_red[0], upper_bound_red[1])

        mask_hor = np.concatenate((mask_1, mask_2), axis=1)

        mask = cv2.bitwise_or(mask_1, mask_2)
        red_frame = cv2.bitwise_and(frame, frame, mask=mask)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        red_hor = np.concatenate((mask, red_frame), axis=1)
        final_complete = np.concatenate((original_and_gray_horizontal, red_hor), axis=0)


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