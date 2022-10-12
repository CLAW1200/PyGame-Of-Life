"""
Choose From Different Search Algorithms
"""

if __name__ == "__main__":
    pass

def basic_search(self):
    """
    Basic Search Algorithm: Every cell on the grid is checked individually.
    Very Slow
    """
    for i in range(self.grid.cell_width):
        for j in range(self.grid.cell_height):
            num_neighbors = self.grid.get_cell(i, j).get_num_neighbors()
            if self.grid.get_cell(i, j).get_alive():
                if num_neighbors < 2 or num_neighbors > 3:
                    self.grid.get_cell(i, j).set_next_dead()
                else:
                    self.grid.get_cell(i, j).set_next_alive()
            else:
                if num_neighbors == 3:
                    self.grid.get_cell(i, j).set_next_alive()
                else:
                    self.grid.get_cell(i, j).set_next_dead()


def new_search(self):
    #advanced cell search method
    pass