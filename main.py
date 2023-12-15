class CellNotInitialisedError(Exception):
    pass


class Table:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = {}

        for row in range(1, rows + 1):
            for col in range(1, cols + 1):
                cell = f"{chr(65 + col - 1)}{row}"
                self.cells[cell] = None

    def parse_cell_reference(self, cell):
        """
        Parse a cell reference and return the corresponding (row, col) tuple.
        Example: 'A1' -> (1, 1)
        """
        col = ord(cell[0]) - 64
        row = int(cell[1:])
        return row, col

    def get_values(self, cell_range):
        """
        Given a cell range (e.g., 'A1:B3'), return a list of values from those cells.
        """
        start, end = cell_range.split(":")
        start_row, start_col = self.parse_cell_reference(start)
        end_row, end_col = self.parse_cell_reference(end)

        values = []
        for row in range(start_row, end_row + 1):
            for col in range(0, end_col):
                cell = chr(65 + col) + str(row)
                values.append(self.get_value(cell))
        
        return values


    def set_value(self, cell, value):
        if cell in self.cells:
            self.cells[cell] = value
        else:
            raise CellNotInitialisedError()

    def get_value(self, cell):
        return self.cells.get(cell, 0)
    
    # Addition of two or more cells
    def add(self, *cells):
        result = 0
        for cell in cells:
            if ':' in cell:  # Handle cell ranges
                result += sum(self.get_values_from_range(cell))
            else:
                result += self.get_value(cell)
        return result

    # Subtraction of two or more cells        
    def subtract(self, result_cell, *cells):
        result = self.get_value(cells[0])
        for cell in cells[1:]:
            result -= self.get_value(cell)
        self.set_value(result_cell, result)

    # Division of two cells
    def divide(self, result_cell, cell_one, cell_two):
        try:
            result = self.get_value(cell_one) / self.get_value(cell_two)
            self.set_value(result_cell, result)

        except ZeroDivisionError:
            print("Division by zero not allowed")

        
    # Multiplication of two or more cells
    def mul(self, *cells):
        result = 1
        for cell in cells:
            if ':' in cell:  # Handle cell ranges
                result *= sum(self.get_values_from_range(cell))
            else:
                result *= self.get_value(cell)
        return result

    def average(self, *cells):
        values = []
        for cell in cells:
            if ':' in cell:  # Handle cell ranges
                values.extend(self.get_values_from_range(cell))
            else:
                values.append(self.get_value(cell))

        if not values:
            raise ValueError("At least one cell must be provided to calculate the mean")

    def sum(self, *args):
        result = 0

        for arg in args:
            if (isinstance(arg, str) and ':' in arg):
                values = self.get_values(arg)
                total += sum(values)
            elif isinstance(arg, str):
                total += self.get_value(arg)
            else:
                total += arg


    def count(self, *args):
        result = 0