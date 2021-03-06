from unittest import TestCase

import url_parser


class TestUrlParser(TestCase):
    def test_parses_url_without_www(self):
        url = 'example.com'
        result = url_parser.parse_url(url)
        self.assertEqual(result['domain'], 'example')
        self.assertEqual(result['top_domain'], 'com')

    def test_parses_url_with_www(self):
        url = 'www.example.com'
        result = url_parser.parse_url(url)
        self.assertEqual(result['domain'], 'example')
        self.assertEqual(result['top_domain'], 'com')

    def test_returns_null_if_protocol_is_missing(self):
        url = 'www.example.com'
        result = url_parser.parse_url(url)
        self.assertIsNone(result['protocol'])

    def test_returns_null_if_www_is_missing(self):
        url = 'http://example.com'
        result = url_parser.parse_url(url)
        self.assertIsNone(result['www'])

    def test_removes_extra_dot_from_www(self):
        url = 'http://www..example.com'
        result = url_parser.parse_url(url)
        has_dot = '.' in result['www']
        self.assertFalse(has_dot)

    def test_returns_null_if_sub_domain_is_missing(self):
        url = 'http://example.com'
        result = url_parser.parse_url(url)
        self.assertIsNone(result['sub_domain'])

    def test_finds_sub_domain(self):
        url = 'mysubdomain.example.com'
        result = url_parser.parse_url(url)
        self.assertEqual(result['sub_domain'], 'mysubdomain')

    def test_finds_multiple_subdomains(self):
        url = 'my.subdomain.example.com'
        result = url_parser.parse_url(url)
        self.assertEqual(result['sub_domain'], 'my.subdomain')

    def test_finds_protocol(self):
        url = 'http://mysubdomain.example.com'
        result = url_parser.parse_url(url)
        self.assertEqual(result['protocol'], 'http')

        url = 'https://mysubdomain.example.com'
        result = url_parser.parse_url(url)
        self.assertEqual(result['protocol'], 'https')

        url = 'ftp://mysubdomain.example.com'
        result = url_parser.parse_url(url)
        self.assertEqual(result['protocol'], 'ftp')

    def test_finds_dir(self):
        url = 'http://mysubdomain.example.com/folder/'
        result = url_parser.parse_url(url)
        self.assertEqual(result['dir'], '/folder/')

        url = 'http://mysubdomain.example.com/multiple/folders/'
        result = url_parser.parse_url(url)
        self.assertEqual(result['dir'], '/multiple/folders/')

        url = 'http://mysubdomain.example.com/multiple/folders/with_a_file.js'
        result = url_parser.parse_url(url)
        self.assertEqual(result['dir'], '/multiple/folders/')

    def test_does_not_mistake_file_for_dir(self):
        url = 'http://mysubdomain.example.com/folder/test'
        result = url_parser.parse_url(url)
        self.assertEqual(result['dir'], '/folder/')
        self.assertNotEqual(result['dir'], '/folder/test')

    def test_finds_domain(self):
        url = 'http://mysubdomain.example.com'
        result = url_parser.parse_url(url)
        self.assertEqual(result['domain'], 'example')

    def test_finds_top_domain(self):
        url = 'http://mysubdomain.example.com'
        result = url_parser.parse_url(url)
        self.assertEqual(result['top_domain'], 'com')

        url = 'http://mysubdomain.example.co.uk'
        result = url_parser.parse_url(url)
        self.assertEqual(result['top_domain'], 'co.uk')

    def test_finds_file(self):
        url = 'http://mysubdomain.example.com/cool.jpg'
        result = url_parser.parse_url(url)
        self.assertEqual(result['file'], 'cool.jpg')

        url = 'http://mysubdomain.example.com/directory/here/sample.mp4'
        result = url_parser.parse_url(url)
        self.assertEqual(result['file'], 'sample.mp4')

    def test_finds_path(self):
        url = 'http://mysubdomain.example.com/path'
        result = url_parser.parse_url(url)
        self.assertEqual(result['path'], '/path')

        url = 'http://mysubdomain.example.com/this/is/the/path'
        result = url_parser.parse_url(url)
        self.assertEqual(result['path'], '/this/is/the/path')

        url = 'http://mysubdomain.example.com/path/with/file.js'
        result = url_parser.parse_url(url)
        self.assertEqual(result['path'], '/path/with/file.js')

    def test_finds_fragment(self):
        url = 'http://mysubdomain.example.com#my_fragment'
        result = url_parser.parse_url(url)
        self.assertEqual(result['fragment'], 'my_fragment')

        url = 'http://mysubdomain.example.com/path/#my_fragment'
        result = url_parser.parse_url(url)
        self.assertEqual(result['fragment'], 'my_fragment')

        url = 'http://mysubdomain.example.com/path/file.js#my_fragment'
        result = url_parser.parse_url(url)
        self.assertEqual(result['fragment'], 'my_fragment')

        url = 'http://mysubdomain.example.com#my_fragment?myargs=test'
        result = url_parser.parse_url(url)
        self.assertEqual(result['fragment'], 'my_fragment')

        url = 'http://mysubdomain.example.com/test/path.js#my_fragment?myargs=test'
        result = url_parser.parse_url(url)
        self.assertEqual(result['fragment'], 'my_fragment')

    def test_finds_query(self):
        url = 'http://mysubdomain.example.com?myquery=test'
        result = url_parser.parse_url(url)
        self.assertEqual(result['query']['myquery'], 'test')

        url = 'http://mysubdomain.example.com?myquery=test&one=two&test'
        result = url_parser.parse_url(url)
        self.assertEqual(result['query']['myquery'], 'test')
        self.assertEqual(result['query']['one'], 'two')
        self.assertIsNone(result['query']['test'])

        url = 'http://mysubdomain.example.com/file.js?myquery=test&one=two'
        result = url_parser.parse_url(url)
        self.assertEqual(result['query']['myquery'], 'test')
        self.assertEqual(result['query']['one'], 'two')

        url = 'http://mysubdomain.example.com/path/and/file.js?myquery=test&one=two'
        result = url_parser.parse_url(url)
        self.assertEqual(result['query']['myquery'], 'test')
        self.assertEqual(result['query']['one'], 'two')

        url = 'http://mysubdomain.example.com/path/?myquery=test&one=two'
        result = url_parser.parse_url(url)
        self.assertEqual(result['query']['myquery'], 'test')
        self.assertEqual(result['query']['one'], 'two')

    def test_catastrophic_backtracking(self):
        url = 'http://very_long-and-complixated_subdomaind-for-page.mywebpageishere.com/'
        result = url_parser.parse_url(url)
        self.assertEqual(result['top_domain'], 'com')
        self.assertEqual(result['domain'], 'mywebpageishere')
        self.assertEqual(result['sub_domain'], 'very_long-and-complixated_subdomaind-for-page')

    def test_domain_that_starts_with_same_letters_as_top_domain(self):
        url = 'http://domains-stars-with-same-top-domain.nogo.no/'
        result = url_parser.parse_url(url)
        self.assertEqual(result['top_domain'], 'no')
        self.assertEqual(result['domain'], 'nogo')
        self.assertEqual(result['sub_domain'], 'domains-stars-with-same-top-domain')

    def test_domain_that_includes_a_top_domain_in_sub_domain(self):
        url = 'http://test.com.hello.nogo.no/'
        result = url_parser.parse_url(url)
        self.assertEqual(result['top_domain'], 'no')
        self.assertEqual(result['domain'], 'nogo')
        self.assertEqual(result['sub_domain'], 'test.com.hello')

    def test_domain_that_includes_a_top_domain_in_query(self):
        url = 'http://test.com.hello.nogo.no?my_query_domain=www.test.com'
        result = url_parser.parse_url(url)
        self.assertEqual(result['top_domain'], 'no')
        self.assertEqual(result['domain'], 'nogo')
        self.assertEqual(result['sub_domain'], 'test.com.hello')
        self.assertEqual(result['query']['my_query_domain'], 'www.test.com')


class TestGetUrl(TestCase):
    def test_parses_url_without_www(self):
        url = 'example.com'
        result = url_parser.get_url(url)
        self.assertEqual(result.domain, 'example')
        self.assertEqual(result.top_domain, 'com')

    def test_parses_url_with_www(self):
        url = 'www.example.com'
        result = url_parser.get_url(url)
        self.assertEqual(result.domain, 'example')
        self.assertEqual(result.top_domain, 'com')

    def test_returns_null_if_protocol_is_missing(self):
        url = 'www.example.com'
        result = url_parser.get_url(url)
        self.assertIsNone(result.protocol)

    def test_returns_null_if_www_is_missing(self):
        url = 'http://example.com'
        result = url_parser.get_url(url)
        self.assertIsNone(result.www)

    def test_removes_extra_dot_from_www(self):
        url = 'http://www..example.com'
        result = url_parser.get_url(url)
        has_dot = '.' in result.www
        self.assertFalse(has_dot)

    def test_returns_null_if_sub_domain_is_missing(self):
        url = 'http://example.com'
        result = url_parser.get_url(url)
        self.assertIsNone(result.sub_domain)

    def test_finds_sub_domain(self):
        url = 'mysubdomain.example.com'
        result = url_parser.get_url(url)
        self.assertEqual(result.sub_domain, 'mysubdomain')

    def test_finds_multiple_subdomains(self):
        url = 'my.subdomain.example.com'
        result = url_parser.get_url(url)
        self.assertEqual(result.sub_domain, 'my.subdomain')

    def test_finds_protocol(self):
        url = 'http://mysubdomain.example.com'
        result = url_parser.get_url(url)
        self.assertEqual(result.protocol, 'http')

        url = 'https://mysubdomain.example.com'
        result = url_parser.get_url(url)
        self.assertEqual(result.protocol, 'https')

        url = 'ftp://mysubdomain.example.com'
        result = url_parser.get_url(url)
        self.assertEqual(result.protocol, 'ftp')

    def test_finds_dir(self):
        url = 'http://mysubdomain.example.com/folder/'
        result = url_parser.get_url(url)
        self.assertEqual(result.dir, '/folder/')

        url = 'http://mysubdomain.example.com/multiple/folders/'
        result = url_parser.get_url(url)
        self.assertEqual(result.dir, '/multiple/folders/')

        url = 'http://mysubdomain.example.com/multiple/folders/with_a_file.js'
        result = url_parser.get_url(url)
        self.assertEqual(result.dir, '/multiple/folders/')

    def test_does_not_mistake_file_for_dir(self):
        url = 'http://mysubdomain.example.com/folder/test'
        result = url_parser.get_url(url)
        self.assertEqual(result.dir, '/folder/')
        self.assertNotEqual(result.dir, '/folder/test')

    def test_finds_domain(self):
        url = 'http://mysubdomain.example.com'
        result = url_parser.get_url(url)
        self.assertEqual(result.domain, 'example')

    def test_finds_top_domain(self):
        url = 'http://mysubdomain.example.com'
        result = url_parser.get_url(url)
        self.assertEqual(result.top_domain, 'com')

        url = 'http://mysubdomain.example.co.uk'
        result = url_parser.get_url(url)
        self.assertEqual(result.top_domain, 'co.uk')

    def test_finds_file(self):
        url = 'http://mysubdomain.example.com/cool.jpg'
        result = url_parser.get_url(url)
        self.assertEqual(result.file, 'cool.jpg')

        url = 'http://mysubdomain.example.com/directory/here/sample.mp4'
        result = url_parser.get_url(url)
        self.assertEqual(result.file, 'sample.mp4')

    def test_finds_path(self):
        url = 'http://mysubdomain.example.com/path'
        result = url_parser.get_url(url)
        self.assertEqual(result.path, '/path')

        url = 'http://mysubdomain.example.com/this/is/the/path'
        result = url_parser.get_url(url)
        self.assertEqual(result.path, '/this/is/the/path')

        url = 'http://mysubdomain.example.com/path/with/file.js'
        result = url_parser.get_url(url)
        self.assertEqual(result.path, '/path/with/file.js')

    def test_finds_fragment(self):
        url = 'http://mysubdomain.example.com#my_fragment'
        result = url_parser.get_url(url)
        self.assertEqual(result.fragment, 'my_fragment')

        url = 'http://mysubdomain.example.com/path/#my_fragment'
        result = url_parser.get_url(url)
        self.assertEqual(result.fragment, 'my_fragment')

        url = 'http://mysubdomain.example.com/path/file.js#my_fragment'
        result = url_parser.get_url(url)
        self.assertEqual(result.fragment, 'my_fragment')

        url = 'http://mysubdomain.example.com#my_fragment?myargs=test'
        result = url_parser.get_url(url)
        self.assertEqual(result.fragment, 'my_fragment')

        url = 'http://mysubdomain.example.com/test/path.js#my_fragment?myargs=test'
        result = url_parser.get_url(url)
        self.assertEqual(result.fragment, 'my_fragment')

    def test_finds_query(self):
        url = 'http://mysubdomain.example.com?myquery=test'
        result = url_parser.get_url(url)
        self.assertEqual(result.query['myquery'], 'test')

        url = 'http://mysubdomain.example.com?myquery=test&one=two&test'
        result = url_parser.get_url(url)
        self.assertEqual(result.query['myquery'], 'test')
        self.assertEqual(result.query['one'], 'two')
        self.assertIsNone(result.query['test'])

        url = 'http://mysubdomain.example.com/file.js?myquery=test&one=two'
        result = url_parser.get_url(url)
        self.assertEqual(result.query['myquery'], 'test')
        self.assertEqual(result.query['one'], 'two')

        url = 'http://mysubdomain.example.com/path/and/file.js?myquery=test&one=two'
        result = url_parser.get_url(url)
        self.assertEqual(result.query['myquery'], 'test')
        self.assertEqual(result.query['one'], 'two')

        url = 'http://mysubdomain.example.com/path/?myquery=test&one=two'
        result = url_parser.get_url(url)
        self.assertEqual(result.query['myquery'], 'test')
        self.assertEqual(result.query['one'], 'two')


class TestGetBasicUrl(TestCase):
    def test_basic_url(self):
        url = 'http://example.com'
        result = url_parser.get_base_url(url)
        self.assertEqual(result, 'http://example.com')

        url = 'https://example.com'
        result = url_parser.get_base_url(url)
        self.assertEqual(result, 'https://example.com')

        url = 'https://www.example.com'
        result = url_parser.get_base_url(url)
        self.assertEqual(result, 'https://www.example.com')

        url = 'example.com'
        result = url_parser.get_base_url(url)
        self.assertEqual(result, 'http://example.com')

    def test_sub_domain_basic_url(self):
        url = 'http://mysubdomain.example.com'
        result = url_parser.get_base_url(url)
        self.assertEqual(result, 'http://mysubdomain.example.com')

        url = 'https://mysubdomain.example.com'
        result = url_parser.get_base_url(url)
        self.assertEqual(result, 'https://mysubdomain.example.com')

        url = 'ftp://mysubdomain.example.com'
        result = url_parser.get_base_url(url)
        self.assertEqual(result, 'ftp://mysubdomain.example.com')

    def test_path_url(self):
        url = 'https://mysubdomain.example.com/path/to/wisdom'
        result = url_parser.get_base_url(url)
        self.assertEqual(result, 'https://mysubdomain.example.com')

    def test_long_url(self):
        url = 'https://mysubdomain.example.com/path/to/wisdom?query=2&this=3'
        result = url_parser.get_base_url(url)
        self.assertEqual(result, 'https://mysubdomain.example.com')

        url = 'https://www.example.com/path/to/wisdom?query=2&this=3'
        result = url_parser.get_base_url(url)
        self.assertEqual(result, 'https://www.example.com')

        url = 'https://example.com/path/to/wisdom?query=2&this=3'
        result = url_parser.get_base_url(url)
        self.assertEqual(result, 'https://example.com')

        url = 'example.com/path/to/wisdom?query=2&this=3'
        result = url_parser.get_base_url(url)
        self.assertEqual(result, 'http://example.com')