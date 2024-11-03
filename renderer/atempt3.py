import pygame, math, numpy as np, copy

H = 800
W = 800
FOV = 90

Zn = 0.1
Zf = 1000
fTheta = 0

a = W/H
f = 1/math.tan(math.radians(FOV/2))
q = Zf / (Zf - Zn)

file_path = "X_wing.obj"

exit = False
clock = pygame.time.Clock()
canvas = pygame.display.set_mode((W, W)) 


projectiom_matrix = np.array([
        [a*f, 0, 0, 0],
        [0, f, 0, 0],
        [0,0,q,1],
        [0,0,-Zn*q,0]
    ])

class triangle:
    def __init__(self, p:list[np.ndarray]) -> None:
        p1,p2,p3 = p
        self.points = np.array([
            p1,
            p2,
            p3
        ])
    
    def execute(self,func, **kwargs):
        for index, point in enumerate(self.points):
            self.points[index] = func(point, **kwargs)
              
def miltiply_matrix(i, m):
    local_i = np.matmul(np.array([i[0], i[1], i[2], 1]),m)
    if local_i[3] == 0: local_i[3] = 1

    return np.array([local_i[0]/local_i[3], local_i[1]/local_i[3], local_i[2]/local_i[3]])

def read_mehs_from_obj(path):
    mesh = []
    points = []
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            points.append(np.array(list(map(float, line[2:].split())))) if line[0] == "v" else mesh.append(triangle(list(map(lambda x: points[int(x)-1], line[2:].split()))))
    
    return mesh 

def vector_normalize(v):
    l = np.linalg.norm(v)
    return np.array([v[0] / l, v[1] / l, v[2] / l ])

def Matrix_PointAt(pos, target, up):
	
    new_forward_vector = vector_normalize(target - pos)
    a = new_forward_vector * np.dot(up, new_forward_vector)
    new_up = up - a
    new_up = vector_normalize(new_up)

    new_right= np.cross(new_up, new_forward_vector)
    matrix = np.array(
        [
        [new_right[0],	new_right[1],   new_right[2],	0.0],
        [new_up[0],		new_up[1], new_up[2],	0.0],
        [new_forward_vector[0],	new_forward_vector[1],	new_forward_vector[2], 0.0],
        [pos[0],  pos[1], pos[2], 1.0]
        ]
    )
    return matrix

def Matrix_QuickInverse(m): ## // Only for Rotation/Translation Matrices
	
    matrix = np.zeros((4, 4))

    # Fill in the values for the first three rows and columns
    matrix[0, 0] = m[0, 0]; matrix[0, 1] = m[1, 0]; matrix[0, 2] = m[2, 0]; matrix[0, 3] = 0.0
    matrix[1, 0] = m[0, 1]; matrix[1, 1] = m[1, 1]; matrix[1, 2] = m[2, 1]; matrix[1, 3] = 0.0
    matrix[2, 0] = m[0, 2]; matrix[2, 1] = m[1, 2]; matrix[2, 2] = m[2, 2]; matrix[2, 3] = 0.0

    # Calculate the fourth row
    matrix[3, 0] = -(m[3, 0] * matrix[0, 0] + m[3, 1] * matrix[1, 0] + m[3, 2] * matrix[2, 0])
    matrix[3, 1] = -(m[3, 0] * matrix[0, 1] + m[3, 1] * matrix[1, 1] + m[3, 2] * matrix[2, 1])
    matrix[3, 2] = -(m[3, 0] * matrix[0, 2] + m[3, 1] * matrix[1, 2] + m[3, 2] * matrix[2, 2])
    matrix[3, 3] = 1.0
    return matrix
	


if __name__ == "__main__":
    pygame.display.set_caption("My Board")        
    pygame.init() 

    camera  = np.array([0,0,0])
    yaw = 0.0
    while not exit: 
        fTheta += 0.000
        tris_for_projection = []
        
        light_direction = np.array([0,0,-1])
        
        
        
        vUp = np.array([ 0,1,0 ])
        vtarget = np.array([0,0,1])
        mat_rot_cam =  np.array([
            [math.cos(yaw), 0 ,  math.sin(yaw), 0],
            [0,            1.0,  0, 0],
            [-math.sin(yaw),0,math.cos(yaw),0],
            [0,0,0,1]
        ])
        look_dir = miltiply_matrix(vtarget, mat_rot_cam)
        vtarget = camera + look_dir
        mat_cam = Matrix_PointAt(camera, vtarget, vUp)
        

        mat_viev = Matrix_QuickInverse(mat_cam)
        vForward = look_dir * 0.1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    camera = np.array([camera[0], camera[1] + 0.1, camera[2]])
                if event.key == pygame.K_DOWN:
                    camera = np.array([camera[0], camera[1] - 0.1, camera[2]])


                if event.key == pygame.K_LEFT:
                    camera = np.array([camera[0] - 0.1, camera[1], camera[2]])
                if event.key == pygame.K_RIGHT:
                    camera = np.array([camera[0] + 0.1, camera[1], camera[2]])

                

                if event.key == pygame.K_a:
                    yaw += 0.1
                if event.key == pygame.K_d:
                    yaw -= 0.1
                
                if event.key == pygame.K_w:
                    camera = camera + vForward
                if event.key == pygame.K_s:
                    camera = camera - vForward
                    
        canvas.fill((0,0,1)) 
        


        matRotZ = np.array([
            [math.cos(fTheta),math.sin(fTheta),0,0],
            [-math.sin(fTheta),math.cos(fTheta),0,0],
            [0,0,1,0],
            [0,0,0,1],
        ])
        matRotX = np.array([
                [1,0,0,0],
                [0,math.cos(fTheta * 0.5),math.sin(fTheta * 0.5),0],
                [0,-math.sin(fTheta * 0.5),math.cos(fTheta * 0.5),0],
                [0,0,0,1],
            ])
    
        for tri in read_mehs_from_obj(file_path):
            workable_tri = copy.deepcopy(tri)

            workable_tri.execute(miltiply_matrix,m = matRotZ)
            workable_tri.execute(miltiply_matrix,m = matRotX)

            workable_tri.points[0][2] = workable_tri.points[0][2] + 10
            workable_tri.points[1][2] = workable_tri.points[1][2] + 10
            workable_tri.points[2][2] = workable_tri.points[2][2] + 10

            vec1 = workable_tri.points[1] - workable_tri.points[0]
            vec2 = workable_tri.points[2] - workable_tri.points[0]

            normal = vector_normalize(np.cross(vec1, vec2))
            dot = np.dot(normal, camera - workable_tri.points[0])
            light_dot = np.dot(normal, vector_normalize(light_direction))

            if  dot > 0: tris_for_projection.append((workable_tri, (0, 0, light_dot*60 + 90)))
                
        for triproj, color in sorted(tris_for_projection, key = lambda x: (x[0].points[0][2] + x[0].points[1][2] + x[0].points[2][2])/3, reverse=True):
            print(mat_viev)
            triproj.execute(miltiply_matrix, m = mat_viev)

            triproj.execute(miltiply_matrix, m = projectiom_matrix)
            pygame.draw.polygon(canvas, color, 
                [
                    ((triproj.points[0][0] + 1) * W/2, (triproj.points[0][1] + 1) * W/2),
                    ((triproj.points[1][0] + 1) * W/2, (triproj.points[1][1] + 1) * W/2),
                    ((triproj.points[2][0] + 1) * W/2, (triproj.points[2][1] + 1) * W/2)
                ])
        pygame.display.update()
