# Magic Cube

Start by running

```
python3 cube_mpl.py
```

Usage:

```
usage: cube_mpl.py [-h] [-n N] [-r R]

MagicCubeMPL

optional arguments:
  -h, --help  show this help message and exit
  -n N        cube size (only 2 or 3 are supported yet)
  -r R        amount of random rotations when initializing
```

![Eight Views 3](other/eight_views_3.png)

![Eight Views 3 Randomized](other/eight_views_3_rand.png)

![Eight Views 2](other/eight_views_2.png)

![Eight Views 2 Randomized](other/eight_views_2_rand.png)

# TODO
- implement solver
- allow n >= 4 and implement rotations for the mids (n >= 3)
