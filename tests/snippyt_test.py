import unittest
import main

code = """some source code"""
title = """title"""
class SnippytTest(unittest.TestCase):
    def setUp(self):
        import tempfile
        main.shelve_name = tempfile.mktemp()
    def tearDown(self):
        import os
        try:
            os.remove(main.shelve_name)
        except:
            pass

    def test_post(self):
        client = main.app.test_client()
        ret = client.post("/",  data=dict(source_code=code, title=title))
        self.assertGreater(400,ret.status_code)

if __name__ == '__main__':
    unittest.main()