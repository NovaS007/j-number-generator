import csv

def writeCSV(filename, results):
    fieldnames = ["j_num", "a", "b", "c", "k", "prime_factors", "is_prime"]

    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for j_num, info in sorted(results.items()):
            writer.writerow({
                "j_num": j_num,
                "a": info["a"],
                "b": info["b"],
                "c": info["c"],
                "k": info["k"],
                "prime_factors": ";".join(map(str, info["prime_factors"])) if info["prime_factors"] else "",
                "is_prime": info["is_prime"],
            })

