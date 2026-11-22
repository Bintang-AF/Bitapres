<div align="center">

# 🎬 Bitapres

**Kompres video sesuai target ukuran (MB) — 100% offline, cepat, dan privat.**

🌐 [English](README.md) | **Bahasa Indonesia**

[![Rilis Terbaru](https://img.shields.io/github/v/release/Bintang-AF/Bitapres?style=for-the-badge&color=28a745)](https://github.com/Bintang-AF/Bitapres/releases/latest)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](#download--cara-menggunakan)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

[Download v1.1.0](https://github.com/Bintang-AF/Bitapres/releases/latest) • [Fitur Utama](#-fitur-utama-v110) • [Mode 1-Pass vs 2-Pass](#-mode-kompresi) • [Roadmap](#-roadmap-pengembangan)

</div>

---

<!-- Hapus tanda komentar di bawah setelah menambahkan screenshot ke assets/screenshot.png -->
<!-- <p align="center"><img src="assets/screenshot.png" alt="Tampilan Bitapres" width="500"></p> -->

## 💡 Kenapa Bitapres?

Sering kesulitan mengecilkan klip game agar muat di **Discord (<10 MB)** atau kompres tugas video kampus tanpa harus mengunggah file pribadi ke situs online yang penuh iklan? **Bitapres** menghitung *bitrate* secara otomatis dan memproses video langsung di komputermu lewat FFmpeg—tanpa internet, tanpa *watermark*, dan tanpa batas unggah.

---

## ✨ Fitur Utama (v1.1.0)

* 🎯 **Presisi Target Ukuran (MB):** Cukup masukkan target MB yang diinginkan, Bitapres otomatis menghitung *bitrate* optimal agar hasil tidak melewati batas.
* 📊 **Real-Time Progress & Batal:** Pantau kemajuan kompresi asli (0%–100%) langsung dari FFmpeg, atau batalkan kapan saja—file setengah jadi otomatis dihapus agar tidak menyampah.
* 🔍 **Info Metadata Otomatis:** Langsung menampilkan ukuran asli, durasi, resolusi, dan FPS begitu file video dipilih.
* ⚡ **Mode 1-Pass & 2-Pass:** Bebas pilih antara proses cepat atau mode *2-Pass* yang lebih presisi dengan kualitas gambar lebih tajam.
* 📁 **Folder Simpan Bebas & Statistik Hemat:** Tentukan folder tujuan sesukamu dan lihat langsung ringkasan penghematannya (contoh: `20.4 MB → 7.4 MB • Hemat 63.7%`).
* 🛡️ **Pengaman & Validasi Ketat:** Mencegah file tertimpa (`_1`, `_2`, dst.), mendeteksi file rusak, serta memberi rekomendasi minimal MB yang realistis jika target terlalu kecil.

---

## ⚙️ Mode Kompresi

| Mode | Cocok Untuk | Kecepatan | Akurasi Ukuran & Kualitas |
| :--- | :--- | :---: | :---: |
| **Cepat (1-Pass)** | Kirim cepat (WhatsApp, chat) | ⚡⚡⚡ Cepat | Cukup Baik |
| **Akurat (2-Pass)** | Batas ketat (Discord, portal) | ⚡⚡ Sedang | 🎯 Sangat Presisi & Lebih Tajam |

---

## 📥 Download & Cara Menggunakan

Tidak perlu menginstal Python untuk memakai Bitapres.

1. Unduh file **`Bitapres-v1.1.0-Windows.zip`** di halaman [**Latest Release**](https://github.com/Bintang-AF/Bitapres/releases/latest).
2. Ekstrak seluruh isi ZIP ke satu folder *(pastikan `Bitapres.exe`, `ffmpeg.exe`, dan `ffprobe.exe` tetap berada di folder yang sama)*.
3. Klik dua kali **`Bitapres.exe`**.
4. Pilih video, masukkan target ukuran (MB), pilih mode **1-Pass** atau **2-Pass**, lalu klik **Mulai Kompres**.

> [!NOTE]
> **Windows SmartScreen:** Karena Bitapres adalah aplikasi *open-source* mandiri tanpa sertifikat digital berbayar, Windows mungkin menampilkan peringatan *"Windows protected your PC"*. Klik **More info** → **Run anyway** untuk tetap membukanya.

---

## 🛠️ Menjalankan dari Source Code (Developer)

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