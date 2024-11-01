import tkinter as tk
import time as TIME
import threading
from tkinter import ttk
from a_star import a_star
from ucs import ucs
from dfs import dfs
from bfs import bfs
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
    player_pos = ()
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
                player_pos = (i, j)
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
                player_pos = (i, j)
                switches_pos += ((i, j), )
    return w, h, player_pos, stones_pos, switches_pos, walls_pos

actionsMap = 'urdlURDL'
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

class App:
    def __init__(self, root):
        self.root = root
        self.width = 64 * 15
        self.height = 64 * 10
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='gray')
        self.root.resizable(False, False)
        self.canvas.pack()
        for i in range(10):
            for j in range(12):
                self.drawCell((i, j))
        # self.canvas.create_line(768, 0, 768, 640)
        self.root.title("Search Visualization")
        self.player_image = tk.PhotoImage(file="./Assets/player.png")
        self.crate_image = tk.PhotoImage(file="./Assets/crate.png")
        self.goal_image = tk.PhotoImage(file="./Assets/goal.png")
        self.block_image = tk.PhotoImage(file="./Assets/block.png")
        self.switches_pos = ()
        self.speed = 200
        self.file_name = None
        self.W = 0
        self.H = 0
        self.running = False
        self.animation_state = 0

        self.button = tk.Button(
            root, 
            text="Load", 
            command=self.load,
            width=8,
            height=1,
            padx=5, pady=5
        )
        self.button.place(x = sz * 13.1, y = sz * 2.35)
        
        self.button = tk.Button(
            root, 
            text="Start", 
            command=self.start,
            width=8,
            height=2,
            padx=5, pady=5
        )
        self.button.place(x = sz * 12.25, y = sz * 7.25)
        
        self.button = tk.Button(
            root, 
            text="Stop", 
            command=self.stop,
            width=8,
            height=2, 
            padx=5, pady=5
        )
        self.button.place(x = sz * 13.75, y = sz * 7.25)

        self.button = tk.Button(
            root, 
            text="Restart", 
            command=self.restart,
            width=8,
            height=2,
            padx=5, pady=5
        )
        self.button.place(x = sz * 12.25, y = sz * 8.5)
        
        self.button = tk.Button(
            root, 
            text="Quit", 
            command=self.quit,
            width=8,
            height=2,
            padx=5, pady=5
        )
        self.button.place(x = sz * 13.75, y = sz * 8.5)

        self.algorithm_label = tk.Label(root, 
            text="Select Algorithm",
            font=("Arial", 13, "bold"),
            background='gray',
            # width=15,
            # padx=5, pady=5
        )
        self.algorithm_label.place(x=sz * 12.5, y=sz * 0.25)
        self.algorithm_combobox = ttk.Combobox(root, 
            values=["DFS","BFS", "UCS", "A*"],
            state='readonly',
            width=10,
            font=("Arial", 12),
            # padx=5, pady=5
        )
        self.actions = ''
        self.algorithm_combobox.set("select")  # Set default value
        self.algorithm_combobox.place(x=sz * 12 + sz * 3 // 4, y=sz * 0.75)
        self.input_label = tk.Label(root, 
            text="Select Input",
            font=("Arial", 13, "bold"),
            background='gray',
            padx=5, pady=5
        )
        self.input_label.place(x=sz * 12.75, y=sz * 1.25)
        self.input_combobox = ttk.Combobox(root, 
            values=["input-01", "input-02", "input-03", "input-04", "input-06"],
            state='readonly',
            width=10,
            font=("Arial", 12),
            # padx=5, pady=5
        )
        self.input_combobox.set("select")  # Set default value
        self.input_combobox.place(x=sz * 12 + sz * 3 // 4, y=sz * 1.75)
        self.info_label = tk.Label(
            root, 
            text="Steps:\n\nWeight:\n\nNode:\n\nTime:\n\nMemory:",
            font=("Arial", 13),
            background='gray',
            justify="left",
            wraplength=170
        )
        self.info_label.place(x = 12.2 * sz, y = 3.5 * sz)
        self.loading = False

        self.loading_label = tk.Label(
            root,
            text = 'Status: ',
            font=("Arial", 13, "bold"),
            background='gray',
        )
        self.loading_label.place(x = 12.5 * sz, y = 3 * sz)
        self.dots = 0

    def load(self):
        self.file_name = self.input_combobox.get() + '.txt'
        selected_algorithm = self.algorithm_combobox.get()
        if self.file_name == 'select.txt' or selected_algorithm == 'select': return
        self.loading = True
        self.run_loading_animation() 
        task = threading.Thread(target=self.run_algorithm, args=(selected_algorithm,))
        task.start()

    def run_algorithm(self, selected_algorithm):
        if selected_algorithm == 'DFS':
            self.actions, steps, weight, node, time, memory = dfs(self.file_name)
        elif selected_algorithm == 'BFS':
            self.actions, steps, weight, node, time, memory = bfs(self.file_name)
        elif selected_algorithm == 'UCS':
            self.actions, steps, weight, node, time, memory = ucs(self.file_name)
        elif selected_algorithm == 'A*':
            self.actions, steps, weight, node, time, memory = a_star(self.file_name)
        self.root.after(0, self.finish_loading, steps, weight, node, time, memory)

    def finish_loading(self, steps, weight, node, time, memory):
        self.loading = False
        self.dots = 0
        self.display_info(steps, weight, node, time, memory)
        self.restart()
        self.loading_label.config(text="Status: Done!")

    def run_loading_animation(self):
        if self.loading:
            self.loading_label.config(text="Status: Loading" + "." * self.dots)
            self.dots = (self.dots + 1) % 4  
            self.root.after(500, self.run_loading_animation)

    def quit(self):
        exit()
        
    def restart(self):
        if self.file_name is None: return
        matrix = [[]]
        self.clear_map()
        self.W, self.H, player_pos, stones_pos, self.switches_pos, walls_pos = readMap(matrix, self.file_name)
        for i in range(self.H):
            for j in range(self.W):
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
        self.loading_label.config(text="Status: ")

    def clear_map(self):
        for i in range(self.H):
            for j in range(self.W):
                self.drawCell((i, j))

    def start(self):
        if not self.running:
            self.running = True
            self.animate() 
        
    def display_info(self, steps, weight, node, time, memory):
        self.info_label.config(text = f'Steps: {steps}\n \
                                       Weight: {weight}\n \
                                       Node: {node}\n \
                                       Time (ms): {time:.2f}\n \
                                       Memory (MB): {memory / 1e6:.2f}')

    def stop(self):
        self.running = False
        self.loading_label.config(text="Status: Stop")

    def animate(self):
        if self.running:
            self.loading_label.config(text="Status: Running")
            if self.animation_state < len(self.actions):
                self.drawCell(self.player_pos)
                self.player_pos = self.move(self.player_pos, actionsMap.find(self.actions[self.animation_state]))
                self.drawCell(self.player_pos, self.player_image)
                self.animation_state += 1
                self.root.after(self.speed, self.animate)
            else:
                self.loading_label.config(text="Status: Done!")
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

def run():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    run()