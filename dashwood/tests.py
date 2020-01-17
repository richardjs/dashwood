import unittest

from dashwood import state


class StateTests(unittest.TestCase):
    def test_initial_children_count(self):
        s = state.initial()
        self.assertEqual(len(list(state.children(s))), 16*15)


if __name__ == '__main__':
    unittest.main()
