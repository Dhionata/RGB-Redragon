# 🌸 OpenRGB Flowers Blooming & Mosaico Cromático (C++20 Nativo)

[![CI](https://github.com/Dhionata/RGB-Redragon/actions/workflows/release.yml/badge.svg)](https://github.com/Dhionata/RGB-Redragon/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![C++20](https://img.shields.io/badge/standard-C%2B%2B20-blue.svg)](https://en.cppreference.com/w/cpp/20)
[![Tamanho do Binário](https://img.shields.io/badge/binario-1.45%20MB-success.svg)](https://github.com/Dhionata/RGB-Redragon/releases)
[![Plataforma: Windows](https://img.shields.io/badge/plataforma-Windows%2010%20%7C%2011-lightgrey.svg)](https://github.com/Dhionata/RGB-Redragon)

Efeitos de iluminação RGB orgânicos e procedurais de altíssima performance desenvolvidos especificamente para o teclado mecânico **Redragon K556RGB-M** (Devarajas) e compatíveis com todo o ecossistema **OpenRGB**.

Reescrito em **100% C++20 nativo puro** com **zero dependências externas de runtime**, eliminando o Python, interpretadores embutidos e heurísticas de empacotamento, garantindo **0 falsos positivos em Antivírus e no VirusTotal**.

---

## 📑 Sumário

- [Por que C++20 Nativo Puro? (Antivírus e Performance)](#-por-que-c20-nativo-puro-antivírus-e-performance)
- [Destaques do Projeto](#-destaques-do-projeto)
- [Motores de Efeito em Detalhes](#-motores-de-efeito-em-detalhes)
  - [1. Flores Desabrochando (`blooming`)](#1--flores-desabrochando-blooming)
  - [2. Mosaico de Cores Aleatórias (`random_blend`)](#2--mosaico-de-cores-aleatórias-random_blend)
- [Paletas de Cores](#-paletas-de-cores)
- [Bandeja do Windows (System Tray) e Execução em Segundo Plano](#-bandeja-do-windows-system-tray-e-execução-em-segundo-plano)
- [Inicialização Automática com o Windows](#-inicialização-automática-com-o-windows)
- [Uso via Linha de Comando (CLI)](#-uso-via-linha-de-comando-cli)
- [Arquivo de Configuração (`user_config.json`)](#-arquivo-de-configuração-user_configjson)
- [Protocolo de Hardware e USB HID Win32 Direto](#-protocolo-de-hardware-e-usb-hid-win32-direto)
- [Compilação a partir do Código-Fonte (CMake e MinGW / MSVC)](#-compilação-a-partir-do-código-fonte-cmake-e-mingw--msvc)
- [Arquitetura de Software (SOLID & DRY)](#-arquitetura-de-software-solid--dry)
- [Testes Automatizados](#-testes-automatizados)

---

## 🛡️ Por que C++20 Nativo Puro? (Antivírus e Performance)

Versões anteriores empacotadas via Python e ferramentas de bundling (PyInstaller/Nuitka) acionavam alertas heurísticos em motores antivírus (ex.: Avast, AVG, VirusTotal) devido aos padrões genéricos de descompactação de bytecode em tempo de execução.

Ao reconstruir o projeto em **C++20 nativo puro**:
- **0 Falsos Positivos**: Binário PE Windows limpo, com recurso oficial `VS_VERSION_INFO` embutido (`version.rc`).
- **Tamanho Mínimo**: O executável standalone possui apenas **1.45 MB** (com símbolos removidos e runtime estático) e **585 KB** compactado em `.zip`, reduzindo em mais de 95% os mais de 35 MB anteriores.
- **Inicialização Instantânea**: Inicialização a frio em **< 5 ms** (sem carregar VM Python, interpretadores ou bibliotecas dinâmicas pesadas).
- **Uso de CPU Próximo de Zero**: Cálculos vetoriais de cor otimizados para SIMD, buffers de renderização com zero alocações dinâmicas, processando cada quadro em **< 0.02 ms** (< 0.1% de uso da CPU).
- **Zero Dependências**: Vinculado estaticamente com `libgcc` e `libstdc++`. Funciona imediatamente em instalações limpas do Windows 10/11 sem requerer Python, pacotes redistribuíveis do Visual C++ ou DLLs extras.

---

## ✨ Destaques do Projeto

- **Transmissão USB HID Win32 Direta**: Comunicação nativa em nível de kernel com o microcontrolador do Redragon K556RGB-M (`VID: 0x2E3C, PID: 0xC365, Interface 2`) via `SetupDi` e `hid.dll`, ativando o Modo 10 e transmitindo 8 chunks por quadro sem necessidade de software proprietário de terceiros.
- **Fallback Automático OpenRGB**: Cliente TCP Winsock2 suportando o protocolo OpenRGB SDK v4 na porta `6742`.
- **Dois Motores Procedurais**:
  - *Flores Desabrochando*: Brotos orgânicos que nascem estocasticamente, abrem pétalas polares harmônicas e se dissolvem suavemente.
  - *Mosaico de Cores*: **100% das teclas constantemente acesas**, transicionando suavemente entre cores da paleta usando interpolação cúbica Hermite (*smoothstep*).
- **8 Paletas Calibradas**: Esquemas botânicos e vibrantes calibrados para a curva cromática dos LEDs mecânicos.
- **Bandeja do Windows (System Tray)**: Ícone nativo via Win32 `Shell_NotifyIconW` com menu de contexto e encerramento limpo.
- **Inicialização com o Windows**: Registro nativo em `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` sem exigir privilégios de Administrador.

---

## 🎨 Motores de Efeito em Detalhes

### 1. 🌸 Flores Desabrochando (`blooming`)

- **Conceito Matemático**:
  Cada flor nasce estocasticamente sobre a matriz física $(x, y)$ das teclas. As pétalas são modeladas por curvas polares harmônicas:
  $$r(\theta) = R \cdot \left(1 + \epsilon \cos(k \theta)\right)$$
  onde $k \in \{4, 5, 6, 8\}$ define o número de pétalas e $\epsilon$ a intensidade das ondulações.
- **Ciclo de Vida Temporal**:
  - **Fase de Brotamento (0.0 a 0.3)**: O estame central nasce e se expande rapidamente a partir da cor primária da paleta.
  - **Fase de Floração Plena (0.3 a 0.7)**: As pétalas abrem completamente com degradê radial em direção às pontas.
  - **Fase de Desvanecimento (0.7 a 1.0)**: Dissipação suave por decaimento exponencial de fótons.
- **Estratégias de Mesclagem**:
  Onde múltiplas pétalas se cruzam, o motor calcula a cor resultante através de:
  - `weighted` (padrão): Média ponderada pela intensidade de cada pétala, preservando o equilíbrio cromático.
  - `screen`: Mesclagem fotográfica de tela ($1 - (1-a)(1-b)$), gerando sobreposições luminosas.
  - `additive`: Adição direta de valores RGB saturados em 255.
- **Brisa Ambiental**: Pulsação senoidal suave em tons terrosos/verdes sutis para manter o teclado levemente iluminado entre florescimentos.

### 2. ✨ Mosaico de Cores Aleatórias (`random_blend`)

- **Conceito**:
  Projetado para manter **todas as teclas físicas 100% iluminadas o tempo todo**. Cada tecla possui uma máquina de estados cromática assíncrona individual.
- **Interpolação Suave (Hermite Smoothstep)**:
  A transição entre a cor de origem e a próxima cor de destino segue o polinômio:
  $$t_{\text{smooth}} = 3t^2 - 2t^3$$
  $$C(t) = C_0 \cdot (1 - t_{\text{smooth}}) + C_1 \cdot t_{\text{smooth}}$$
  eliminando saltos de cor e acelerações bruscas.
- **Harmonia Orgânica**:
  Cada tecla tem tempo de transição independente (entre 1.5s e 4.5s) e defasagem de fase, criando um mosaico dinâmico e hipnótico.

---

## 🌈 Paletas de Cores

| Paleta | Identificador | Características e Cores Principais | Referência Hex |
|---|---|---|---|
| 🌸 **Sakura** | `sakura` | Rosa cerejeira, magenta floral, estame dourado e pontas marfim | `#FFE4E1`, `#FF69B4`, `#FF1493`, `#FFD700` |
| 🌈 **Rainbow** | `rainbow` | Arco-íris espectral contínuo de alta pureza | Espectro HSV completo |
| ⚡ **Cyberpunk** | `cyberpunk` | Ciano neon, magenta laser, amarelo ácido e violeta escuro | `#00F0FF`, `#FF007F`, `#FFE600`, `#7B2CBF` |
| 🌌 **Aurora** | `aurora` | Verde boreal, turquesa ártico, índigo escuro e violeta real | `#00FF87`, `#60EFFF`, `#1A0B2E`, `#9B5DE5` |
| 💜 **Lavender** | `lavender` | Lilás campestre, lavanda suave, azul pervinca e orquídea | `#E6E6FA`, `#9370DB`, `#8A2BE2`, `#4B0082` |
| 🪷 **Lotus** | `lotus` | Rosa lótus oriental, verde esmeralda d'água e branco pérola | `#FFB7C5`, `#FF6B81`, `#00A86B`, `#F4F1DE` |
| 🌻 **Sunflower** | `sunflower` | Amarelo ouro, âmbar aquecido, laranja pôr do sol e centro café | `#FFD700`, `#FFA500`, `#FF8C00`, `#4A2C00` |
| 🌹 **Rose** | `rose` | Vermelho carmim imperial, rubi vivo, escarlate e rosa aveludado | `#E63946`, `#C1121F`, `#780000`, `#FF758F` |

---

## 🌸 Bandeja do Windows (System Tray) e Execução em Segundo Plano

Ao executar no modo de interface ou com `--tray`:
- Um ícone de flor é inserido na **Bandeja do Sistema (System Tray)** próximo ao relógio do Windows.
- O motor de iluminação executa suavemente em uma thread em segundo plano.
- **Menu de Contexto (botão direito no ícone)**:
  - `🌸 OpenRGB Flowers Blooming`: Exibição de status.
  - `✕ Sair / Exit`: Encerra a transmissão no hardware, desliga o modo custom e finaliza o processo com segurança.

---

## ⚡ Inicialização Automática com o Windows

Quando o computador é ligado, o microcontrolador do Redragon K556 reinicia no modo padrão de fábrica. Para manter seus efeitos ativos automaticamente:

1. **Ativar via Linha de Comando**:
   ```powershell
   .\FlowersBlooming.exe --install-startup
   ```
2. **Desativar via Linha de Comando**:
   ```powershell
   .\FlowersBlooming.exe --uninstall-startup
   ```

**Como funciona**:
- O aplicativo grava a entrada em `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.
- Não necessita de privilégios de Administrador (sem avisos de UAC).
- Ao fazer login no Windows, inicia silenciosamente em segundo plano (`--autostart`), carregando as preferências salvas em `~/.openrgb_flowers/user_config.json`.

---

## 🚀 Uso via Linha de Comando (CLI)

O executável C++ suporta argumentos bilingues em Português e Inglês:

```powershell
# Executar Flores Desabrochando com paleta Sakura:
.\FlowersBlooming.exe --efeito blooming --paleta sakura --velocidade 1.2 --brilho 0.9

# Executar Mosaico Aleatório com paleta Rainbow via USB HID direto do K556:
.\FlowersBlooming.exe --efeito random_blend --paleta rainbow --driver redragon --velocidade 1.4

# Executar com tema Cyberpunk em segundo plano com ícone na bandeja:
.\FlowersBlooming.exe --efeito blooming --paleta cyberpunk --bandeja

# Modo de simulação (sem enviar pacotes ao teclado):
.\FlowersBlooming.exe --simular --max-frames 100

# Configurar inicialização automática com o Windows:
.\FlowersBlooming.exe --instalar-inicio
```

### Tabela Completa de Parâmetros da CLI:

| Parâmetro em Inglês | Parâmetro em Português | Padrão | Descrição |
|---|---|---|---|
| `--effect, -e` | `--efeito` | `blooming` | Tipo de efeito: `blooming` ou `random_blend` |
| `--palette, -p` | `--paleta` | `sakura` | Paleta: `sakura`, `rainbow`, `cyberpunk`, `aurora`, `lavender`, `lotus`, `sunflower`, `rose` |
| `--driver, -d` | `--driver` | `auto` | Driver: `auto` (detecta K556 USB ou OpenRGB), `redragon`, `openrgb`, `mock` |
| `--speed, -s` | `--velocidade` | `1.0` | Multiplicador de velocidade da animação (0.2 a 4.0) |
| `--brightness, -b` | `--brilho` | `1.0` | Fator de brilho global (0.0 a 1.0) |
| `--saturation` | `--saturacao` | `1.0` | Multiplicador de saturação de cor (0.0 a 2.5) |
| `--fps` | `--fps` | `30.0` | Taxa de quadros alvo por segundo (15 a 60 FPS) |
| `--max-flowers, -m` | `--max-flores` | `7` | Máximo de flores simultâneas (modo `blooming`) |
| `--spawn-rate` | `--taxa-surgimento`| `1.4` | Taxa média de novas flores por segundo |
| `--blend` | `--mesclagem` | `weighted` | Modo de fusão: `weighted`, `screen`, `additive` |
| `--tray` | `--bandeja` | `false` | Ativa o ícone na Bandeja do Sistema (System Tray) |
| `--gui` | `--interface` | `false` | Inicia com interface / bandeja |
| `--mock` | `--simular` | `false` | Modo de simulação (sem comunicação de hardware) |
| `--config, -c` | `--config` | *vazio* | Caminho para arquivo JSON de configuração customizado |
| `--max-frames` | `--max-frames` | *infinito* | Encerra após quantidade especificada de quadros |
| `--autostart` | `--autostart` | `false` | Execução silenciosa na inicialização do Windows |
| `--install-startup`| `--instalar-inicio`| `false` | Registra no boot do Windows |
| `--uninstall-startup`| `--desinstalar-inicio`| `false`| Remove do boot do Windows |
| `--help, -h` | `--ajuda` | - | Exibe o menu de ajuda e encerra |

---

## 📄 Arquivo de Configuração (`user_config.json`)

As configurações são salvas automaticamente em `%USERPROFILE%\.openrgb_flowers\user_config.json`:

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

## 🔬 Protocolo de Hardware e USB HID Win32 Direto

O driver nativo C++ comunica-se diretamente com o teclado mecânico através das APIs Win32 de HID:

- **Identificadores USB**: `VID: 0x2E3C`, `PID: 0xC365`, `Interface: 2`.
- **Ativação do Modo 10**: Envio do Feature Report `0x07` com o valor `10` ativa o Custom Lighting Mode.
- **Empacotamento com Zero Alocação**: Cada quadro é dividido em 8 chunks de 65 bytes (comando `0x09`), enviados sequencialmente:
  - Report ID `0x01`, Comando `0x09`, Perfil `0x00`
  - Índice do Chunk (16-bit big-endian)
  - Comprimento dos dados (54 bytes nos chunks 0 a 6; 18 bytes no chunk 7)
  - Triplets RGB contíguos (18 teclas $\times$ 3 bytes)
- **Brilho Máximo do Hardware**: O microcontrolador opera no nível de brilho 4 e a atenuação de brilho é feita via software para evitar cintilação PWM.

---

## 🔨 Compilação a partir do Código-Fonte (CMake e MinGW / MSVC)

### Pré-requisitos:
- CMake 3.20+
- MinGW-w64 (GCC 13+) ou Microsoft Visual C++ (MSVC 2022+)

### Compilação em 1 Clique:
Execute o script automatizado:
```powershell
.\build.bat
```
O script localiza automaticamente a toolchain, configura o CMake, compila `dist\FlowersBlooming.exe`, roda todos os testes unitários, gera `dist\FlowersBlooming_Portable.zip` e compila o instalador Inno Setup se instalado.

### Compilação Manual via CMake:
```powershell
mkdir build
cd build
cmake .. -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release --parallel
ctest --output-on-failure
```

---

## 🏛️ Arquitetura de Software (SOLID & DRY)

A base de código em C++ é estritamente modularizada respeitando os princípios de Clean Architecture:

```text
openrgb_flowers_blooming/
├── include/openrgb_flowers/         # Interfaces e Contratos C++20 (.hpp)
│   ├── core/                        # Modelos (ColorRGB, ColorHSV, RenderFrame, JsonValue) e Interfaces
│   ├── math/                        # FastColorMath, EasingFunctions, SpatialGrid
│   ├── effects/                     # PetalGeometry, FlowerInstance, BloomingEngine, RandomBlendEngine, Palettes
│   ├── hardware/                    # RedragonK556Transmitter, OpenRGBTransmitter, Layouts
│   ├── service/                     # RunnerService, ConfigStorageService, WindowsStartupService
│   ├── gui/                         # SystemTray (Win32 Shell_NotifyIconW)
│   └── cli/                         # ArgumentParser
├── src/                             # Implementações C++20 (.cpp)
│   ├── core/                        # json_helper.cpp, models.cpp
│   ├── math/                        # fast_color_math.cpp, easing_functions.cpp, spatial_grid.cpp
│   ├── effects/                     # petal_geometry.cpp, flower_instance.cpp, engines, palettes, blend strategies
│   ├── hardware/                    # redragon_k556_transmitter.cpp, openrgb_transmitter.cpp, layouts
│   ├── service/                     # runner_service.cpp, config_storage_service.cpp, windows_startup_service.cpp
│   ├── gui/                         # system_tray.cpp
│   ├── cli/                         # argument_parser.cpp
│   ├── version.rc                   # Recurso de Versão do Windows PE
│   └── main.cpp                     # Ponto de Entrada da Aplicação
├── tests/cpp/                       # Bateria de Testes em C++ (9 módulos, tests_cpp.exe)
├── CMakeLists.txt                   # Definição do CMake
├── build.bat                        # Script de compilação nativa
└── installer.iss                    # Script do Instalador Inno Setup
```

---

## 🧪 Testes Automatizados

A suíte nativa em `tests/cpp/` valida todos os módulos sem dependência de hardware físico:

```powershell
.\build\tests_cpp.exe
```

Cobertura de testes:
1. `test_color_models`: Conversões bidirecionais HSV/RGB, saturação, brilho e comparação.
2. `test_math`: LERP, smoothstep cúbico, harmônicos polares, correção de proporção no spatial grid.
3. `test_palettes`: Todas as 8 paletas botânicas, interpolação cíclica e resolução no PaletteRegistry.
4. `test_blending`: Fórmulas de mesclagem Weighted, Screen e Additive.
5. `test_engines`: Ciclo de vida das flores no BloomingEngine e cobertura de 100% no RandomBlendEngine.
6. `test_layouts`: Mapeamento ANSI de 104 teclas e matriz 6x22 de firmware.
7. `test_hardware_packets`: Chunks Modo 10 do Redragon K556, alinhamento de 65 bytes e cabeçalhos OpenRGB.
8. `test_config`: Parser e serializador JSON sem dependências externas, validação de ida e volta.
9. `test_main`: Parser de linha de comando com suporte bilíngue e validação de flags.

---

## 🛡️ Solução de Problemas com Antivírus (Modo Rigoroso / Hardened Mode do Avast)

Se você compilar o projeto localmente em uma máquina com o antivírus **Avast** (ou AVG) com o **Modo Rigoroso (Hardened Mode)** ativado:
- **Por que ele bloqueia**: O Modo Rigoroso do Avast (`HardenedMode: 1`) intercepta a execução de processos recém-compilados (`Motivo: 0x00020000`) exclusivamente porque o hash do executável gerado no seu computador ainda não possui reputação acumulada na nuvem do Avast. Isso **não é detecção de vírus**, mas uma política de bloqueio para arquivos desconhecidos sem reputação.
- **Como resolver para compilação local**:
  1. No Avast -> **Menu** -> **Configurações** -> **Exceções** -> **Adicionar Exceção** -> selecione a pasta do projeto ou a subpasta `dist`, OU
  2. No Avast -> **Proteção** -> **Módulos Principais** -> role até **Modo Rigoroso** e configure para Moderado ou Desativado durante o desenvolvimento local.
  3. Versões oficiais pré-compiladas baixadas da aba de Releases do GitHub já possuem validação e integridade, não sofrendo esse bloqueio de reputação local.
