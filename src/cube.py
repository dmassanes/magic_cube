from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import to_rgba
from scipy.spatial.transform import Rotation
import matplotlib.pyplot as plt
import numpy as np


GREEN   = "#009b48"
BLUE    = "#0046ad"
RED     = "#b71234"
ORANGE  = "#ff5800"
YELLOW  = "#ffd500"
WHITE   = "#ffffff"

VIEWS = [
    ("U-F-R", 30, -60),
    ("U-R-B", 30, 30),
    ("U-B-L", 30, 120),
    ("U-L-F", 30, 210),
    ("D-L-B", 210, -30),
    ("D-F-L", 210, 60),
    ("D-R-F", 210, 150),
    ("D-B-R", 210, 240)
]

DEFAULT_N = 3
DEFAULT_RANDOM_MOVES = 50
DFEAULT_FIGSIZE = (20, 10)

ROT_XP = Rotation.from_euler("xyz", [90, 0, 0], degrees=True)
ROT_XN = Rotation.from_euler("xyz", [-90, 0, 0], degrees=True)
ROT_YP = Rotation.from_euler("xyz", [0, 90, 0], degrees=True)
ROT_YN = Rotation.from_euler("xyz", [0, -90, 0], degrees=True)
ROT_ZP = Rotation.from_euler("xyz", [0, 0, 90], degrees=True)
ROT_ZN = Rotation.from_euler("xyz", [0, 0, -90], degrees=True)

MOVES = {
    "L"     : ROT_XP,
    "R"     : ROT_XN,
    "F"     : ROT_YP,
    "B"     : ROT_YN,
    "D"     : ROT_ZP,
    "U"     : ROT_ZN,
    "L'"    : ROT_XN,
    "R'"    : ROT_XP,
    "F'"    : ROT_YN,
    "B'"    : ROT_YP,
    "D'"    : ROT_ZN,
    "U'"    : ROT_ZP
}

class MagicCubeMPL():
    def __init__(self, n=DEFAULT_N, random_moves=DEFAULT_RANDOM_MOVES, figsize=DFEAULT_FIGSIZE) -> None:
        if n < 2 or n > 3:
            raise ValueError("n has to be >= 2 and <= 3")
        self.__n = n
        self.__nn = n ** 2
        self.__face_slices = {
            "L": slice(0 * self.__nn, 1 * self.__nn),
            "R": slice(1 * self.__nn, 2 * self.__nn),
            "F": slice(2 * self.__nn, 3 * self.__nn),
            "B": slice(3 * self.__nn, 4 * self.__nn),
            "D": slice(4 * self.__nn, 5 * self.__nn),
            "U": slice(5 * self.__nn, 6 * self.__nn)
        }
        self.__face_neighbors = {
            "L":
                [i for i in range(self.__face_slices["F"].start, self.__face_slices["F"].start + self.__n, 1)] + \
                [i for i in range(self.__face_slices["B"].start, self.__face_slices["B"].start + self.__n, 1)] + \
                [i for i in range(self.__face_slices["D"].start, self.__face_slices["D"].start + self.__n, 1)] + \
                [i for i in range(self.__face_slices["U"].start, self.__face_slices["U"].start + self.__n, 1)],
            "R":
                [i for i in range(self.__face_slices["F"].stop - 1, self.__face_slices["F"].stop - self.__n - 1, -1)] + \
                [i for i in range(self.__face_slices["B"].stop - 1, self.__face_slices["B"].stop - self.__n - 1, -1)] + \
                [i for i in range(self.__face_slices["D"].stop - 1, self.__face_slices["D"].stop - self.__n - 1, -1)] + \
                [i for i in range(self.__face_slices["U"].stop - 1, self.__face_slices["U"].stop - self.__n - 1, -1)],
            "F":
                [i for i in range(self.__face_slices["L"].start, self.__face_slices["L"].start + self.__n, 1)] + \
                [i for i in range(self.__face_slices["R"].start, self.__face_slices["R"].start + self.__n, 1)] + \
                [i for i in range(self.__face_slices["D"].start, self.__face_slices["D"].start + self.__nn, self.__n)] + \
                [i for i in range(self.__face_slices["U"].start, self.__face_slices["U"].start + self.__nn, self.__n)],
            "B":
                [i for i in range(self.__face_slices["L"].stop - 1, self.__face_slices["L"].stop - self.__n - 1, -1)] + \
                [i for i in range(self.__face_slices["R"].stop - 1, self.__face_slices["R"].stop - self.__n - 1, -1)] + \
                [i for i in range(self.__face_slices["D"].stop - 1, self.__face_slices["D"].stop - self.__nn - 1, -self.__n)] + \
                [i for i in range(self.__face_slices["U"].stop - 1, self.__face_slices["U"].stop - self.__nn - 1, -self.__n)],
            "D":
                [i for i in range(self.__face_slices["L"].start, self.__face_slices["L"].start + self.__nn, self.__n)] + \
                [i for i in range(self.__face_slices["R"].start, self.__face_slices["R"].start + self.__nn, self.__n)] + \
                [i for i in range(self.__face_slices["F"].start, self.__face_slices["F"].start + self.__nn, self.__n)] + \
                [i for i in range(self.__face_slices["B"].start, self.__face_slices["B"].start + self.__nn, self.__n)],
            "U":
                [i for i in range(self.__face_slices["L"].stop - 1, self.__face_slices["L"].stop - self.__nn - 1, -self.__n)] + \
                [i for i in range(self.__face_slices["R"].stop - 1, self.__face_slices["R"].stop - self.__nn - 1, -self.__n)] + \
                [i for i in range(self.__face_slices["F"].stop - 1, self.__face_slices["F"].stop - self.__nn - 1, -self.__n)] + \
                [i for i in range(self.__face_slices["B"].stop - 1, self.__face_slices["B"].stop - self.__nn - 1, -self.__n)],
        }
        self.__figure = plt.figure(figsize=figsize)
        self.__init_faces()
        self.__init_facecolors()
        self.__init_axes()
        self.__init_key_events()
        for m in np.random.choice(list(MOVES.keys()), random_moves):
            self.move(m)

    def __init_faces(self):
        n = self.__n
        nn = self.__nn
        self.__faces = np.zeros(shape=(6 * nn, 4, 3))
        for i in range(n):
            for j in range(n):
                self.__faces[i * n + j]            = [ [ 0 , i , j ] , [ 0 , i , j + 1 ] , [ 0 , i + 1 , j + 1 ] , [ 0 , i + 1 , j ] ]  # left
                self.__faces[(i + n) * n + j]      = [ [ n , i , j ] , [ n , i , j + 1 ] , [ n , i + 1 , j + 1 ] , [ n , i + 1 , j ] ]  # right
                self.__faces[(i + 2 * n) * n + j]  = [ [ i , 0 , j ] , [ i , 0 , j + 1 ] , [ i + 1 , 0 , j + 1 ] , [ i + 1 , 0 , j ] ]  # front
                self.__faces[(i + 3 * n) * n + j]  = [ [ i , n , j ] , [ i , n , j + 1 ] , [ i + 1 , n , j + 1 ] , [ i + 1 , n , j ] ]  # back
                self.__faces[(i + 4 * n) * n + j]  = [ [ i , j , 0 ] , [ i , j + 1 , 0 ] , [ i + 1 , j + 1 , 0 ] , [ i + 1 , j , 0 ] ]  # down
                self.__faces[(i + 5 * n) * n + j]  = [ [ i , j , n ] , [ i , j + 1 , n ] , [ i + 1 , j + 1 , n ] , [ i + 1 , j , n ] ]  # up
        self.__faces -= n / 2

    def __init_facecolors(self):
        nn = self.__nn
        self.__facecolors = np.zeros(shape=(6 * nn, 4))
        self.__facecolors[self.__face_slices["L"]] = to_rgba(GREEN)  # left
        self.__facecolors[self.__face_slices["R"]] = to_rgba(BLUE)   # right
        self.__facecolors[self.__face_slices["F"]] = to_rgba(RED)    # front
        self.__facecolors[self.__face_slices["B"]] = to_rgba(ORANGE) # back
        self.__facecolors[self.__face_slices["D"]] = to_rgba(YELLOW) # down
        self.__facecolors[self.__face_slices["U"]] = to_rgba(WHITE)  # up

    def __init_axes(self):
        def __init_ax(pos, xyzlim, collection, box_aspect, title, elev, azim):
            ax = self.__figure.add_subplot(pos, projection="3d")
            ax.add_collection(collection)
            ax.set(title=title, xlim =xyzlim, ylim =xyzlim, zlim =xyzlim)
            ax.set_box_aspect(box_aspect)
            ax.set_axis_off()
            ax.disable_mouse_rotation()
            ax.view_init(elev, azim)
            return ax
        n = self.__n
        xyzlim = (-n / 2 - 0.1, n / 2 + 0.1)
        box_aspect = (np.ptp(self.__faces[:,:,0]), np.ptp(self.__faces[:,:,1]), np.ptp(self.__faces[:,:,2]))
        self.__axes = [
            __init_ax(
                int("24" + str(i + 1)),
                xyzlim,
                Poly3DCollection(verts=self.__faces, facecolors=self.__facecolors, edgecolors="black"),
                box_aspect,
                *view
            )
            for i, view in enumerate(VIEWS)
        ]

    def __init_key_events(self):
        def __key_press_event(event):
            if event.key == "4" or event.key == "l":
                self.move("L")
            elif event.key == "shift+left" or event.key == "L":
                self.move("L'")
            elif event.key == "6" or event.key == "r":
                self.move("R")
            elif event.key == "shift+right" or event.key == "R":
                self.move("R'")
            elif event.key == "7" or event.key == "f":
                self.move("F")
            elif event.key == "shift+home" or event.key == "F":
                self.move("F'")
            elif event.key == "9" or event.key == "b":
                self.move("B")
            elif event.key == "shift+pageup" or event.key == "B":
                self.move("B'")
            elif event.key == "5" or event.key == "d":
                self.move("D")
            elif event.key == "shift+clear" or event.key == "D":
                self.move("D'")
            elif event.key == "8" or event.key == "u":
                self.move("U")
            elif event.key == "shift+up" or event.key == "U":
                self.move("U'")
        self.__figure.canvas.mpl_connect("key_press_event", __key_press_event)
        plt.rcParams["keymap.fullscreen"].remove("f")
        plt.rcParams["keymap.home"].remove("r")
        plt.rcParams["keymap.xscale"].remove("L")
        plt.rcParams["keymap.yscale"].remove("l")

    def get_figure(self):
        return self.__figure

    def get_axes(self):
        return self.__axes

    def get_faces(self):
        return self.__faces

    def get_facecolors(self):
        return self.__facecolors

    def get_n(self):
        return self.__n

    def get_nn(self):
        return self.__nn
    
    def get_slices(self):
        return self.__face_slices

    def get_face_neighbors(self):
        return self.__face_neighbors

    def move(self, m):
        for idx in list(range(self.__face_slices[m[0]].start, self.__face_slices[m[0]].stop)) + \
                    self.__face_neighbors[m[0]]:
            self.__faces[idx] = np.round(MOVES[m].apply(self.__faces[idx]), 3)
        for ax in self.__axes:
            ax.collections[0].set_verts(self.__faces)
        self.__figure.canvas.draw_idle()

    def solve(self):
        pass

