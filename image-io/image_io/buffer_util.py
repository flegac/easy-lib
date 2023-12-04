import cv2
import numpy as np

from image_io.resolution import Resolution

MAX_PIXEL_VALUE = 255


class BufferUtil:
    @staticmethod
    def mirror_tile(buffer: np.ndarray):
        top = np.hstack([buffer, np.fliplr(buffer)])
        return np.vstack([top, np.flipud(top)])

    @staticmethod
    def resize(buffer: np.ndarray, resolution: Resolution, seamless: bool = False):
        res = cv2.resize(buffer, dsize=resolution.raw(), interpolation=cv2.INTER_LANCZOS4)
        if seamless:
            res[-1, :] = res[0, :]
            res[:, -1] = res[:, 0]
        return res

    @staticmethod
    def normalize(buffer: np.ndarray, png_format: bool = False):
        if buffer.min() != buffer.max():
            buffer -= buffer.min()
        if buffer.max() != 0:
            buffer = buffer / buffer.max()

        if png_format:
            buffer = (buffer * MAX_PIXEL_VALUE).astype('uint8')
        else:
            buffer = buffer.astype('float32')

        return buffer
