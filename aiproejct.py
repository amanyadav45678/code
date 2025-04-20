import tkinter as tk
import heapq

# -----------------------------
# Grid Configuration
# -----------------------------
grid = [
    ['S', '.', '.', '#', 'C'],
    ['.', '#', '.', '.', '.'],
    ['.', '#', '.', '#', '.'],
    ['.', '.', '.', '#', 'I'],
    ['#', '#', '.', '.', '.']
]

start = (0, 0)
command_center = (0, 4)
intruder = (3, 4)

rows, cols = len(grid), len(grid[0])

# -----------------------------
# Utility Functions
# -----------------------------
def is_valid(x, y):
    return 0 <= x < rows and 0 <= y < cols and grid[x][y] != '#'

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# -----------------------------
# DFS Algorithm
# -----------------------------
def dfs(x, y, visited, canvas, cell_size):
    if not is_valid(x, y) or (x, y) in visited:
        return
    visited.add((x, y))
    draw_cell(canvas, x, y, "yellow", cell_size)
    canvas.update()
    canvas.after(150)
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        dfs(x+dx, y+dy, visited, canvas, cell_size)

# -----------------------------
# Best First Search
# -----------------------------
def best_first_search(start, goal, canvas, cell_size):
    visited = set()
    heap = [(heuristic(start, goal), start)]
    came_from = {start: None}

    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            break
        if current in visited:
            continue
        visited.add(current)
        draw_cell(canvas, current[0], current[1], "orange", cell_size)
        canvas.update()
        canvas.after(100)

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = current[0]+dx, current[1]+dy
            if is_valid(nx, ny) and (nx, ny) not in visited:
                heapq.heappush(heap, (heuristic((nx, ny), goal), (nx, ny)))
                came_from[(nx, ny)] = current

    path = []
    node = goal
    while node:
        path.append(node)
        node = came_from.get(node)
    path.reverse()
    return path

# -----------------------------
# Minimax Decision
# -----------------------------
def minimax(depth, is_bot_turn, risk_attack=30, risk_report=10):
    if depth == 0:
        return -risk_attack if is_bot_turn else -risk_report
    if is_bot_turn:
        return max(minimax(depth-1, False, risk_attack, risk_report),
                   minimax(depth-1, False, risk_attack, risk_report))
    else:
        return min(minimax(depth-1, True, risk_attack, risk_report),
                   minimax(depth-1, True, risk_attack, risk_report))

# -----------------------------
# UI Drawing
# -----------------------------
def draw_grid(canvas, cell_size):
    for i in range(rows):
        for j in range(cols):
            color = "white"
            if grid[i][j] == '#':
                color = "black"
            elif grid[i][j] == 'S':
                color = "blue"
            elif grid[i][j] == 'C':
                color = "green"
            elif grid[i][j] == 'I':
                color = "red"
            draw_cell(canvas, i, j, color, cell_size)

def draw_cell(canvas, i, j, color, cell_size):
    x1 = j * cell_size
    y1 = i * cell_size
    x2 = x1 + cell_size
    y2 = y1 + cell_size
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

# -----------------------------
# Main Execution with UI
# -----------------------------
def run_bot(canvas, label, cell_size):
    draw_grid(canvas, cell_size)
    
    # DFS Patrol
    visited = set()
    dfs(start[0], start[1], visited, canvas, cell_size)

    # Best First Search Path to Intruder
    path = best_first_search(start, intruder, canvas, cell_size)
    for x, y in path:
        draw_cell(canvas, x, y, "lightblue", cell_size)
        canvas.update()
        canvas.after(100)

    # Minimax Decision
    decision_score = minimax(depth=2, is_bot_turn=True)
    decision = "ATTACK!" if decision_score == -30 else "REPORT!"
    label.config(text=f"Decision: Bot chooses to {decision}", font=("Arial", 16), fg="darkgreen")

# -----------------------------
# Tkinter UI Setup
# -----------------------------
def start_ui():
    root = tk.Tk()
    root.title("AI Security Bot Simulation")

    cell_size = 80
    canvas = tk.Canvas(root, width=cols*cell_size, height=rows*cell_size)
    canvas.pack()

    decision_label = tk.Label(root, text="Decision: ", font=("Arial", 14))
    decision_label.pack(pady=10)

    start_button = tk.Button(root, text="Run AI Bot", command=lambda: run_bot(canvas, decision_label, cell_size),
                             font=("Arial", 12), bg="blue", fg="white")
    start_button.pack(pady=10)

    root.mainloop()

# Run the UI
if __name__ == "__main__":
    start_ui()
