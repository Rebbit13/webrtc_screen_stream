import os

import numpy
from PIL import ImageGrab
from aiortc.mediastreams import VideoStreamTrack

from av import VideoFrame

import settings


class ScreenTrack(VideoStreamTrack):
    top = settings.SCREEN_TOP
    bottom = settings.SCREEN_BOTTOM
    left = settings.SCREEN_LEFT
    right = settings.SCREEN_RIGHT

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        image = ImageGrab.grab(bbox=(self.left, self.top, self.right, self.bottom))
        image_array = numpy.array(image)
        image.close()
        frame = VideoFrame.from_ndarray(image_array)
        frame.pts, frame.time_base = pts, time_base
        return frame
