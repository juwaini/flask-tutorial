import unittest
from selenium import webdriver

class TestFlaskPage(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://localhost:5000')

    def test_index_page(self):
        self.assertIn('Hello, world!', self.browser.page_source)

    def tearDown(self):
        self.browser.quit()

if __name__ == '__main__':
    unittest.main()
