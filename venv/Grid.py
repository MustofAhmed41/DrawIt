from Utils import COLOR_WHITE


class Grid:
    def __init__(self, position_x, position_y, color, row, column):
        self.position_x = position_x
        self.position_y = position_y
        self.color = color
        self.row = row
        self.column = column



GRID_WIDTH = 5
GRID_HEIGHT = 5

NUMBER_OF_GRID_COLUMNS = 160
NUMBER_OF_GRID_ROWS = 160
grid = [[Grid(i * 5, j * 5, COLOR_WHITE, j, i) \
         for i in range(NUMBER_OF_GRID_COLUMNS)] for j in range(NUMBER_OF_GRID_ROWS)]


#print(nodes[0][159].position_x)
#print(nodes[0][159].position_x,nodes[0][159].position_y)