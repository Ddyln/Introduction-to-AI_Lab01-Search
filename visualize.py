import tkinter as tk
import time as TIME
from tkinter import ttk
from a_star import a_star
from ucs import ucs
from dfs import dfs

sz = 64
start_x, start_y = 0, 0

def readMap(matrix, file_name):
    inp = open(file_name).read().split('\n')
    w = list(map(int, inp[0].split()))
    stones_cost = list(map(int, inp[0].split()))
    inp = inp[1:]
    w = max([len(line) for line in inp])
    h = len(inp)
    matrix = [i for i in inp]
    matrix = [','.join(i).split(',') for i in matrix]
    player_pos = []
    stones_pos = ()
    switches_pos = ()
    walls_pos = ()
    cnt = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == ' ': matrix[i][j] = 0 # space
            elif matrix[i][j] == '#': # walls
                matrix[i][j] = 1
                walls_pos += ((i, j), )
            elif matrix[i][j] == '$': # stones
                matrix[i][j] = 2
                stones_pos += ((i, j, stones_cost[cnt]), )
                cnt += 1
            elif matrix[i][j] == '@': # ares
                matrix[i][j] = 3
                player_pos = [i, j]
            elif matrix[i][j] == '.': # switches
                matrix[i][j] = 4
                switches_pos += ((i, j), )
            elif matrix[i][j] == '*': # stones + switches
                matrix[i][j] = 5
                stones_pos += ((i, j, stones_cost[cnt]), )
                cnt += 1
                switches_pos += ((i, j), )
            elif matrix[i][j] == '+': # ares + switches
                matrix[i][j] = 6
                player_pos = [i, j]
    return w, h, player_pos, stones_pos, switches_pos, walls_pos

actionsMap = 'urdlURDL'
file_name = 'input-01.txt'
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

class CanvasDemo:
    def __init__(self, root):
        self.root = root
        self.width = 64 * 15
        self.height = 64 * 10
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='gray')
        self.root.resizable(False, False)
        self.canvas.pack()
        self.root.title("Search Visualization")
        self.player_image = tk.PhotoImage(file="./Assets/player.png")
        self.ground_image = tk.PhotoImage(file="./Assets/ground.png")
        self.crate_image = tk.PhotoImage(file="./Assets/crate.png")
        self.goal_image = tk.PhotoImage(file="./Assets/goal.png")
        self.block_image = tk.PhotoImage(file="./Assets/block.png")
        self.switches_pos = ()
        self.speed = 500
        # self.restart()
        self.button = tk.Button(
            root, 
            text="Start", 
            command=self.start,
            width=8,
            height=2
        )
        self.button.place(x = sz * 13, y = sz * 2)
        
        self.button = tk.Button(
            root, 
            text="Stop", 
            command=self.stop,
            width=8,
            height=2
        )
        self.button.place(x = sz * 13, y = sz * 3.25)

        self.button = tk.Button(
            root, 
            text="Restart", 
            command=self.restart,
            width=8,
            height=2
        )
        self.button.place(x = sz * 13, y = sz * 4.5)

        self.algorithm_label = tk.Label(root, 
            text="Select Algorithm",
            font=("Arial", 13)
        )
        self.algorithm_label.place(x=sz * 12.5, y=sz * 0.5)
        self.algorithm_combobox = ttk.Combobox(root, 
            values=["DFS", "UCS", "A*"], 
            state='readonly',
            width=10,
            font=("Arial", 12)
        )
        self.actions = ''
        self.algorithm_combobox.set("DFS")  # Set default value
        self.algorithm_combobox.place(x=sz * 12 + sz * 3 // 4, y=sz * 1)
        self.algorithm_combobox.bind("<<ComboboxSelected>>", self.on_algorithm_selected)
        self.on_algorithm_selected(tk.Event())
    def restart(self):
        matrix = [[]]
        W, H, player_pos, stones_pos,self.switches_pos, walls_pos = readMap(matrix, file_name)

        for i in range(H):
            for j in range(W):
                self.root.after(10, lambda pos=(i,j): self.drawCell(pos))
        self.root.after(20, lambda: self.drawCell(player_pos, self.player_image))
        for i in stones_pos:
            self.root.after(20, lambda pos=i: self.drawCell(pos, self.crate_image))
        for i in self.switches_pos:
            self.root.after(20, lambda pos=i: self.drawCell(pos, self.goal_image))
        for i in walls_pos:
            self.root.after(20, lambda pos=i: self.drawCell(pos, self.block_image))
        self.running = False
        self.player_pos = player_pos 
        self.animation_state = 0

    def on_algorithm_selected(self, event):
        selected_algorithm = self.algorithm_combobox.get()
        if selected_algorithm == 'DFS':
            self.root.after(0, self.run_dfs)
        elif selected_algorithm == 'UCS':
            self.root.after(0, self.run_ucs)
        elif selected_algorithm == 'A*':
            self.root.after(0, self.run_a_star)
        self.restart()

    def start(self):
        if not self.running:
            self.running = True
            self.animate() 
        
    def run_dfs(self):
        self.actions, steps, weight, node, time, memory = dfs(file_name)
        
    def run_ucs(self):
        self.actions, steps, weight, node, time, memory = ucs(file_name)

    def run_a_star(self):
        self.actions, steps, weight, node, time, memory = a_star(file_name)

    def stop(self):
        self.running = False

    def animate(self):
        if self.running:
            if self.animation_state < len(self.actions):
                # ok = False
                # for i in self.switches_pos:
                #     if self.player_pos == [i[0], i[1]]:
                #         ok = True
                self.drawCell(self.player_pos)
                # if ok: self.drawCell(self.player_pos, self.goal_image)
                self.player_pos = self.move(self.player_pos, actionsMap.find(self.actions[self.animation_state]))
                self.drawCell(self.player_pos, self.player_image)
                self.animation_state += 1
                self.root.after(self.speed, self.animate)
            else:
                self.running = False

    def drawCell(self, coordinate, image = None):
        y = coordinate[0]
        x = coordinate[1]
        if image is None:
            self.canvas.create_rectangle(start_x + x * sz,
                                    start_y + y * sz,
                                    start_x + (x + 1) * sz,
                                    start_y + (y + 1) * sz, 
                                    fill='gray')
        else:
            self.canvas.create_image(sz // 2 + sz * x, sz // 2 + sz * y, image=image)

    def move(self, coordinate, direction):
        ok = False
        if direction > 3:
            direction -= 4
            ok = True
        pos = [coordinate[0] + dx[direction], coordinate[1] + dy[direction]]
        if ok:
            self.drawCell(pos)
            newpos = [pos[0] + dx[direction], pos[1] + dy[direction]]
            self.drawCell(newpos, self.crate_image)
        for i in self.switches_pos:
            self.drawCell(i, self.goal_image)
        return pos

if __name__ == "__main__":
    root = tk.Tk()
    app = CanvasDemo(root)
    root.mainloop()