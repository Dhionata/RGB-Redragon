# 🌸 OpenRGB Flowers Blooming

High-performance, organic RGB lighting effect for the **Redragon K556RGB-M** mechanical keyboard and the broader **OpenRGB** ecosystem.

The effect simulates blooming flowers spreading organically across individual keyboard keys: floral buds sprout at stochastic locations, expand harmonic petal lobes, blend rich botanical color gradients, and gently dissolve into an ambient meadow breeze.

Provided for the community in **two integration options**:
1. **Standalone Python Package & CLI (`openrgb-python`)**: Production-ready, SOLID & DRY architecture, vectorized with NumPy, 24-bit TrueColor terminal live preview, and low-latency Direct mode transmission.
2. **GLSL Fragment Shader for OpenRGB Effects Plugin (`flowers_blooming.frag`)**: Ready to copy & paste into the OpenRGB Effects Plugin Shader tab.

---

## 🏛️ SOLID & DRY Design

Strictly adhering to clean code standards:
- **Single Responsibility**: Every class resides in its own file.
- **Open/Closed**: New botanical palettes and blend strategies can be plugged in without modifying core engine code.
- **Liskov Substitution**: Standardized interfaces (`ILayoutProvider`, `IFrameTransmitter`, `IBlendStrategy`).
- **Interface Segregation**: Lean, focused interfaces in `core/interfaces/`.
- **Dependency Inversion**: Decoupled from physical I/O via mockable abstractions.

---

## ⚡ Performance Highlights

- **Vectorized Color Math**: Coordinate grids, Euclidean distances with physical keyboard aspect ratio correction (~3.7:1), petal boundary falloffs, and HSV/RGB color mappings run in vectorized NumPy routines.
- **CPU Usage < 0.5%**: Frame rendering takes under 0.2 milliseconds.
- **OpenRGB Direct Mode with `fast=True`**: Bypasses synchronous state updates, sending frames at up to 60 FPS smoothly without lag.

---

## 🚀 Quick Start

### Installation
```bash
pip install -e .
```

### Running with OpenRGB
Make sure OpenRGB is running with the SDK Server enabled (default port 6742).
```bash
openrgb-flowers --palette sakura --fps 30
```

### Live Terminal Preview (Offline / Mock mode)
```bash
openrgb-flowers --mock --preview --palette lotus
```

### Running Unit Tests
```bash
pytest
```
