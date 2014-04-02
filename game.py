from random import randint

class Game:
    def __init__(self, size=4):
        self.size = size
        
        self.grid = [0]*size*size
        self.rows = [slice(i*size, (i+1)*size) for i in range(size)]
        self.cols = [slice(i, size**2, size) for i in range(size)]

        self.add_tile()
        self.add_tile()

    def __repr__(self):
        rows = []
        for s in self.rows:
            rows.append("\t".join([str(i) for i in self.grid[s]]))
        return "\n".join(rowss)

    @property
    def finished(self):
        return self.grid.count(2048) > 0

    @property
    def solvable(self):
        if self.grid.count(0) > 0:
            return True

        for i in range(self.size**2):
            if (i != self.size**2-1 and self.grid[i] == self.grid[i+1] or
                    i != 0 and self.grid[i] == self.grid[i-1] or
                    i < self.size**2-self.size and self.grid[i] == self.grid[i+self.size] or
                    i > self.size and self.grid[i] == self.grid[i-self.size]):
                return True

        return False
    
    def move(self, slices, sort, join_range, step):
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
            self.grid = grid
            return True
        return False

    def move_up(self):
        return self.move(self.cols, lambda i: not bool(i), range(self.size)[-1:0:-1], -1)

    def move_down(self):
        return self.move(self.cols, lambda i: bool(i), range(self.size-1), 1)

    def move_left(self):
        return self.move(self.rows, lambda i: not bool(i), range(self.size)[-1:0:-1], -1)

    def move_right(self):
        return self.move(self.rows, lambda i: bool(i), range(self.size-1), 1)

    def add_tile(self):
        if self.grid.count(0) > 0:
            i = randint(0, self.size**2-1)
            while self.grid[i]:
                i = randint(0, self.size**2-1)
            self.grid[i] = 2
