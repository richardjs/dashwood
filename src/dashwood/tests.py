import unittest

from dashwood import search, state
from dashwood.ui import tui


class StateTests(unittest.TestCase):
    def test_initial_children_count(self):
        s = state.initial()
        self.assertEqual(len(list(state.children(s))), 16*15)

    def test_is_win(self):
        s = state.initial()
        self.assertFalse(state.is_win(s))
        state.move(s, 0, 1)
        self.assertFalse(state.is_win(s))
        state.move(s, 1, 2)
        self.assertFalse(state.is_win(s))
        state.move(s, 2, 4)
        self.assertFalse(state.is_win(s))
        state.move(s, 3, 4)
        self.assertTrue(state.is_win(s))

    def test_minimax_find_immediate_win(self):
        s = state.initial()
        state.move(s, 0, 1)
        self.assertNotEqual(search.minimax(s, 1), 1.0)
        state.move(s, 1, 2)
        self.assertNotEqual(search.minimax(s, 1), 1.0)
        state.move(s, 2, 4)
        self.assertEqual(search.minimax(s, 1), 1.0)



if __name__ == '__main__':
    unittest.main()
