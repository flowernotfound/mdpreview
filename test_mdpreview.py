import unittest
from mdpreview import Config, read_markdown_file, convert_markdown_to_html, FileReadError
import os

class TestConfig(unittest.TestCase):
    def test_default_config(self):
        config = Config()
        self.assertEqual(config.theme, 'default')
        self.assertFalse(config.toc)
        self.assertTrue(config.highlight)

    def test_custom_config(self):
        config = Config(theme='custom', toc=True, highlight=False)
        self.assertEqual(config.theme, 'custom')
        self.assertTrue(config.toc)
        self.assertFalse(config.highlight)
        
    def test_load_from_file(self):
        config_path = 'test_data/config.json'
        os.makedirs('test_data', exist_ok=True)
        with open(config_path, 'w') as f:
            f.write('{"theme": "custom", "toc": true, "highlight": false}')

        config = Config()
        config.load_from_file(config_path)
        self.assertEqual(config.theme, 'custom')
        self.assertTrue(config.toc)
        self.assertFalse(config.highlight)

        os.remove(config_path)
        os.rmdir('test_data')
        
class TestMarkdownReader(unittest.TestCase):
    def setUp(self):
        self.markdown_file = 'test_data/sample.md'
        os.makedirs('test_data', exist_ok=True)
        with open(self.markdown_file, 'w') as f:
            f.write('# Sample Markdown\n\nThis is a sample markdown file.')

    def tearDown(self):
        os.remove(self.markdown_file)
        os.rmdir('test_data')

    def test_read_markdown_file(self):
        content = read_markdown_file(self.markdown_file)
        self.assertIsInstance(content, str)
        self.assertTrue(content.startswith('# Sample Markdown'))

    def test_read_markdown_file_exception(self):
        with self.assertRaises(FileReadError):
            read_markdown_file('nonexistent.md')

class TestMarkdownConverter(unittest.TestCase):
    def test_convert_markdown_to_html(self):
        config = Config(theme='default', toc=True, highlight=True)
        content = '# Sample Markdown\n\nThis is a sample markdown file.'
        html = convert_markdown_to_html(content, config)
        self.assertIsInstance(html, str)
        self.assertTrue(html.startswith('<style>'))
        self.assertTrue('Sample Markdown' in html)

if __name__ == '__main__':
    unittest.main()