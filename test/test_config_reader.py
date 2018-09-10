# export the PYTHONPATH till the project folder as I added another folder test for writing the test cases and Python
# wouldn't be able to recognize the other packages.
# export PYTHONPATH=$PYTHONPATH:/Users/hmandadi/Documents/harsh/scorer.py/
# Run test case from scorer/ folder
# python -m unittest discover ../test/

import unittest
from mock import MagicMock
import scorer.config_reader as config_reader


class ConfigReaderTestCases(unittest.TestCase):

    def test_wrong_json_path(self):
        config_reader.read_json = MagicMock(return_value=str('No such file or directory'))
        self.assertEqual(config_reader.read_json('/path/not/found/'), 'No such file or directory')

    def test_json_file_unable_to_open(self):
        config_reader.read_json = MagicMock(return_value=str('No JSON object could be decoded'))
        self.assertEqual(config_reader.read_json('/filenotabletoberead/sample-template.abc'),
                         'No JSON object could be decoded')


if __name__ == '__main__':
    unittest.main()
