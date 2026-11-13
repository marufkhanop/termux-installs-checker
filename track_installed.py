#!/usr/init/env python3
import os
import json
import sys
from pathlib import Path

LEDGER_DIR = Path.home() / ".config" / "package_tracker"
LEDGER_DIR.mkdir(parents=True, exist_ok=True)
LEDGER_FILE = LEDGER_DIR / "intentional_installs.json"

# Clean manual ledger for Termux and Pip ONLY
DEFAULT_LEDGER = {
    "Termux Tools": [
        "python",
        "python-pip",
        "git",
        "proot-distro"
    ],
    "Python Packages (Pip)": [
        "django",
        "django-htmx",
        "mutagen",
        "sqlparse",
        "asgiref"
    ]
}

def load_ledger():
    if not LEDGER_FILE.exists():
        save_ledger(DEFAULT_LEDGER)
    try:
        data = json.loads(LEDGER_FILE.read_text())
        for k in DEFAULT_LEDGER:
            if k not in data:
                data[k] = DEFAULT_LEDGER[k]
        return data
    except Exception:
        return DEFAULT_LEDGER

def save_ledger(data):
    LEDGER_FILE.write_text(json.dumps(data, indent=4))

def scan_dynamic_proots():
    """Dynamically scan Termux proot-distro directories for ANY installed Linux distros."""
    # Get Termux prefix dynamically from environment
    prefix = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
    rootfs_dir = Path(prefix) / "var" / "lib" / "proot-distro" / "installed-rootfs"
    
    distros = {}
    if rootfs_dir.exists():
        for distro_path in rootfs_dir.iterdir():
            if distro_path.is_dir():
                distro_name = distro_path.name
                markers = []
                
                # Check for OpenCode
                if (distro_path / "root" / ".opencode").exists():
                    markers.append("opencode (v2.2.5)")
                
                # Scan dpkg database inside the rootfs for user packages
                dpkg_status = distro_path / "var" / "lib" / "dpkg" / "status"
                if dpkg_status.exists():
                    content = dpkg_status.read_text(errors="ignore")
                    if "python3-pil" in content:
                        markers.append("python3-pil (Pillow)")
                    if "python3-venv" in content:
                        markers.append("python3-venv")
                        
                distros[distro_name] = markers if markers else ["Base rootfs installed"]
    return distros

def show_report():
    ledger = load_ledger()
    print("=" * 55)
    print("       🎯 TERMUX INSTALLS TRACKER - MRUFX    ")
    print("=" * 55)
    
    # Show manual Termux & Pip entries
    for category, items in ledger.items():
        print(f"\n[+] {category}:")
        if items:
            for item in items:
                print(f"  - {item}")
        else:
            print("  (None)")

    # Show dynamically discovered proot distros (Ubuntu, Kali, etc.)
    print("\n[+] Proot-Distro Environments (Dynamic):")
    detected_proots = scan_dynamic_proots()
    if detected_proots:
        for distro, details in detected_proots.items():
            print(f"  🐧 Distro: {distro.capitalize()}")
            for detail in details:
                print(f"    ↳ {detail}")
    else:
        print("  (No proot-distro environments found)")

    print("=" * 55)
    print("\nTip: Add manual items using: python track_installed.py add <termux|pip> <name>")

def add_item():
    if len(sys.argv) < 4:
        print("Usage: python track_installed.py add <termux|pip> <package_name>")
        return
    
    cat_arg = sys.argv[2].lower()
    item_name = sys.argv[3]
    
    ledger = load_ledger()
    target_key = "Termux Tools" if cat_arg == "termux" else "Python Packages (Pip)"
    
    if item_name not in ledger[target_key]:
        ledger[target_key].append(item_name)
        save_ledger(ledger)
        print(f"✅ Added '{item_name}' to {target_key}.")
    else:
        print(f"⚠️ '{item_name}' is already in the ledger.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "add":
        add_item()
    else:
        show_report()
