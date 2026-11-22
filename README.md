<div align="center">

# 🎬 Bitapres

**Compress videos to your exact target size (MB) — 100% offline, fast, and private.**

🌐 **English** | [Bahasa Indonesia](README.id.md)

[![Latest Release](https://img.shields.io/github/v/release/Bintang-AF/Bitapres?style=for-the-badge&color=28a745)](https://github.com/Bintang-AF/Bitapres/releases/latest)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](#download--quick-start)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

[Download v1.1.0](https://github.com/Bintang-AF/Bitapres/releases/latest) • [Features](#-key-features) • [1-Pass vs 2-Pass](#-compression-modes) • [Roadmap](#-roadmap)

</div>

---

<!-- Uncomment the line below after adding your screenshot to assets/screenshot.png -->
<!-- <p align="center"><img src="assets/screenshot.png" alt="Bitapres UI" width="500"></p> -->

## 💡 Why Bitapres?

Need to shrink a gaming clip under **10 MB for Discord** or compress a video assignment for a campus portal without uploading private files to ad-filled websites? **Bitapres** calculates the exact bitrate needed and compresses your video locally using FFmpeg—no internet, no watermarks, no file size upload limits.

---

## ✨ Key Features (v1.1.0)

* 🎯 **Target-Size Precision:** Enter your desired size in MB, and Bitapres automatically calculates the optimal bitrate to stay right under your limit.
* 📊 **Real-Time Progress & Cancel:** Track actual FFmpeg encoding progress (0%–100%) in real time, or cancel anytime with automatic cleanup of incomplete files.
* 🔍 **Instant Video Metadata:** Automatically inspects and displays file size, duration, resolution, and FPS right after you pick a video.
* ⚡ **1-Pass & 2-Pass Modes:** Choose between fast encoding or high-precision 2-Pass encoding for sharper quality at the exact target size.
* 📁 **Custom Output Folder & Savings Stats:** Pick where to save your compressed file and see exactly how much space you saved (e.g., `20.4 MB → 7.4 MB • Saved 63.7%`).
* 🛡️ **Smart Safety Guards:** Prevents overwriting existing files (`_1`, `_2`, etc.), validates corrupted videos, and warns you with realistic minimum MB recommendations if the target is too small.

---

## ⚙️ Compression Modes

| Mode | Best For | Speed | Size Accuracy & Quality |
| :--- | :--- | :---: | :---: |
| **Fast (1-Pass)** | Quick sharing (WhatsApp, chat) | ⚡⚡⚡ Fast | Good |
| **Accurate (2-Pass)** | Strict limits (Discord, portals) | ⚡⚡ Moderate | 🎯 High Precision & Sharper |

---

## 📥 Download & Quick Start

No Python installation required.

1. Download **`Bitapres-v1.1.0-Windows.zip`** from the [**Latest Release page**](https://github.com/Bintang-AF/Bitapres/releases/latest).
2. Extract all files into a single folder *(keep `Bitapres.exe`, `ffmpeg.exe`, and `ffprobe.exe` together)*.
3. Double-click **`Bitapres.exe`**.
4. Select your video, set the target size (MB), choose **1-Pass** or **2-Pass**, and click **Mulai Kompres**.

> [!NOTE]
> **Windows SmartScreen:** Because Bitapres is an independent open-source app without a paid digital certificate, Windows may display *"Windows protected your PC"*. Click **More info** → **Run anyway** to launch it.

---

## 🛠️ Run from Source (Developers)

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

# 4. Run the app
python app.py