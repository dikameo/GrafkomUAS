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
point_size = 5
transform_translate = [0, 0]
transform_rotate = 0
transform_scale = 1.0
window_rect = []

def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)  # White background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)

def apply_transform(x, y):
    """Apply current transformations (translate, rotate, scale) to a point."""
    # Scale
    x_s = x * transform_scale
    y_s = y * transform_scale
    # Rotate
    rad = transform_rotate * pi / 180
    x_r = x_s * cos(rad) - y_s * sin(rad)
    y_r = x_s * sin(rad) + y_s * cos(rad)
    # Translate
    x_t = x_r + transform_translate[0]
    y_t = y_r + transform_translate[1]
    return x_t, y_t

def inverse_transform(x, y):
    """Apply inverse transformations to a point."""
    # Inverse translate
    x_t = x - transform_translate[0]
    y_t = y - transform_translate[1]
    # Inverse rotate
    rad = -transform_rotate * pi / 180
    x_r = x_t * cos(rad) - y_t * sin(rad)
    y_r = x_t * sin(rad) + y_t * cos(rad)
    # Inverse scale
    x_s = x_r / transform_scale if transform_scale != 0 else x_r
    y_s = y_r / transform_scale if transform_scale != 0 else y_r
    return x_s, y_s

def point_inside_rect(x, y, rect):
    """Check if a point is inside the clipping rectangle."""
    return rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]

def cohen_sutherland_clip(x1, y1, x2, y2, rect):
    INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8

    def compute_out_code(x, y):
        code = INSIDE
        if x < rect[0]: code |= LEFT
        elif x > rect[2]: code |= RIGHT
        if y < rect[1]: code |= BOTTOM
        elif y > rect[3]: code |= TOP
        return code

    # Handle degenerate case
    if x1 == x2 and y1 == y2:
        return point_inside_rect(x1, y1, rect), (x1, y1, x2, y2)

    outcode1 = compute_out_code(x1, y1)
    outcode2 = compute_out_code(x2, y2)
    max_iterations = 100  # Prevent infinite loops
    iteration = 0

    while True:
        if iteration >= max_iterations:
            return False, ()

        if not (outcode1 | outcode2):
            return True, (x1, y1, x2, y2)
        elif outcode1 & outcode2:
            return False, ()
        else:
            outcode_out = outcode1 if outcode1 else outcode2
            x, y = 0, 0
            if outcode_out & TOP:
                x = x1 + (x2 - x1) * (rect[3] - y1) / (y2 - y1 + 1e-10)
                y = rect[3]
            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (rect[1] - y1) / (y2 - y1 + 1e-10)
                y = rect[1]
            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (rect[2] - x1) / (x2 - x1 + 1e-10)
                x = rect[2]
            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (rect[0] - x1) / (x2 - x1 + 1e-10)
                x = rect[0]
            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_out_code(x1, y1)
            else:
                x2, y2 = x, y
                outcode2 = compute_out_code(x2, y2)
        iteration += 1

def clip_square(pts, rect):
    """Clip a square by treating it as four line segments."""
    x1, y1 = pts[0]
    x2, y2 = pts[1]
    # Define the four corners of the square
    corners = [
        (x1, y1), (x1, y2),
        (x1, y2), (x2, y2),
        (x2, y2), (x2, y1),
        (x2, y1), (x1, y1)
    ]
    clipped_lines = []
    for i in range(0, 8, 2):
        inside, clipped = cohen_sutherland_clip(corners[i][0], corners[i][1], corners[i+1][0], corners[i+1][1], rect)
        if inside:
            clipped_lines.append(clipped)
    return clipped_lines

def clip_ellipse(cx, cy, rx, ry, rect):
    """Clip an ellipse by approximating it as line segments."""
    segments = []
    n_segments = 100
    for i in range(n_segments):
        angle1 = 2 * pi * i / n_segments
        angle2 = 2 * pi * (i + 1) / n_segments
        x1 = cx + cos(angle1) * rx
        y1 = cy + sin(angle1) * ry
        x2 = cx + cos(angle2) * rx
        y2 = cy + sin(angle2) * ry
        inside, clipped = cohen_sutherland_clip(x1, y1, x2, y2, rect)
        if inside:
            segments.append(clipped)
    return segments

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(*transform_translate, 0)
    glScalef(transform_scale, transform_scale, 1)
    glRotatef(transform_rotate, 0, 0, 1)

    for obj in objects:
        shape, pts, color, thickness, size = obj
        glLineWidth(thickness)
        glPointSize(size if shape == 'point' else 1)

        # Transform points to window coordinates for clipping
        if shape == 'point':
            x, y = apply_transform(*pts[0])
            if window_rect and point_inside_rect(x, y, window_rect):
                glColor3f(0, 1, 0)  # Green if inside
            else:
                glColor3f(*color)
            glBegin(GL_POINTS)
            glVertex2f(*pts[0])
            glEnd()
        elif shape == 'line':
            x1, y1 = apply_transform(*pts[0])
            x2, y2 = apply_transform(*pts[1])
            if window_rect:
                inside, clipped = cohen_sutherland_clip(x1, y1, x2, y2, window_rect)
                if inside:
                    # Transform clipped points back to object space (approximate)
                    cx1, cy1 = inverse_transform(clipped[0], clipped[1])
                    cx2, cy2 = inverse_transform(clipped[2], clipped[3])
                    glColor3f(0, 1, 0)
                    glBegin(GL_LINES)
                    glVertex2f(cx1, cy1)
                    glVertex2f(cx2, cy2)
                    glEnd()
                else:
                    glColor3f(*color)
                    glBegin(GL_LINES)
                    glVertex2f(*pts[0])
                    glVertex2f(*pts[1])
                    glEnd()
            else:
                glColor3f(*color)
                glBegin(GL_LINES)
                glVertex2f(*pts[0])
                glVertex2f(*pts[1])
                glEnd()
        elif shape == 'square':
            if window_rect:
                x1, y1 = apply_transform(*pts[0])
                x2, y2 = apply_transform(*pts[1])
                clipped_lines = clip_square([(x1, y1), (x2, y2)], window_rect)
                if clipped_lines:
                    glColor3f(0, 1, 0)
                    glBegin(GL_LINES)
                    for line in clipped_lines:
                        cx1, cy1 = inverse_transform(line[0], line[1])
                        cx2, cy2 = inverse_transform(line[2], line[3])
                        glVertex2f(cx1, cy1)
                        glVertex2f(cx2, cy2)
                    glEnd()
                else:
                    glColor3f(*color)
                    x1, y1 = pts[0]
                    x2, y2 = pts[1]
                    glBegin(GL_LINE_LOOP)
                    glVertex2f(x1, y1)
                    glVertex2f(x1, y2)
                    glVertex2f(x2, y2)
                    glVertex2f(x2, y1)
                    glEnd()
            else:
                glColor3f(*color)
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
            cx_t, cy_t = apply_transform(cx, cy)
            if window_rect:
                clipped_segments = clip_ellipse(cx_t, cy_t, rx * transform_scale, ry * transform_scale, window_rect)
                if clipped_segments:
                    glColor3f(0, 1, 0)
                    glBegin(GL_LINES)
                    for segment in clipped_segments:
                        cx1, cy1 = inverse_transform(segment[0], segment[1])
                        cx2, cy2 = inverse_transform(segment[2], segment[3])
                        glVertex2f(cx1, cy1)
                        glVertex2f(cx2, cy2)
                    glEnd()
                else:
                    glColor3f(*color)
                    glBegin(GL_LINE_LOOP)
                    for i in range(100):
                        angle = 2 * pi * i / 100
                        glVertex2f(cx + cos(angle) * rx, cy + sin(angle) * ry)
                    glEnd()
            else:
                glColor3f(*color)
                glBegin(GL_LINE_LOOP)
                for i in range(100):
                    angle = 2 * pi * i / 100
                    glVertex2f(cx + cos(angle) * rx, cy + sin(angle) * ry)
                glEnd()

    if len(window_rect) == 4:
        glLoadIdentity()  # Draw window_rect in window coordinates
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
            objects.append((current_shape, clicks[:2], current_color, line_thickness, point_size))
            clicks = []
        elif current_shape == 'point' and len(clicks) == 1:
            objects.append(('point', [clicks[0]], current_color, line_thickness, point_size))
            clicks = []
        elif current_shape == 'ellipse' and len(clicks) == 1:
            objects.append(('ellipse', [clicks[0]], current_color, line_thickness, point_size))
            clicks = []
        elif current_shape == 'window' and len(clicks) == 2:
            x1, y1 = clicks[0]
            x2, y2 = clicks[1]
            window_rect = [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]
            clicks = []
    glutPostRedisplay()

def keyboard(key, x, y):
    global current_shape, current_color, line_thickness, point_size
    global transform_translate, transform_rotate, transform_scale, window_rect
    if key == b'1': current_shape = 'point'
    elif key == b'2': current_shape = 'line'
    elif key == b'3': current_shape = 'square'
    elif key == b'4': current_shape = 'ellipse'
    elif key == b'5': current_shape = 'window'
    elif key == b'6': window_rect = []  # Disable clipping
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
    elif key == b']': point_size += 1
    elif key == b'[': point_size = max(1, point_size - 1)
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

cheatsheet = """
====================[ CHEATSHEET GRAFIKA 2D - PyOpenGL ]====================

🎨 PILIHAN OBJEK (GAMBAR):
  [1] Titik
  [2] Garis
  [3] Persegi
  [4] Ellipse
  [5] Window (untuk clipping)

🖱️ PENGGAMBARAN:
  - Klik 1x: Titik atau pusat Ellipse
  - Klik 2x: Garis, Persegi, atau Window (dua titik sudut)

🎨 PILIHAN WARNA:
  [z] Merah     [x] Hijau     [c] Biru

✏️ KETEBALAN GARIS:
  [+] Tambah ketebalan
  [-] Kurangi ketebalan (min: 1)

🔹 UKURAN TITIK:
  []] Tambah ukuran titik
  [[] Kurangi ukuran titik (min: 1)

🛠️ TRANSFORMASI OBJEK (BERLAKU UNTUK SEMUA OBJEK):
  🔁 Translasi (Geser):
    [w] Atas     [s] Bawah     [a] Kiri     [d] Kanan
  🔃 Rotasi:
    [r] Putar searah jarum jam (+10°)
  🔍 Scaling:
    [e] Perbesar     [q] Perkecil (min: 0.1x)

✂️ WINDOWING & CLIPPING:
  - Tekan [5], klik 2 titik → Membuat window aktif (kotak biru)
  - Tekan [6] → Menonaktifkan clipping
  - Objek dalam window (Titik, Garis, Persegi, Ellipse) → Warna hijau
  - Objek di luar window → Warna asli objek

============================================================================
"""

print(cheatsheet)

if __name__ == '__main__':
    main()