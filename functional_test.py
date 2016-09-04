import unittest
from selenium import webdriver

class TestFlaskPage(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_index_page(self):
        self.browser.get('http://localhost:5000')
        self.assertIn('Hello, world!', self.browser.page_source)
        self.assertIn('Hi there!', self.browser.title)

    def test_test_page(self):
        self.browser.get('localhost:5000/test')
        self.assertIn('This is a \'test\' page', self.browser.page_source)

    def tearDown(self):
        self.browser.quit()

if __name__ == '__main__':
    unittest.main()
