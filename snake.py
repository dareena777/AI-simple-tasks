import random
import tkinter as tk

class Game:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = [[0] * grid_size for _ in range(grid_size)]
        self.start = None
        self.current_goal = None
        self.achieved_goals = []
        self.visited_goals = []
        self.generate()

    def generate(self):
        # Choose a random starting position
        self.start = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
        self.grid[self.start[0]][self.start[1]] = 1

        # Choose a new goal position
        self.current_goal = self.generate_goal()

        # Reset the list of achieved goals and visited goals
        self.achieved_goals = []
        self.visited_goals = []

    def generate_goal(self):
        # Choose a random goal position that is not the starting position
        goal = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
        while goal == self.start or goal in self.achieved_goals:
            goal = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
        self.grid[goal[0]][goal[1]] = 2
        return goal

    def is_goal(self, cell):
        return cell == self.current_goal

    def is_valid_move(self, cell):
        x, y = cell
        return x >= 0 and x < self.grid_size and y >= 0 and y < self.grid_size and self.grid[x][y] != 0

    def get_neighbors(self, cell):
        x, y = cell
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        return [n for n in neighbors if self.is_valid_move(n)]

    def find_path(self, start, goal):
        queue = [[start]]
        while queue:
            path = queue.pop(0)
            current = path[-1]
            if current == goal:
                return path
            for neighbor in self.get_neighbors(current):
                new_path = path + [neighbor]
                queue.append(new_path)

    def has_path_to_goal(self):
        return self.find_path(self.start, self.current_goal) is not None

    def move_player(self, dx, dy):
        x, y = self.start
        if x+dx < 0 or x+dx >= self.grid_size or \
           y+dy < 0 or y+dy >= self.grid_size or \
           self.grid[x+dx][y+dy] == 0:
            return
        if self.game.is_goal((x+dx, y+dy)):
            self.achieved_goals.append(self.current_goal)
            self.grid[self.current_goal[0]][self.current_goal[1]] = 0
            while not self.has_path_to_goal():
                self.current_goal = self.generate_goal()
            self.visited_goals.append(self.current_goal)
            self.current_goal = self.generate_goal()
        self.start = (x+dx, y+dy)

class GameWindow:
    def __init__(self, grid_size):
        self.game = Game(grid_size)
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=grid_size*50, height=grid_size*50)
        self.canvas.pack()
        self.draw_grid()
        self.player = self.draw_player()
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
                elif (i, j) in self.game.visited_goals:
                    color = "light gray"
                elif (i, j) in self.game.achieved_goals:
                    color = "yellow"
                elif (i, j) == self.game.current_goal:
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
        player_rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")

        # Draw visited goals as part of the player
        for goal in self.game.visited_goals:
            x, y = goal
            x1, y1 = y*50+15, x*50+15
            x2, y2 = x1+20, y1+20
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="light gray", outline="light gray")

        return player_rect

    def move_player(self, dx, dy):
        self.game.move_player(dx, dy)
        self.canvas.move(self.player, dy*50, dx*50)
        self.draw_grid()

    def move_up(self, event):
        self.move_player(-1, 0)

    def move_left(self, event):
        self.move_player(0, -1)

    def move_down(self, event):
        self.move_player(1, 0)

    def move_right(self, event):
        self.move_player(0, 1)

GameWindow(10)