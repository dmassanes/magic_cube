import matplotlib.pyplot as plt
import argparse
import cube
import numpy as np

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="MagicCubeMPL main")
    parser.add_argument("-n", dest="n", type=int, required=False, default=cube.DEFAULT_N, help="n")
    parser.add_argument("-rm", dest="rm", type=int, required=False, default=cube.DEFAULT_RANDOM_MOVES, help="amount of random moves when initializing")
    args = parser.parse_args()

    c = cube.MagicCubeMPL(n=args.n, random_moves=args.rm)

    faces = c.get_faces()
    axes = c.get_axes()
    slices = c.get_slices()
    face_neighbors = c.get_face_neighbors()

    # add numbering
    for i, ids in enumerate(np.array(cube.VIEWS)[:, 0]):
        for id in ids.split("-"):
            for idx, face in zip(range(slices[id].start, slices[id].stop), faces[slices[id]]):
                axes[i].text(face[:, 0].mean(), face[:, 1].mean(), face[:, 2].mean(), idx)

    plt.show()
