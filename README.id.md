# Bitapres

🌐 **Bahasa:** [English](README.md) | **Bahasa Indonesia**

![GitHub release (latest by date)](https://img.shields.io/github/v/release/Bintang-AF/Bitapres?style=flat-square&color=blue)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?style=flat-square&logo=windows)
![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white)

**Bitapres** adalah aplikasi desktop lokal berbasis Python dan FFmpeg untuk mengompres ukuran video berdasarkan **target ukuran (MB)** tanpa perlu koneksi internet. Cocok untuk mengecilkan klip game agar muat di Discord (<10 MB) atau tugas video untuk portal kampus tanpa harus mengunggah file pribadi ke situs online.

<!-- Hapus tanda komentar di bawah setelah menambahkan screenshot ke assets/screenshot.png -->
<!-- ![Tampilan Bitapres](assets/screenshot.png) -->

---

## Fitur Utama (v1.0.1)

- **Kompresi Target Ukuran (MB):** Menghitung *bitrate* video secara otomatis agar hasil kompresi mendekati target ukuran tanpa melewati batas.
- **100% Lokal & Privat:** Semua proses berjalan di komputermu sendiri tanpa internet dan tanpa iklan.
- **Mendukung Format Umum:** Bisa memproses `.mp4`, `.mkv`, `.mov`, dan `.avi`.
- **Validasi & Pengaman Ketat:** Otomatis menolak input tidak valid, memberi tahu batas minimal MB yang realistis jika target terlalu kecil, serta mencegah file hasil tertimpa dengan penomoran otomatis (`_1`, `_2`, dst.).
- **Antarmuka Ringan (Dark Mode):** Dibangun dengan CustomTkinter dan *background threading* agar aplikasi tidak macet (*Not Responding*) saat memproses video.

---

## Download & Cara Menggunakan (Pengguna Umum)

Kamu tidak perlu menginstal Python untuk memakai Bitapres.

1. Unduh file **`Bitapres-v1.0.1-Windows.zip`** melalui halaman [**Latest Release di sini**](https://github.com/Bintang-AF/Bitapres/releases/latest).
2. Ekstrak seluruh isi file ZIP ke dalam satu folder. Pastikan `Bitapres.exe`, `ffmpeg.exe`, dan `ffprobe.exe` tetap berada di folder yang sama.
3. Klik dua kali **`Bitapres.exe`** untuk membuka aplikasi.
4. Pilih video, masukkan target ukuran (MB), lalu klik **Mulai Kompres**. File hasil akan tersimpan otomatis di folder yang sama dengan video asli.

> **Catatan Keamanan Windows:** Karena aplikasi ini belum memiliki sertifikat digital berbayar, Windows SmartScreen mungkin menampilkan peringatan *"Windows protected your PC"*. Klik **More info** lalu pilih **Run anyway**.

---

## Menjalankan dari Source Code (Developer)

**Prasyarat:** Python 3.12+ dan [FFmpeg](https://ffmpeg.org/) sudah terinstal di sistem (PATH).

```bash
# 1. Clone repositori
git clone [https://github.com/Bintang-AF/Bitapres.git](https://github.com/Bintang-AF/Bitapres.git)
cd Bitapres

# 2. Buat dan aktifkan virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Instal library yang dibutuhkan
pip install -r requirements.txt

# 4. Jalankan aplikasi
python app.py