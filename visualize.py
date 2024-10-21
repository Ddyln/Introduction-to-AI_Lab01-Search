import tkinter as tk
import time as TIME

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
    return player_pos, stones_pos, switches_pos, walls_pos

file_name = 'input-01.txt'
matrix = [[]]
player_pos, stones_pos, switches_pos, walls_pos = readMap(matrix, file_name)
actions = 'rUruLLddlluRRuulDrdLrurDllulDrdrRRRRRR'

class CanvasDemo:
    def __init__(self, root):
        self.root = root
        self.width = 64 * 14
        self.height = 64 * 10
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='white')
        self.root.resizable(False, False)
        self.canvas.pack()
        self.root.title("Search Visualization")
        self.player_image = tk.PhotoImage(file="./Assets/player.png")
        self.ground_image = tk.PhotoImage(file="./Assets/ground.png")
        self.crate_image = tk.PhotoImage(file="./Assets/crate.png")
        self.goal_image = tk.PhotoImage(file="./Assets/goal.png")
        self.block_image = tk.PhotoImage(file="./Assets/block.png")
        for i in range(self.height // sz):
            for j in range(self.width // sz):
                self.root.after(10, lambda pos=(j,i): self.drawCell(pos))
        # print(player_pos)
        self.root.after(20, lambda: self.drawCell(player_pos, self.player_image))
        for i in stones_pos:
            self.root.after(20, lambda pos=i: self.drawCell(pos, self.crate_image))
        for i in switches_pos:
            self.root.after(20, lambda pos=i: self.drawCell(pos, self.goal_image))
        for i in walls_pos:
            self.root.after(20, lambda pos=i: self.drawCell(pos, self.block_image))

    
        self.button = tk.Button(
            root, 
            text="Click Me", 
            command=self.change_text,
            width=4,
            height=2
        )
        self.button.place(x = sz * 13, y = sz * 5)

    def change_text(self):
        for c in actions:
            print(c)
            TIME.sleep(1)
        # self.label.config(text="Button clicked! The text has changed.")
        
    def drawCell(self, coordinate, image = None):
        y = coordinate[0]
        x = coordinate[1]
        if image is None:
            self.canvas.create_rectangle(start_x + y * sz,
                                    start_y + x * sz,
                                    start_x + (y + 1) * sz,
                                    start_y + (x + 1) * sz, 
                                    fill='gray')
        else:
            self.canvas.create_image(sz // 2 + sz * x, sz // 2 + sz * y, image=image)


if __name__ == "__main__":
    root = tk.Tk()
    app = CanvasDemo(root)
    root.mainloop()