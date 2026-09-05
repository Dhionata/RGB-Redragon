# 🌸 OpenRGB Flowers Blooming & Chromatic Blend

High-performance, organic RGB lighting effects for the **Redragon K556RGB-M** mechanical keyboard and the broader **OpenRGB** ecosystem.

Featuring **two distinct lighting effect engines**, **8 vibrant color palettes**, **native USB HID direct transmission**, and an **interactive graphical interface (GUI)** with real-time physical keyboard layout preview.

---

## 🎨 Effect Engines

1. **🌸 Flowers Blooming (`blooming`)**:
   - Stochastic floral blooms sprout across keyboard keys, expand harmonic petal lobes ($4, 5, 6, 8$ petals), and blend rich botanical gradients.
2. **✨ Random Matrix Blend (`random_blend`)**:
   - **100% of keys remain illuminated simultaneously**. Each key smoothly and asynchronously transitions between random colors from the selected palette using cubic Hermite (*smoothstep*) interpolation, producing an organic, ever-shifting chromatic tapestry.

---

## 🖥️ Interactive GUI Dashboard

Launch the modern dark-themed GUI dashboard:

```bash
python -m openrgb_flowers --gui
```

### GUI Features
- **Visualização em Tempo Real**: Pré-visualização animada contínua no teclado virtual da tela antes mesmo de iniciar o efeito.
- **Controle Dinâmico ("Aplicar" e "Desfazer")**: Altere velocidade, saturação, paleta, brilho ou modo de efeito durante a execução e clique em **"✓ Aplicar"** para recarregar a quente sem interromper a transmissão USB, ou **"⟲ Desfazer"** para reverter.
- **Contraste Aprimorado**: Caixas de seleção (comboboxes) em alto contraste, totalmente legíveis.
- **Slider de Saturação**: Ajuste a vivacidade das cores de 0% (monocromático) a 200% (super saturado).
- **Brilho Máximo do Hardware**: Nível de hardware configurado para o valor máximo do microcontrolador (nível 4) com gama linear para máxima intensidade luminosa dos LEDs.

---

## 🚀 CLI Usage

```bash
# Launch interactive GUI:
python -m openrgb_flowers --gui

# Run Random Blend effect (all keys illuminated, shifting colors, full saturation):
python -m openrgb_flowers --effect random_blend --palette rainbow --speed 1.3 --saturation 1.5

# Run Blooming Flowers effect with Cyberpunk neon palette and terminal preview:
python -m openrgb_flowers --effect blooming --palette cyberpunk --speed 1.0 --preview

# Run Nordic Aurora on native Redragon K556RGB-M:
python -m openrgb_flowers --effect random_blend --palette aurora --driver redragon
```

---

## 🏛️ SOLID & DRY Architecture

- **Single Responsibility (SRP)**: Every model, engine, layout, and visualizer resides in its own isolated file.
- **Open/Closed (OCP)**: New palettes and engines register dynamically via `PaletteRegistry` and `EffectEngineFactory`.
- **Liskov Substitution (LSP)**: Interchangeable implementations for `IEffectEngine`, `ILayoutProvider`, and `IFrameTransmitter`.
- **High Efficiency**: 100% vectorized NumPy rendering with zero per-frame heap allocations (< 0.5% CPU usage).
- **Direct USB HID**: Native communication with Redragon K556RGB-M Interface 2 (`2E3C:C365`) in Mode 10 via Command `0x09`.

---

## 🧪 Unit Tests

```bash
python -m pytest tests -v
```
