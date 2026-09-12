# 🌸 OpenRGB Flowers Blooming & Chromatic Blend (Pure C++20)

[![CI](https://github.com/Dhionata/RGB-Redragon/actions/workflows/release.yml/badge.svg)](https://github.com/Dhionata/RGB-Redragon/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![C++20](https://img.shields.io/badge/standard-C%2B%2B20-blue.svg)](https://en.cppreference.com/w/cpp/20)
[![Binary Size](https://img.shields.io/badge/binary-1.45%20MB-success.svg)](https://github.com/Dhionata/RGB-Redragon/releases)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-lightgrey.svg)](https://github.com/Dhionata/RGB-Redragon)

High-performance, procedural, organic RGB lighting effects engineered specifically for the **Redragon K556RGB-M** (Devarajas) mechanical keyboard and compatible across the broader **OpenRGB** ecosystem.

Written in **100% pure native C++20** with **zero external runtime dependencies**, eliminating Python, runtime interpreters, and packer heuristics to guarantee **0 false positives on Antivirus / VirusTotal**.

---

## 📑 Table of Contents

- [Why Pure C++20? (Antivirus & Performance)](#-why-pure-c20-antivirus--performance)
- [Project Highlights](#-project-highlights)
- [Lighting Engines in Detail](#-lighting-engines-in-detail)
  - [1. Flowers Blooming (`blooming`)](#1--flowers-blooming-blooming)
  - [2. Random Matrix Blend (`random_blend`)](#2--random-matrix-blend-random_blend)
- [Color Palettes](#-color-palettes)
- [Windows System Tray & Background Execution](#-windows-system-tray--background-execution)
- [Windows Auto-Start on Boot](#-windows-auto-start-on-boot)
- [Command-Line Interface (CLI) Reference](#-command-line-interface-cli-reference)
- [Configuration File (`user_config.json`)](#-configuration-file-user_configjson)
- [Hardware Protocol & Direct Win32 USB HID](#-hardware-protocol--direct-win32-usb-hid)
- [Compiling from Source (CMake & MinGW / MSVC)](#-compiling-from-source-cmake--mingw--msvc)
- [Software Architecture (SOLID & DRY)](#-software-architecture-solid--dry)
- [Automated Tests](#-automated-tests)

---

## 🛡️ Why Pure C++20? (Antivirus & Performance)

Earlier iterations packaged with Python and runtime bundlers (PyInstaller/Nuitka) triggered heuristic false positives in certain antivirus engines (e.g., Avast, AVG) due to generic bytecode unpacking patterns. 

By rewriting the entire codebase in **pure native C++20**:
- **0 False Positives**: Clean PE Windows binary with embedded standard `VS_VERSION_INFO` resource.
- **Tiny Footprint**: Standalone executable is only **1.45 MB** (stripped, static runtime) and **585 KB** compressed as `.zip`, down from over 35 MB.
- **Instantaneous Startup**: Cold launch in **< 5 ms** (no Python VM initialization, no dynamic module imports).
- **Near-Zero CPU Usage**: Optimized SIMD-friendly color transformations, zero-allocation render buffers, computing frames in **< 0.02 ms** (< 0.1% CPU).
- **Zero Runtime Dependencies**: Statically linked against `libgcc` and `libstdc++`. Runs out-of-the-box on clean Windows 10/11 installations without requiring Python, Visual C++ Redistributables, or third-party DLLs.

---

## ✨ Project Highlights

- **Direct Win32 USB HID Driver**: Direct kernel communication with the Redragon K556RGB-M microcontroller (`VID: 0x2E3C, PID: 0xC365, Interface 2`) via `SetupDi` and `hid.dll`, switching to Mode 10 and transmitting 8 chunks per frame with zero intermediate drivers.
- **OpenRGB Fallback**: Winsock2 TCP client supporting OpenRGB SDK protocol v4 on port `6742`.
- **Two Procedural Engines**:
  - *Flowers Blooming*: Organic blossoms spawning stochastically, unfurling polar harmonic petals, and fading softly.
  - *Random Matrix Blend*: **100% of keys illuminated at all times**, transitioning smoothly between palette colors using Hermite cubic smoothstep interpolation.
- **8 Calibrated Palettes**: Botanical and neon schemes mapped to mechanical keyboard LED chromatic response.
- **Windows System Tray**: Native Win32 `Shell_NotifyIconW` background tray with right-click menu and clean exit.
- **Windows Startup**: Automatically registers in `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` without requiring Administrator privileges.

---

## 🎨 Lighting Engines in Detail

### 1. 🌸 Flowers Blooming (`blooming`)

- **Mathematical Concept**:
  Each flower spawns stochastically across the physical $(x, y)$ key matrix. Petals are parameterized by polar harmonic boundary curves:
  $$r(\theta) = R \cdot \left(1 + \epsilon \cos(k \theta)\right)$$
  where $k \in \{4, 5, 6, 8\}$ governs lobe count and $\epsilon$ dictates edge waviness.
- **Temporal Lifecycle**:
  - **Sprout Phase (0.0 to 0.3)**: Central stamen emerges and rapidly expands with the palette's primary tone.
  - **Full Bloom Phase (0.3 to 0.7)**: Petals unfurl with radial gradients fading toward petal tips.
  - **Dissipation Phase (0.7 to 1.0)**: Petals gently decay through natural light fading.
- **Color Blending Modes**:
  When multiple flower lobes overlap, the engine calculates combined light using:
  - `weighted` (default): Weighted average preserving chromatic balance.
  - `screen`: Screen blending formula ($1 - (1-a)(1-b)$), yielding luminous floral overlays.
  - `additive`: Pure photon addition clamped at 255.
- **Ambient Breeze**: Sinusoidal background breathing prevents keyboard from going completely dark between blooms.

### 2. ✨ Random Matrix Blend (`random_blend`)

- **Concept**:
  Designed for users who want **every single key continuously illuminated**. Each physical key maintains an independent, asynchronous color state machine.
- **Smooth Transition (Hermite Smoothstep)**:
  Transitions between color stops follow a cubic polynomial:
  $$t_{\text{smooth}} = 3t^2 - 2t^3$$
  $$C(t) = C_0 \cdot (1 - t_{\text{smooth}}) + C_1 \cdot t_{\text{smooth}}$$
  eliminating linear color stepping and harsh acceleration jumps.
- **Asynchronous Harmony**:
  Each key features a randomized transition period (1.5s to 4.5s) and phase offset, producing a living chromatic mosaic.

---

## 🌈 Color Palettes

| Palette | Identifier | Tones & Characteristics | Hex Reference |
|---|---|---|---|
| 🌸 **Sakura** | `sakura` | Cherry blossom pink, floral magenta, golden stamen, ivory tips | `#FFE4E1`, `#FF69B4`, `#FF1493`, `#FFD700` |
| 🌈 **Rainbow** | `rainbow` | High-purity continuous spectral rainbow | Full HSV spectrum |
| ⚡ **Cyberpunk** | `cyberpunk` | Electric cyan neon, deep magenta, acid yellow, and night violet | `#00F0FF`, `#FF007F`, `#FFE600`, `#7B2CBF` |
| 🌌 **Aurora** | `aurora` | Boreal polar green, arctic turquoise, deep indigo, and royal violet | `#00FF87`, `#60EFFF`, `#1A0B2E`, `#9B5DE5` |
| 💜 **Lavender** | `lavender` | Country lilac, soft lavender, periwinkle blue, and deep orchid | `#E6E6FA`, `#9370DB`, `#8A2BE2`, `#4B0082` |
| 🪷 **Lotus** | `lotus` | Oriental aquatic pink, water emerald, and pearl white | `#FFB7C5`, `#FF6B81`, `#00A86B`, `#F4F1DE` |
| 🌻 **Sunflower** | `sunflower` | Warm gold, rich amber, sunset orange, and roasted coffee center | `#FFD700`, `#FFA500`, `#FF8C00`, `#4A2C00` |
| 🌹 **Rose** | `rose` | Imperial carmine red, ruby, vivid scarlet, and velvet rose | `#E63946`, `#C1121F`, `#780000`, `#FF758F` |

---

## 🌸 Windows System Tray & Background Execution

When launched in GUI mode or with `--tray`:
- The application places a flower icon in the **Windows Notification Area (System Tray)** next to the clock.
- Lighting effects run smoothly in a dedicated background worker thread.
- **Right-click tray menu**:
  - `🌸 OpenRGB Flowers Blooming`: Status indicator.
  - `✕ Exit / Sair`: Cleanly stops hardware transmission, restores device state, and exits.

---

## ⚡ Windows Auto-Start on Boot

When your PC boots, the Redragon K556RGB-M resets to its factory firmware mode. To keep your custom lighting running seamlessly:

1. **Enable via CLI**:
   ```powershell
   .\FlowersBlooming.exe --install-startup
   ```
2. **Disable via CLI**:
   ```powershell
   .\FlowersBlooming.exe --uninstall-startup
   ```

**How it works**:
- Registers in `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.
- Does not require Administrator privileges.
- On login, starts silently in the background (`--autostart`), loading your preferences from `~/.openrgb_flowers/user_config.json`.

---

## 🚀 Command-Line Interface (CLI) Reference

The native binary supports bilingual English and Portuguese command-line arguments:

```powershell
# Run Flowers Blooming with Sakura palette:
.\FlowersBlooming.exe --effect blooming --palette sakura --speed 1.2 --brightness 0.9

# Run Random Matrix Blend with Rainbow palette on native Redragon USB HID:
.\FlowersBlooming.exe --effect random_blend --palette rainbow --driver redragon --speed 1.4

# Run with Cyberpunk theme in background with System Tray icon:
.\FlowersBlooming.exe --effect blooming --palette cyberpunk --tray

# Run simulation mode without transmitting to hardware:
.\FlowersBlooming.exe --mock --max-frames 100

# Register to start automatically with Windows:
.\FlowersBlooming.exe --install-startup
```

### Complete CLI Argument Table:

| Argument | Portuguese Alias | Default | Description |
|---|---|---|---|
| `--effect, -e` | `--efeito` | `blooming` | Effect type: `blooming` or `random_blend` |
| `--palette, -p` | `--paleta` | `sakura` | Palette: `sakura`, `rainbow`, `cyberpunk`, `aurora`, `lavender`, `lotus`, `sunflower`, `rose` |
| `--driver, -d` | `--driver` | `auto` | Driver: `auto` (detects K556 USB or OpenRGB), `redragon`, `openrgb`, `mock` |
| `--speed, -s` | `--velocidade` | `1.0` | Animation speed multiplier (0.2 to 4.0) |
| `--brightness, -b` | `--brilho` | `1.0` | Global brightness factor (0.0 to 1.0) |
| `--saturation` | `--saturacao` | `1.0` | Color saturation multiplier (0.0 to 2.5) |
| `--fps` | `--fps` | `30.0` | Target frames per second (15 to 60 FPS) |
| `--max-flowers, -m` | `--max-flores` | `7` | Maximum simultaneous flowers (`blooming` mode) |
| `--spawn-rate` | `--taxa-surgimento`| `1.4` | Average flowers spawned per second |
| `--blend` | `--mesclagem` | `weighted` | Blend mode: `weighted`, `screen`, `additive` |
| `--tray` | `--bandeja` | `false` | Enable Windows System Tray icon and context menu |
| `--gui` | `--interface` | `false` | Launch graphical interface / system tray |
| `--mock` | `--simular` | `false` | Simulation mode (no hardware communication) |
| `--config, -c` | `--config` | *empty* | Path to custom JSON configuration file |
| `--max-frames` | `--max-frames` | *infinite*| Exit after specified number of frames |
| `--autostart` | `--autostart` | `false` | Run silently on Windows logon |
| `--install-startup`| `--instalar-inicio`| `false` | Register application for Windows auto-start |
| `--uninstall-startup`| `--desinstalar-inicio`| `false`| Unregister application from Windows auto-start |
| `--help, -h` | `--ajuda` | - | Display help menu and exit |

---

## 📄 Configuration File (`user_config.json`)

Configuration is persisted automatically to `%USERPROFILE%\.openrgb_flowers\user_config.json`:

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
  "device_name": ""
}
```

---

## 🔬 Hardware Protocol & Direct Win32 USB HID

The native driver communicates directly with the keyboard microcontroller using standard Windows HID APIs:

- **Identifiers**: `VID: 0x2E3C`, `PID: 0xC365`, `Interface: 2`.
- **Mode 10 Activation**: Feature report `0x07` with value `10` sets Custom Lighting Mode.
- **Zero-Allocation Chunking**: Each frame is packed into 8 chunks of 65 bytes (`0x09` report), sent sequentially:
  - Report ID `0x01`, Command `0x09`, Profile `0x00`
  - Chunk index (16-bit big-endian)
  - Data length (54 bytes for chunks 0-6; 18 bytes for chunk 7)
  - Contiguous RGB triplets (18 keys $\times$ 3 bytes)
- **Microcontroller Max Brightness**: Firmware level 4 is activated; fine brightness scaling is performed in software.

---

## 🔨 Compiling from Source (CMake & MinGW / MSVC)

### Prerequisites:
- CMake 3.20+
- MinGW-w64 (GCC 13+) or Microsoft Visual C++ (MSVC 2022+)

### One-Click Build:
Run the automated build script:
```powershell
.\build.bat
```
This script detects the toolchain, configures CMake, compiles `dist\FlowersBlooming.exe`, runs all unit tests, generates `dist\FlowersBlooming_Portable.zip`, and optionally compiles the Inno Setup installer.

### Manual CMake Build:
```powershell
mkdir build
cd build
cmake .. -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release --parallel
ctest --output-on-failure
```

---

## 🏛️ Software Architecture (SOLID & DRY)

The C++ codebase is organized strictly according to Clean Architecture:

```text
openrgb_flowers_blooming/
├── include/openrgb_flowers/         # C++20 Header Interfaces & Contracts
│   ├── core/                        # Models (ColorRGB, ColorHSV, RenderFrame, JsonValue) & Interfaces
│   ├── math/                        # FastColorMath, EasingFunctions, SpatialGrid
│   ├── effects/                     # PetalGeometry, FlowerInstance, BloomingEngine, RandomBlendEngine, Palettes
│   ├── hardware/                    # RedragonK556Transmitter, OpenRGBTransmitter, Layouts
│   ├── service/                     # RunnerService, ConfigStorageService, WindowsStartupService
│   ├── gui/                         # SystemTray (Win32 Shell_NotifyIconW)
│   └── cli/                         # ArgumentParser
├── src/                             # C++20 Implementations
│   ├── core/                        # json_helper.cpp, models.cpp
│   ├── math/                        # fast_color_math.cpp, easing_functions.cpp, spatial_grid.cpp
│   ├── effects/                     # petal_geometry.cpp, flower_instance.cpp, engines, palettes, blend strategies
│   ├── hardware/                    # redragon_k556_transmitter.cpp, openrgb_transmitter.cpp, layouts
│   ├── service/                     # runner_service.cpp, config_storage_service.cpp, windows_startup_service.cpp
│   ├── gui/                         # system_tray.cpp
│   ├── cli/                         # argument_parser.cpp
│   ├── version.rc                   # Windows PE Version Resource
│   └── main.cpp                     # Application entry point
├── tests/cpp/                       # C++ Test Suite (9 modules, tests_cpp.exe)
├── CMakeLists.txt                   # CMake build definition
├── build.bat                        # One-click native build script
└── installer.iss                    # Inno Setup installer script
```

---

## 🧪 Automated Tests

The native test suite in `tests/cpp/` verifies all subsystems without hardware dependencies:

```powershell
.\build\tests_cpp.exe
```

Test coverage includes:
1. `test_color_models`: HSV/RGB bidirectional conversion, clipping, equality.
2. `test_math`: LERP, cubic smoothstep, polar harmonics, spatial grid aspect ratio mapping.
3. `test_palettes`: All 8 palettes, cyclic interpolation, PaletteRegistry resolution.
4. `test_blending`: Weighted, Screen, and Additive blending formulas.
5. `test_engines`: BloomingEngine flower life cycles, RandomBlendEngine full-key coverage.
6. `test_layouts`: 104-key ANSI mapping, 6x22 firmware matrix coordinates.
7. `test_hardware_packets`: Redragon Mode 10 chunks, 65-byte report alignment, OpenRGB packet headers.
8. `test_config`: Zero-dependency JSON parser, serializer, roundtrip validation.
9. `test_main`: Argument parser bilingual flags and validation.

---

## 🛡️ Antivirus Troubleshooting (Avast Hardened Mode / Zero Reputation)

If you are compiling from source on a machine with **Avast Antivirus** (or AVG) and have **Hardened Mode** enabled:
- **Why it blocks**: Avast Hardened Mode (`HardenedMode: 1`) intercepts process execution (`Reason: 0x00020000`) for any locally compiled `.exe` solely because its newly generated hash has not yet accumulated cloud reputation. This is **not a virus detection**, but an unknown executable block policy.
- **Solution for local builds**:
  1. Open Avast -> **Menu** -> **Settings** -> **Exceptions** -> **Add Exception** -> add your project directory or `dist` folder, OR
  2. In Avast -> **Protection** -> **Core Shields** -> scroll down to **Hardened Mode** and set it to Moderate or Off while compiling locally.
  3. Pre-compiled official releases downloaded from GitHub Releases are signed and validated, avoiding this local unknown-binary lock.
