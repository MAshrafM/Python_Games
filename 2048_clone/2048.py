"""
Clone of 2048 game.
"""
import random
import poc_2048_gui        

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = []
    for idx in range(len(line)):
        if line[idx] == 0:
            pass
        else:
            result.append(line[idx])
            
    while len(result) < len(line):
        result.append(0)
    result.append(0)    
    for idx in range(len(line)):
        if result[idx] == result[idx+1]:
            result[idx] = result[idx]+result[idx+1]
            result.pop(idx+1)
            result.append(0)        
    result.pop()
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.board = []
        self.reset()
        
        tiles_left = []
        tiles_right = []
        tiles_up = []
        tiles_down = []
        
        for index in range(self.width):
            tiles_left.append([index, 0])
            tiles_right.append([index, self.height-1])
            tiles_up.append([0, index])
            tiles_down.append([self.width-1, index])

        
        self.dic_keys = {UP: tiles_up, 
                    DOWN: tiles_down, 
                    LEFT: tiles_left, 
                    RIGHT: tiles_right}
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.board = [ [0 for col in range(self.width)] for row in range(self.height)]
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self.board)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        new_line = []
        for row,col in self.dic_keys[direction]:
            temp_list = []
            drow = row
            dcol = col
            while row >=0 and col >=0 and row < self.width and col < self.height:
                dummyx = self.board[row][col]
                temp_list.append(dummyx)
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
            new_line = merge(temp_list)
            idx = 0
            while drow >=0 and dcol >=0 and drow < self.width and dcol < self.height and idx<len(new_line):
                self.board[drow][dcol] = new_line[idx]
                idx += 1
                drow += OFFSETS[direction][0]
                dcol += OFFSETS[direction][1]
        self.new_tile()      
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_place = []
        tile_value = 2
        
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == 0:
                    empty_place.append([row, col])
                
                    
        if random.random() < 0.9:
            tile_value = 2
        else:
            tile_value = 4
        
        rand_row, rand_col = random.choice(empty_place)
        self.board[rand_row][rand_col] = tile_value
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.board[row][col] = value
        

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self.board[row][col]
 
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
