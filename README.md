# optimalmeetingpoint_gha

## Solution for Optimal Meeting Point

This repository contains an optimized Python solution for finding the minimum total Manhattan distance from all houses to a single meeting point on empty land in a grid.

### Setup & Install Dependencies

1. Make sure you have Python 3.7+ installed.
2. Install all dependencies:
	```sh
	pip install -r requirements.txt
	```

### How to Run Tests

You can use either `unittest` or `pytest` to run the tests:

**With unittest:**
```sh
python -m unittest test_optimal_meeting_point.py
```

**With pytest:**

```sh
pytest test_optimal_meeting_point.py
```

### How to Check Code Coverage

1. Run tests with coverage:

```sh
coverage run --source=optimal_meeting_point -m pytest
```

2. See the coverage report:

```sh
coverage report -m
```

## Algorithm & Complexity

This project implements two strategies inside `min_total_distance`:

- Fast separable path (used when the grid contains only 0 and 1):
	- Uses per-row and per-column cost computations with prefix sums.
	- Time: O(M * N), Space: O(M + N) extra.
	- Good when the grid has many houses and no obstacles.

- General BFS-per-house fallback (used when grid contains obstacles / other values):
	- Runs BFS from each house to compute distances to reachable empty cells.
	- Time: O(H * M * N), Space: O(M * N).
	- Guarantees correctness for arbitrary grids containing obstacles.

Use the test and coverage instructions above to validate behavior.

## Benchmarks

I ran a small benchmark comparing the fast separable path and the BFS fallback on a 120x120 grid with three densities. Results:

- Low density (N=120, density=0.05): houses=659 -> fast=0.002s, bfs=6.551s
- Medium density (N=120, density=0.2): houses=2900 -> fast=0.002s, bfs=27.782s
- Dense (N=120, density=0.5): houses=7203 -> fast=0.002s, bfs=65.639s

The benchmark scripts are in the `benchmarks/` directory:

- `benchmarks/benchmarks_run.py` — runs fast vs BFS once for three densities and prints timings.
- `benchmarks/benchmarks_plot.py` — repeated runs that produce PNG charts (bar + ratio charts).
- `benchmarks/benchmarks_full.py` — heavier comprehensive run that produces metric PNGs and a summary file.

Benchmark parameter explanations:
- N: grid size (grid is N x N).
- density: probability (0..1) that a cell is a house (1). For example, density=0.2 means ~20% of cells are houses.

How to run the benchmarks:

```sh
python -m benchmarks.benchmarks_run
# or plotting runner
python -m benchmarks.benchmarks_plot
```

If you generated plots with the plotting helper, the following files are created in the repository root:

- `benchmark_N80.png` — bar chart (fast vs bfs means ± std) for N=80
- `benchmark_N120.png` — bar chart (fast vs bfs means ± std) for N=120
- `ratio_density_5.png` — bfs/fast time ratio for density=0.05
- `ratio_density_20.png` — bfs/fast time ratio for density=0.20
- `ratio_density_50.png` — bfs/fast time ratio for density=0.50

Quick interpretation:
- The fast separable path (used when the grid only contains 0s and 1s) is orders of magnitude faster than the BFS-per-house fallback on the tested sizes and densities.
- BFS runtime grows quickly with the number of houses and grid size; the fast path runs in roughly O(M*N) and shows very small timing variance.

To (re)generate the charts locally run (from repo root):

```sh
python -m benchmarks.benchmarks_plot
```
