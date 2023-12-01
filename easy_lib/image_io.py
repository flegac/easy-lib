from pathlib import Path

import cv2
import numpy as np
from loguru import logger
from tifffile import imwrite, imread

MAX_PIXEL_VALUE = 255


class ImageIO:

    @staticmethod
    def write(path: Path, buffer: np.ndarray):
        logger.debug(f'saving buffer {buffer.min():.3f}-{buffer.max():.3f} to {path}')
        path.parent.mkdir(parents=True, exist_ok=True)
        filename = str(path)
        match buffer.ndim:
            case 2:
                imwrite(filename, buffer)
                # cv2.imwrite(filename, buffer)
            case 3:
                buffer = cv2.cvtColor(buffer, cv2.COLOR_RGB2BGR)
        cv2.imwrite(filename, buffer)

    @staticmethod
    def read(path: Path) -> np.ndarray:
        filename = str(path)
        buffer = imread(filename)
        # buffer = cv2.imread(filename)

        logger.debug(f'reading buffer {buffer.min(), buffer.max()} from {path}')
        match buffer.ndim:
            case 3:
                buffer = cv2.cvtColor(buffer, cv2.COLOR_RGB2BGR)

        return buffer


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
