import cv2
import numpy as np
from functools import partial

MIN_SUFFIX = " min"
MAX_SUFFIX = " max"

class _ColorTrackBar:
    def __init__(self, img, name="Filter Window"):
        self._name = name
        self._img = img.copy()
        self._converted = self._converter(img)
        self._lower_bound = np.array(self._channel_mins)
        self._upper_bound = np.array(self._channel_maxes)

    def _updateLowerBound(self, channel, pos):
        self._lower_bound[channel] = pos
        self._update()

    def _updateUpperBound(self, channel, pos):
        self._upper_bound[channel] = pos
        self._update()
    
    def _update(self):
        mask = cv2.inRange(self._converted, self._lower_bound, self._upper_bound)
        masked = cv2.bitwise_and(self._img, self._img, mask=mask)
        cv2.imshow(self._name, masked)
    
    def _initializeWindow(self):
        cv2.namedWindow(self._name)
        for i, (name, min_, max_) in enumerate(zip(self._channel_names, self._channel_mins, self._channel_maxes)):
            cv2.createTrackbar(name + MIN_SUFFIX, self._name, min_, max_, partial(self._updateLowerBound, i))
            cv2.setTrackbarMin(name + MIN_SUFFIX, self._name, min_)
            cv2.createTrackbar(name + MAX_SUFFIX, self._name, max_, max_, partial(self._updateUpperBound, i))
        self._update()
    
    def show(self):
        self._initializeWindow()
        while True:
            print("Press [q] or [esc] to close the window.")
            k = cv2.waitKey() & 0xFF
            if k in (ord("q"), ord("\x1b")):
                break
        values = {}
        for name in self._channel_names:
            values[name + MIN_SUFFIX] = cv2.getTrackbarPos(name + MIN_SUFFIX, self._name)
            values[name + MAX_SUFFIX] = cv2.getTrackbarPos(name + MAX_SUFFIX, self._name)
        cv2.destroyWindow(self._name)
        return values

class BGRFilter(_ColorTrackBar):
    def __init__(self, img):
        self._converter = lambda img: img
        self._channel_names = ["B", "G", "R"]
        self._channel_mins = [0, 0, 0]
        self._channel_maxes = [255, 255, 255]
        super(BGRFilter, self).__init__(img)

class HSVFilter(_ColorTrackBar):
    def __init__(self, img):
        self._converter = partial(cv2.cvtColor, code=cv2.COLOR_BGR2HSV)
        self._channel_names = ["H", "S", "V"]
        self._channel_mins = [0, 0, 0]
        self._channel_maxes = [180, 255, 255]
        super(HSVFilter, self).__init__(img)

    def __delete__(self, instance):
        print("I was deletedd")