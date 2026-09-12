# 🌸 OpenRGB Flowers Blooming & Chromatic Blend

[![CI](https://github.com/Dhionata/RGB-Redragon/actions/workflows/ci.yml/badge.svg)](https://github.com/Dhionata/RGB-Redragon/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows | Linux](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)](https://github.com/Dhionata/RGB-Redragon)

High-performance, procedural, organic RGB lighting effects engineered specifically for the **Redragon K556RGB-M** (Devarajas) mechanical keyboard and compatible across the broader **OpenRGB** ecosystem.

Featuring **two exclusive lighting engines**, **8 refined color palettes**, **direct native USB HID communication** (eliminating the need for third-party software), a **modern dark-themed graphical interface (GUI)** with real-time physical keyboard preview, **hot-reload controls**, support for a **standalone executable (.exe)**, and **Windows Auto-Start**.

---

## 📑 Table of Contents

- [Project Highlights](#-project-highlights)
- [Lighting Engines in Detail](#-lighting-engines-in-detail)
  - [1. Flowers Blooming (`blooming`)](#1--flowers-blooming-blooming)
  - [2. Random Matrix Blend (`random_blend`)](#2--random-matrix-blend-random_blend)
- [Color Palettes](#-color-palettes)
- [Interactive Graphical User Interface (GUI)](#-interactive-graphical-user-interface-gui)
- [Standalone Executable (.exe) & Running Without PowerShell](#-standalone-executable-exe--running-without-powershell)
- [Windows Auto-Start on Boot](#-windows-auto-start-on-boot)
- [Command-Line Interface (CLI) Reference](#-command-line-interface-cli-reference)
- [Configuration File (`config.json`)](#-configuration-file-configjson)
- [Hardware Protocol & Reverse Engineering](#-hardware-protocol--reverse-engineering)
- [Software Architecture (SOLID & DRY)](#-software-architecture-solid--dry)
- [Repository Directory Structure](#-repository-directory-structure)
- [Automated Tests & CI](#-automated-tests--ci)

---

## ✨ Project Highlights

- **Zero-Allocation Rendering**: Geometry and color math are 100% vectorized using **NumPy**, computing each frame in under `0.1 ms` with CPU usage below `0.5%`.
- **Direct USB HID Transmission**: Native communication with the Redragon K556RGB-M microcontroller (`VID: 0x2E3C, PID: 0xC365, Interface 2`) in Mode 10 via command `0x09`, without depending on proprietary drivers or bloated background software.
- **Two Distinct Lighting Philosophies**:
  - *Flowers Blooming*: Organic floral blossoms that sprout, expand harmonic lobes, and softly dissolve.
  - *Random Matrix Blend*: **100% of keys remain constantly illuminated**, shifting asynchronously between random palette stops using cubic Hermite (*smoothstep*) interpolation.
- **Interactive GUI with Live 2D Layout Preview**: Animated canvas displaying the physical keyboard matrix in real time before and during execution.
- **Hot-Reload Controls ("✓ Apply" and "⟲ Undo")**: Modify palette, speed, brightness, saturation, and effect types on the fly without interrupting USB transmission.
- **Native Windows Installer & Portable Binary (`FlowersBlooming_Setup.exe` / `FlowersBlooming.exe`)**: Zero-dependency standalone C++ compilation via Nuitka with an automated Inno Setup installer, desktop shortcuts, and auto-start.

---

## 🎨 Lighting Engines in Detail

### 1. 🌸 Flowers Blooming (`blooming`)

- **Mathematical Concept**:
  Each flower spawns stochastically across the $(x, y)$ key matrix. Petals are parameterized by polar harmonic functions:
  $$r(\theta) = R \cdot \left(1 + \epsilon \cos(k \theta)\right)$$
  where $k \in \{4, 5, 6, 8\}$ governs the number of lobes and $\epsilon$ dictates edge waviness.
- **Temporal Progression**:
  - **Sprout Phase (0.0 to 0.3)**: Central floral stamen emerges and rapidly expands from the palette's primary tone.
  - **Full Bloom Phase (0.3 to 0.7)**: Petals unfurl fully with radial gradients fading outward toward the petal tips.
  - **Dissipation Phase (0.7 to 1.0)**: Petals gently decay through natural light fading.
- **Color Blending Strategies**:
  When multiple flower lobes overlap, the engine calculates combined light using one of three strategies:
  - `weighted` (default): Weighted average preserving chromatic balance.
  - `screen`: Screen blending formula ($1 - (1-a)(1-b)$), yielding luminous floral overlays.
  - `additive`: Pure photon addition clamped at 255.
- **Ambient Breathing Breeze**: A gentle sinusoidal background current in subtle earthy/emerald tones prevents the keyboard from going entirely dark between blooms.

### 2. ✨ Random Matrix Blend (`random_blend`)

- **Concept**:
  Designed for users who want **every single key illuminated simultaneously at all times**. Each physical key runs an independent, asynchronous color state machine.
- **Smooth Transition (Smoothstep)**:
  Color transitions from current color $C_0$ to next randomly chosen palette target $C_1$ occur along a cubic Hermite polynomial:
  $$t_{\text{smooth}} = 3t^2 - 2t^3$$
  $$C(t) = C_0 \cdot (1 - t_{\text{smooth}}) + C_1 \cdot t_{\text{smooth}}$$
  This eliminates jarring acceleration spikes and color stepping.
- **Asynchronous Harmony**:
  Each key has a distinct transition duration (1.5s to 4.5s) and randomized phase offset, creating an ever-shifting, hypnotic chromatic tapestry where adjacent keys contrast and blend smoothly.

---

## 🌈 Color Palettes

All palettes are calibrated for high-fidelity vibrancy on mechanical keyboard RGB LEDs:

| Palette | Identifier | Key Tones & Characteristics | Hex Samples |
|---|---|---|---|
| 🌸 **Sakura** | `sakura` | Cherry blossom pink, floral magenta, golden stamen, ivory tips | `#FFE4E1`, `#FF69B4`, `#FF1493`, `#FFD700` |
| 🌈 **Rainbow** | `rainbow` | High-purity spectral rainbow (Red, Orange, Yellow, Green, Cyan, Blue, Magenta) | Full continuous HSV spectrum |
| ⚡ **Cyberpunk** | `cyberpunk` | Electric cyan neon, deep magenta, acid yellow, and night violet | `#00F0FF`, `#FF007F`, `#FFE600`, `#7B2CBF` |
| 🌌 **Aurora** | `aurora` | Boreal polar green, arctic turquoise, deep indigo, and royal violet | `#00FF87`, `#60EFFF`, `#1A0B2E`, `#9B5DE5` |
| 💜 **Lavender** | `lavender` | Country lilac, soft lavender, periwinkle blue, and deep orchid | `#E6E6FA`, `#9370DB`, `#8A2BE2`, `#4B0082` |
| 🪷 **Lotus** | `lotus` | Oriental aquatic pink, water emerald, and pearl white | `#FFB7C5`, `#FF6B81`, `#00A86B`, `#F4F1DE` |
| 🌻 **Sunflower** | `sunflower` | Warm gold, rich amber, sunset orange, and roasted coffee center | `#FFD700`, `#FFA500`, `#FF8C00`, `#4A2C00` |
| 🌹 **Rose** | `rose` | Imperial carmine red, ruby, vivid scarlet, and velvet rose | `#E63946`, `#C1121F`, `#780000`, `#FF758F` |

---

## 🖥️ Interactive Graphical User Interface (GUI)

Launch the modern dark dashboard:

```bash
python -m openrgb_flowers --gui
```

### Dashboard Features:
1. **Live Keyboard Canvas Preview**:
   - 2D animated canvas drawing the physical K556 matrix key-by-key.
   - Responds dynamically to slider adjustments even when the physical effect is stopped.
2. **Hot-Reload Controls ("✓ Apply" and "⟲ Undo")**:
   - Modify any parameter while the physical keyboard is active.
   - Click **"✓ Apply"** to hot-reload settings into the active lighting loop without disconnecting from USB.
   - Click **"⟲ Undo"** to immediately revert to the active running configuration.
3. **High-Contrast Dark Theme**:
   - Custom dropdowns (*comboboxes*) in dark slate `#1e222b` with crisp white text and sky blue focus `#38bdf8`, offering maximum legibility.
4. **Dynamic Adjustment Sliders**:
   - **Speed**: from `0.2x` (slow and relaxing) to `4.0x` (fast and energetic).
   - **Brightness**: from `10%` to `100%` mapped to microcontroller hardware level 4.
   - **Saturation**: from `0%` (monochrome) to `200%` (hyper-vibrant).
   - **FPS**: from `15` to `60` frames per second.
   - **Max Flowers**: adjustable from `2` to `16` (in Blooming mode).
5. **"Start with Windows" Checkbox**:
   - Automatically registers the application in the Windows logon registry with no administrator privileges required.

---

## 📦 Windows Installer, Standalone Executable & Launchers

You don't need to open PowerShell or type commands to use the application every day.

### Option 1: Professional Windows Installer (`FlowersBlooming_Setup.exe`)
Download the pre-compiled installer from GitHub Releases or compile it locally with Inno Setup:

```bash
gerar_instalador.bat
# Or via Python:
python build_installer.py --compile-nuitka
```

- **Clean Installation**: Installs to `{localappdata}\Programs\OpenRGB Flowers` without requiring Administrator privileges.
- **Desktop & Start Menu**: Creates desktop and Start Menu shortcuts automatically.
- **Windows Integration**: Proper uninstaller in Windows Settings / Control Panel.

### Option 2: Portable Standalone (`FlowersBlooming_Portable/`)
Zero-installation portable bundle generated via Nuitka C++ compilation:

```bash
gerar_executavel.bat
# Or via Python:
python build_nuitka.py --standalone
```

The portable folder and zip are generated in:
```text
dist/FlowersBlooming_Portable/FlowersBlooming.exe
dist/FlowersBlooming_Portable.zip
```

### Option 3: Developer 1-Click Launcher
For development from source, run:
- [`run_gui.bat`](file:///C:/Users/xiyun/Documents/openrgb_flowers_blooming/run_gui.bat): Quick batch launcher via `pythonw.exe`.

---

## ⚡ Windows Auto-Start on Boot

When your PC restarts, the Redragon K556RGB-M loses power and powers back up in its default factory firmware mode (typically a static rainbow).

To keep your lighting effects continuously running after reboots:

### How to Enable:
1. **Via the Graphical Interface**:
   - Open the GUI (`FlowersBlooming.exe` or `python -m openrgb_flowers --gui`).
   - Check the box: **`[x] Iniciar com o Windows`** (Start with Windows).
2. **Via Command Line**:
   ```bash
   python -m openrgb_flowers --install-startup
   ```
   *(To disable in the future: `python -m openrgb_flowers --uninstall-startup`)*.

### How It Works Under the Hood:
- Registers an entry under `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.
- Does not require Administrator elevation (UAC).
- On Windows logon, the application launches silently with `--autostart`.
- It loads your saved configuration (effect, palette, brightness, saturation, and speed) from `~/.openrgb_flowers/user_config.json`, connects to the keyboard USB interface, and runs the lighting loop in the background with zero desktop interruption.

---

## 🚀 Command-Line Interface (CLI) Reference

```bash
# Launch interactive graphical GUI:
python -m openrgb_flowers --gui

# Random Matrix Blend (all keys illuminated, rich saturation):
python -m openrgb_flowers --effect random_blend --palette rainbow --speed 1.3 --saturation 1.5

# Flowers Blooming with Cyberpunk theme and terminal live preview:
python -m openrgb_flowers --effect blooming --palette cyberpunk --speed 1.0 --preview

# Random Blend with Nordic Aurora theme on native USB HID driver:
python -m openrgb_flowers --effect random_blend --palette aurora --driver redragon

# Classic Flowers Blooming with Sakura theme:
python -m openrgb_flowers --effect blooming --palette sakura --speed 1.2 --brightness 0.9

# Register application to auto-start on Windows boot:
python -m openrgb_flowers --install-startup

# Remove application from Windows auto-start:
python -m openrgb_flowers --uninstall-startup
```

### Complete CLI Argument Table:

| Argument | Default | Description |
|---|---|---|
| `--gui` | `False` | Launch interactive graphical user interface |
| `--effect, -e` | `blooming` | Effect type: `blooming` (flowers) or `random_blend` (mosaic) |
| `--palette, -p` | `sakura` | Palette: `sakura`, `rainbow`, `cyberpunk`, `aurora`, `lavender`, `lotus`, `sunflower`, `rose` |
| `--driver` | `auto` | Driver: `auto` (detects K556 USB or OpenRGB), `redragon` (native USB HID), `openrgb`, `mock` |
| `--speed, -s` | `1.0` | Animation speed multiplier (0.2 to 4.0) |
| `--brightness, -b` | `1.0` | Global brightness factor (0.0 to 1.0) |
| `--saturation` | `1.0` | Color saturation multiplier (0.0 to 2.5) |
| `--fps` | `30.0` | Target frames per second (15 to 60 FPS) |
| `--max-flowers, -m` | `7` | Maximum simultaneous blooming flowers |
| `--spawn-rate` | `1.4` | Average flowers spawned per second |
| `--blend` | `weighted` | Petal color blending mode: `weighted`, `screen`, `additive` |
| `--preview` | `False` | Render 24-bit TrueColor animation in the terminal |
| `--mock` | `False` | Run simulation mode without transmitting to hardware |
| `--config, -c` | `None` | Path to custom JSON configuration file |
| `--max-frames` | `None` | Optional limit of frames before exiting |
| `--autostart` | `False` | Run in background with saved preferences (used on Windows logon) |
| `--install-startup` | `False` | Register application to launch on Windows startup |
| `--uninstall-startup` | `False` | Unregister application from Windows startup |

---

## 📄 Configuration File (`config.json`)

Custom presets can be loaded and saved via JSON:

```json
{
  "effect_type": "random_blend",
  "palette_name": "rainbow",
  "speed": 1.2,
  "brightness": 1.0,
  "saturation": 1.2,
  "fps": 30.0,
  "max_flowers": 7,
  "spawn_rate": 1.4,
  "blend_mode": "weighted",
  "host": "127.0.0.1",
  "port": 6742,
  "device_name": null
}
```

To run using a configuration file:
```bash
python -m openrgb_flowers --config config.json
```

---

## 🔬 Hardware Protocol & Reverse Engineering

The native Redragon K556RGB-M driver was developed through reverse engineering of the vendor's USB WebHID protocol:

- **USB Identifiers**:
  - `VID`: `0x2E3C`
  - `PID`: `0xC365`
  - `Interface`: `2` (Proprietary HID control interface)
- **Custom Lighting Mode**:
  - Command `0x07` with parameter `10` switches the keyboard into **Mode 10 (Custom Lighting Mode)**.
- **Color Chunk Packet Structure**:
  - Each complete frame is sent across **8 chunks of 65 bytes** using command `0x09`:
    - `Byte 0`: Report ID `0x01`
    - `Byte 1`: Command `0x09` (Custom Light Chunk)
    - `Byte 2`: Lighting profile `0x00`
    - `Byte 3`: `(chunk_index >> 8) & 0xFF`
    - `Byte 4`: `chunk_index & 0xFF` (chunks 0 through 7)
    - `Byte 5`: Byte payload length (54 bytes for chunks 0-6; 18 bytes for chunk 7)
    - `Bytes 6..60`: Contiguous RGB triplets (18 keys $\times$ 3 bytes)
- **Hardware Brightness Level**:
  - The microcontroller accepts levels 0 through 4. The driver sets hardware level 4 (maximum physical LED intensity) and applies linear software scaling for brightness tuning.
- **OpenRGB SDK Fallback**:
  - If the native Redragon device is not connected, the system automatically checks for a running OpenRGB SDK server on port `6742`.

---

## 📦 Native C++ Compilation (Nuitka) & Standalone Distributions

The project supports high-performance native C++ compilation via **Nuitka**, avoiding packer-based heuristic false positives:

```bash
# Build Standalone / Portable directory (Recommended: 0 Static ML false positives):
python build_nuitka.py --standalone

# Build single executable (.exe Onefile):
python build_nuitka.py
```

Alternatively, double-click [`gerar_executavel.bat`](file:///gerar_executavel.bat) to launch the interactive build menu.

### 🌸 Windows System Tray Minimization
- Clicking **Minimize (`_`)** or **Close (`X`)** hides the window from the screen and taskbar, keeping it active in the **Windows Notification Area (System Tray)** next to the clock.
- Lighting effects continue executing uninterrupted in the background.
- **Right-click the flower icon in the tray**:
  - `🌸 Abrir Painel` (or double click): Restores the dashboard immediately.
  - `✕ Encerrar`: Cleanly terminates lighting transmission and exits the application.

---

## 🏛️ Software Architecture (SOLID & DRY)

The codebase strictly adheres to Clean Architecture and software design best practices:

- **Single Responsibility Principle (SRP)**:
  Each class is dedicated to one responsibility in an isolated file:
  - Lighting engines: [`BloomingEngine`](file:///src/openrgb_flowers/effects/blooming_engine.py), [`RandomBlendEngine`](file:///src/openrgb_flowers/effects/random_blend_engine.py).
  - Hardware transmitters: [`RedragonK556Transmitter`](file:///src/openrgb_flowers/hardware/redragon_k556_transmitter.py), [`OpenRGBTransmitter`](file:///src/openrgb_flowers/hardware/openrgb_transmitter.py), [`MockTransmitter`](file:///src/openrgb_flowers/hardware/mock_transmitter.py).
  - Services: [`ConfigStorageService`](file:///src/openrgb_flowers/service/config_storage_service.py), [`WindowsStartupService`](file:///src/openrgb_flowers/service/windows_startup_service.py).
  - System tray: [`SystemTrayManager`](file:///src/openrgb_flowers/gui/system_tray.py).
  - Math & Geometry: [`FlowerGeometry`](file:///src/openrgb_flowers/effects/flower_geometry.py), [`FastColorMath`](file:///src/openrgb_flowers/math/fast_color_math.py).
- **Open/Closed Principle (OCP)**:
  New palettes and engines register dynamically via `PaletteRegistry` and `EffectEngineFactory` without modifying existing core code.
- **Liskov Substitution Principle (LSP)**:
  Any `IEffectEngine` or `IFrameTransmitter` can be seamlessly substituted into `RunnerService`.
- **Interface Segregation Principle (ISP)**:
  Precise, minimal interfaces (`IFrameTransmitter`, `IEffectEngine`, `ILayoutProvider`, `IAutoStartService`, `IConfigStorageService`, `ISystemTray`).
- **Dependency Inversion Principle (DIP)**:
  High-level classes depend upon constructor-injected abstractions.

---

## 📂 Repository Directory Structure

```text
openrgb_flowers_blooming/
├── .github/
│   ├── dependabot.yml               # Dependabot configuration (pip & github-actions)
│   └── workflows/
│       └── ci.yml                   # CI pipeline (Ubuntu & Windows across Python 3.10, 3.11, 3.12)
├── src/
│   └── openrgb_flowers/
│       ├── cli/                     # CLI argument parsing and execution
│       ├── core/
│       │   ├── exceptions/          # Typed hardware and network exceptions
│       │   ├── interfaces/          # Contracts (Transmitter, Engine, Layout, Storage, Startup, Tray)
│       │   └── models/              # Immutable models (RGBColor, RenderFrame, EffectConfig)
│       ├── effects/
│       │   ├── blending/            # Color blending strategies (Weighted, Screen, Additive)
│       │   ├── palettes/            # 8 botanical palettes and central registry
│       │   ├── blooming_engine.py   # Procedural flower blooming engine
│       │   ├── random_blend_engine.py # Chromatic mosaic blend engine
│       │   └── effect_engine_factory.py # Effect factory
│       ├── gui/                     # Dark control panel, canvas preview, system tray, and async runner
│       ├── hardware/                # Redragon K556 WebHID transmitter and physical layouts
│       ├── math/                    # Vectorized color math and interpolation
│       ├── preview/                 # Terminal TrueColor live visualizer
│       └── service/                 # Loop runners, Windows startup, and config persistence
├── tests/                           # 91 automated unit and integration tests with pytest
├── build_tools/                     # Modular build system (SOLID & DRY)
│   ├── inno_builder.py              # Inno Setup compilation orchestrator
│   ├── inno_locator.py              # Inno Setup compiler detection
│   ├── nuitka_builder.py            # Nuitka C++ native builder
│   ├── nuitka_runner.py             # Resilient compiler execution with lock retries
│   ├── process_manager.py           # Safe process termination
│   └── version_reader.py            # Version extraction from pyproject.toml
├── build_installer.py               # CLI entrypoint for Inno Setup installer
├── build_nuitka.py                  # Standalone C++ compiler entrypoint
├── gerar_instalador.bat             # 1-click installer creation script
├── gerar_executavel.bat             # 1-click standalone compilation script
├── installer.iss                    # Inno Setup installation script
├── launcher.py                      # Application launcher entry point
├── run_gui.bat                      # 1-click batch launcher
├── requirements.txt                 # Production dependencies
├── requirements-dev.txt             # Development and test dependencies
├── pyproject.toml                   # Packaging configuration
├── setup.py                         # Secondary setuptools distribution config
├── README.md                        # English documentation
└── README_PTBR.md                   # Brazilian Portuguese documentation
```

---

## 🧪 Automated Tests & CI

The repository includes **91 automated tests** verifying mathematical models, interpolation, hardware packet formatting, layout geometry, interfaces, and GUI behavior:

```bash
python -m pytest tests -v
```

All commits and pull requests are continuously tested in GitHub Actions across operating systems and Python versions.
