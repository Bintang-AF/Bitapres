import math
import os
import threading
from tkinter import filedialog
import customtkinter as ctk
from engine import kompres_video, ambil_info_video

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BitapresApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Bitapres v1.1.0 - Kompresor Video")
        self.geometry("480x500")
        self.resizable(False, False)

        self.path_video = ""
        self.folder_output = ""
        self.cancel_event = threading.Event()

        # Judul Aplikasi
        self.label_judul = ctk.CTkLabel(self, text="Bitapres", font=("Arial", 26, "bold"))
        self.label_judul.pack(pady=(20, 5))

        self.label_sub = ctk.CTkLabel(self, text="Kompres video sesuai target ukuran (MB)", text_color="gray")
        self.label_sub.pack(pady=(0, 15))

        # Tombol Pilih Video & Info Metadata
        self.btn_pilih = ctk.CTkButton(self, text="Pilih File Video", command=self.pilih_file)
        self.btn_pilih.pack(pady=5)

        self.label_file = ctk.CTkLabel(self, text="Belum ada file dipilih", text_color="gray")
        self.label_file.pack(pady=(5, 0))

        self.label_info_video = ctk.CTkLabel(self, text="", text_color="#a0a0a0", font=("Arial", 12))
        self.label_info_video.pack(pady=(0, 10))

        # Pilihan Folder Output
        self.frame_output = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_output.pack(pady=5)

        self.btn_folder = ctk.CTkButton(
            self.frame_output, text="Folder Simpan", command=self.pilih_folder,
            fg_color="#3b3b3b", hover_color="#4f4f4f", width=110
        )
        self.btn_folder.pack(side="left", padx=5)

        self.label_folder = ctk.CTkLabel(
            self.frame_output, text="Default: Sama dengan video asli", text_color="gray", width=260, anchor="w"
        )
        self.label_folder.pack(side="left", padx=5)

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
        self.progress_bar = ctk.CTkProgressBar(self, width=380)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(10, 2))

        self.label_persen = ctk.CTkLabel(self, text="0%", text_color="gray")
        self.label_persen.pack(pady=(0, 5))

        # Label Status & Statistik Hasil
        self.label_status = ctk.CTkLabel(
            self, text="Siap digunakan", text_color="white", wraplength=420
        )
        self.label_status.pack(pady=5)

    def format_durasi(self, detik):
        menit, sisa_detik = divmod(int(detik), 60)
        return f"{menit:02d}:{sisa_detik:02d}"

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

            # Ambil dan tampilkan metadata video
            info = ambil_info_video(file_terpilih)
            if info:
                teks_info = (
                    f"{info['ukuran_mb']:.2f} MB  •  "
                    f"{self.format_durasi(info['durasi'])}  •  "
                    f"{info['resolusi']}  •  {info['fps']} FPS"
                )
                self.label_info_video.configure(text=teks_info, text_color="#a0a0a0")
            else:
                self.label_info_video.configure(text="Info video tidak terbaca", text_color="#ff4d4d")

    def pilih_folder(self):
        folder = filedialog.askdirectory(title="Pilih Folder Penyimpanan")
        if folder:
            self.folder_output = folder
            # Potong teks path jika terlalu panjang agar rapi
            tampilan = folder if len(folder) <= 35 else "..." + folder[-32:]
            self.label_folder.configure(text=tampilan, text_color="white")

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

        self.cancel_event.clear()
        self.progress_bar.set(0)
        self.label_persen.configure(text="0%", text_color="white")

        self.btn_kompres.configure(state="disabled")
        self.btn_pilih.configure(state="disabled")
        self.btn_folder.configure(state="disabled")
        self.btn_batal.configure(state="normal")
        self.label_status.configure(text="Sedang mengompres...", text_color="#ffc107")

        thread = threading.Thread(target=self.proses_kompresi, args=(target_mb,), daemon=True)
        thread.start()

    def batalkan_proses(self):
        self.cancel_event.set()
        self.btn_batal.configure(state="disabled")
        self.label_status.configure(text="Membatalkan proses...", text_color="#ffc107")

    def update_progress(self, nilai):
        self.after(0, lambda: self._terapkan_progress(nilai))

    def _terapkan_progress(self, nilai):
        self.progress_bar.set(nilai)
        self.label_persen.configure(text=f"{int(nilai * 100)}%")

    def proses_kompresi(self, target_mb):
        berhasil = False
        pesan = "Terjadi kesalahan tidak terduga."
        try:
            nama_file_dasar = os.path.splitext(os.path.basename(self.path_video))[0]
            folder_tujuan = self.folder_output if self.folder_output else os.path.dirname(self.path_video)
            output_path = os.path.join(folder_tujuan, f"{nama_file_dasar}_bitapres.mp4")

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
        self.btn_folder.configure(state="normal")
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