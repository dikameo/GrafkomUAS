# GrafkomUAS - Tugas Besar UAS Grafika Komputer

## Tim Pengembang
- **Wahyu Andika** (202310370311075)
- **Ahmad Nur Mu’minin** (202310370311089)
- **Yogi Aditya Narotama** (202310370311069)

## Deskripsi Proyek
Proyek ini merupakan **Tugas Besar UAS Grafika Komputer** yang bertujuan untuk mengembangkan aplikasi grafika interaktif berbasis **2D** dan **3D** menggunakan **PyOpenGL**. Aplikasi ini mencakup dua modul utama: **Modul A (Objek 2D)** dan **Modul B (Objek 3D)**, dengan fungsionalitas yang mencakup penggambaran objek, transformasi geometri, windowing, clipping, visualisasi 3D, serta implementasi pencahayaan dan perspektif.

---

## Modul A: Objek 2D
Modul ini berfokus pada penggambaran dan manipulasi objek 2D dengan fitur interaktif.

### A. Fungsi Penggambaran Objek
1. **Gambar Objek Dasar**:
   - Titik
   - Garis
   - Persegi
   - Ellipse
2. **Input Koordinat**:
   - Koordinat ditentukan melalui **klik mouse** pada canvas OpenGL.

### B. Fungsi Warna & Ketebalan
3. **Pemilihan Atribut**:
   - **Warna Objek**: Pengguna dapat memilih warna melalui tombol atau shortcut keyboard.
   - **Ketebalan Garis**: Dapat diatur untuk objek berbasis `GL_LINES` atau `GL_LINE_LOOP`.

### C. Transformasi Geometri
4. **Jenis Transformasi**:
   - Translasi
   - Rotasi
   - Scaling
5. **Kontrol Transformasi**:
   - Dilakukan melalui **keyboard**, **tombol menu**, atau **shortcut**.

### D. Windowing dan Clipping
6. **Penentuan Window**:
   - Pengguna dapat menentukan area window aktif dengan **klik dua titik sudut** sebagai batas.
7. **Perilaku Objek**:
   - Objek di dalam window akan **berubah warna** (contoh: menjadi hijau).
   - Objek di luar window akan **dikenai clipping**, hanya menampilkan bagian dalam window.
   - Algoritma clipping yang digunakan: **Cohen-Sutherland** atau **Liang-Barsky** untuk garis.
8. **Manipulasi Window**:
   - Window dapat **digeser** atau **diubah ukurannya**.

---

## Modul B: Objek 3D
Modul ini berfokus pada visualisasi dan manipulasi objek 3D dengan fitur pencahayaan dan proyeksi perspektif.

### 1. Visualisasi Objek 3D
- Menampilkan minimal satu objek 3D, seperti:
  - **Kubus** atau **Piramida**.
  - Objek dapat dibaca dari **file .obj** atau digambar secara manual (vertex dan face).

### 2. Transformasi Objek 3D
- **Translasi** dan **rotasi** menggunakan **keyboard** atau **drag mouse**.

### 3. Shading & Pencahayaan
- Implementasi model pencahayaan sederhana (**Phong** atau **Gouraud**).
- Komponen pencahayaan:
  - **Ambient Light**
  - **Diffuse Light**
  - **Specular Light**

### 4. Kamera dan Perspektif
- **Pengaturan Kamera**: Menggunakan `gluLookAt` untuk mengatur posisi dan arah kamera.
- **Proyeksi Perspektif**: Menggunakan `gluPerspective` untuk visualisasi 3D.

---

## Teknologi yang Digunakan
- **PyOpenGL**: Library utama untuk rendering grafika 2D dan 3D.
- **Python**: Bahasa pemrograman untuk implementasi logika aplikasi.
- **Algoritma Clipping**: Cohen-Sutherland atau Liang-Barsky untuk clipping garis.
- **File .obj**: Untuk membaca model 3D (opsional).

---

## Cara Menjalankan
1. Pastikan **Python** dan **PyOpenGL** telah terinstal.
   ```bash
   pip install PyOpenGL PyOpenGL_accelerate
   ```
2. Clone atau unduh repositori proyek ini.
3. Jalankan file utama aplikasi (misalnya: `main.py`).
   ```bash
   python main.py
   ```

---

## Kontrol Aplikasi
- **Klik Mouse**: Menentukan koordinat untuk menggambar objek 2D atau window.
- **Keyboard/Shortcut**:
  - Memilih warna dan ketebalan garis.
  - Melakukan transformasi (translasi, rotasi, scaling).
- **Drag Mouse**: Rotasi atau translasi objek 3D.
- **Tombol Menu**: Akses fungsi tambahan seperti transformasi atau pengaturan window.

---

## Struktur Direktori
```
GrafkomUAS/
├── main.py              # File utama aplikasi
├── assets/              # Folder untuk file .obj atau aset lainnya
├── src/                 # Folder untuk kode sumber
│   ├── 2d/             # Modul untuk fungsi 2D
│   ├── 3d/             # Modul untuk fungsi 3D
├── README.md            # Dokumentasi proyek
└── requirements.txt     # Daftar dependensi
```

---

## Catatan Pengembang
- Pastikan perangkat mendukung OpenGL untuk rendering yang optimal.
- File `.obj` harus memiliki format yang sesuai jika digunakan untuk visualisasi 3D.
- Dokumentasi ini akan diperbarui seiring pengembangan proyek.

---
