import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
import os

class Object3D:
    def __init__(self):
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.translation_x = 0
        self.translation_y = 0
        self.translation_z = -5
        
    def rotate(self, x, y, z):
        self.rotation_x += x
        self.rotation_y += y
        self.rotation_z += z
        
    def translate(self, x, y, z):
        self.translation_x += x
        self.translation_y += y
        self.translation_z += z

class Cube(Object3D):
    def __init__(self):
        super().__init__()
        self.vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # belakang
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]       # depan
        ]
        
        # Face indices (counter-clockwise untuk normal yang benar)
        self.faces = [
            [0, 1, 2, 3],  # belakang
            [4, 7, 6, 5],  # depan
            [0, 4, 5, 1],  # bawah
            [2, 6, 7, 3],  # atas
            [0, 3, 7, 4],  # kiri
            [1, 5, 6, 2]   # kanan
        ]
        
        # Normal untuk setiap face
        self.normals = [
            [0, 0, -1],   # belakang
            [0, 0, 1],    # depan
            [0, -1, 0],   # bawah
            [0, 1, 0],    # atas
            [-1, 0, 0],   # kiri
            [1, 0, 0]     # kanan
        ]
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.translation_x, self.translation_y, self.translation_z)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        glRotatef(self.rotation_z, 0, 0, 1)
        
        glBegin(GL_QUADS)
        for i, face in enumerate(self.faces):
            glNormal3fv(self.normals[i])
            for vertex_idx in face:
                glVertex3fv(self.vertices[vertex_idx])
        glEnd()
        
        glPopMatrix()

class Pyramid(Object3D):
    def __init__(self):
        super().__init__()
        # Vertex koordinat untuk piramida
        self.vertices = [
            [0, 1, 0],      # puncak
            [-1, -1, 1],    # base kiri depan
            [1, -1, 1],     # base kanan depan
            [1, -1, -1],    # base kanan belakang
            [-1, -1, -1]    # base kiri belakang
        ]
        
        # Face indices
        self.faces = [
            [1, 2, 3, 4],   # base
            [0, 2, 1],      # depan
            [0, 3, 2],      # kanan
            [0, 4, 3],      # belakang
            [0, 1, 4]       # kiri
        ]
    
    def calculate_normal(self, p1, p2, p3):
        # Menghitung normal dari 3 titik
        v1 = np.array(p2) - np.array(p1)
        v2 = np.array(p3) - np.array(p1)
        normal = np.cross(v1, v2)
        norm = np.linalg.norm(normal)
        if norm > 0:
            normal = normal / norm
        return normal
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.translation_x, self.translation_y, self.translation_z)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        glRotatef(self.rotation_z, 0, 0, 1)
        
        # Base (quad)
        glBegin(GL_QUADS)
        glNormal3f(0, -1, 0)  # normal menghadap ke bawah
        for vertex_idx in self.faces[0]:
            glVertex3fv(self.vertices[vertex_idx])
        glEnd()
        
        # Triangular faces
        glBegin(GL_TRIANGLES)
        for face in self.faces[1:]:
            p1 = self.vertices[face[0]]
            p2 = self.vertices[face[1]]
            p3 = self.vertices[face[2]]
            normal = self.calculate_normal(p1, p2, p3)
            glNormal3fv(normal)
            for vertex_idx in face:
                glVertex3fv(self.vertices[vertex_idx])
        glEnd()
        
        glPopMatrix()

class OBJLoader:
    """Class untuk membaca file .obj"""
    @staticmethod
    def load_obj(filename):
        """Load file .obj dan return vertices, faces, normals"""
        vertices = []
        normals = []
        faces = []
        face_normals = []
        
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('v '):  # Vertex
                        parts = line.split()
                        vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                        vertices.append(vertex)
                    elif line.startswith('vn '):  # Vertex normal
                        parts = line.split()
                        normal = [float(parts[1]), float(parts[2]), float(parts[3])]
                        normals.append(normal)
                    elif line.startswith('f '):  # Face
                        parts = line.split()[1:]  # Skip 'f'
                        face = []
                        face_normal_indices = []
                        
                        for part in parts:
                            # Handle different .obj formats: v, v/vt, v/vt/vn, v//vn
                            indices = part.split('/')
                            vertex_idx = int(indices[0]) - 1  # .obj uses 1-based indexing
                            face.append(vertex_idx)
                            
                            # Check if normal index exists
                            if len(indices) >= 3 and indices[2]:
                                normal_idx = int(indices[2]) - 1
                                face_normal_indices.append(normal_idx)
                        
                        faces.append(face)
                        if face_normal_indices:
                            face_normals.append(face_normal_indices)
                        else:
                            face_normals.append([])
            
            print(f"OBJ loaded: {len(vertices)} vertices, {len(faces)} faces")
            return {
                'vertices': vertices,
                'faces': faces,
                'normals': normals,
                'face_normals': face_normals
            }
        except FileNotFoundError:
            print(f"File {filename} tidak ditemukan!")
            return None
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None

class OBJObject(Object3D):
    """Object 3D yang dibuat dari file .obj"""
    def __init__(self, obj_data):
        super().__init__()
        self.vertices = obj_data['vertices']
        self.faces = obj_data['faces']
        self.normals = obj_data['normals']
        self.face_normals = obj_data['face_normals']
    
    def calculate_normal(self, p1, p2, p3):
        """Hitung normal dari 3 titik jika tidak ada di file"""
        v1 = np.array(p2) - np.array(p1)
        v2 = np.array(p3) - np.array(p1)
        normal = np.cross(v1, v2)
        norm = np.linalg.norm(normal)
        if norm > 0:
            normal = normal / norm
        return normal
    
    def draw(self):
        glPushMatrix()
        glTranslatef(self.translation_x, self.translation_y, self.translation_z)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        glRotatef(self.rotation_z, 0, 0, 1)
        
        # Render faces
        for i, face in enumerate(self.faces):
            if len(face) == 3:  # Triangle
                glBegin(GL_TRIANGLES)
            elif len(face) == 4:  # Quad
                glBegin(GL_QUADS)
            else:  # Polygon
                glBegin(GL_POLYGON)
            
            # Use normals from file if available
            if i < len(self.face_normals) and len(self.face_normals[i]) > 0:
                for j, vertex_idx in enumerate(face):
                    if j < len(self.face_normals[i]):
                        normal_idx = self.face_normals[i][j]
                        if normal_idx < len(self.normals):
                            glNormal3fv(self.normals[normal_idx])
                    glVertex3fv(self.vertices[vertex_idx])
            else:
                # Calculate normal if not in file
                if len(face) >= 3:
                    p1 = self.vertices[face[0]]
                    p2 = self.vertices[face[1]]
                    p3 = self.vertices[face[2]]
                    normal = self.calculate_normal(p1, p2, p3)
                    glNormal3fv(normal)
                
                for vertex_idx in face:
                    if vertex_idx < len(self.vertices):
                        glVertex3fv(self.vertices[vertex_idx])
            
            glEnd()
        
        glPopMatrix()

class Camera:
    def __init__(self):
        self.eye_x, self.eye_y, self.eye_z = 0, 0, 5
        self.center_x, self.center_y, self.center_z = 0, 0, 0
        self.up_x, self.up_y, self.up_z = 0, 1, 0
        self.fov = 45
        self.near = 0.1
        self.far = 100.0
        
    def setup_perspective(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, width/height, self.near, self.far)
        
    def setup_view(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.eye_x, self.eye_y, self.eye_z,
                  self.center_x, self.center_y, self.center_z,
                  self.up_x, self.up_y, self.up_z)
    
    def move(self, dx, dy, dz):
        self.eye_x += dx
        self.eye_y += dy
        self.eye_z += dz

class Lighting:
    def __init__(self):
        self.setup_lighting()
    
    def setup_lighting(self):
        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        
        # Ambient light
        ambient = [0.2, 0.2, 0.2, 1.0]
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
        
        # Diffuse light
        diffuse = [0.8, 0.8, 0.8, 1.0]
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
        
        # Specular light
        specular = [1.0, 1.0, 1.0, 1.0]
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
        
        # Light position
        position = [2.0, 2.0, 2.0, 1.0]
        glLightfv(GL_LIGHT0, GL_POSITION, position)
        
        # Material properties
        mat_ambient = [0.3, 0.3, 0.3, 1.0]
        mat_diffuse = [0.7, 0.1, 0.1, 1.0]
        mat_specular = [1.0, 1.0, 1.0, 1.0]
        mat_shininess = [50.0]
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)

def create_sample_obj_files():
    """Buat file .obj sample jika tidak ada"""
    
    # Buat file cube.obj
    cube_obj = """# Cube OBJ file
v -1.0 -1.0 -1.0
v  1.0 -1.0 -1.0
v  1.0  1.0 -1.0
v -1.0  1.0 -1.0
v -1.0 -1.0  1.0
v  1.0 -1.0  1.0
v  1.0  1.0  1.0
v -1.0  1.0  1.0

vn  0.0  0.0 -1.0
vn  0.0  0.0  1.0
vn  0.0 -1.0  0.0
vn  0.0  1.0  0.0
vn -1.0  0.0  0.0
vn  1.0  0.0  0.0

f 1//1 2//1 3//1 4//1
f 5//2 8//2 7//2 6//2
f 1//3 5//3 6//3 2//3
f 3//4 7//4 8//4 4//4
f 1//5 4//5 8//5 5//5
f 2//6 6//6 7//6 3//6
"""
    
    
    tetrahedron_obj = """# Piramid OBJ file
v  0.0  1.0  0.0
v -1.0 -1.0  1.0
v  1.0 -1.0  1.0
v  0.0 -1.0 -1.0

f 2 3 4
f 1 3 2
f 1 4 3
f 1 2 4
"""
    
    # Tulis file jika belum ada
    if not os.path.exists("cube.obj"):
        with open("cube.obj", "w") as f:
            f.write(cube_obj)
        print("Created cube.obj")
    
    if not os.path.exists("tetrahedron.obj"):
        with open("tetrahedron.obj", "w") as f:
            f.write(tetrahedron_obj)
        print("Created tetrahedron.obj")
    
class Graphics3D:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Graphics - Modul B")
        
        # Initialize components
        self.camera = Camera()
        self.lighting = Lighting()
        
        # Objects manual
        self.cube = Cube()
        self.pyramid = Pyramid()
        
        # Objects dari file OBJ
        self.obj_objects = []
        self.load_obj_files()
        
        # List semua objects
        self.all_objects = [self.cube, self.pyramid] + self.obj_objects
        self.current_object_index = 0
        self.current_object = self.all_objects[0]
        
        # Mouse control
        self.mouse_dragging = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
        # Setup initial view
        self.camera.setup_perspective(self.width, self.height)
        
        # Background color
        glClearColor(0.1, 0.1, 0.15, 1.0)
        
        self.clock = pygame.time.Clock()
    
    def load_obj_files(self):
        """Load semua file .obj yang tersedia"""
        # Buat file sample jika belum ada
        create_sample_obj_files()
        
        obj_files = ['cube.obj', 'tetrahedron.obj']
        
        for filename in obj_files:
            if os.path.exists(filename):
                obj_data = OBJLoader.load_obj(filename)
                if obj_data:
                    obj_object = OBJObject(obj_data)
                    obj_object.translation_x = len(self.obj_objects) * 3  # Spread objects
                    self.obj_objects.append(obj_object)
                    print(f"Loaded {filename}")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                # Switch objects
                if event.key == pygame.K_1:
                    self.current_object_index = 0
                    self.current_object = self.all_objects[0]  # Cube manual
                    print("Switched to Manual Cube")
                elif event.key == pygame.K_2:
                    self.current_object_index = 1
                    self.current_object = self.all_objects[1]  # Pyramid manual
                    print("Switched to Manual Pyramid")
                elif event.key == pygame.K_3 and len(self.all_objects) > 2:
                    self.current_object_index = 2
                    self.current_object = self.all_objects[2]  # First OBJ
                    print("Switched to OBJ Cube")
                elif event.key == pygame.K_4 and len(self.all_objects) > 3:
                    self.current_object_index = 3
                    self.current_object = self.all_objects[3]  # Second OBJ
                    print("Switched to OBJ Pyramid")
                
                # Cycle through objects dengan TAB
                elif event.key == pygame.K_TAB:
                    self.current_object_index = (self.current_object_index + 1) % len(self.all_objects)
                    self.current_object = self.all_objects[self.current_object_index]
                    object_names = ["Manual Cube", "Manual Pyramid", "OBJ Cube", "OBJ Pyramid"]
                    if self.current_object_index < len(object_names):
                        print(f"Switched to {object_names[self.current_object_index]}")
                
                # Camera movement
                elif event.key == pygame.K_w:
                    self.camera.move(0, 0, -0.5)
                elif event.key == pygame.K_s:
                    self.camera.move(0, 0, 0.5)
                elif event.key == pygame.K_a:
                    self.camera.move(-0.5, 0, 0)
                elif event.key == pygame.K_d:
                    self.camera.move(0.5, 0, 0)
                elif event.key == pygame.K_q:
                    self.camera.move(0, 0.5, 0)
                elif event.key == pygame.K_e:
                    self.camera.move(0, -0.5, 0)
                
                # Object translation
                elif event.key == pygame.K_UP:
                    self.current_object.translate(0, 0.2, 0)
                elif event.key == pygame.K_DOWN:
                    self.current_object.translate(0, -0.2, 0)
                elif event.key == pygame.K_LEFT:
                    self.current_object.translate(-0.2, 0, 0)
                elif event.key == pygame.K_RIGHT:
                    self.current_object.translate(0.2, 0, 0)
                
                # Object rotation
                elif event.key == pygame.K_x:
                    self.current_object.rotate(5, 0, 0)
                elif event.key == pygame.K_y:
                    self.current_object.rotate(0, 5, 0)
                elif event.key == pygame.K_z:
                    self.current_object.rotate(0, 0, 5)
                    
                elif event.key == pygame.K_ESCAPE:
                    return False
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.mouse_dragging = True
                    self.last_mouse_x, self.last_mouse_y = event.pos
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_dragging = False
                    
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_dragging:
                    mouse_x, mouse_y = event.pos
                    dx = mouse_x - self.last_mouse_x
                    dy = mouse_y - self.last_mouse_y
                    
                    # Rotate object based on mouse movement
                    self.current_object.rotate(dy * 0.5, dx * 0.5, 0)
                    
                    self.last_mouse_x = mouse_x
                    self.last_mouse_y = mouse_y
                    
        return True
    
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Setup camera view
        self.camera.setup_view()
        
        # Draw current object
        self.current_object.draw()
        
        pygame.display.flip()
    
    def print_controls(self):
        print("\n=== KONTROL PROGRAM ===")
        print("OBJECT SELECTION:")
        print("1: Manual Cube")
        print("2: Manual Pyramid") 
        print("3: OBJ Cube")
        print("4: OBJ Pyramid")
        print("TAB: Cycle through objects")
        print("\nCONTROLS:")
        print("Mouse drag: Rotasi objek")
        print("X/Y/Z: Rotasi objek pada sumbu")
        print("Arrow keys: Translate objek")
        print("WASD: Gerakkan kamera horizontal")
        print("Q/E: Gerakkan kamera vertikal")
        print("ESC: Keluar")
        print("======================\n")
    
    def run(self):
        self.print_controls()
        running = True
        
        while running:
            running = self.handle_events()
            self.render()
            self.clock.tick(60)  # 60 FPS
            
        pygame.quit()

# Jalankan program
if __name__ == "__main__":
    try:
        app = Graphics3D()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        print("Pastikan PyOpenGL dan pygame terinstall:")
        print("pip install PyOpenGL PyOpenGL_accelerate pygame numpy")