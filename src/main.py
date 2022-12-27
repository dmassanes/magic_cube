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

    plt.show()
