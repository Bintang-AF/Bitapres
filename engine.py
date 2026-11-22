import glob
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

def cari_binary(nama_exe):
    """Mencari ffmpeg.exe / ffprobe.exe di folder aplikasi dulu, baru ke PATH sistem."""
    if getattr(sys, "frozen", False):
        folder_app = os.path.dirname(sys.executable)
    else:
        folder_app = os.path.dirname(os.path.abspath(__file__))

    lokasi_lokal = os.path.join(folder_app, f"{nama_exe}.exe")
    if os.path.isfile(lokasi_lokal):
        return lokasi_lokal

    return shutil.which(nama_exe)

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

def ambil_info_video(path_video):
    """Membaca metadata video (ukuran, durasi, resolusi, FPS) sekaligus lewat FFprobe JSON."""
    path_ffprobe = cari_binary("ffprobe")
    if not path_ffprobe or not os.path.isfile(path_video):
        return None

    perintah = [
        path_ffprobe, "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-show_entries", "format=duration",
        "-of", "json",
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
            return None

        data = json.loads(hasil.stdout)
        stream = data.get("streams", [{}])[0]
        fmt = data.get("format", {})

        lebar = stream.get("width", 0)
        tinggi = stream.get("height", 0)
        durasi = float(fmt.get("duration", 0))
        ukuran_mb = os.path.getsize(path_video) / (1024 * 1024)

        fps_str = stream.get("r_frame_rate", "0/1")
        if "/" in fps_str:
            pembilang, penyebut = fps_str.split("/")
            fps = float(pembilang) / float(penyebut) if float(penyebut) != 0 else 0
        else:
            fps = float(fps_str)

        return {
            "ukuran_mb": ukuran_mb,
            "durasi": durasi,
            "resolusi": f"{lebar}x{tinggi}" if lebar and tinggi else "Tidak diketahui",
            "fps": round(fps)
        }
    except Exception:
        return None

def _jalankan_ffmpeg(perintah, durasi, progress_callback=None, cancel_event=None, offset=0.0, skala=1.0):
    """Menjalankan satu proses FFmpeg sambil memantau progres dan sinyal batal."""
    try:
        proses = subprocess.Popen(
            perintah,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        )

        for baris in proses.stdout:
            if cancel_event and cancel_event.is_set():
                proses.terminate()
                proses.wait()
                return "CANCELLED", "Kompresi dibatalkan oleh pengguna."

            baris = baris.strip()
            if baris.startswith("out_time_us="):
                nilai = baris.split("=", 1)[1]
                if nilai.isdigit():
                    detik_berjalan = int(nilai) / 1_000_000
                    persen_lokal = min(max(detik_berjalan / durasi, 0.0), 1.0)
                    if progress_callback:
                        progress_callback(offset + (persen_lokal * skala))

        proses.wait()
        stderr_output = proses.stderr.read().strip()

        if proses.returncode != 0:
            baris_err = stderr_output.splitlines()
            detail = baris_err[-1] if baris_err else "Kode error tidak diketahui."
            return "ERROR", f"FFmpeg gagal memproses video: {detail}"

        return "OK", None
    except Exception as e:
        return "ERROR", f"Gagal menjalankan FFmpeg: {e}"

def _hapus_file_aman(path_file):
    if path_file and os.path.exists(path_file):
        try:
            os.remove(path_file)
        except OSError:
            pass

def kompres_video(input_path, output_path, target_mb, mode="1-pass", progress_callback=None, cancel_event=None):
    """
    mode: "1-pass" (cepat) atau "2-pass" (akurat & kualitas lebih baik).
    Mengembalikan tuple: (berhasil: bool, pesan: str, final_output_path: str | None)
    """
    if not isinstance(target_mb, (int, float)) or not math.isfinite(target_mb) or target_mb <= 0:
        return False, "Target ukuran harus berupa angka positif yang valid.", None

    if not input_path or not os.path.isfile(input_path):
        return False, "File video tidak ditemukan atau sudah dipindahkan.", None

    path_ffmpeg = cari_binary("ffmpeg")
    path_ffprobe = cari_binary("ffprobe")
    if not path_ffmpeg or not path_ffprobe:
        return False, "ffmpeg.exe atau ffprobe.exe tidak ditemukan.", None

    durasi, err_durasi = ambil_durasi(input_path, path_ffprobe)
    if err_durasi:
        return False, err_durasi, None

    audio_bitrate = 128
    min_video_bitrate = 50
    total_bitrate = (target_mb * 8192 * 0.95) / durasi
    video_bitrate = total_bitrate - audio_bitrate

    if video_bitrate < min_video_bitrate:
        min_mb = ((min_video_bitrate + audio_bitrate) * durasi) / (8192 * 0.95)
        return (
            False,
            f"Target {target_mb} MB terlalu kecil untuk durasi {durasi:.0f} detik. "
            f"Minimal disarankan sekitar {min_mb:.2f} MB.",
            None
        )

    final_output = buat_path_unik(output_path)

    if mode == "2-pass":
        # Simpan file log sementara 2-pass di folder Temp sistem
        log_prefix = os.path.join(tempfile.gettempdir(), f"bitapres_pass_{os.getpid()}")
        try:
            # Pass 1: Analisis video (0% -> 50%)
            cmd_pass1 = [
                path_ffmpeg, "-y", "-v", "error",
                "-i", input_path,
                "-c:v", "libx264",
                "-b:v", f"{int(video_bitrate)}k",
                "-pass", "1",
                "-passlogfile", log_prefix,
                "-an", "-f", "mp4",
                "-progress", "pipe:1", "-nostats",
                os.devnull
            ]
            status, pesan_err = _jalankan_ffmpeg(
                cmd_pass1, durasi, progress_callback, cancel_event, offset=0.0, skala=0.5
            )
            if status != "OK":
                return False, pesan_err, None

            # Pass 2: Kompresi aktual (50% -> 100%)
            cmd_pass2 = [
                path_ffmpeg, "-y", "-v", "error",
                "-i", input_path,
                "-c:v", "libx264",
                "-b:v", f"{int(video_bitrate)}k",
                "-pass", "2",
                "-passlogfile", log_prefix,
                "-c:a", "aac", "-b:a", f"{audio_bitrate}k",
                "-progress", "pipe:1", "-nostats",
                final_output
            ]
            status, pesan_err = _jalankan_ffmpeg(
                cmd_pass2, durasi, progress_callback, cancel_event, offset=0.5, skala=0.5
            )
            if status != "OK":
                _hapus_file_aman(final_output)
                return False, pesan_err, None
        finally:
            # Bersihkan semua file log sementara milik 2-pass
            for file_log in glob.glob(f"{log_prefix}*"):
                _hapus_file_aman(file_log)
    else:
        # Mode 1-Pass (0% -> 100%)
        cmd_1pass = [
            path_ffmpeg, "-y", "-v", "error",
            "-i", input_path,
            "-c:v", "libx264",
            "-b:v", f"{int(video_bitrate)}k",
            "-c:a", "aac", "-b:a", f"{audio_bitrate}k",
            "-progress", "pipe:1", "-nostats",
            final_output
        ]
        status, pesan_err = _jalankan_ffmpeg(
            cmd_1pass, durasi, progress_callback, cancel_event, offset=0.0, skala=1.0
        )
        if status != "OK":
            _hapus_file_aman(final_output)
            return False, pesan_err, None

    if not os.path.isfile(final_output) or os.path.getsize(final_output) == 0:
        return False, "File hasil tidak terbentuk atau ukurannya 0 byte.", None

    _, err_hasil = ambil_durasi(final_output, path_ffprobe)
    if err_hasil:
        return False, "File hasil terbentuk, tetapi rusak/tidak dapat dibaca.", None

    if progress_callback:
        progress_callback(1.0)

    ukuran_awal = os.path.getsize(input_path) / (1024 * 1024)
    ukuran_akhir = os.path.getsize(final_output) / (1024 * 1024)
    nama_hasil = os.path.basename(final_output)

    if ukuran_awal > 0 and ukuran_akhir < ukuran_awal:
        hemat_persen = ((ukuran_awal - ukuran_akhir) / ukuran_awal) * 100
        info_hemat = f"Hemat {hemat_persen:.1f}%"
    else:
        info_hemat = "Ukuran tidak menyusut"

    return (
        True,
        f"Selesai! {nama_hasil}\n{ukuran_awal:.2f} MB → {ukuran_akhir:.2f} MB ({info_hemat})",
        final_output
    )