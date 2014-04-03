from random import choice


class Game:
    '''
    Contains all the logic for the 2048 game.
    '''
    def __init__(self, size=4):
        self.size = size
        
        self.grid = [0]*size*size
        self.rows = [slice(i*size, (i+1)*size) for i in range(size)]
        self.cols = [slice(i, size**2, size) for i in range(size)]

        self.add_tile()
        self.add_tile()

    def __repr__(self):
        ''' Print the board out as a size-by-size grid '''
        rows = []
        for s in self.rows:
            rows.append("\t".join([str(i) for i in self.grid[s]]))
        return "\n".join(rows)

    @property
    def finished(self):
        ''' Is True when 2048 appears on the board, False otherwise. '''
        return self.grid.count(2048) > 0

    @property
    def solvable(self):
        ''' Is True when gameplay can continue, False otherwise. '''
        if self.grid.count(0) > 0:
            return True

        for i in range(self.size**2):
            if (i != self.size**2-1 and self.grid[i] == self.grid[i+1] or
                    i != 0 and self.grid[i] == self.grid[i-1] or
                    i < self.size**2-self.size and self.grid[i] == self.grid[i+self.size] or
                    i > self.size and self.grid[i] == self.grid[i-self.size]):
                return True

        return False

    def add_tile(self):
        ''' Attempt to add a tile to the board '''
        zeros = zip(*filter(lambda (i,v): v==0, enumerate(self.grid)))[0]
        if zeros: self.grid[choice(zeros)] = 2
    
    def move(self, slices, sort, join_range, step):
        ''' Move the numbers in a certain direction '''
        grid = self.grid[:]
        for s in slices:
            # Move 0's out of the way
            grid[s] = sorted(grid[s], key=sort)

            # Join tiles
            for j in join_range:
                if grid[s][j] and grid[s][j] == grid[s][j+step]:
                    grid[s] = map(lambda (i,v): (i!=j)*v + (i==(j+step))*v, enumerate(grid[s]))
                    break  # only join one tile per slice

            # Move 0's out of the way
            grid[s] = sorted(grid[s], key=sort)

        if grid != self.grid:
            # Grid was changed
            self.grid = grid
            return True
        # Grid was unchanged
        return False

    def move_up(self):
        return self.move(self.cols, lambda i: not bool(i), range(self.size)[-1:0:-1], -1)

    def move_down(self):
        return self.move(self.cols, lambda i: bool(i), range(self.size-1), 1)

    def move_left(self):
        return self.move(self.rows, lambda i: not bool(i), range(self.size)[-1:0:-1], -1)

    def move_right(self):
        return self.move(self.rows, lambda i: bool(i), range(self.size-1), 1)
