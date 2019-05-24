import unittest
import urllib.parse


class URLTestCase(unittest.TestCase):

    def assertQueryStringArgsEqual(self, querystring1, querystring2):
        # clean-up '?'
        if isinstance(querystring1, str) and querystring1.startswith('?'):
            querystring1 = querystring1[1:]
        if isinstance(querystring2, str) and querystring2.startswith('?'):
            querystring2 = querystring2[1:]

        if isinstance(querystring1, str) or isinstance(querystring1, unicode):
            querystring1 = urllib.parse.parse_qs(querystring1)

        if isinstance(querystring2, str) or isinstance(querystring2, unicode):
            querystring2 = urllib.parse.parse_qs(querystring2)

        self.assertDictEqual(querystring1, querystring2)
