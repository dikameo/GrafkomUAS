# GrafkomUAS
Wahyu Andika			          (202310370311075)
Ahmad Nur Mu’minin		      (202310370311089)
Yogi Aditya Narotama	    	(202310370311069)


Tugas Besar UAS Grafika Komputer
“Pengembangan Aplikasi Grafika 2D dan 3D InteraktifMenggunakan PyOpenGL“

Modul A: Objek 2D
A. Fungsi Penggambaran Objek
  1. Gambar Objek Dasar:
      a) Titik
      b) Garis
      c) Persegi
      d) Ellipse
2. Koordinat input dilakukan dengan klik mouse pada canvas OpenGL.
B. Fungsi Warna & Ketebalan
3. Pengguna dapat memilih:
  a) Warna objek (melalui tombol atau shortcut keyboard).
  b) Ketebalan garis (jika menggunakan GL_LINES atau GL_LINE_LOOP).
C. Transformasi Geometri
4. Objek yang telah digambar dapat dikenai transformasi:
    a) Translasi
    b) Rotasi
    c) Scaling
5. Transformasi dilakukan melalui keyboard, tombol menu, atau shortcut.
D. Windowing dan Clipping
6. Pengguna dapat menentukan window aktif (misalnya dengan klik 2 titik sudut sebagai batas window).
7. Objek yang:
    a) Masuk ke window: akan berubah warna (misalnya menjadi hijau).
    b) Di luar window: akan dikenai clipping, hanya bagian dalam window yang ditampilkan
    (gunakan algoritma Cohen-Sutherland atau Liang-Barsky untuk garis)
8. Window dapat digeser atau diubah ukurannya.


Modul B: Objek 3D
1. Visualisasi Objek 3D
Tampilkan minimal 1 objek 3D berbentuk:
  a) Kubus atau Piramida
  b) Dibaca dari file .obj atau digambar manual (vertex, face)
2. Transformasi Objek 3D
  Translasi, rotasi (dengan keyboard atau mouse drag)
3. Shading & Pencahayaan
  a) Implementasikan model pencahayaan sederhana (Phong / Gouraud)
  b) Gunakan:
▪ Ambient Light
▪ Diffuse Light
▪ Specular Light
4. Kamera dan Perspektif
  a) Mengatur posisi kamera (gluLookAt)
  b) Gunakan proyeksi perspektif (gluPerspective) untuk 3D.
