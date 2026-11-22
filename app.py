import math
import os
import threading
from tkinter import filedialog
import customtkinter as ctk
from engine import kompres_video

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BitapresApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bitapres v1.1.0 - Kompresor Video")
        self.geometry("460x400")
        self.resizable(False, False)

        self.path_video = ""
        self.cancel_event = threading.Event()

        # Judul Aplikasi
        self.label_judul = ctk.CTkLabel(self, text="Bitapres", font=("Arial", 26, "bold"))
        self.label_judul.pack(pady=(20, 5))

        self.label_sub = ctk.CTkLabel(self, text="Kompres video sesuai target ukuran (MB)", text_color="gray")
        self.label_sub.pack(pady=(0, 15))

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
        self.entry_target.insert(0, "8")
        self.entry_target.pack(side="left", padx=5)

        # Frame Tombol Mulai & Batal
        self.frame_aksi = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_aksi.pack(pady=10)

        self.btn_kompres = ctk.CTkButton(
            self.frame_aksi, text="Mulai Kompres", command=self.mulai_proses,
            fg_color="#28a745", hover_color="#218838"
        )
        self.btn_kompres.pack(side="left", padx=5)

        self.btn_batal = ctk.CTkButton(
            self.frame_aksi, text="Batal", command=self.batalkan_proses,
            fg_color="#dc3545", hover_color="#c82333", width=80, state="disabled"
        )
        self.btn_batal.pack(side="left", padx=5)

        # Progress Bar & Persentase
        self.progress_bar = ctk.CTkProgressBar(self, width=360)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(10, 2))

        self.label_persen = ctk.CTkLabel(self, text="0%", text_color="gray")
        self.label_persen.pack(pady=(0, 5))

        # Label Status
        self.label_status = ctk.CTkLabel(
            self, text="Siap digunakan", text_color="white", wraplength=400
        )
        self.label_status.pack(pady=5)

    def pilih_file(self):
        file_terpilih = filedialog.askopenfilename(
            title="Pilih Video",
            filetypes=[("File Video", "*.mp4 *.mkv *.mov *.avi")]
        )
        if file_terpilih:
            self.path_video = file_terpilih
            nama_file = os.path.basename(file_terpilih)
            self.label_file.configure(text=nama_file, text_color="white")
            self.progress_bar.set(0)
            self.label_persen.configure(text="0%")

    def mulai_proses(self):
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

        # Reset sakelar batal & progress bar
        self.cancel_event.clear()
        self.progress_bar.set(0)
        self.label_persen.configure(text="0%", text_color="white")

        self.btn_kompres.configure(state="disabled")
        self.btn_pilih.configure(state="disabled")
        self.btn_batal.configure(state="normal")
        self.label_status.configure(text="Sedang mengompres...", text_color="#ffc107")

        thread = threading.Thread(target=self.proses_kompresi, args=(target_mb,), daemon=True)
        thread.start()

    def batalkan_proses(self):
        """Menyalakan sinyal batal untuk menghentikan FFmpeg."""
        self.cancel_event.set()
        self.btn_batal.configure(state="disabled")
        self.label_status.configure(text="Membatalkan proses...", text_color="#ffc107")

    def update_progress(self, nilai):
        """Memperbarui progress bar secara aman dari background thread."""
        self.after(0, lambda: self._terapkan_progress(nilai))

    def _terapkan_progress(self, nilai):
        self.progress_bar.set(nilai)
        self.label_persen.configure(text=f"{int(nilai * 100)}%")

    def proses_kompresi(self, target_mb):
        berhasil = False
        pesan = "Terjadi kesalahan tidak terduga."
        try:
            nama_dasar, _ = os.path.splitext(self.path_video)
            output_path = f"{nama_dasar}_bitapres.mp4"
            berhasil, pesan, _ = kompres_video(
                self.path_video,
                output_path,
                target_mb,
                progress_callback=self.update_progress,
                cancel_event=self.cancel_event
            )
        except Exception as e:
            berhasil = False
            pesan = f"Error sistem: {e}"
        finally:
            self.after(0, lambda: self.selesai_proses(berhasil, pesan))

    def selesai_proses(self, berhasil, pesan):
        self.btn_kompres.configure(state="normal")
        self.btn_pilih.configure(state="normal")
        self.btn_batal.configure(state="disabled")

        if berhasil:
            self.progress_bar.set(1.0)
            self.label_persen.configure(text="100%", text_color="#28a745")
            self.label_status.configure(text=pesan, text_color="#28a745")
        else:
            self.progress_bar.set(0)
            self.label_persen.configure(text="0%", text_color="gray")
            self.label_status.configure(text=pesan, text_color="#ff4d4d")

if __name__ == "__main__":
    app = BitapresApp()
    app.mainloop()