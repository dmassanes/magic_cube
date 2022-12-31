import matplotlib.pyplot as plt
import argparse
from cube_mpl import *

if __name__ == "__main__":

    parser = arg_parser()
    args = parser.parse_args()

    cube = MagicCubeMPL(n=args.n, r=args.r)

    face_ranges = cube._MagicCubeMPL__face_ranges
    face_colors = cube._MagicCubeMPL__face_colors
    face_verts = cube._MagicCubeMPL__face_verts

    for i, d in enumerate(cube._MagicCubeMPL__view_settings["views"]):
        for id in d["title"].split("-"):
            for idx, verts in zip(face_ranges[id], face_verts[face_ranges[id]]):
                cube._MagicCubeMPL__axes[i].text(verts[:, 0].mean(), verts[:, 1].mean(), verts[:, 2].mean(), idx)

    plt.show()
