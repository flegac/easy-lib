from pathlib import Path

import cv2
import numpy as np
from loguru import logger
from tifffile import imwrite, imread, TiffFileError

from easy_kit.timing import time_func


class ImageIO:

    @staticmethod
    @time_func
    def write(path: Path | str, buffer: np.ndarray):
        path = Path(path)
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
    @time_func
    def read(path: Path | str) -> np.ndarray:
        filename = str(path)
        try:
            buffer = imread(filename)
        except TiffFileError:
            buffer = cv2.imread(filename)

        logger.debug(f'reading buffer {buffer.min(), buffer.max()} from {path}')
        match buffer.ndim:
            case 3:
                buffer = cv2.cvtColor(buffer, cv2.COLOR_RGB2BGR)

        return buffer
