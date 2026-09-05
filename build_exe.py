"""PyInstaller build script to generate standalone Windows executable."""
import subprocess
import sys

def build():
    print("Building standalone RedragonRGB.exe...")
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name",
        "OpenRGBFlowers",
        "--paths",
        "src",
        "--collect-all",
        "openrgb_flowers",
        "--hidden-import",
        "hid",
        "--hidden-import",
        "openrgb",
        "--clean",
        "-y",
        "launcher.py",
    ]
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("\n[SUCCESS] Standalone executable generated at: dist/OpenRGBFlowers.exe")
    else:
        print(f"\n[ERROR] Build failed with exit code: {result.returncode}")
    return result.returncode

if __name__ == "__main__":
    sys.exit(build())
