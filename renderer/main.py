import pygame 
import numpy as np
import math
pygame.init() 

W = 500
H = 500
# CREATING CANVAS 
canvas = pygame.display.set_mode((W, H)) 

"""
class vertex:
	def __init__(self, x,y,z):
		self.pos = (x, y, z)
		
class traiangle:
	def __init__(self, veretx1 : vertex, veretx2 : vertex, veretx3 : vertex):
		self.vertisies = [veretx1, veretx2, veretx3]
		
class mesh:
    def __init__(self, traiangels: list[traiangle]):
        self.tiles = traiangels
"""

Zn = 0.1
Zf = 1000
FOV = 90


mesh = [
    # SOUTH
        [[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]],
        [[0.0, 0.0, 0.0], [1.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
    # EAST
        [[1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [1.0, 1.0, 1.0]],
        [[1.0, 0.0, 0.0], [1.0, 1.0, 1.0], [1.0, 0.0, 1.0]],
    # NORTH
        [[1.0, 0.0, 1.0], [1.0, 1.0, 1.0], [0.0, 1.0, 1.0]],
        [[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [0.0, 0.0, 1.0]],
    # WEST
        [[0.0, 0.0, 1.0], [0.0, 1.0, 1.0], [0.0, 1.0, 0.0]],
        [[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [0.0, 0.0, 0.0]],
    # TOP
        [[0.0, 1.0, 0.0], [0.0, 1.0, 1.0], [1.0, 1.0, 1.0]],
        [[0.0, 1.0, 0.0], [1.0, 1.0, 1.0], [1.0, 1.0, 0.0]],
    # BOTTOM
        [[1.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0]],
        [[1.0, 0.0, 1.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
]



a = W/H
f = 1/math.tan(math.radians(FOV/2))
q = Zf / (Zf - Zn)


projectiom_matrix = [
    [a*f, 0, 0, 0],
    [0, f, 0, 0],
    [0,0,q,1],
    [0,0,-Zn*q,0]
]


# TITLE OF CANVAS
# # Define two 2D arrays

# Perform matrix multiplication
#result = 

#print(result) 

pygame.display.set_caption("My Board") 
camera = [0,0,0]
exit = False
angle_x = 0
angle_z = 0
angle_y = 0
center = H/2
scale = 150
while not exit: 
    canvas.fill((0,0,1))
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True
    #translation (rotation)

 
    rotation_x = np.matrix([
            [1, 0, 0],
            [0, math.cos(angle_x), -math.sin(angle_x)],
            [0, math.sin(angle_x), math.cos(angle_x)],
    ])

    rotation_y = np.matrix([
            [math.cos(angle_y), 0, math.sin(angle_y)],
            [0, 1, 0],
            [-math.sin(angle_y), 0, math.cos(angle_y)],
        ])

    rotation_z = np.matrix([
            [math.cos(angle_z), -math.sin(angle_z), 0],
            [math.sin(angle_z), math.cos(angle_z), 0],
            [0, 0, 1],
        ])
    rotated_mesh = []
    for index, triangle in enumerate(mesh):
        rotated_mesh.append([])
        for vertext in triangle:
            print(vertext)
            roteted_vetrex = np.matmul(vertext, rotation_x)
            roteted_vetrex = np.matmul(roteted_vetrex, rotation_y)
            roteted_vetrex = np.matmul(roteted_vetrex, rotation_z) 
            rotated_mesh[index].append(roteted_vetrex.tolist()[0])
    angle_x += 0.001
    angle_z += 0.000
    angle_y += 0.000
    #projection    
    for face in rotated_mesh:
        triangle = []
        line1 = [face[1][0]-face[0][0], face[1][1]-face[0][1], face[1][2]-face[0][2]]
        line2 = [face[2][0]-face[0][0], face[2][1]-face[0][1], face[2][2]-face[0][2]]

        normal = [
            (line1[1] * line2[2]) - (line1[2] * line2[1]),
            (line1[2] * line2[0]) - (line1[0] * line2[2]),
            (line1[0] * line2[1]) - (line1[1] * line2[0])
                  ]
        
        l = math.sqrt(normal[0]*normal[0] + normal[1]*normal[1] + normal[2]*normal[2])
        normal[0] /= l
        normal[1] /= l
        normal[2] /= l
        dot = (normal[0] * (face[0][0]- camera[0])) + (normal[1] * (face[0][1]- camera[1])) + (normal[2] * (face[0][2]- camera[2]))
        if normal[2] > 0:
            for verticy in face:
                v = verticy
                triangle.append(np.matmul(v+[1], projectiom_matrix)[:2])
            pygame.draw.polygon(canvas, (255, 0, 0), [triangle[0]*scale+center, triangle[1]*scale+center, triangle[2]*scale+center], 1)
    
    pygame.display.update() 
