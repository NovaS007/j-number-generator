import csv


def writeCSV(filename, results):
    """
    Export results to CSV with optimizations.

    OPTIMIZATIONS:
    - Buffered I/O (8KB buffer)
    - Single pass through results
    - Sorted iteration for consistency
    """
    fieldnames = ["j_num", "a", "b", "c", "k", "prime_factors", "is_prime"]

    with open(filename, "w", newline="", buffering=8192) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for j_num in sorted(results.keys()):
            info = results[j_num]
            writer.writerow({
                "j_num": j_num,
                "a": info["a"],
                "b": info["b"],
                "c": info["c"],
                "k": info["k"],
                "prime_factors": ";".join(map(str, info["prime_factors"])) if info["prime_factors"] else "",
                "is_prime": info["is_prime"],
            })
