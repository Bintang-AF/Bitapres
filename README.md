# Bitapres

🌐 **Language:** **English** | [Bahasa Indonesia](README.id.md)

![GitHub release (latest by date)](https://img.shields.io/github/v/release/Bintang-AF/Bitapres?style=flat-square&color=blue)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?style=flat-square&logo=windows)
![Python](https://img.shields.io/badge/python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white)

**Bitapres** is a local desktop application built with Python and FFmpeg to compress videos to a specific **target file size (MB)** completely offline. Ideal for shrinking gaming clips to fit Discord's upload limit (<10 MB) or submitting video assignments without uploading private files to ad-filled online compressors.

<!-- Uncomment the line below after adding your screenshot to assets/screenshot.png -->
<!-- ![Bitapres Screenshot](assets/screenshot.png) -->

---

## Key Features (v1.0.1)

- **Target-Size Compression (MB):** Automatically calculates the required video bitrate so the output stays as close as possible to your target size without exceeding it.
- **100% Local & Private:** Runs entirely on your machine—no internet connection, no file upload limits, and no ads.
- **Common Format Support:** Supports `.mp4`, `.mkv`, `.mov`, and `.avi`.
- **Strict Validation & Safety:** Rejects invalid inputs, calculates realistic minimum MB recommendations if the target is too small, and prevents overwriting existing files by auto-numbering (`_1`, `_2`, etc.).
- **Lightweight UI (Dark Mode):** Built with CustomTkinter and background threading to keep the interface responsive during compression.

---

## Download & Usage (End Users)

No Python installation is required to run Bitapres.

1. Download **`Bitapres-v1.0.1-Windows.zip`** from the [**Latest Release page**](https://github.com/Bintang-AF/Bitapres/releases/latest).
2. Extract all files into a single folder. Make sure `Bitapres.exe`, `ffmpeg.exe`, and `ffprobe.exe` stay in the same directory.
3. Double-click **`Bitapres.exe`** to launch the app.
4. Select your video, enter the target size (MB), and click **Mulai Kompres**. The compressed file will be saved in the same folder as the original video.

> **Windows SmartScreen Note:** Because this app is not signed with a paid digital certificate, Windows SmartScreen may show *"Windows protected your PC"*. Click **More info**, then select **Run anyway**.

---

## Running from Source Code (Developers)

**Prerequisites:** Python 3.12+ and [FFmpeg](https://ffmpeg.org/) installed in your system PATH.

```bash
# 1. Clone the repository
git clone [https://github.com/Bintang-AF/Bitapres.git](https://github.com/Bintang-AF/Bitapres.git)
cd Bitapres

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
