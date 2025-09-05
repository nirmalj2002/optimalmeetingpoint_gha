"""
Optimal Meeting Point in a Grid

Problem:
Given a 2D grid of integers where 1 represents a house and 0 represents empty land,
find the minimum total Manhattan distance from all houses to a single meeting point
that must be located on an empty land cell. If no valid meeting point exists, return -1.

High-level approaches implemented:
- BFS-per-house (general): For grids that may contain obstacles or values other than 0/1,
    run a BFS from each house to accumulate distances and reach counts for empty cells.
    This guarantees correctness in the presence of obstacles but costs O(H * M * N) time.

- Fast separable path (optimized): For pure 0/1 grids (no obstacles), the Manhattan distance
    cost separates across rows and columns. We compute per-row and per-column costs using
    prefix sums (O(M + N) extra work) and evaluate the best empty cell in O(M*N) time.
    This removes the H factor and is much faster for dense grids with many houses.

Complexity:
- General BFS approach: time O(H * M * N), space O(M * N) for distance/reach arrays.
- Optimized separable approach (0/1 grids): time O(M * N) and extra space O(M + N).

Notes:
- The function returns -1 for invalid inputs (empty grid) or when no empty cell is reachable
    from all houses.
"""

from collections import deque
from typing import List

def min_total_distance(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return -1
    m, n = len(grid), len(grid[0])
    total_houses = sum(cell for row in grid for cell in row)
    if total_houses == 0:
        return -1
    # collect house coordinates once to avoid scanning multiple times
    houses = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == 1]
    # Fast path: if grid contains only 0s and 1s (no obstacles),
    # we can compute the total Manhattan distance using separable row/col costs
    # and pick the minimum over empty cells in O(M*N) time.
    has_only_01 = True
    for row in grid:
        for v in row:
            if v not in (0, 1):
                has_only_01 = False
                break
        if not has_only_01:
            break

    if has_only_01:
        # counts per row and per column
        row_count = [0]*m
        col_count = [0]*n
        for i, j in houses:
            row_count[i] += 1
            col_count[j] += 1

        # compute cost for each row: cost_row[r] = sum_i row_count[i]*abs(i-r)
        cost_row = [0]*m
        # initial cost at row 0
        cost_row[0] = sum(row_count[i]*i for i in range(m))
        prefix = 0
        total = total_houses
        for r in range(1, m):
            prefix += row_count[r-1]
            # moving from r-1 to r changes cost by (2*prefix - total)
            cost_row[r] = cost_row[r-1] + (2*prefix - total)

        # compute cost for each column similarly
        cost_col = [0]*n
        cost_col[0] = sum(col_count[j]*j for j in range(n))
        prefix = 0
        for c in range(1, n):
            prefix += col_count[c-1]
            cost_col[c] = cost_col[c-1] + (2*prefix - total)

        # now check empty cells only
        min_cost = float('inf')
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    min_cost = min(min_cost, cost_row[i] + cost_col[j])
        return min_cost if min_cost != float('inf') else -1

    # General case with obstacles: BFS from each house (original approach)
    return _bfs_total_distance(grid, houses, m, n, total_houses)


def _fast_total_distance(grid: List[List[int]], houses, m: int, n: int, total_houses: int) -> int:
    """Fast separable path for pure 0/1 grids."""
    row_count = [0]*m
    col_count = [0]*n
    for i, j in houses:
        row_count[i] += 1
        col_count[j] += 1

    cost_row = [0]*m
    cost_row[0] = sum(row_count[i]*i for i in range(m))
    prefix = 0
    total = total_houses
    for r in range(1, m):
        prefix += row_count[r-1]
        cost_row[r] = cost_row[r-1] + (2*prefix - total)

    cost_col = [0]*n
    cost_col[0] = sum(col_count[j]*j for j in range(n))
    prefix = 0
    for c in range(1, n):
        prefix += col_count[c-1]
        cost_col[c] = cost_col[c-1] + (2*prefix - total)

    min_cost = float('inf')
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0:
                min_cost = min(min_cost, cost_row[i] + cost_col[j])
    return min_cost if min_cost != float('inf') else -1


def _bfs_total_distance(grid: List[List[int]], houses, m: int, n: int, total_houses: int) -> int:
    """BFS-per-house fallback for grids with obstacles."""
    dist = [[0]*n for _ in range(m)]
    reach = [[0]*n for _ in range(m)]
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    visited_mark = [[0]*n for _ in range(m)]
    visit_id = 1
    for i, j in houses:
        q = deque()
        q.append((i, j, 0))
        visited_mark[i][j] = visit_id
        while q:
            x, y, d = q.popleft()
            for dx, dy in directions:
                nx, ny = x+dx, y+dy
                # allow traversal through houses (1) and empty (0); treat 2 as obstacle
                if 0<=nx<m and 0<=ny<n and visited_mark[nx][ny] != visit_id and grid[nx][ny] != 2:
                    visited_mark[nx][ny] = visit_id
                    # only accumulate distance/reach for empty land cells
                    if grid[nx][ny] == 0:
                        dist[nx][ny] += d+1
                        reach[nx][ny] += 1
                    q.append((nx, ny, d+1))
        visit_id += 1
    min_dist = float('inf')
    for i in range(m):
        for j in range(n):
            if grid[i][j]==0 and reach[i][j]==total_houses:
                min_dist = min(min_dist, dist[i][j])
    return min_dist if min_dist != float('inf') else -1
