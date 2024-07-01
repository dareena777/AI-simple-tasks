import random
import tkinter as tk

class Game:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = [[0] * grid_size for _ in range(grid_size)]
        self.start = None
        self.goal = None
        self.generate()

    def generate(self):
        # Choose a random starting position
        self.start = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
        self.grid[self.start[0]][self.start[1]] = 1

        # Choose a random goal position
        self.goal = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
        while self.goal == self.start:
            self.goal = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
        self.grid[self.goal[0]][self.goal[1]] = 2

        # Generate a maze using the greedy or DFS algorithm randomly
        if random.random() < 0.5:
            self.generate_greedy()
        else:
            self.generate_dfs()

    def generate_greedy(self):
        # Generate a maze using the greedy algorithm
        current = self.start
        while current != self.goal:
            neighbors = []
            if current[0] > 0 and self.grid[current[0]-1][current[1]] == 0:
                neighbors.append((current[0]-1, current[1]))
            if current[1] > 0 and self.grid[current[0]][current[1]-1] == 0:
                neighbors.append((current[0], current[1]-1))
            if current[0] < self.grid_size-1 and self.grid[current[0]+1][current[1]] == 0:
                neighbors.append((current[0]+1, current[1]))
            if current[1] < self.grid_size-1 and self.grid[current[0]][current[1]+1] == 0:
                neighbors.append((current[0], current[1]+1))
            if not neighbors:
                break
            heuristic = lambda x: abs(x[0]-self.goal[0]) + abs(x[1]-self.goal[1])
            current = min(neighbors, key=heuristic)
            self.grid[current[0]][current[1]] = 1

    def generate_dfs(self):
        # Generate a maze using the DFS algorithm
        stack = [self.start]
        while stack:
            current = stack.pop()
            if current == self.goal:
                break
            neighbors = []
            if current[0] > 0 and self.grid[current[0]-1][current[1]] == 0:
                neighbors.append((current[0]-1, current[1]))
            if current[1] > 0 and self.grid[current[0]][current[1]-1] == 0:
                neighbors.append((current[0], current[1]-1))
            if current[0] < self.grid_size-1 and self.grid[current[0]+1][current[1]] == 0:
                neighbors.append((current[0]+1, current[1]))
            if current[1] < self.grid_size-1 and self.grid[current[0]][current[1]+1] == 0:
                neighbors.append((current[0], current[1]+1))
            if not neighbors:
                continue
            neighbor = random.choice(neighbors)
            self.grid[neighbor[0]][neighbor[1]] = 1
            stack.append(current)
            stack.append(neighbor)

class GameWindow:
    def __init__(self, grid_size):
        self.game = Game(grid_size)
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=grid_size*50, height=grid_size*50)
        self.canvas.pack()
        self.draw_grid()
        self.draw_player()
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Right>", self.move_right)
        self.root.mainloop()

    def draw_grid(self):
        for i in range(self.game.grid_size):
            for j in range(self.game.grid_size):
                if self.game.grid[i][j] == 1:
                    color = "white"
                elif self.game.grid[i][j] == 2:
                    color = "green"
                else:
                    color = "gray"
                x1, y1 = j*50, i*50
                x2, y2 = x1+50, y1+50
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def draw_player(self):
        x, y = self.game.start
        x1, y1 = y*50+10, x*50+10
        x2, y2 = x1+30, y1+30
        self.player = self.canvas.create_oval(x1, y1, x2, y2, fill="red")

    def move_player(self, dx, dy):
        x, y = self.game.start
        if x+dx < 0 or x+dx >= self.game.grid_size or \
           y+dy < 0 or y+dy >= self.game.grid_size or \
           self.game.grid[x+dx][y+dy] == 0:
            return
        self.game.start = (x+dx, y+dy)
        self.canvas.move(self.player, dy*50, dx*50)
        if self.game.start == self.game.goal:
            self.canvas.itemconfig(self.player, fill="yellow")
            self.canvas.unbind("<Up>")
            self.canvas.unbind("<Left>")
            self.canvas.unbind("<Down>")
            self.canvas.unbind("<Right>")
            self.canvas.bind("<Button-1>", self.restart)

    def move_up(self, event):
        self.move_player(-1, 0)

    def move_left(self, event):
        self.move_player(0, -1)

    def move_down(self, event):
        self.move_player(1, 0)

    def move_right(self, event):
        self.move_player(0, 1)

    def restart(self, event):
        self.canvas.delete("all")
        self.game.generate()
        self.draw_grid()
        self.draw_player()

GameWindow(10)

