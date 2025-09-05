"""Comprehensive benchmarks: run multiple repetitions across sizes and densities,
collect timings and produce plots saved to disk.
"""
import random
import time
import statistics
import matplotlib.pyplot as plt
from optimal_meeting_point import _fast_total_distance, _bfs_total_distance

SIZES = [80, 120, 160]
DENSITIES = [0.05, 0.2, 0.5]
REPS = 5

results = []
for N in SIZES:
    for density in DENSITIES:
        fast_times = []
        bfs_times = []
        houses_counts = []
        for rep in range(REPS):
            random.seed(1000 + rep)
            grid = [[1 if random.random() < density else 0 for _ in range(N)] for _ in range(N)]
            houses = [(i, j) for i in range(N) for j in range(N) if grid[i][j] == 1]
            total_houses = len(houses)

            t0 = time.perf_counter()
            _fast_total_distance(grid, houses, N, N, total_houses)
            t1 = time.perf_counter()

            t2 = time.perf_counter()
            _bfs_total_distance(grid, houses, N, N, total_houses)
            t3 = time.perf_counter()

            fast_times.append(t1-t0)
            bfs_times.append(t3-t2)
            houses_counts.append(total_houses)

        results.append({
            'N': N,
            'density': density,
            'fast_mean': statistics.mean(fast_times),
            'fast_std': statistics.stdev(fast_times) if len(fast_times) > 1 else 0,
            'bfs_mean': statistics.mean(bfs_times),
            'bfs_std': statistics.stdev(bfs_times) if len(bfs_times) > 1 else 0,
            'houses_mean': statistics.mean(houses_counts),
        })

# plot results
for metric in ('fast_mean', 'bfs_mean'):
    plt.figure(figsize=(8,6))
    for density in DENSITIES:
        xs = [r['N'] for r in results if r['density']==density]
        ys = [r[metric] for r in results if r['density']==density]
        plt.plot(xs, ys, marker='o', label=f'density={density}')
    plt.xlabel('Grid size N (N x N)')
    plt.ylabel('Time (s)')
    plt.title(metric)
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{metric}.png')

# numeric summary
with open('benchmark_summary.txt', 'w') as f:
    for r in results:
        f.write(f"N={r['N']} density={r['density']} houses_mean={r['houses_mean']:.1f} "
                f"fast={r['fast_mean']:.6f}s±{r['fast_std']:.6f} "
                f"bfs={r['bfs_mean']:.6f}s±{r['bfs_std']:.6f}\n")

print('Benchmarks complete. Outputs: fast_mean.png, bfs_mean.png, benchmark_summary.txt')
