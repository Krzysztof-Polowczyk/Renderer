import math
tile_size = 32

rows = 15
cols = 10
window_height = cols * tile_size
window_widht = rows * tile_size

FOV = math.radians(60)

RES = 4
NUM_RAYS = window_widht // RES