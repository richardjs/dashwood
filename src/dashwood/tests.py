import unittest

from dashwood.state import State


class StateTests(unittest.TestCase):
    def test_initial_children_count(self):
        s = State()
        self.assertEqual(len(list(s.actions)), 16*15)

    def test_basic_is_win(self):
        s = State()
        self.assertFalse(s.is_win)
        s.move((0, 1))
        self.assertFalse(s.is_win)
        s.move((1, 2))
        self.assertFalse(s.is_win)
        s.move((2, 3))
        self.assertFalse(s.is_win)
        s.move((3, 4))
        self.assertTrue(s.is_win)

    def test_minimax_find_immediate_win(self):
        s = State()
        s.move((0, 1))
        self.assertNotEqual(s.minimax(1), 1.0)
        s.move((1, 2))
        self.assertNotEqual(s.minimax(1), 1.0)
        s.move((2, 4))
        self.assertEqual(s.minimax(1), 1.0)


if __name__ == '__main__':
    unittest.main()
