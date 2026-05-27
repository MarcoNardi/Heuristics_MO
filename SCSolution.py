class SCSolution:
    def __init__(self, m, n, costs, columns, rows):
        self.m = m
        self.n = n
        self.costs = costs
        self.columns = columns
        self.rows = rows

        # solution
        self.selected = [False] * n

        # coverage tracking
        self.cover_count = [0] * m

        # uncovered rows
        self.uncovered = list(range(m))
        self.row_to_uncovered_idx = {i: i for i in range(m)}

        self.total_cost = 0

    def add_column(self, j):
        if self.selected[j]:
            return
        self.selected[j] = True
        self.total_cost += self.costs[j]

        for i in self.columns[j]:
            self.cover_count[i] += 1
            if self.cover_count[i] == 1:
                # O(1) removal from uncovered list
                idx = self.row_to_uncovered_idx[i]
                last_row = self.uncovered[-1]
                self.uncovered[idx] = last_row
                self.row_to_uncovered_idx[last_row] = idx
                self.uncovered.pop()
                del self.row_to_uncovered_idx[i]

    def remove_column(self, j):
        if not self.selected[j]:
            return
        self.selected[j] = False
        self.total_cost -= self.costs[j]

        for i in self.columns[j]:
            self.cover_count[i] -= 1
            if self.cover_count[i] == 0:
                # Add back to uncovered
                self.row_to_uncovered_idx[i] = len(self.uncovered)
                self.uncovered.append(i)

    def is_redundant(self, j):
        """
        Check if the column j is redundant, meaning that all the rows are already covered by other selected columns.
        """
        for i in self.columns[j]:
            if self.cover_count[i] <= 1:
                return False
        return True

    def remove_redundant_columns(self):
        """Sort by cost to remove expensive redundant columns first."""
        selected_cols = [j for j, s in enumerate(self.selected) if s]
        # Heuristic: try removing high-cost columns first
        selected_cols.sort(key=lambda x: self.costs[x], reverse=True)

        for j in selected_cols:
            is_red = True
            for i in self.columns[j]:
                if self.cover_count[i] <= 1:
                    is_red = False
                    break
            if is_red:
                self.remove_column(j)

    def get_critical_rows(self):
        return [i for i in range(self.m) if self.cover_count[i] == 1]

    def copy(self):
        new = SCSolution(self.m, self.n, self.costs, self.columns, self.rows)
        new.selected = self.selected.copy()
        new.cover_count = self.cover_count.copy()
        new.uncovered = self.uncovered.copy()
        new.row_to_uncovered_idx = self.row_to_uncovered_idx.copy()
        new.total_cost = self.total_cost
        return new
