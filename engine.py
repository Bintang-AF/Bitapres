import os
import subprocess

def ambil_durasi(path_video):
    """Membaca durasi video dalam satuan detik menggunakan ffprobe."""
    perintah = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path_video
    ]
    hasil = subprocess.check_output(perintah).decode().strip()
    return float(hasil)

def kompres_video(input_path, output_path, target_mb):
    """Mengompres video agar ukurannya mendekati target_mb."""
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' tidak ditemukan!")
        return False

    print(f"Membaca durasi {input_path}...")
    durasi = ambil_durasi(input_path)

    # Rumus konversi: 1 MB = 8192 kilobit.
    # Kita ambil 95% dari target sebagai ruang aman agar hasil tidak lewat batas.
    total_bitrate = (target_mb * 8192 * 0.95) / durasi
    audio_bitrate = 128  # Standar audio jernih (128 kbps)
    video_bitrate = total_bitrate - audio_bitrate

    # Jika durasi terlalu panjang untuk target MB yang terlalu kecil
    if video_bitrate <= 50:
        print("Error: Target ukuran terlalu kecil untuk durasi video ini!")
        return False

    print(f"Durasi: {durasi:.1f} detik | Target Video Bitrate: {int(video_bitrate)} kbps")
    print("Sedang mengompres... (tunggu sebentar)")

    perintah_ffmpeg = [
        "ffmpeg", "-y",                 # -y artinya timpa file lama jika namanya sama
        "-i", input_path,               # File sumber
        "-b:v", f"{int(video_bitrate)}k", # Target bitrate video
        "-b:a", f"{audio_bitrate}k",    # Target bitrate audio
        output_path                     # File hasil
    ]

    # Jalankan FFmpeg. stdout & stderr disembunyikan agar terminal tidak penuh teks rumit
    subprocess.run(perintah_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    ukuran_akhir = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Selesai! Ukuran hasil: {ukuran_akhir:.2f} MB (Disimpan di: {output_path})")
    return True

# Bagian ini hanya berjalan jika file engine.py dijalankan langsung
if __name__ == "__main__":
    kompres_video("tes.mp4", "hasil_kompres.mp4", 8)