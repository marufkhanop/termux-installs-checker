# termux-installs-checker
# Termux & Proot Package Tracker

If you use **Termux** regularly for coding or testing projects, you probably know how fast things pile up. After a few weeks of installing tools, trying out scripts, and pulling in Python libraries, your phone storage gets cluttered—and it gets hard to remember what you actually installed yourself.

Running standard package manager commands (`dpkg` or `apt`) dumps a huge list of background system dependencies and libraries (`libssl`, `make`, `nano`, etc.) that you never directly asked for. It makes it really tough to see what **you** intentionally put on your device.

I made this lightweight Python script to fix that. It keeps a clean personal record of your manual installs in Termux and Pip, while **automatically scanning** your proot-distro environments (like Ubuntu, Kali, Debian, etc.) to show what is installed inside them.

---

## What It Does

* **No Dependency Noise:** Ignores background system libraries and package manager clutter so you only see the tools you actually care about.
* **Manual Ledger for Termux & Pip:** Keeps a persistent JSON record of your core Termux tools and global Python packages.
* **Dynamic Proot Scanning:** Automatically detects any installed Linux distros inside Termux (`proot-distro`) without hardcoding anything. If you install Kali or Arch later, it shows up automatically.
* **Environment Markers:** Checks proot rootfs filesystems to detect custom setups (like OpenCode, `venv` tools, or Pillow) on the fly.

---

## Requirements

* Android device with **Termux** installed
* **Python 3** (`pkg install python`)
* *(Optional)* `proot-distro` if you run Linux containers inside Termux

---

## How to Use It

### 1. Get the Script
Save `track_installed.py` anywhere in your Termux storage (for example, inside your home directory `~/` or a scripts folder).

### 2. Run the Report
Run the script directly from **native Termux** (outside of any proot shell):

```bash
python track_installed.py
```

It will print out a clean, structured summary showing:
1. Your intentionally installed Termux tools
2. Your intentionally installed Python (`pip`) packages
3. All active `proot-distro` Linux environments and their detected additions

---

## Adding New Installs

Whenever you intentionally install a new tool or Python library down the road, log it into your tracker using the `add` command:

```bash
# Track a new Termux package
python track_installed.py add termux htop

# Track a new Python package
python track_installed.py add pip requests
```

> **Note:** You don't need to manually add proot distributions (like Ubuntu or Kali)—the script scans your Termux `proot-distro` folder automatically every time you run it.

---

## Where Data is Stored

Your manual tracking list is stored locally in a simple JSON file:

```text
~/.config/package_tracker/intentional_installs.json
```

If you ever switch devices or reset Termux, just back up this single `.json` file alongside `track_installed.py` to keep your full history intact.
