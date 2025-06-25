# Modul A: Aplikasi Grafika 2D Interaktif dengan PyOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import sin, cos, pi

window_width, window_height = 800, 600
objects = []
clicks = []
current_shape = 'point'
current_color = (1.0, 0.0, 0.0)
line_thickness = 2
transform_translate = [0, 0]
transform_rotate = 0
transform_scale = 1.0
window_rect = []

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Latar belakang hitam
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)

def cohen_sutherland_clip(x1, y1, x2, y2, rect):
    INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

    def compute_out_code(x, y):
        code = INSIDE
        if x < rect[0]: code |= LEFT
        elif x > rect[2]: code |= RIGHT
        if y < rect[1]: code |= BOTTOM
        elif y > rect[3]: code |= TOP
        return code

    outcode1 = compute_out_code(x1, y1)
    outcode2 = compute_out_code(x2, y2)

    while True:
        if not (outcode1 | outcode2):
            return True, (x1, y1, x2, y2)
        elif outcode1 & outcode2:
            return False, ()
        else:
            outcode_out = outcode1 if outcode1 else outcode2
            if outcode_out & TOP:
                x = x1 + (x2 - x1) * (rect[3] - y1) / (y2 - y1)
                y = rect[3]
            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (rect[1] - y1) / (y2 - y1)
                y = rect[1]
            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (rect[2] - x1) / (x2 - x1)
                x = rect[2]
            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (rect[0] - x1) / (x2 - x1)
                x = rect[0]
            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_out_code(x1, y1)
            else:
                x2, y2 = x, y
                outcode2 = compute_out_code(x2, y2)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(*transform_translate, 0)
    glScalef(transform_scale, transform_scale, 1)
    glRotatef(transform_rotate, 0, 0, 1)

    for obj in objects:
        shape, pts, color, thickness = obj
        glColor3f(*color)
        glLineWidth(thickness)

        if window_rect and shape == 'line':
            inside, clipped = cohen_sutherland_clip(*pts[0], *pts[1], window_rect)
            if not inside:
                continue
            pts = [(clipped[0], clipped[1]), (clipped[2], clipped[3])]
            glColor3f(0, 1, 0)  # Warna hijau jika dalam window

        if shape == 'point':
            glBegin(GL_POINTS)
            glVertex2f(*pts[0])
            glEnd()
        elif shape == 'line':
            glBegin(GL_LINES)
            glVertex2f(*pts[0])
            glVertex2f(*pts[1])
            glEnd()
        elif shape == 'square':
            x1, y1 = pts[0]
            x2, y2 = pts[1]
            glBegin(GL_LINE_LOOP)
            glVertex2f(x1, y1)
            glVertex2f(x1, y2)
            glVertex2f(x2, y2)
            glVertex2f(x2, y1)
            glEnd()
        elif shape == 'ellipse':
            cx, cy = pts[0]
            rx, ry = 50, 30
            glBegin(GL_LINE_LOOP)
            for i in range(100):
                angle = 2 * pi * i / 100
                glVertex2f(cx + cos(angle) * rx, cy + sin(angle) * ry)
            glEnd()

    if len(window_rect) == 4:
        glColor3f(0, 0, 1)
        glLineWidth(1)
        glBegin(GL_LINE_LOOP)
        glVertex2f(window_rect[0], window_rect[1])
        glVertex2f(window_rect[2], window_rect[1])
        glVertex2f(window_rect[2], window_rect[3])
        glVertex2f(window_rect[0], window_rect[3])
        glEnd()

    glutSwapBuffers()

def mouse(button, state, x, y):
    global clicks, window_rect
    y = window_height - y
    if state == GLUT_DOWN:
        clicks.append((x, y))
        if current_shape in ['line', 'square'] and len(clicks) == 2:
            objects.append((current_shape, clicks[:2], current_color, line_thickness))
            clicks = []
        elif current_shape == 'point' and len(clicks) == 1:
            objects.append(('point', [clicks[0]], current_color, line_thickness))
            clicks = []
        elif current_shape == 'ellipse' and len(clicks) == 1:
            objects.append(('ellipse', [clicks[0]], current_color, line_thickness))
            clicks = []
        elif current_shape == 'window' and len(clicks) == 2:
            x1, y1 = clicks[0]
            x2, y2 = clicks[1]
            window_rect = [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]
            clicks = []
    glutPostRedisplay()

def keyboard(key, x, y):
    global current_shape, current_color, line_thickness
    global transform_translate, transform_rotate, transform_scale
    if key == b'1': current_shape = 'point'
    elif key == b'2': current_shape = 'line'
    elif key == b'3': current_shape = 'square'
    elif key == b'4': current_shape = 'ellipse'
    elif key == b'w': transform_translate[1] += 10
    elif key == b's': transform_translate[1] -= 10
    elif key == b'a': transform_translate[0] -= 10
    elif key == b'd': transform_translate[0] += 10
    elif key == b'r': transform_rotate += 10
    elif key == b'e': transform_scale += 0.1
    elif key == b'q': transform_scale = max(0.1, transform_scale - 0.1)
    elif key == b'z': current_color = (1, 0, 0)
    elif key == b'x': current_color = (0, 1, 0)
    elif key == b'c': current_color = (0, 0, 1)
    elif key == b'+': line_thickness += 1
    elif key == b'-': line_thickness = max(1, line_thickness - 1)
    elif key == b'5': current_shape = 'window'
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Modul A - PyOpenGL 2D")
    init()
    glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == '__main__':
    main()
