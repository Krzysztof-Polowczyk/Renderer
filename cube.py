import pygame as pg
import numpy as np
from math import * 
 

#jak widać ściana czerwona jest zawsze z przodu
# jest to problem
#...
pg.init()
clock = pg.time.Clock()
wight = 1000
height = 800
scale = 100
running = True
window = pg.display.set_mode((wight, height))
window.fill((255, 255, 255))
points = []
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1,  1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))
 
angle = 0
colors = [(200,0,0), (0,0,200), (0,200,0)]




transwformation_matrix = np.matrix([
    [1,0,0],
    [0,1,0],
])
 


faces = [
    ({4,5,6}, 1),
    ({4,7,6}, 2),
    ({0,2,3},0),
    ({0,2,1},2),

    ]
def rotate(angle_z,angle_y,angle_x):
    for index, point in enumerate(points):
        rotation_z = np.matrix([
            [cos(angle_z), -sin(angle_z), 0],
            [sin(angle_z), cos(angle_z), 0],
            [0, 0, 1],
        ])

        rotation_y = np.matrix([
            [cos(angle_y), 0, sin(angle_y)],
            [0, 1, 0],
            [-sin(angle_y), 0, cos(angle_y)],
        ])

        rotation_x = np.matrix([
            [1, 0, 0],
            [0, cos(angle_x), -sin(angle_x)],
            [0, sin(angle_x), cos(angle_x)],
        ])



        rotated_point = np.dot(rotation_z, point.reshape(3,1))
        rotated_point = np.dot(rotation_x, rotated_point)
        rotated_point = np.dot(rotation_y, rotated_point)

        points[index] = rotated_point

def transform(rotated_point):
    point_2D = np.dot(transwformation_matrix, rotated_point.reshape(3,1))
    x = int(point_2D[1][0] * scale) + wight/2
    y = int(point_2D[0][0] * scale) + height/2
    return [x,y]



while running:
    clock.tick(60)
    window.fill((255, 255, 255))
    for e in pg.event.get():

        if e.type == pg.QUIT:
            running = False
    #end event handling

    
    for index, point in enumerate(points):
        pg.draw.circle(window, (0,0,0), transform(point), 3)
    for face in faces:
        tile = []
        for point in face[0]:
            tile.append(transform(points[point]))      

        pg.draw.polygon(window,colors[face[1]], tile)
    rotate(0,0.01,0)
    pg.display.flip()

#end main loop
pg.quit()