import tkinter as tk

root = tk.Tk()
root.title("Search Visualization")

# Create a canvas widget
canvas = tk.Canvas(root, width=832, height=640, bg='white')

# # Pack the canvas into the root window
canvas.pack()
root.resizable(False, False)
player_image = tk.PhotoImage(file="./Assets/player.png")
ground_image = tk.PhotoImage(file="./Assets/ground.png")
crate_image = tk.PhotoImage(file="./Assets/crate.png")
goal_image = tk.PhotoImage(file="./Assets/goal.png")
# # Draw something on the canvas
sz = 64
start_x, start_y = 0, 0
for i in range(10):
    for j in range(13):
        # canvas.create_image(32 + sz * j, 32 + sz * i, image=ground_image)
        canvas.create_rectangle(start_x + j * sz,
                                start_y + i * sz,
                                start_x + (j + 1) * sz,
                                start_y + (i + 1) * sz, 
                                        fill='gray')
canvas.create_image(32, 32, image=player_image)
canvas.create_image(32 + 64 * 4, 32 + 64 * 7, image=crate_image)
canvas.create_image(32 + 64 * 6, 32 + 64 * 3, image=goal_image)
root.mainloop()
