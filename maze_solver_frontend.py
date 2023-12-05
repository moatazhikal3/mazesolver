# maze_solver_frontend.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QComboBox, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QPen, QColor
from PyQt6.QtCore import Qt
from maze_solver_backend import generate_maze_iterative, dijkstra, a_star

#display window
class GraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        
    #for viewing purposes of a dense maze
    def wheelEvent(self, event):
        factor = 1.1
        if event.angleDelta().y() > 0:
            self.scale(factor, factor)
        else:
            self.scale(1 / factor, 1 / factor)
            
#load the space to draw the maze
class MazeSolverApp(QMainWindow):
    maze_w = 400
    maze_h = 250
    def __init__(self):
        super().__init__()
        self.initUI()
        
    #UI additatives, buttons and etc.
    def initUI(self):
        # Window setup
        self.setWindowTitle("Maze Solver")
        self.setGeometry(100, 100, 1200, 800)

        # Central Widget and Layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Algorithm Selection Dropdown
        self.algorithm_selection = QComboBox()
        self.algorithm_selection.addItems(["Dijkstra's Algorithm", "A* Algorithm"])
        layout.addWidget(self.algorithm_selection)

        # size Selection Dropdown
        self.size_selection = QComboBox()
        self.size_selection.addItems(["Maze size: 400x250", "Maze size: 150x100", "Maze size: 40x25", "Maze size: 20x10"])
        layout.addWidget(self.size_selection)

        # Maze Generation Button
        self.generate_maze_button = QPushButton("Generate Maze", self)
        self.generate_maze_button.clicked.connect(self.generateMaze)
        layout.addWidget(self.generate_maze_button)

        # Solve Maze Button
        self.solve_maze_button = QPushButton("Solve Maze", self)
        self.solve_maze_button.clicked.connect(self.solveMaze)
        layout.addWidget(self.solve_maze_button)

        # Maze Visualization
        self.scene = QGraphicsScene()
        self.view = GraphicsView(self.scene)
        self.view.setFixedSize(1000, 600)

        #Scrolling mechanism
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        layout.addWidget(self.view)

    #random generation of maze, selection of sizes for better presentation
    def generateMaze(self):
        cur_size = self.size_selection.currentIndex()
        if cur_size == 0:
            #400X250 maze size
            self.maze_w = 400
            self.maze_h = 250
            self.view.resetTransform()
            self.view.scale(1, 1)

        if cur_size == 1:
            #150X100 maze size
            self.maze_w = 150
            self.maze_h = 100
            self.view.resetTransform()
            self.view.scale(2.5, 2.5)

        if cur_size == 2:
            #40X25 maze size
            self.maze_w = 40
            self.maze_h = 25
            self.view.resetTransform()
            self.view.scale(10, 10)

        if cur_size == 3:
            #20X10 maze size
            self.maze_w = 20
            self.maze_h = 10
            self.view.resetTransform()
            self.view.scale(20, 20)

        #after selection, generate and draw the layout of maze in backend
        self.maze = generate_maze_iterative(self.maze_w, self.maze_h)
        self.drawMaze()
        self.drawStartExit()

    #drawing random empty maze, cells in stack from backend will be colored white
    def drawMaze(self):
        cell_size = 2  # size of each cell in the visualization
        self.scene.setSceneRect(0, 0, self.maze_w * cell_size, self.maze_h * cell_size)
        self.scene.clear()
        self.scene.addRect(-cell_size, -cell_size, (self.maze_w+2)*cell_size, (self.maze_h+2)*cell_size, QPen(Qt.GlobalColor.black), QColor(Qt.GlobalColor.black))

        for y in range(self.maze_h):
            for x in range(self.maze_w):
                color = Qt.GlobalColor.white
                if self.maze[y][x] == 1:  # avoid drawing over the edge
                    self.scene.addRect(x * cell_size, y * cell_size, cell_size-1, cell_size-1, QPen(color), QColor(color))
    
    #indicators of start (grey) and end (blue) cells
    def drawStartExit(self):
        cell_size = 2  # size of each cell in the visualization

        # mark the start
        start_x, start_y = (1), (0)  #
        exit_color = Qt.GlobalColor.gray  #
        self.scene.addRect(start_x * cell_size, start_y * cell_size, cell_size-1, cell_size-1, QPen(exit_color),
                           QColor(exit_color))
        # mark the exit
        exit_x, exit_y = (self.maze_w-2), (self.maze_h-1)  # adjust if your exit coordinates are different
        exit_color = Qt.GlobalColor.blue  # exit marked in blue
        self.scene.addRect(exit_x * cell_size, exit_y * cell_size, cell_size-1, cell_size-1, QPen(exit_color),
                           QColor(exit_color))
    #re-generating maze -> clear and re-initalize the maze generation
    def redrawMaze(self):
        cell_size = 2  # size of each cell in the visualization
        self.scene.clear()  # clear the scene first
        for y in range(self.maze_h):
            for x in range(self.maze_w):
                color = Qt.GlobalColor.white if self.maze[y][x] == 0 else Qt.GlobalColor.black
                self.scene.addRect(x * cell_size, y * cell_size, cell_size, cell_size, QPen(color), QColor(color))
    
    # redefines start and end points after generation of maze and calls pathfinding algorithms
    def solveMaze(self):
        self.drawMaze()  # redraw the maze to clear previous paths
        start_point = (1, 0)  # entrance
        end_point = (self.maze_w-2, self.maze_h-1)  # exit
        selected_algorithm = self.algorithm_selection.currentText()

        if selected_algorithm == "Dijkstra's Algorithm":
            self.path, self.all_steps = dijkstra(self.maze, start_point, end_point)
        else:
            self.path, self.all_steps = a_star(self.maze, start_point, end_point)

        self.drawPath()
        self.drawStartExit()
        print(selected_algorithm, "Number of steps:", len(self.all_steps))
        print(selected_algorithm, "Length of path:", len(self.path))
        
    # Given the path from maze_solver_backend, draw paths (green) and steps (red)
    def drawPath(self):
        cell_size = 2  # Adjust as needed
        all_steps_pen = QPen(QColor(255, 0, 0))  # Red color for all steps
        path_pen = QPen(QColor(0, 255, 0))  # Green color for the shortest path
        path_pen.setWidth(1)

        # Draw all steps
        for step in self.all_steps:
            self.scene.addRect(step[0] * cell_size, step[1] * cell_size, cell_size-1, cell_size-1, all_steps_pen)

        # Draw the shortest path
        if self.path:
            last_point = self.path[0]
            for point in self.path[1:]:
                self.scene.addLine(last_point[0] * cell_size, last_point[1] * cell_size,
                                   point[0] * cell_size, point[1] * cell_size, path_pen)
                last_point = point

def main():
    app = QApplication(sys.argv)
    ex = MazeSolverApp()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
