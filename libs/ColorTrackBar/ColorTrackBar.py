import cv2
import numpy as np
from functools import partial

MIN_SUFFIX = " min"
MAX_SUFFIX = " max"

# Bas class for the trackbars. Should not be accessed.
class _ColorTrackBar:
    def __init__(self,
                 img,
                 channel_mins,
                 channel_maxes,
                 channel_names,
                 position,
                 converter=(lambda img: img),
                 name="TrackBar Window"):
        self._name = name
        self._img = img.copy()
        self._converted = converter(self._img)
        self._channel_mins = channel_mins
        self._channel_maxes = channel_maxes
        self._channel_names = channel_names
        self._lower_bound = np.array(channel_mins)
        self._upper_bound = np.array(channel_maxes)
        self._initializeWindow(position)

    # Updates the lower bound of the channel with the position of the trackbar.
    def _updateLowerBound(self, channel, pos):
        self._lower_bound[channel] = pos
        self._update()

    # Updates the upper bound of the channel with the position of the trackbar.
    def _updateUpperBound(self, channel, pos):
        self._upper_bound[channel] = pos
        self._update()
    
    # Updates the image with the new values of the filter.
    def _update(self):
        mask = cv2.inRange(self._converted, self._lower_bound, self._upper_bound)
        masked = cv2.bitwise_and(self._img, self._img, mask=mask)
        cv2.imshow(self._name, masked)
    
    # Initializes the window on the set position.
    def _initializeWindow(self, position):
        cv2.namedWindow(self._name)
        for i, (name, min_, max_) in enumerate(zip(self._channel_names, self._channel_mins, self._channel_maxes)):
            cv2.createTrackbar(name + MIN_SUFFIX, self._name, min_, max_, partial(self._updateLowerBound, i))
            cv2.setTrackbarMin(name + MIN_SUFFIX, self._name, min_)
            cv2.createTrackbar(name + MAX_SUFFIX, self._name, max_, max_, partial(self._updateUpperBound, i))
        self._setTrackbarPos(position)
        self._update()

    # Sets the position of the trackbars.
    def _setTrackbarPos(self, positions):
        if positions:
            for name, pos in zip(self._channel_names, positions):
                cv2.setTrackbarPos(name + MIN_SUFFIX, self._name, pos[0])
                cv2.setTrackbarPos(name + MAX_SUFFIX, self._name, pos[1])
    
    # runs until an exit command has been pressed and returns the value of the trackbars.
    # Note: This function should always be called.
    def showAndGetValues(self):
        while True:
            print("Press [q] or [esc] to close the window.")
            k = cv2.waitKey() & 0xFF
            if k in (ord("q"), ord("\x1b")):
                break
        values = {}
        for name in self._channel_names:
            values[name] = (cv2.getTrackbarPos(name + MIN_SUFFIX, self._name), cv2.getTrackbarPos(name + MAX_SUFFIX, self._name))
        cv2.destroyWindow(self._name)
        return values

class BGRTrackBar(_ColorTrackBar):
    def __init__(self, img, custom_position = []):
        super(BGRTrackBar, self).__init__(img,
                                          [0, 0, 0],
                                          [255, 255, 255],
                                          ['B', 'G', 'R'],
                                          custom_position,
                                          name='BGR TrackBar')

class HSVTrackBar(_ColorTrackBar):
    def __init__(self, img, custom_position = []):
        super(HSVTrackBar, self).__init__(img,
                                          [0, 0, 0],
                                          [180, 255, 255],
                                          ['H', 'S', 'V'],
                                          custom_position,
                                          partial(cv2.cvtColor, code=cv2.COLOR_BGR2HSV),
                                          'HSV TrackBar')