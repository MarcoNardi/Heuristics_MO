import numpy as np
import matplotlib.pyplot as plt


def greedy_scp_visualizer(m, n, costs, columns, pause=0.5):
    uncovered = set(range(m))
    selected = []
    total_cost = 0

    # tracking
    covered_progress = []
    cost_progress = []

    plt.ion()
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    step = 0

    while uncovered:
        best_j = None
        best_score = float("inf")
        best_new_rows = set()

        # find best column
        for j in range(n):
            new_rows = columns[j] & uncovered
            if not new_rows:
                continue

            score = costs[j] / len(new_rows)

            if score < best_score:
                best_score = score
                best_j = j
                best_new_rows = new_rows

        if best_j is None:
            print("No feasible solution!")
            break

        # select column
        selected.append(best_j)
        total_cost += costs[best_j]
        uncovered -= best_new_rows

        # track progress
        covered_progress.append(m - len(uncovered))
        cost_progress.append(total_cost)

        # --- Visualization ---
        ax[0].cla()
        ax[1].cla()

        # Coverage progress
        ax[0].plot(covered_progress, marker="o")
        ax[0].set_title("Covered Rows Progress")
        ax[0].set_xlabel("Step")
        ax[0].set_ylabel("Rows Covered")
        ax[0].set_ylim(0, m)

        # Cost progress
        ax[1].plot(cost_progress, marker="o")
        ax[1].set_title("Total Cost")
        ax[1].set_xlabel("Step")
        ax[1].set_ylabel("Cost")

        plt.suptitle(f"Step {step} | Picked column {best_j} | +{len(best_new_rows)} rows")

        plt.pause(pause)

        step += 1

    plt.ioff()
    plt.show()

    return selected, total_cost


def load_scp_column_format(filepath):
    with open(filepath, "r") as f:
        data = list(map(int, f.read().split()))

    idx = 0

    # problem size
    m = data[idx]
    idx += 1
    n = data[idx]
    idx += 1

    costs = []
    columns = []  # columns[j] = set of rows covered by column j

    for _ in range(n):
        cost = data[idx]
        idx += 1

        k = data[idx]
        idx += 1

        rows = data[idx : idx + k]
        idx += k

        # convert to 0-based indexing
        rows = [r - 1 for r in rows]

        costs.append(cost)
        columns.append(set(rows))

    return m, n, costs, columns


folder = "./rail/instances/"
m, n, costs, columns = load_scp_column_format(folder + "rail507")
selected, total_cost = greedy_scp_visualizer(m, n, costs, columns, pause=0.2)

print("Solution size:", len(selected))
print("Total cost:", total_cost)
