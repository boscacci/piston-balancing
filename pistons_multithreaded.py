import itertools
import multiprocessing
import numpy as np
import time

########### SETTINGS ##########

n_cylinders = 5

### Random data (replace with actual data) ###
mass_pistons = np.random.uniform(500, 750, n_cylinders).round(1)
mass_rods = np.random.uniform(400, 600, n_cylinders).round(1)
mass_pins = np.random.uniform(60, 100, n_cylinders).round(1)

### Actual Data (enter a list of masses): ###
# mass_pistons = [515, 612, 740, 623, 597, 701]
# mass_rods = []
# mass_pins = []

################################


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.4f} seconds to execute.")
        return result

    return wrapper


def weight_variance(sets):
    total_weights = [sum(s) for s in sets]
    return np.var(total_weights)


def find_optimal_arrangement(args):
    rod_combinations, piston_combinations, pin_combinations = args
    min_var = float("inf")
    optimal_arrangement = None

    for rods in rod_combinations:
        for pistons in piston_combinations:
            for pins in pin_combinations:
                sets = list(zip(rods, pistons, pins))
                var = weight_variance(sets)
                if var < min_var:
                    min_var = var
                    optimal_arrangement = sets
                    print(f"Found smaller var: {round(min_var,4)}")

    return min_var, optimal_arrangement


@timer_decorator
def main():
    print()
    print(f"Piston masses: {sorted([m for m in mass_pistons])}")
    print()
    print(f"Rod Masses: {sorted([m for m in mass_rods])}")
    print()
    print(f"Pin masses: {sorted([m for m in mass_pins])}")
    print()

    # Calculate all possible combinations of sets
    pin_combinations = list(itertools.permutations(mass_pins))
    piston_combinations = list(itertools.permutations(mass_pistons))
    rod_combinations = list(itertools.permutations(mass_rods))

    # Divide the search space into smaller chunks
    rod_chunk_size = len(rod_combinations) // (multiprocessing.cpu_count() * 5)
    rod_chunks = [
        rod_combinations[i : i + rod_chunk_size]
        for i in range(0, len(rod_combinations), rod_chunk_size)
    ]
    print(f"rod_chunk_size: {rod_chunk_size}\n")

    min_var = float("inf")
    optimal_arrangement = None

    # Parallelize the computation
    with multiprocessing.Pool() as pool:
        results = pool.map(
            find_optimal_arrangement,
            [
                (rod_chunk, piston_combinations, pin_combinations)
                for rod_chunk in rod_chunks
            ],
        )

        for var, arrangement in results:
            if var < min_var:
                min_var = var
                optimal_arrangement = arrangement

    total_weights = sorted([sum(a) for a in optimal_arrangement])
    print(f"\nLowest variance between sets: {round(min_var, 2)}g")
    print(f"Lowest std between sets: {round(np.sqrt(min_var), 2)}g")
    print("Arrangement for least variance:", optimal_arrangement)
    print(f"Total weights: {total_weights}")


if __name__ == "__main__":
    main()
