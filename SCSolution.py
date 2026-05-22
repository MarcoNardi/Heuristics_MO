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
        self.uncovered = set(range(m))

        self.total_cost = 0

    def add_column(self, j):
        """
        Add column j to the solution, updating coverage and cost.
        """
        if self.selected[j]:
            return

        self.selected[j] = True
        self.total_cost += self.costs[j]

        for i in self.columns[j]:
            self.cover_count[i] += 1
            if self.cover_count[i] == 1:
                self.uncovered.discard(i)

    def remove_column(self, j):
        """
        Remove column j from the solution, updating coverage and cost.
        """
        if not self.selected[j]:
            return

        self.selected[j] = False
        self.total_cost -= self.costs[j]

        for i in self.columns[j]:
            self.cover_count[i] -= 1
            if self.cover_count[i] == 0:
                self.uncovered.add(i)

    def is_redundant(self, j):
        """
        Check if the column j is redundant, meaning that all the rows are already covered by other selected columns.
        """
        for i in self.columns[j]:
            if self.cover_count[i] <= 1:
                return False
        return True

    def remove_redundant_columns(self):
        queue = [j for j in range(self.n) if self.selected[j]]

        while queue:
            j = queue.pop()

            if not self.selected[j]:
                continue

            if self.is_redundant(j):
                self.remove_column(j)

                # removing j may make other columns redundant
                for i in self.columns[j]:
                    for k in self.rows[i]:
                        if self.selected[k]:
                            queue.append(k)

    def get_critical_rows(self):
        return [i for i in range(self.m) if self.cover_count[i] == 1]

    def copy(self):
        new = SCSolution(self.m, self.n, self.costs, self.columns, self.rows)

        new.selected = self.selected.copy()
        new.cover_count = self.cover_count.copy()
        new.uncovered = self.uncovered.copy()
        new.total_cost = self.total_cost

        return new
