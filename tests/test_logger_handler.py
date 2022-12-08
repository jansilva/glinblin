from unittest import TestCase

from glinblin.glinblin import LoggerHandler


class TestLogger(TestCase):

    def setUp(self):
        pass

    def tearDown(self) -> None:
        pass

    def test_is_singleton_logger_handler(self):
        self.assertIs(LoggerHandler(), LoggerHandler())

    # def test_info_message(self):
    #     with self.assertLogs() as logs:
    #         pass # call method with logger.
    #     self.assertEqual(len(logs), 1)
    #     self.assertEqual(logs.records[0].getMessage(), "Testing log method")