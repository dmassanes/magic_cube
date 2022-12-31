from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
from utils import *

class MagicCubeMPL():

    def __init__(self, n=DEFAULT_N, r=DEFAULT_RANDOM_ROTATIONS, colors=DEFAULT_COLORS, figsize=DEFAULT_FIGSIZE, view_settings=DEFAULT_VIEW_SETTINGS):

        if n < 2 or n > 3:
            raise ValueError("n has to be >= 2 and <= 3")

        # aux vars
        self.__n = n
        self.__nn = n ** 2
        self.__nh = n / 2
        self.__n_faces = 6 * self.__nn
        self.__face_ranges = {
            "U": range(0 * self.__nn, 1 * self.__nn),
            "L": range(1 * self.__nn, 2 * self.__nn),
            "F": range(2 * self.__nn, 3 * self.__nn),
            "D": range(3 * self.__nn, 4 * self.__nn),
            "R": range(4 * self.__nn, 5 * self.__nn),
            "B": range(5 * self.__nn, self.__n_faces)
        }
        
        # face indices (used for the logic)
        self.__face_indices = np.arange(self.__n_faces)

        # face colors
        self.__face_colors = np.zeros((self.__n_faces, 4))
        self.__face_colors[self.__face_ranges["U"]] = colors["U"]
        self.__face_colors[self.__face_ranges["L"]] = colors["L"]
        self.__face_colors[self.__face_ranges["F"]] = colors["F"]
        self.__face_colors[self.__face_ranges["D"]] = colors["D"]
        self.__face_colors[self.__face_ranges["R"]] = colors["R"]
        self.__face_colors[self.__face_ranges["B"]] = colors["B"]

        # face vertices
        self.__face_verts = np.zeros(shape=(self.__n_faces, 4, 3))
        for y in range(n):
            for x in range(n):
                self.__face_verts[y * n + x]            = [ [ y , x , n ] , [ y , x + 1 , n ] , [ y + 1 , x + 1 , n ] , [ y + 1 , x , n ] ] # U
                self.__face_verts[(y + n) * n + x]      = [ [ 0 , y , x ] , [ 0 , y , x + 1 ] , [ 0 , y + 1 , x + 1 ] , [ 0 , y + 1 , x ] ] # L
                self.__face_verts[(y + 2 * n) * n + x]  = [ [ y , 0 , x ] , [ y , 0 , x + 1 ] , [ y + 1 , 0 , x + 1 ] , [ y + 1 , 0 , x ] ] # F
                self.__face_verts[(y + 3 * n) * n + x]  = [ [ y , x , 0 ] , [ y , x + 1 , 0 ] , [ y + 1 , x + 1 , 0 ] , [ y + 1 , x , 0 ] ] # D
                self.__face_verts[(y + 4 * n) * n + x]  = [ [ n , y , x ] , [ n , y , x + 1 ] , [ n , y + 1 , x + 1 ] , [ n , y + 1 , x ] ] # R
                self.__face_verts[(y + 5 * n) * n + x]  = [ [ y , n , x ] , [ y , n , x + 1 ] , [ y + 1 , n , x + 1 ] , [ y + 1 , n , x ] ] # B
        self.__face_verts -= self.__nh

        # set up the rotations
        self.__face_neighbor_indices = {
            "U": # F L B R
                [i for i in range(self.__face_ranges["F"].stop - 1, self.__face_ranges["F"].start, -self.__n)] + \
                [i for i in range(self.__face_ranges["L"].start + self.__n - 1, self.__face_ranges["L"].stop, self.__n)] + \
                [i for i in range(self.__face_ranges["B"].start + self.__n - 1, self.__face_ranges["B"].stop, self.__n)] + \
                [i for i in range(self.__face_ranges["R"].stop - 1, self.__face_ranges["R"].start, -self.__n)],
            "L": # U F D B
                [i for i in range(self.__face_ranges["U"].start + self.__n - 1, self.__face_ranges["U"].start - 1, -1)] + \
                [i for i in range(self.__face_ranges["F"].start + self.__n - 1, self.__face_ranges["F"].start - 1, -1)] + \
                [i for i in range(self.__face_ranges["D"].start, self.__face_ranges["D"].start + self.__n, 1)] + \
                [i for i in range(self.__face_ranges["B"].start, self.__face_ranges["B"].start + self.__n, 1)],
            "F": # U R D L
                [i for i in range(self.__face_ranges["U"].start, self.__face_ranges["U"].stop, self.__n)] + \
                [i for i in range(self.__face_ranges["R"].start + self.__n - 1, self.__face_ranges["R"].start - 1, -1)] + \
                [i for i in range(self.__face_ranges["D"].stop - self.__n, self.__face_ranges["D"].start - 1, -self.__n)] + \
                [i for i in range(self.__face_ranges["L"].start, self.__face_ranges["L"].start + self.__n, 1)],
            "D": # F R B L
                [i for i in range(self.__face_ranges["F"].start, self.__face_ranges["F"].stop, self.__n)] + \
                [i for i in range(self.__face_ranges["R"].start, self.__face_ranges["R"].stop, self.__n)] + \
                [i for i in range(self.__face_ranges["B"].stop - self.__n, self.__face_ranges["B"].start - 1, -self.__n)] + \
                [i for i in range(self.__face_ranges["L"].stop - self.__n, self.__face_ranges["L"].start - 1, -self.__n)],
            "R": # U B D F
                [i for i in range(self.__face_ranges["U"].stop - self.__n, self.__face_ranges["U"].stop, 1)] + \
                [i for i in range(self.__face_ranges["B"].stop - 1, self.__face_ranges["B"].stop - self.__n - 1, -1)] + \
                [i for i in range(self.__face_ranges["D"].stop - 1, self.__face_ranges["D"].stop - self.__n - 1, -1)] + \
                [i for i in range(self.__face_ranges["F"].stop - self.__n, self.__face_ranges["F"].stop, 1)],
            "B": # U L D R
                [i for i in range(self.__face_ranges["U"].stop - 1, self.__face_ranges["U"].start, -self.__n)] + \
                [i for i in range(self.__face_ranges["L"].stop - 1, self.__face_ranges["L"].stop - self.__n - 1, -1)] + \
                [i for i in range(self.__face_ranges["D"].start + self.__n - 1, self.__face_ranges["D"].stop, self.__n)] + \
                [i for i in range(self.__face_ranges["R"].stop - self.__n, self.__face_ranges["R"].stop, 1)],
        }
        self.__rotations = {
            "U": [
                np.concatenate([self.__face_neighbor_indices["U"], self.__face_indices[self.__face_ranges["U"]]]),
                np.concatenate([np.roll(self.__face_neighbor_indices["U"], -self.__n), np.rot90(self.__face_indices[self.__face_ranges["U"]].reshape(n, n), 1).flatten()])
            ],
            "U'": [
                np.concatenate([self.__face_neighbor_indices["U"], self.__face_indices[self.__face_ranges["U"]]]),
                np.concatenate([np.roll(self.__face_neighbor_indices["U"], self.__n), np.rot90(self.__face_indices[self.__face_ranges["U"]].reshape(n, n), 3).flatten()])
            ],
            "L": [
                np.concatenate([self.__face_neighbor_indices["L"], self.__face_indices[self.__face_ranges["L"]]]),
                np.concatenate([np.roll(self.__face_neighbor_indices["L"], -self.__n), np.rot90(self.__face_indices[self.__face_ranges["L"]].reshape(n, n), 3).flatten()])
            ],
            "L'": [
                np.concatenate([self.__face_neighbor_indices["L"], self.__face_indices[self.__face_ranges["L"]]]),
                np.concatenate([np.roll(self.__face_neighbor_indices["L"], self.__n), np.rot90(self.__face_indices[self.__face_ranges["L"]].reshape(n, n), 1).flatten()])
            ],
            "F": [
                np.concatenate([self.__face_neighbor_indices["F"], self.__face_indices[self.__face_ranges["F"]]]),
                np.concatenate([np.roll(self.__face_neighbor_indices["F"], -self.__n), np.rot90(self.__face_indices[self.__face_ranges["F"]].reshape(n, n), 1).flatten()])
            ],
            "F'": [
                np.concatenate([self.__face_neighbor_indices["F"], self.__face_indices[self.__face_ranges["F"]]]),
                np.concatenate([np.roll(self.__face_neighbor_indices["F"], self.__n), np.rot90(self.__face_indices[self.__face_ranges["F"]].reshape(n, n), 3).flatten()])
            ],
            "D": [
                np.concatenate([self.__face_neighbor_indices["D"], self.__face_indices[self.__face_ranges["D"]]]),
                np.concatenate([np.roll(self.__face_neighbor_indices["D"], -self.__n), np.rot90(self.__face_indices[self.__face_ranges["D"]].reshape(n, n), 3).flatten()])
            ],
            "D'": [
                np.concatenate([self.__face_neighbor_indices["D"], self.__face_indices[self.__face_ranges["D"]]]),
                np.concatenate([np.roll(self.__face_neighbor_indices["D"], self.__n), np.rot90(self.__face_indices[self.__face_ranges["D"]].reshape(n, n), 1).flatten()])
            ],
            "R": [
                np.concatenate([self.__face_neighbor_indices["R"], self.__face_indices[self.__face_ranges["R"]]]),
                np.concatenate([np.roll(self.__face_neighbor_indices["R"], -self.__n), np.rot90(self.__face_indices[self.__face_ranges["R"]].reshape(n, n), 1).flatten()])
            ],
            "R'": [
                np.concatenate([self.__face_neighbor_indices["R"], self.__face_indices[self.__face_ranges["R"]]]),
                np.concatenate([np.roll(self.__face_neighbor_indices["R"], self.__n), np.rot90(self.__face_indices[self.__face_ranges["R"]].reshape(n, n), 3).flatten()])
            ],
            "B": [
                np.concatenate([self.__face_neighbor_indices["B"], self.__face_indices[self.__face_ranges["B"]]]),
                np.concatenate([np.roll(self.__face_neighbor_indices["B"], -self.__n), np.rot90(self.__face_indices[self.__face_ranges["B"]].reshape(n, n), 3).flatten()])
            ],
            "B'": [
                np.concatenate([self.__face_neighbor_indices["B"], self.__face_indices[self.__face_ranges["B"]]]),
                np.concatenate([np.roll(self.__face_neighbor_indices["B"], self.__n), np.rot90(self.__face_indices[self.__face_ranges["B"]].reshape(n, n), 1).flatten()])
            ]
        }

        # set up the figure and axes
        self.__figure = plt.figure(figsize=figsize)
        def __init_ax(pos, xyzlim, collection, box_aspect, view):
            ax = self.__figure.add_subplot(pos, projection="3d")
            ax.add_collection(collection)
            ax.set(title=view["title"], xlim =xyzlim, ylim =xyzlim, zlim =xyzlim)
            ax.set_box_aspect(box_aspect)
            ax.set_axis_off()
            if view["disable_mouse_rotation"]:
                ax.disable_mouse_rotation()
            ax.view_init(view["elev"], view["azim"])
            return ax
        xyzlim = (-n / 2 - 0.1, n / 2 + 0.1)
        box_aspect = (np.ptp(self.__face_verts[:,:,0]), np.ptp(self.__face_verts[:,:,1]), np.ptp(self.__face_verts[:,:,2]))
        self.__view_settings = view_settings
        self.__axes = [
            __init_ax(
                int(view_settings["gridspec"] + str(i + 1)),
                xyzlim,
                Poly3DCollection(verts=self.__face_verts, facecolors=self.__face_colors, edgecolors="black"),
                box_aspect,
                view
            )
            for i, view in enumerate(self.__view_settings["views"])
        ]

        # randomly rotate the cube
        for rot in np.random.choice(list(self.__rotations.keys()), r):
            self.__rotate(rot)
        
        # init the key events
        def __key_press_event(event):
            if event.key == "8" or event.key == "u":
                self.__rotate("U")
            elif event.key == "shift+up" or event.key == "U":
                self.__rotate("U'")
            elif event.key == "4" or event.key == "l":
                self.__rotate("L")
            elif event.key == "shift+left" or event.key == "L":
                self.__rotate("L'")
            elif event.key == "7" or event.key == "f":
                self.__rotate("F")
            elif event.key == "shift+home" or event.key == "F":
                self.__rotate("F'")
            elif event.key == "5" or event.key == "d":
                self.__rotate("D")
            elif event.key == "shift+clear" or event.key == "D":
                self.__rotate("D'")
            elif event.key == "6" or event.key == "r":
                self.__rotate("R")
            elif event.key == "shift+right" or event.key == "R":
                self.__rotate("R'")
            elif event.key == "9" or event.key == "b":
                self.__rotate("B")
            elif event.key == "shift+pageup" or event.key == "B":
                self.__rotate("B'")
        self.__figure.canvas.mpl_connect("key_press_event", __key_press_event)
        plt.rcParams["keymap.fullscreen"].remove("f")
        plt.rcParams["keymap.home"].remove("r")
        plt.rcParams["keymap.xscale"].remove("L")
        plt.rcParams["keymap.yscale"].remove("l")

    def __update_axes(self):
        for ax in self.__axes:
            ax.collections[0].set_facecolors(self.__face_colors)
        self.__figure.canvas.draw_idle()

    def __rotate(self, rot):
        self.__face_indices[self.__rotations[rot][0]], self.__face_indices[self.__rotations[rot][1]] = self.__face_indices[self.__rotations[rot][1]], self.__face_indices[self.__rotations[rot][0]]
        self.__face_colors[self.__rotations[rot][0]], self.__face_colors[self.__rotations[rot][1]] = self.__face_colors[self.__rotations[rot][1]], self.__face_colors[self.__rotations[rot][0]]
        self.__update_axes()

if __name__ == "__main__":

    parser = arg_parser()
    args = parser.parse_args()

    cube = MagicCubeMPL(n=args.n, r=args.r)

    plt.show()
