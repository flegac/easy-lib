from unittest import TestCase

from easy_lib.event import Event


class TestEvent(TestCase):
    def test_event(self):
        toto = Event(name='TotoQueue')

        @toto.observe
        def send_hello(data: str):
            return f'hello {data}'

        @toto.connect
        def handler(data: str):
            print(f'echo: {data}')

        toto.emit('coucou')
        send_hello('toto')
