import pygame 
import math
import numpy as np
import copy

class point:
    def __init__(self, x,y,z) -> None:
        self.x = x
        self.y = y
        self.z = z
class triangle:
    def __init__(self, p) -> None:
        p1,p2,p3 = p
        self.points = [
            point(p1[0], p1[1], p1[2]), 
            point(p2[0], p2[1], p2[2]), 
            point(p3[0], p3[1], p3[2])
        ]
class mesh:
    def __init__(self, *tris) -> None:
        self.triangles = []
        for tri in tris:
            self.triangles.append(triangle(tri))

H = 800
W = 800
FOV = 90

Zn = 0.1
Zf = 1000

a = W/H
f = 1/math.tan(math.radians(FOV/2))
q = Zf / (Zf - Zn)

def miltiply_matrix(i, m):
    o = point(0,0,0)
    o.x = (i.x * m[0][0]) + (i.y * m[1][0]) + (i.z * m[2][0]) + m[3][0]
    o.y = (i.x * m[0][1]) + (i.y * m[1][1]) + (i.z * m[2][1]) + m[3][1]
    o.z = (i.x * m[0][2]) + (i.y * m[1][2]) + (i.z * m[2][2]) + m[3][2]
    w  =  (i.x * m[0][3]) + (i.y * m[1][3]) + (i.z * m[2][3]) + m[3][3]

    if w != 0.0:
        o.x /= w; o.y /= w; o.z /= w

    return o

projectiom_matrix = [
    [a*f, 0, 0, 0],
    [0, f, 0, 0],
    [0,0,q,1],
    [0,0,-Zn*q,0]
]

cube_mesh = mesh(
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
)

  
pygame.init() 

# CREATING CANVAS 
canvas = pygame.display.set_mode((W, W)) 
  
# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 
exit = False

fTheta = 0 
camera = point(0,0,0)
light_direction = point(0,0,-1)

while not exit: 
    canvas.fill((0,0,1))

    fTheta += 0.001
    matRotZ = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
    ]
    matRotX = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
    ]
    #Rotation Z
    matRotZ[0][0] = math.cos(fTheta)
    matRotZ[0][1] = math.sin(fTheta)
    matRotZ[1][0] = -math.sin(fTheta)
    matRotZ[1][1] = math.cos(fTheta)
    matRotZ[2][2] = 1
    matRotZ[3][3] = 1

    # Rotation X
    matRotX[0][0] = 1
    matRotX[1][1] = math.cos(fTheta * 0.5)
    matRotX[1][2] = math.sin(fTheta * 0.5)
    matRotX[2][1] = -math.sin(fTheta * 0.5)
    matRotX[2][2] = math.cos(fTheta * 0.5)
    matRotX[3][3] = 1
    
    #project 
    for tri in cube_mesh.triangles:
        triRotatedZ = triangle([[0,0,0],[0,0,0],[0,0,0]])

        triRotatedZ.points[0] = miltiply_matrix(tri.points[0], matRotZ)
        triRotatedZ.points[1] = miltiply_matrix(tri.points[1], matRotZ)
        triRotatedZ.points[2] = miltiply_matrix(tri.points[2], matRotZ)
			# Rotate in X-Axis
        triRotatedXZ = triangle([[0,0,0],[0,0,0],[0,0,0]])

        triRotatedXZ.points[0] = miltiply_matrix(triRotatedZ.points[0], matRotX)
        triRotatedXZ.points[1] = miltiply_matrix(triRotatedZ.points[1], matRotX)
        triRotatedXZ.points[2] = miltiply_matrix(triRotatedZ.points[2], matRotX)



        
        tritrans = copy.deepcopy(triRotatedXZ)
        
        tritrans.points[0].z = triRotatedXZ.points[0].z + 3
        tritrans.points[1].z = triRotatedXZ.points[1].z + 3
        tritrans.points[2].z = triRotatedXZ.points[2].z + 3

        line1 = [
            tritrans.points[1].x - tritrans.points[0].x, 
            tritrans.points[1].y - tritrans.points[0].y,
            tritrans.points[1].z - tritrans.points[0].z
            ]
        line2 = [
            tritrans.points[2].x - tritrans.points[0].x, 
            tritrans.points[2].y - tritrans.points[0].y, 
            tritrans.points[2].z - tritrans.points[0].z
            ]

        normal = [
            (line1[1] * line2[2]) - (line1[2] * line2[1]),
            (line1[2] * line2[0]) - (line1[0] * line2[2]),
            (line1[0] * line2[1]) - (line1[1] * line2[0])
                  ]
        
        
        l = math.sqrt((normal[0]*normal[0]) + (normal[1]*normal[1]) + (normal[2]*normal[2]))
        normal[0] = normal[0] /l
        normal[1] = normal[1]/ l
        normal[2] = normal[2] /l

        dot = (normal[0] * (tritrans.points[0].x- camera.x)) + (normal[1] * (tritrans.points[0].y- camera.y)) + (normal[2] * (tritrans.points[0].z- camera.z))
        
        if dot < 0:
            l = math.sqrt((light_direction.x*light_direction.x) + (light_direction.y*light_direction.y) + (light_direction.z*light_direction.z))
            light_direction.x /= l; light_direction.y /= l; light_direction.z /= l
            
            light_dot = (normal[0] * light_direction.x) + (normal[1] * light_direction.y) + (normal[2]* light_direction.z)
            triproj = [
                miltiply_matrix(tritrans.points[0], projectiom_matrix),
                miltiply_matrix(tritrans.points[1], projectiom_matrix),
                miltiply_matrix(tritrans.points[2], projectiom_matrix)
                ]
        
            pygame.draw.polygon(canvas, (0, 0, abs(130*light_dot+20)), 
                [
                ((triproj[0].x + 1) * W/2, (triproj[0].y + 1) * W/2),
                ((triproj[1].x + 1) * W/2, (triproj[1].y + 1) * W/2),
                ((triproj[2].x + 1) * W/2, (triproj[2].y + 1) * W/2)
                ])
    
    pygame.display.update() 