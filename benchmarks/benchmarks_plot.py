"""Run repeated benchmarks and save comparison plots (fast vs BFS).

This script runs a few repetitions for each (N, density) pair, records times,
computes mean/std, and saves plots as PNG files in the repo root.
"""
import random
import time
import statistics
import os
from optimal_meeting_point import _fast_total_distance, _bfs_total_distance

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT_DIR = '.'

def run_pair(N, density, reps=3, seed=0):
    fast_times = []
    bfs_times = []
    for r in range(reps):
        random.seed(seed + r)
        grid = [[1 if random.random() < density else 0 for _ in range(N)] for _ in range(N)]
        houses = [(i, j) for i in range(N) for j in range(N) if grid[i][j] == 1]
        total_houses = len(houses)

        t0 = time.perf_counter()
        _fast_total_distance(grid, houses, N, N, total_houses)
        t1 = time.perf_counter()
        fast_times.append(t1-t0)

        t2 = time.perf_counter()
        _bfs_total_distance(grid, houses, N, N, total_houses)
        t3 = time.perf_counter()
        bfs_times.append(t3-t2)

    return {
        'fast_mean': statistics.mean(fast_times),
        'fast_std': statistics.stdev(fast_times) if len(fast_times)>1 else 0.0,
        'bfs_mean': statistics.mean(bfs_times),
        'bfs_std': statistics.stdev(bfs_times) if len(bfs_times)>1 else 0.0,
        'fast_times': fast_times,
        'bfs_times': bfs_times,
    }

if __name__ == '__main__':
    sizes = [80, 120]
    densities = [0.05, 0.2, 0.5]
    reps = 3

    summary = {}
    for N in sizes:
        for d in densities:
            print(f"Running N={N}, density={d}")
            r = run_pair(N, d, reps=reps, seed=42)
            summary[(N,d)] = r
            print(f"  fast mean={r['fast_mean']:.4f}s ±{r['fast_std']:.4f}  bfs mean={r['bfs_mean']:.4f}s ±{r['bfs_std']:.4f}")

    # Create a grouped bar chart for each size
    for N in sizes:
        labels = [str(d) for d in densities]
        fast_means = [summary[(N,d)]['fast_mean'] for d in densities]
        fast_err = [summary[(N,d)]['fast_std'] for d in densities]
        bfs_means = [summary[(N,d)]['bfs_mean'] for d in densities]
        bfs_err = [summary[(N,d)]['bfs_std'] for d in densities]

        x = range(len(densities))
        width = 0.35
        fig, ax = plt.subplots(figsize=(8,4))
        ax.bar([i-width/2 for i in x], fast_means, width, yerr=fast_err, label='fast')
        ax.bar([i+width/2 for i in x], bfs_means, width, yerr=bfs_err, label='bfs')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_xlabel('density')
        ax.set_ylabel('time (s)')
        ax.set_title(f'Benchmark N={N} (mean ± std over {reps} runs)')
        ax.legend()
        out_file = os.path.join(OUT_DIR, f'benchmark_N{N}.png')
        fig.tight_layout()
        fig.savefig(out_file)
        print(f'Wrote {out_file}')

    # Also create a combined heatmap-like table (fast vs bfs ratios)
    for d in densities:
        Ns = sizes
        ratios = [summary[(N,d)]['bfs_mean'] / (summary[(N,d)]['fast_mean'] + 1e-12) for N in Ns]
        fig, ax = plt.subplots(figsize=(6,3))
        ax.bar([str(N) for N in Ns], ratios)
        ax.set_xlabel('N')
        ax.set_ylabel('bfs / fast time ratio')
        ax.set_title(f'Ratio at density={d}')
        out_file = os.path.join(OUT_DIR, f'ratio_density_{int(d*100)}.png')
        fig.tight_layout()
        fig.savefig(out_file)
        print(f'Wrote {out_file}')

    print('\nDone. Charts saved in repo root.')
