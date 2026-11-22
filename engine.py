import math
import os
import shutil
import subprocess
import sys

def cari_binary(nama_exe):
    """Mencari ffmpeg.exe / ffprobe.exe di folder aplikasi dulu, baru ke PATH sistem."""
    if getattr(sys, "frozen", False):
        # Jika dijalankan sebagai .exe hasil PyInstaller
        folder_app = os.path.dirname(sys.executable)
    else:
        # Jika dijalankan sebagai script Python biasa
        folder_app = os.path.dirname(os.path.abspath(__file__))

    lokasi_lokal = os.path.join(folder_app, f"{nama_exe}.exe")
    if os.path.isfile(lokasi_lokal):
        return lokasi_lokal

    # Fallback: cari di Environment Variables (PATH) Windows
    lokasi_sistem = shutil.which(nama_exe)
    if lokasi_sistem:
        return lokasi_sistem

    return None

def buat_path_unik(output_path):
    """Mencegah file tertimpa dengan menambah angka (_1, _2, dst.) jika sudah ada."""
    if not os.path.exists(output_path):
        return output_path

    nama_dasar, ekstensi = os.path.splitext(output_path)
    angka = 1
    while True:
        kandidat = f"{nama_dasar}_{angka}{ekstensi}"
        if not os.path.exists(kandidat):
            return kandidat
        angka += 1

def ambil_durasi(path_video, path_ffprobe):
    """Membaca durasi video dengan penanganan error lengkap."""
    perintah = [
        path_ffprobe, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path_video
    ]
    try:
        hasil = subprocess.run(
            perintah,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        )
        if hasil.returncode != 0:
            return None, "File video rusak atau formatnya tidak didukung."

        durasi = float(hasil.stdout.strip())
        if not math.isfinite(durasi) or durasi <= 0:
            return None, "Metadata durasi video tidak valid atau kosong."
        return durasi, None
    except ValueError:
        return None, "Gagal membaca durasi. Pastikan file benar-benar berisi video."
    except Exception as e:
        return None, f"Gagal menjalankan FFprobe: {e}"

def kompres_video(input_path, output_path, target_mb):
    """
    Mengembalikan tuple: (berhasil: bool, pesan: str, final_output_path: str | None)
    """
    # Poin 4: Validasi input target MB (tolak <= 0, NaN, Infinity)
    if not isinstance(target_mb, (int, float)) or not math.isfinite(target_mb) or target_mb <= 0:
        return False, "Target ukuran harus berupa angka positif yang valid.", None

    # Poin 5: Validasi keberadaan file video
    if not input_path or not os.path.isfile(input_path):
        return False, "File video tidak ditemukan atau sudah dipindahkan.", None

    # Poin 8: Pastikan ffmpeg & ffprobe tersedia
    path_ffmpeg = cari_binary("ffmpeg")
    path_ffprobe = cari_binary("ffprobe")
    if not path_ffmpeg or not path_ffprobe:
        return False, "ffmpeg.exe atau ffprobe.exe tidak ditemukan di folder aplikasi maupun sistem.", None

    # Poin 2: Ambil durasi dengan error handling
    durasi, err_durasi = ambil_durasi(input_path, path_ffprobe)
    if err_durasi:
        return False, err_durasi, None

    # Poin 9: Hitung bitrate & tangani target terlalu kecil dengan pesan informatif
    audio_bitrate = 128  # kbps
    min_video_bitrate = 50  # kbps (batas bawah agar video tidak rusak)
    total_bitrate = (target_mb * 8192 * 0.95) / durasi
    video_bitrate = total_bitrate - audio_bitrate

    if video_bitrate < min_video_bitrate:
        # Hitung batas minimal MB yang realistis untuk durasi video ini
        min_mb = ((min_video_bitrate + audio_bitrate) * durasi) / (8192 * 0.95)
        return (
            False,
            f"Target {target_mb} MB terlalu kecil untuk durasi {durasi:.0f} detik. "
            f"Minimal disarankan sekitar {min_mb:.2f} MB.",
            None
        )

    # Poin 7: Cegah output tertimpa
    final_output = buat_path_unik(output_path)

    perintah_ffmpeg = [
        path_ffmpeg, "-y",
        "-i", input_path,
        "-b:v", f"{int(video_bitrate)}k",
        "-b:a", f"{audio_bitrate}k",
        final_output
    ]

    # Poin 1: Cek kode keluar (returncode) FFmpeg
    try:
        proses = subprocess.run(
            perintah_ffmpeg,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        )
        if proses.returncode != 0:
            # Ambil baris terakhir stderr sebagai ringkasan error
            baris_err = proses.stderr.strip().splitlines()
            detail = baris_err[-1] if baris_err else "Kode error tidak diketahui."
            return False, f"FFmpeg gagal memproses video: {detail}", None
    except Exception as e:
        return False, f"Gagal menjalankan FFmpeg: {e}", None

    # Poin 6: Periksa hasil kompresi (ada, tidak kosong, bisa dibaca ffprobe)
    if not os.path.isfile(final_output) or os.path.getsize(final_output) == 0:
        return False, "File hasil tidak terbentuk atau ukurannya 0 byte.", None

    durasi_hasil, err_hasil = ambil_durasi(final_output, path_ffprobe)
    if err_hasil:
        return False, "File hasil terbentuk, tetapi rusak/tidak dapat dibaca.", None

    ukuran_akhir = os.path.getsize(final_output) / (1024 * 1024)
    nama_hasil = os.path.basename(final_output)
    return True, f"Selesai! {nama_hasil} ({ukuran_akhir:.2f} MB)", final_output