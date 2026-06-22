import random
import time
import sys
import math




def generate_uniform_sorted_array(n: int, low: int = 1, high: int = None) -> list:
   
    if high is None:
        high = n * 10
    if high - low + 1 < n:
        raise ValueError("Range too small to draw n unique values.")
    sample = random.sample(range(low, high + 1), n)
    sample.sort()
    return sample



def interpolation_search(arr: list, key: int):
  
   
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high and arr[low] <= key <= arr[high]:
        if arr[high] == arr[low]:
            comparisons += 1
            if arr[low] == key:
                return low, comparisons
            return -1, comparisons

       
        pos = low + ((key - arr[low]) * (high - low) // (arr[high] - arr[low]))

        comparisons += 1
        if arr[pos] == key:
            return pos, comparisons
        elif arr[pos] < key:
            low = pos + 1
        else:
            high = pos - 1

    return -1, comparisons



def measure_time(arr: list, key: int, runs: int = 500) -> float:
   
    total = 0.0
    for _ in range(runs):
        start = time.perf_counter()
        interpolation_search(arr, key)
        total += time.perf_counter() - start
    return total / runs



def space_info(n: int) -> str:
    array_bytes   = n * sys.getsizeof(0)
    overhead_bytes = sys.getsizeof(0) * 5
    total_kb = (array_bytes + overhead_bytes) / 1024
    return (
        f"  Array storage  : O(n) ≈ {array_bytes:,} bytes  ({n} × {sys.getsizeof(0)} bytes/int)\n"
        f"  Algorithm vars : O(1) ≈ {overhead_bytes} bytes  (fixed overhead)\n"
        f"  Total estimate : ≈ {total_kb:.2f} KB"
    )



def ascii_line_graph(sizes: list, times_us: list,
                     width: int = 60, height: int = 18) -> None:
    
    min_t, max_t = min(times_us), max(times_us)
    t_range = max_t - min_t or 1.0

    # O(log log n) reference curve, scaled to the same y-range
    ref_raw = [math.log2(math.log2(s + 2)) for s in sizes]
    ref_min, ref_max = min(ref_raw), max(ref_raw)
    ref_range = ref_max - ref_min or 1.0
    ref_scaled = [
        min_t + (r - ref_min) / ref_range * t_range for r in ref_raw
    ]

    
    min_s, max_s = min(sizes), max(sizes)
    s_range = max_s - min_s or 1

    def to_col(s):
        return int((s - min_s) / s_range * (width - 1))

    def to_row(t):
        return int((max_t - t) / t_range * (height - 1))

    
    canvas = [[" "] * width for _ in range(height)]

    
    for s, t in zip(sizes, ref_scaled):
        c, r = to_col(s), to_row(t)
        if canvas[r][c] == " ":
            canvas[r][c] = "·"

    
    prev_col, prev_row = None, None
    for s, t in zip(sizes, times_us):
        c, r = to_col(s), to_row(t)
        # Connect to previous point with '-'
        if prev_col is not None:
            step = 1 if c > prev_col else -1
            for ic in range(prev_col + step, c, step):
                # Linear interpolate row
                frac = (ic - prev_col) / (c - prev_col)
                ir = int(prev_row + frac * (r - prev_row))
                if canvas[ir][ic] == " ":
                    canvas[ir][ic] = "-"
        canvas[r][c] = "★"
        prev_col, prev_row = c, r

    
    y_label_width = 8
    print()
    print("  Execution Time vs Input Size  (★ = measured,  · = O(log log n) ref)")
    print()

    for r, row in enumerate(canvas):
        t_val = max_t - r / (height - 1) * t_range
        label = f"{t_val:6.3f}" if r % 3 == 0 else " " * 6
        bar   = "─" if r % 3 == 0 else " "
        print(f"  {label} µs {bar}│ {''.join(row)}")

    
    print(f"  {'':>6}    └{'─' * width}")

    
    mid_idx  = len(sizes) // 2
    col_mid  = to_col(sizes[mid_idx])
    label_lo = f"{sizes[0]:,}"
    label_mi = f"{sizes[mid_idx]:,}"
    label_hi = f"{sizes[-1]:,}"

   
    tick_line = [" "] * width
    for i, ch in enumerate(label_lo):
        if i < width:
            tick_line[i] = ch
    start_mi = col_mid - len(label_mi) // 2
    for i, ch in enumerate(label_mi):
        pos = start_mi + i
        if 0 <= pos < width:
            tick_line[pos] = ch
    start_hi = width - len(label_hi)
    for i, ch in enumerate(label_hi):
        pos = start_hi + i
        if 0 <= pos < width:
            tick_line[pos] = ch

    print(f"  {'':>6}     {''.join(tick_line)}")
    print(f"  {'':>6}     {'Input size  n':^{width}}")
    print()



def main():
    print("=" * 58)
    print("       Interpolation Search  —  Demo Program")
    print("=" * 58)

    
    while True:
        try:
            n = int(input("\nEnter the number of elements (n): "))
            if n < 2:
                print("  Please enter n ≥ 2.")
                continue
            break
        except ValueError:
            print("  Invalid input. Enter an integer.")

   
    arr = generate_uniform_sorted_array(n)
    print(f"\nGenerated a uniformly distributed sorted array of {n} elements.")
    preview = arr[:10]
    suffix  = " ..." if n > 10 else ""
    print(f"  Preview : {preview}{suffix}")
    print(f"  Range   : [{arr[0]}, {arr[-1]}]")

    
    while True:
        try:
            key = int(input("\nEnter the search key: "))
            break
        except ValueError:
            print("  Invalid input. Enter an integer.")

    
    idx, comparisons = interpolation_search(arr, key)
    elapsed = measure_time(arr, key)


    print("\n" + "─" * 58)
    print("  SEARCH RESULTS")
    print("─" * 58)
    if idx != -1:
        print(f"  Found  : key {key} at index {idx}  (position {idx + 1})")
    else:
        print(f"  Result : key {key} not found in the array.")
    print(f"\n  Comparisons performed : {comparisons}")
    print(f"  Avg. execution time   : {elapsed * 1_000_000:.4f} µs  "
          f"({elapsed * 1_000:.6f} ms)")
    print(f"\n  Time Complexity  : O(log log n)  — average case (uniform data)")
    print(f"                     O(n)          — worst case")
    print(f"\n  Space Complexity :")
    print(space_info(n))
    print("─" * 58)

    
    print("\nBenchmarking across multiple input sizes …\n")
    sizes    = [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
    times_us = []

    for s in sizes:
        a   = generate_uniform_sorted_array(s)
        k   = a[len(a) // 2]
        avg = measure_time(a, k, runs=200)
        times_us.append(avg * 1_000_000)
        print(f"  n = {s:>9,}  →  {avg * 1_000_000:.4f} µs")

    ascii_line_graph(sizes, times_us)
    print("Done.")


if __name__ == "__main__":
    main()
