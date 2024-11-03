import pygame, math, numpy as np, copy


class triangle:
    def __init__(self, p:list[np.ndarray]) -> None:
        p1,p2,p3 = p
        self.points = [
            p1,
            p2,
            p3
        ]
mesh = []

H = 500
W = 500
FOV = 90

Zn = 0.1
Zf = 1000

a = W/H
f = 1/math.tan(math.radians(FOV/2))
q = Zf / (Zf - Zn)

with open("cube234.obj", 'r') as file:
    points = []
    for line in file:
        
        line = line.strip()
        points.append(np.array(list(map(float, line[2:].split())))) if line[0] == "v" else mesh.append(triangle(list(map(lambda x: points[int(x)-1], line[2:].split()))))
            



def miltiply_matrix(i, m):
    local_i = np.matmul(np.array([i[0], i[1], i[2], 0]),m)

    if local_i[3] == 0:
        local_i[3] = 1
     
    return np.array([local_i[0]/local_i[3], local_i[1]/local_i[3], local_i[2]/local_i[3]])


    
projectiom_matrix = np.array([
    [a*f, 0, 0, 0],
    [0, f, 0, 0],
    [0,0,q,1],
    [0,0,-Zn*q,0]
])

pygame.init() 

# CREATING CANVAS 
canvas = pygame.display.set_mode((W, W)) 

# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 
exit = False
clock = pygame.time.Clock()


fTheta = 0
camera = np.array([0,0,0])
light_direction = np.array([0,0,-1])
while not exit: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False          

    clock.tick()
    #print("FPS :", clock.get_fps())

    canvas.fill((0,0,1))

    fTheta += 0.001
    matRotZ = np.array([
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
    ])
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
    tris_for_projection = []
    #project 
    for tri in mesh:
       


        triRotatedZ = triangle([[0,0,0],[0,0,0],[0,0,0]])

        triRotatedZ.points[0] = miltiply_matrix(tri.points[0], matRotZ)
        triRotatedZ.points[1] = miltiply_matrix(tri.points[1], matRotZ)
        triRotatedZ.points[2] = miltiply_matrix(tri.points[2], matRotZ)
		#Rotate in X-Axis
        triRotatedXZ = triangle([[0,0,0],[0,0,0],[0,0,0]])

 

        triRotatedXZ.points[0] = miltiply_matrix(triRotatedZ.points[0], matRotX)
        triRotatedXZ.points[1] = miltiply_matrix(triRotatedZ.points[1], matRotX)
        triRotatedXZ.points[2] = miltiply_matrix(triRotatedZ.points[2], matRotX)
        
        

        
        tritrans = copy.deepcopy(triRotatedXZ)

        # ofseting triangle on z axses
        tritrans.points[0][2] = triRotatedXZ.points[0][2] + 10
        tritrans.points[1][2] = triRotatedXZ.points[1][2] + 10
        tritrans.points[2][2] = triRotatedXZ.points[2][2] + 10

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
                miltiply_matrix(tritrans.points[2], projectiom_matrix),
                light_dot
                ]
            tris_for_projection.append(triproj)
    tris_for_projection = sorted(tris_for_projection, key = lambda x: (x[0].z + x[1].z + x[2].z) / 3, reverse=True)
    for triproj in tris_for_projection:
       
        pygame.draw.polygon(canvas, (0, 0, abs(130*triproj[3]+90)), 
            [
                ((triproj[0].x + 1) * W/2, (triproj[0].y + 1) * W/2),
                ((triproj[1].x + 1) * W/2, (triproj[1].y + 1) * W/2),
                ((triproj[2].x + 1) * W/2, (triproj[2].y + 1) * W/2)
            ])
        """
        pygame.draw.polygon(canvas, (255, 255, 255), 
            [
                ((triproj[0].x + 1) * W/2, (triproj[0].y + 1) * W/2),
                ((triproj[1].x + 1) * W/2, (triproj[1].y + 1) * W/2),
                ((triproj[2].x + 1) * W/2, (triproj[2].y + 1) * W/2)
            ],1)
        """
    
    pygame.display.update() 