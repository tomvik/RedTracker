import numpy as np
import cv2

# Initializes the video capturing from the webcam (0)
# From a file, just write string in there.
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object.
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# False the last one if it's going to be on gray scale.
# The size of the window must be correct otherwise, trouble.
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640*2,480))

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
        numpy_horizontal_concat = np.concatenate((frame, gray_3_channel), axis=1)

        # Show the frame on the screen.
        cv2.imshow('Numpy Horizontal Concat', numpy_horizontal_concat)

        # Write the frame.
        out.write(numpy_horizontal_concat)

        # Ends when q has been pressed.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()