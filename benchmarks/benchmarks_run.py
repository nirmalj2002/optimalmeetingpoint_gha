"""Run benchmarks for low, medium, and dense grids comparing fast path vs BFS fallback.

This script uses a fixed random seed for reproducibility and prints timings.
"""
import random
import time
from optimal_meeting_point import _fast_total_distance, _bfs_total_distance

def run_once(N, density, seed=0):
    random.seed(seed)
    grid = [[1 if random.random() < density else 0 for _ in range(N)] for _ in range(N)]
    houses = [(i, j) for i in range(N) for j in range(N) if grid[i][j] == 1]
    total_houses = len(houses)

    # run fast path
    t0 = time.perf_counter()
    fast_res = _fast_total_distance(grid, houses, N, N, total_houses)
    t1 = time.perf_counter()

    # run bfs fallback (may be slow on dense grids)
    t2 = time.perf_counter()
    bfs_res = _bfs_total_distance(grid, houses, N, N, total_houses)
    t3 = time.perf_counter()

    return {
        'N': N,
        'density': density,
        'houses': total_houses,
        'fast_res': fast_res,
        'fast_time': t1-t0,
        'bfs_res': bfs_res,
        'bfs_time': t3-t2,
    }

if __name__ == '__main__':
    # moderate size to keep runtime reasonable
    N = 120
    densities = [0.05, 0.2, 0.5]
    seed = 42
    results = []
    for d in densities:
        print(f"Running N={N}, density={d}")
        r = run_once(N, d, seed)
        results.append(r)
        print(f" houses={r['houses']:6d}  fast_time={r['fast_time']:.3f}s  bfs_time={r['bfs_time']:.3f}s  fast_res={r['fast_res']}  bfs_res={r['bfs_res']}")
    print('\nSummary:')
    for r in results:
        print(f"N={r['N']} density={r['density']} houses={r['houses']:6d} fast={r['fast_time']:.3f}s bfs={r['bfs_time']:.3f}s")
