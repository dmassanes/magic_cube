from cube_mpl import *
from utils import *

if __name__ == "__main__":
    parser = arg_parser()
    args = parser.parse_args()

    view_settings = {
        "gridspec": "11",
        "views": [
            {"title": "Single view", "elev": 30, "azim": -60, "disable_mouse_rotation": False, "face_ids": list(DEFAULT_COLORS.keys())},
        ]
    }
    figsize = (10, 10)

    cube = MagicCubeMPL(n=args.n, r=args.r, figsize=figsize, view_settings=view_settings)

    ax = cube._MagicCubeMPL__axes[0]
    face_ranges = cube._MagicCubeMPL__face_ranges
    face_verts = cube._MagicCubeMPL__face_verts
    nn = cube._MagicCubeMPL__nn
    for id, range in face_ranges.items():
        verts = face_verts[range.start + nn // 2]
        ax.text(verts[:, 0].mean(), verts[:, 1].mean(), verts[:, 2].mean(), id)

    plt.show()
