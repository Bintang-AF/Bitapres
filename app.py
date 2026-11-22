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
        """Validasi input ketat lalu jalankan kompresi di thread terpisah."""
        if not self.path_video or not os.path.isfile(self.path_video):
            self.label_status.configure(text="Pilih file video yang valid dulu!", text_color="#ff4d4d")
            return

        teks_target = self.entry_target.get().strip().replace(",", ".")
        try:
            target_mb = float(teks_target)
            if not math.isfinite(target_mb) or target_mb <= 0:
                raise ValueError
        except ValueError:
            self.label_status.configure(
                text="Masukkan angka target MB positif yang valid (contoh: 8).",
                text_color="#ff4d4d"
            )
            return

        self.btn_kompres.configure(state="disabled")
        self.btn_pilih.configure(state="disabled")
        self.label_status.configure(text="Sedang mengompres... mohon tunggu", text_color="#ffc107")

        thread = threading.Thread(target=self.proses_kompresi, args=(target_mb,), daemon=True)
        thread.start()

    def proses_kompresi(self, target_mb):
        """Menjalankan engine.py dengan pengaman try-except-finally agar GUI tidak pernah nyangkut."""
        berhasil = False
        pesan = "Terjadi kesalahan tidak terduga."
        try:
            nama_dasar, _ = os.path.splitext(self.path_video)
            output_path = f"{nama_dasar}_bitapres.mp4"
            berhasil, pesan, _ = kompres_video(self.path_video, output_path, target_mb)
        except Exception as e:
            berhasil = False
            pesan = f"Error sistem: {e}"
        finally:
            # Dijamin selalu dipanggil apa pun yang terjadi
            self.after(0, lambda: self.selesai_proses(berhasil, pesan))

    def selesai_proses(self, berhasil, pesan):
        self.btn_kompres.configure(state="normal")
        self.btn_pilih.configure(state="normal")
        warna = "#28a745" if berhasil else "#ff4d4d"
        self.label_status.configure(text=pesan, text_color=warna)

if __name__ == "__main__":
    app = BitapresApp()
    app.mainloop()