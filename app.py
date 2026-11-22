import math
import os
import threading
from tkinter import filedialog
import customtkinter as ctk
from engine import kompres_video

# Atur tema tampilan jadi gelap dan warna tombol biru
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BitapresApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bitapres - Kompresor Video")
        self.geometry("450x320")
        self.resizable(False, False)

        self.path_video = ""

        # Judul Aplikasi
        self.label_judul = ctk.CTkLabel(self, text="Bitapres", font=("Arial", 26, "bold"))
        self.label_judul.pack(pady=(20, 5))

        self.label_sub = ctk.CTkLabel(self, text="Kompres video sesuai target ukuran (MB)", text_color="gray")
        self.label_sub.pack(pady=(0, 20))

        # Tombol Pilih Video
        self.btn_pilih = ctk.CTkButton(self, text="Pilih File Video", command=self.pilih_file)
        self.btn_pilih.pack(pady=5)

        self.label_file = ctk.CTkLabel(self, text="Belum ada file dipilih", text_color="gray")
        self.label_file.pack(pady=5)

        # Input Target MB
        self.frame_target = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_target.pack(pady=10)

        self.label_target = ctk.CTkLabel(self.frame_target, text="Target Ukuran (MB):")
        self.label_target.pack(side="left", padx=5)

        self.entry_target = ctk.CTkEntry(self.frame_target, width=70)
        self.entry_target.insert(0, "8")  # Nilai bawaan 8 MB (aman untuk Discord)
        self.entry_target.pack(side="left", padx=5)

        # Tombol Eksekusi
        self.btn_kompres = ctk.CTkButton(
            self, text="Mulai Kompres", command=self.mulai_proses,
            fg_color="#28a745", hover_color="#218838"
        )
        self.btn_kompres.pack(pady=15)

        # Label Status
        self.label_status = ctk.CTkLabel(
            self, text="Siap digunakan", text_color="white", wraplength=400
        )
        self.label_status.pack(pady=5)

    def pilih_file(self):
        """Membuka jendela File Explorer untuk memilih video."""
        file_terpilih = filedialog.askopenfilename(
            title="Pilih Video",
            filetypes=[("File Video", "*.mp4 *.mkv *.mov *.avi")]
        )
        if file_terpilih:
            self.path_video = file_terpilih
            nama_file = os.path.basename(file_terpilih)
            self.label_file.configure(text=nama_file, text_color="white")

    def mulai_proses(self):
        """Validasi input lalu jalankan kompresi di thread terpisah."""
        if not self.path_video:
            self.label_status.configure(text="Pilih file video dulu!", text_color="#ff4d4d")
            return

        try:
            target_mb = float(self.entry_target.get())
            if target_mb <= 0:
                raise ValueError
        except ValueError:
            self.label_status.configure(text="Masukkan angka MB yang valid!", text_color="#ff4d4d")
            return

        # Kunci tombol agar tidak diklik dua kali saat memproses
        self.btn_kompres.configure(state="disabled")
        self.btn_pilih.configure(state="disabled")
        self.label_status.configure(text="Sedang mengompres... mohon tunggu", text_color="#ffc107")

        # Jalankan fungsi proses_kompresi di jalur terpisah (thread)
        thread = threading.Thread(target=self.proses_kompresi, args=(target_mb,), daemon=True)
        thread.start()

    def proses_kompresi(self, target_mb):
        """Memanggil engine.py dan memperbarui status setelah selesai."""
        nama_dasar, _ = os.path.splitext(self.path_video)
        output_path = f"{nama_dasar}_bitapres.mp4"

        berhasil = kompres_video(self.path_video, output_path, target_mb)

        # Kembalikan tampilan ke kondisi siap (pakai self.after agar aman di thread)
        self.after(0, lambda: self.selesai_proses(berhasil, output_path))

    def selesai_proses(self, berhasil, output_path):
        self.btn_kompres.configure(state="normal")
        self.btn_pilih.configure(state="normal")

        if berhasil:
            ukuran = os.path.getsize(output_path) / (1024 * 1024)
            self.label_status.configure(
                text=f"Selesai! Hasil: {ukuran:.2f} MB (folder sama)", text_color="#28a745"
            )
        else:
            self.label_status.configure(
                text="Gagal! Target MB terlalu kecil untuk durasi video.", text_color="#ff4d4d"
            )

if __name__ == "__main__":
    app = BitapresApp()
    app.mainloop()