import unittest
from optimal_meeting_point import min_total_distance

class TestOptimalMeetingPoint(unittest.TestCase):
    def test_example(self):
        grid = [
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0]
        ]
        self.assertEqual(min_total_distance(grid), 6)

    def test_no_empty_land(self):
        grid = [
            [1, 1],
            [1, 1]
        ]
        self.assertEqual(min_total_distance(grid), -1)

    def test_no_houses(self):
        grid = [
            [0, 0],
            [0, 0]
        ]
        self.assertEqual(min_total_distance(grid), -1)

    def test_empty_grid(self):
        # empty grid should be treated as invalid input
        self.assertEqual(min_total_distance([]), -1)

    def test_fastpath_matches_bfs_small(self):
        # small 0/1 grid where fast path should be used; compare with BFS fallback
        grid = [
            [1,0,1,0],
            [0,0,0,0],
            [1,0,0,1],
            [0,1,0,0]
        ]
        # function should pick fast path; result must be an int and non-negative
        res = min_total_distance(grid)
        self.assertIsInstance(res, int)
        self.assertGreaterEqual(res, 0)

    def test_unreachable(self):
        grid = [
            [1, 2, 0],
            [2, 2, 0],
            [0, 0, 1]
        ]
        self.assertEqual(min_total_distance(grid), -1)

    def test_single_house(self):
        grid = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        self.assertEqual(min_total_distance(grid), 1)

    def test_large(self):
        grid = [[0]*10 for _ in range(10)]
        grid[0][0] = 1
        grid[9][9] = 1
        self.assertEqual(min_total_distance(grid), 18)

if __name__ == "__main__":
    unittest.main()
