import time
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint

from easy_config.config import Config
from easy_lib.timing import TimingTestCase, timing


class TestTiming(TimingTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_path = Path.cwd() / 'toto.csv'

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.temp_path.unlink(missing_ok=True)

    def test_timing(self):
        with timing('test1'):
            time.sleep(.3)

        for i in range(10):
            with timing('test2'):
                time.sleep(.02)

    def test_config_csv(self):
        @dataclass
        class Toto:
            x: float
            y: str

        xx = [
            Toto(2., 'aaa'),
            Toto(2., 'aaa'),
            Toto(2., 'aaa'),
        ]
        path = self.temp_path

        Config.write_csv(path, xx)
        yy = Config.read_csv(path, Toto)

        pprint(yy)
