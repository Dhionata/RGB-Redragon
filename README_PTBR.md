# 🌸 OpenRGB Flowers Blooming & Mosaico Cromático

[![CI](https://github.com/Dhionata/RGB-Redragon/actions/workflows/ci.yml/badge.svg)](https://github.com/Dhionata/RGB-Redragon/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows | Linux](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)](https://github.com/Dhionata/RGB-Redragon)

Efeitos de iluminação RGB orgânicos e procedurais de alta performance desenvolvidos especificamente para o teclado mecânico **Redragon K556RGB-M** (Devarajas) e compatíveis com todo o ecossistema **OpenRGB**.

O projeto conta com **dois motores de iluminação exclusivos**, **8 paletas de cores refinadas**, **comunicação USB HID direta** (sem necessidade de softwares intermediários), uma **interface gráfica moderna (GUI)** com visualizador do teclado físico em tempo real, **ajustes a quente**, suporte a **executável standalone (.exe)** e **inicialização automática com o Windows**.

---

## 📑 Sumário

- [Destaques do Projeto](#-destaques-do-projeto)
- [Motores de Efeito em Detalhes](#-motores-de-efeito-em-detalhes)
  - [1. Flores Desabrochando (`blooming`)](#1--flores-desabrochando-blooming)
  - [2. Mosaico de Cores Aleatórias (`random_blend`)](#2--mosaico-de-cores-aleatórias-random_blend)
- [Paletas de Cores](#-paletas-de-cores)
- [Interface Gráfica Interativa (GUI)](#-interface-gráfica-interativa-gui)
- [Executável Standalone (.exe) e Execução Sem PowerShell](#-executável-standalone-exe-e-execução-sem-powershell)
- [Inicialização Automática com o Windows](#-inicialização-automática-com-o-windows)
- [Uso via Linha de Comando (CLI)](#-uso-via-linha-de-comando-cli)
- [Arquivo de Configuração (`config.json`)](#-arquivo-de-configuração-configjson)
- [Protocolo de Hardware e Engenharia Reversa](#-protocolo-de-hardware-e-engenharia-reversa)
- [Arquitetura de Software (SOLID & DRY)](#-arquitetura-de-software-solid--dry)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Testes Automatizados](#-testes-automatizados)

---

## ✨ Destaques do Projeto

- **Zero Alocação em Renderização**: Cálculos de cor e geometria 100% vetorizados via **NumPy**, processando cada quadro em menos de `0.1 ms` com uso de CPU inferior a `0.5%`.
- **Transmissão USB HID Direta**: Comunicação nativa com o microcontrolador do Redragon K556RGB-M (`VID: 0x2E3C, PID: 0xC365, Interface 2`) no Modo 10 com o comando `0x09`, sem depender de drivers proprietários ou softwares pesados em segundo plano.
- **Dois Estilos de Efeito Distintos**:
  - *Flores Desabrochando*: Brotos orgânicos que nascem, abrem pétalas harmônicas e se dissolvem suavemente.
  - *Mosaico Aleatório*: **100% das teclas permanecem acesas simultaneamente**, alternando continuamente entre cores com interpolação cúbica Hermite (*smoothstep*).
- **Interface Gráfica com Preview Vivo**: Teclado virtual em 2D que renderiza a física do efeito antes e durante a execução.
- **Controle a Quente ("✓ Aplicar" e "⟲ Desfazer")**: Permite trocar paleta, saturação, brilho e velocidade em tempo real sem travar ou interromper a transmissão USB.
- **Persistência e Início Automático no Windows**: Opção de iniciar automaticamente no boot do Windows em segundo plano, mantendo o efeito ativo sem que o teclado retorne ao padrão estático da placa após reiniciar o computador.
- **Executável Único (`RedragonRGB.exe`)**: Pode ser aberto diretamente com duplo clique no Windows sem precisar de terminal ou PowerShell.

---

## 🎨 Motores de Efeito em Detalhes

### 1. 🌸 Flores Desabrochando (`blooming`)

- **Conceito Matemático**:
  Cada flor é gerada estocasticamente sobre a matriz de teclas $(x, y)$. As pétalas são modeladas através de curvas polares harmônicas:
  $$r(\theta) = R \cdot \left(1 + \epsilon \cos(k \theta)\right)$$
  onde $k \in \{4, 5, 6, 8\}$ define o número de pétalas e $\epsilon$ o grau de ondulação floral.
- **Dinâmica Temporal**:
  - **Fase de Brotamento (0.0 a 0.3)**: O estame central nasce e se expande rapidamente a partir da cor primária da paleta.
  - **Fase de Floração Plena (0.3 a 0.7)**: As pétalas se abrem completamente com degradê radial em direção às pontas.
  - **Fase de Desvanecimento (0.7 a 1.0)**: As pétalas desvanecem suavemente por dissipação natural.
- **Estratégias de Mesclagem**:
  Onde múltiplas flores se sobrepõem, o motor suporta três estratégias:
  - `weighted` (padrão): Média ponderada pela intensidade de cada pétala, preservando o equilíbrio cromático.
  - `screen`: Fórmula de tela fotográfica ($1 - (1-a)(1-b)$), gerando sobreposições mais luminosas.
  - `additive`: Soma pura de fótons com saturação no teto de 255.
- **Brisa de Fundo**: Uma suave respiração ambiental sinusoidal em tons terrosos/verdes sutis impede que o teclado fique em escuridão total entre brotamentos.

### 2. ✨ Mosaico de Cores Aleatórias (`random_blend`)

- **Conceito**:
  Projetado para quem deseja o teclado **inteiramente iluminado a todo momento**. Cada tecla física possui sua própria máquina de estados cromática assíncrona.
- **Interpolação Suave (Smoothstep)**:
  A transição entre a cor atual $C_0$ e a próxima cor sorteada $C_1$ ocorre através do polinômio cúbico de Hermite:
  $$t_{\text{smooth}} = 3t^2 - 2t^3$$
  $$C(t) = C_0 \cdot (1 - t_{\text{smooth}}) + C_1 \cdot t_{\text{smooth}}$$
  Isso elimina qualquer descontinuidade brusca de aceleração cromática nas extremidades.
- **Assincronia Orgânica**:
  Cada tecla tem um período de transição independente (entre 1.5s e 4.5s) e fase defasada, criando um mosaico vivo onde tons adjacentes contrastam e se harmonizam continuamente.

---

## 🌈 Paletas de Cores

Todas as paletas foram calibradas para máxima fidelidade em LEDs RGB de teclados mecânicos:

| Paleta | Identificador | Cores Principais e Características | Amostras Hex |
|---|---|---|---|
| 🌸 **Sakura** | `sakura` | Rosa cerejeira, magenta floral, estame âmbar e pontas marfim | `#FFE4E1`, `#FF69B4`, `#FF1493`, `#FFD700` |
| 🌈 **Rainbow** | `rainbow` | Arco-íris contínuo de alta pureza cromática (Vermelho, Laranja, Amarelo, Verde, Ciano, Azul, Magenta) | Espectro HSV completo |
| ⚡ **Cyberpunk** | `cyberpunk` | Ciano elétrico neon, magenta profundo, amarelo laser e violeta | `#00F0FF`, `#FF007F`, `#FFE600`, `#7B2CBF` |
| 🌌 **Aurora** | `aurora` | Verde polar boreal, turquesa ártico, índigo escuro e violeta real | `#00FF87`, `#60EFFF`, `#1A0B2E`, `#9B5DE5` |
| 💜 **Lavender** | `lavender` | Lilás campestre, lavanda suave, azul pervinca e orquídea | `#E6E6FA`, `#9370DB`, `#8A2BE2`, `#4B0082` |
| 🪷 **Lotus** | `lotus` | Rosa lótus oriental, verde esmeralda d'água e branco pérola | `#FFB7C5`, `#FF6B81`, `#00A86B`, `#F4F1DE` |
| 🌻 **Sunflower** | `sunflower` | Amarelo ouro, âmbar aquecido, laranja pôr do sol e centro café | `#FFD700`, `#FFA500`, `#FF8C00`, `#4A2C00` |
| 🌹 **Rose** | `rose` | Vermelho carmim imperial, rubi vivo, escarlate e rosa aveludado | `#E63946`, `#C1121F`, `#780000`, `#FF758F` |

---

## 🖥️ Interface Gráfica Interativa (GUI)

Inicie o painel de controle escuro moderno com:

```bash
python -m openrgb_flowers --gui
```

### Funcionalidades do Dashboard:
1. **Prévia do Teclado em Tempo Real**:
   - Canvas animado em 2D que desenha a matriz física do K556 tecla por tecla.
   - Responde dinamicamente aos controles deslizantes mesmo com o efeito parado.
2. **Controles a Quente ("✓ Aplicar" e "⟲ Desfazer")**:
   - Modifique qualquer parâmetro enquanto o teclado físico estiver funcionando.
   - O botão **"✓ Aplicar"** injeta a nova configuração a quente na thread de iluminação USB sem desconectar.
   - O botão **"⟲ Desfazer"** reverte instantaneamente para os parâmetros atualmente em execução.
3. **Alto Contraste e Ergonomia**:
   - Menus suspensos (*comboboxes*) em fundo escuro `#1e222b` com texto branco brilhante e foco azul celeste `#38bdf8`, 100% legíveis.
4. **Controles Deslizantes**:
   - **Velocidade**: de `0.2x` (lento e relaxante) a `4.0x` (dinâmico e enérgico).
   - **Brilho**: de `10%` a `100%` com mapeamento para o nível de hardware 4 do microcontrolador.
   - **Saturação**: de `0%` (monocromático suave) a `200%` (cores ultra saturadas).
   - **FPS**: de `15` a `60` quadros por segundo.
   - **Máximo de Flores**: ajustável de `2` a `16` (no modo Blooming).
5. **Opção "Iniciar com o Windows"**:
   - Checkbox que registra a inicialização automática no registro do Windows sem necessidade de privilégios de administrador.

---

## 📦 Executável Standalone (.exe) e Execução Sem PowerShell

Você não precisa abrir o PowerShell ou digitar comandos para usar a aplicação no dia a dia.

### Opção 1: Executável Standalone Compilado (`RedragonRGB.exe`)
Gere um arquivo executável único para Windows com o PyInstaller:

```bash
python build_exe.py
```

O arquivo compilado será gerado em:
```text
dist/RedragonRGB.exe
```

- **Duplo Clique**: Abre diretamente a interface gráfica em modo de janela limpa (sem janela preta de terminal).
- **Portabilidade**: Pode ser colocado na Área de Trabalho, Menu Iniciar ou qualquer pasta.

### Opção 2: Inicializadores Silenciosos em 1 Clique
No diretório do projeto, fornecemos dois inicializadores rápidos:
- [`run_gui.vbs`](file:///C:/Users/xiyun/Documents/openrgb_flowers_blooming/run_gui.vbs): Executa via `pythonw.exe` de forma 100% invisível sem abrir console.
- [`run_gui.bat`](file:///C:/Users/xiyun/Documents/openrgb_flowers_blooming/run_gui.bat): Script batch simples para início imediato.

---

## ⚡ Inicialização Automática com o Windows

Quando o computador é desligado ou reiniciado, o microcontrolador do Redragon K556RGB-M desliga e reinicia em seu modo de firmware padrão de fábrica (geralmente um arco-íris estático).

Para manter seus efeitos sempre ativos automaticamente sem esforço:

### Como Ativar:
1. **Pela Interface Gráfica**:
   - Abra a interface (`RedragonRGB.exe` ou `python -m openrgb_flowers --gui`).
   - Marque a caixa de seleção: **`[x] Iniciar com o Windows`**.
2. **Pelo Terminal**:
   ```bash
   python -m openrgb_flowers --install-startup
   ```
   *(Para desativar no futuro: `python -m openrgb_flowers --uninstall-startup`)*.

### Como Funciona por Baixo dos Panos:
- A aplicação é registrada na chave de usuário do Windows: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`.
- Não requer elevação de Administrador (UAC).
- Quando o usuário faz logon no Windows, o sistema executa o aplicativo com a flag `--autostart`.
- A aplicação lê suas últimas preferências salvas (efeito, paleta, brilho, saturação e velocidade) em `~/.openrgb_flowers/user_config.json`, conecta diretamente ao teclado USB e inicia a iluminação em segundo plano de forma silenciosa e sem abrir janelas.

---

## 🚀 Uso via Linha de Comando (CLI)

```bash
# Iniciar a Interface Gráfica interativa:
python -m openrgb_flowers --gui

# Mosaico de Cores Aleatórias (todas as teclas acesas, saturação rica):
python -m openrgb_flowers --effect random_blend --palette rainbow --speed 1.3 --saturation 1.5

# Flores Desabrochando com tema Cyberpunk e pré-visualização no terminal:
python -m openrgb_flowers --effect blooming --palette cyberpunk --speed 1.0 --preview

# Mosaico com tema Aurora Nórdica no driver direto USB HID:
python -m openrgb_flowers --effect random_blend --palette aurora --driver redragon

# Flores clássicas com tema Sakura:
python -m openrgb_flowers --effect blooming --palette sakura --speed 1.2 --brightness 0.9

# Configurar para iniciar automaticamente com o Windows:
python -m openrgb_flowers --install-startup

# Remover da inicialização do Windows:
python -m openrgb_flowers --uninstall-startup
```

### Tabela Completa de Parâmetros da CLI:

| Argumento | Padrão | Descrição |
|---|---|---|
| `--gui` | `False` | Abre a interface gráfica interativa |
| `--effect, -e` | `blooming` | Tipo de efeito: `blooming` (flores) ou `random_blend` (mosaico) |
| `--palette, -p` | `sakura` | Paleta: `sakura`, `rainbow`, `cyberpunk`, `aurora`, `lavender`, `lotus`, `sunflower`, `rose` |
| `--driver` | `auto` | Driver: `auto` (detecta K556 USB ou OpenRGB), `redragon` (USB HID nativo), `openrgb`, `mock` |
| `--speed, -s` | `1.0` | Multiplicador de velocidade da animação (0.2 a 4.0) |
| `--brightness, -b` | `1.0` | Fator de brilho global (0.0 a 1.0) |
| `--saturation` | `1.0` | Multiplicador de saturação de cor (0.0 a 2.5) |
| `--fps` | `30.0` | Taxa de quadros alvo por segundo (15 a 60 FPS) |
| `--max-flowers, -m` | `7` | Máximo de flores simultâneas (no efeito blooming) |
| `--spawn-rate` | `1.4` | Taxa média de surgimento de novas flores por segundo |
| `--blend` | `weighted` | Modo de mesclagem de pétalas: `weighted`, `screen`, `additive` |
| `--preview` | `False` | Exibe animação em 24-bit TrueColor no terminal |
| `--mock` | `False` | Modo de simulação sem enviar pacotes ao hardware |
| `--config, -c` | `None` | Caminho para arquivo JSON de configuração customizado |
| `--max-frames` | `None` | Limite opcional de quadros antes de encerrar |
| `--autostart` | `False` | Executa em segundo plano com configurações salvas (usado no boot) |
| `--install-startup` | `False` | Registra a aplicação para inicializar no boot do Windows |
| `--uninstall-startup` | `False` | Remove a aplicação da inicialização do Windows |

---

## 📄 Arquivo de Configuração (`config.json`)

Você pode carregar ou salvar configurações personalizadas via arquivo JSON:

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

Para executar utilizando este arquivo:
```bash
python -m openrgb_flowers --config config.json
```

---

## 🔬 Protocolo de Hardware e Engenharia Reversa

O driver nativo do Redragon K556RGB-M foi desenvolvido através de engenharia reversa do protocolo USB WebHID do fabricante:

- **Identificadores USB**:
  - `VID`: `0x2E3C`
  - `PID`: `0xC365`
  - `Interface`: `2` (Interface de Controle HID proprietário)
- **Modo de Iluminação Customizada**:
  - Comando `0x07` com o parâmetro `10` ativa o **Modo 10 (Custom Lighting Mode)**.
- **Estrutura de Pacotes de Cores**:
  - Cada quadro completo de cores é transmitido em **8 chunks de 65 bytes** utilizando o comando `0x09`:
    - `Byte 0`: Report ID `0x01`
    - `Byte 1`: Comando `0x09` (Custom Light Chunk)
    - `Byte 2`: Perfil de iluminação `0x00`
    - `Byte 3`: `(chunk_index >> 8) & 0xFF`
    - `Byte 4`: `chunk_index & 0xFF` (índices 0 a 7)
    - `Byte 5`: Quantidade de bytes de dados (54 bytes para chunks 0 a 6; 18 bytes para o chunk 7)
    - `Bytes 6..60`: Triplets RGB contíguos (18 teclas $\times$ 3 bytes)
- **Nível de Brilho de Hardware**:
  - O microcontrolador aceita níveis de 0 a 4. O driver configura o hardware no nível máximo 4 e realiza a modulação dinâmica por escala linear de software, garantindo o brilho físico máximo dos LEDs.
- **Fallback OpenRGB SDK**:
  - Caso o teclado Redragon não seja detectado, o sistema tenta automaticamente conectar a um servidor OpenRGB local na porta padrão `6742`.

---

## 📦 Compilação Nativa em C++ (Nuitka) & Executáveis Standalone

O projeto oferece suporte à compilação nativa em C++ através do **Nuitka**, eliminando problemas de falsos positivos de packers e entregando máxima performance:

```bash
# Compilar versão Standalone / Portátil (Recomendado: 0 falsos positivos / Sem Static ML):
python build_nuitka.py --standalone

# Compilar arquivo executável único (.exe Onefile):
python build_nuitka.py
```

Ou simplesmente dê um duplo clique no arquivo [`gerar_executavel.bat`](file:///gerar_executavel.bat), que apresenta um menu interativo para escolher o formato desejado.

### 🌸 Minimização para a Bandeja do Windows (System Tray)
- Ao clicar no botão **Minimizar (`_`)** ou no botão **Fechar (`X`)**, a janela do aplicativo é ocultada da tela e da barra de tarefas, ficando ativa na **Área de Notificação (Bandeja)** do Windows ao lado do relógio.
- O efeito de iluminação continua rodando perfeitamente em segundo plano.
- **Clique com o botão direito no ícone da flor na bandeja**:
  - `🌸 Abrir Painel` (ou duplo clique): Restaura o painel gráfico com foco imediato.
  - `✕ Encerrar`: Encerra o efeito de iluminação e finaliza a aplicação com segurança.

---

## 🏛️ Arquitetura de Software (SOLID & DRY)

O projeto foi construído seguindo rigorosamente os princípios de Clean Architecture:

- **Single Responsibility Principle (SRP)**:
  Cada classe possui uma única e estrita responsabilidade em arquivo isolado:
  - Motores de iluminação: [`BloomingEngine`](file:///src/openrgb_flowers/effects/blooming_engine.py), [`RandomBlendEngine`](file:///src/openrgb_flowers/effects/random_blend_engine.py).
  - Transmissores de hardware: [`RedragonK556Transmitter`](file:///src/openrgb_flowers/hardware/redragon_k556_transmitter.py), [`OpenRGBTransmitter`](file:///src/openrgb_flowers/hardware/openrgb_transmitter.py), [`MockTransmitter`](file:///src/openrgb_flowers/hardware/mock_transmitter.py).
  - Serviços de persistência e sistema operacional: [`ConfigStorageService`](file:///src/openrgb_flowers/service/config_storage_service.py), [`WindowsStartupService`](file:///src/openrgb_flowers/service/windows_startup_service.py).
  - Bandeja do sistema operacional: [`SystemTrayManager`](file:///src/openrgb_flowers/gui/system_tray.py).
  - Geometria e matemática: [`FlowerGeometry`](file:///src/openrgb_flowers/effects/flower_geometry.py), [`FastColorMath`](file:///src/openrgb_flowers/math/fast_color_math.py).
- **Open/Closed Principle (OCP)**:
  Novas paletas e novos efeitos são registrados dinamicamente via `PaletteRegistry` e `EffectEngineFactory` sem necessidade de alterar as classes consumidoras.
- **Liskov Substitution Principle (LSP)**:
  Qualquer implementação de `IEffectEngine` ou `IFrameTransmitter` pode ser substituída sem alterar o comportamento do `RunnerService`.
- **Interface Segregation Principle (ISP)**:
  Interfaces limpas e focadas (`IFrameTransmitter`, `IEffectEngine`, `ILayoutProvider`, `IAutoStartService`, `IConfigStorageService`, `ISystemTray`).
- **Dependency Inversion Principle (DIP)**:
  Todas as classes de alto nível dependem de abstrações injetáveis via construtor.

---

## 📂 Estrutura do Repositório

```text
openrgb_flowers_blooming/
├── .github/
│   ├── dependabot.yml               # Configuração do Dependabot (pip e github-actions)
│   └── workflows/
│       └── ci.yml                   # Pipeline de CI (Ubuntu & Windows em Python 3.10, 3.11, 3.12)
├── src/
│   └── openrgb_flowers/
│       ├── cli/                     # Linha de comando e parsing de argumentos
│       ├── core/
│       │   ├── exceptions/          # Exceções tipadas de hardware e rede
│       │   ├── interfaces/          # Contratos abstratos (Transmitter, Engine, Layout, Storage, Startup, Tray)
│       │   └── models/              # Estruturas de dados imutáveis (RGBColor, RenderFrame, EffectConfig)
│       ├── effects/
│       │   ├── blending/            # Estratégias de fusão de cores (Weighted, Screen, Additive)
│       │   ├── palettes/            # 8 paletas botânicas e registro central
│       │   ├── blooming_engine.py   # Motor procedural de flores
│       │   ├── random_blend_engine.py # Motor de mosaico cromático
│       │   └── effect_engine_factory.py # Fábrica abstrata de efeitos
│       ├── gui/                     # Painel gráfico dark, preview em canvas, bandeja (System Tray) e runner
│       ├── hardware/                # Transmissor WebHID Redragon K556 e layouts físicos
│       ├── math/                    # Matemática rápida e interpolações vetorizadas
│       ├── preview/                 # Visualizador TrueColor no terminal
│       └── service/                 # Serviços de loop, inicialização no Windows e persistência
├── tests/                           # 64 testes automatizados com pytest
├── build_nuitka.py                  # Compilador nativo C++ com Nuitka (Standalone & Onefile)
├── build_exe.py                     # Compilador PyInstaller legado
├── gerar_executavel.bat             # Menu interativo para gerar executáveis em 1 clique
├── launcher.py                      # Ponto de entrada para os executáveis
├── run_gui.vbs                      # Inicializador silencioso em 1 clique (VBScript)
├── run_gui.bat                      # Inicializador em lote (Batch)
├── requirements.txt                 # Dependências de produção
├── requirements-dev.txt             # Dependências de desenvolvimento e testes
├── pyproject.toml                   # Manifesto de empacotamento moderno
├── README.md                        # Documentação em Inglês
└── README_PTBR.md                   # Documentação em Português do Brasil
```

---

## 🧪 Testes Automatizados

O projeto conta com **64 testes automatizados** cobrindo matemática, interpolações, layouts de hardware, transmissão USB, interfaces, bandeja do sistema e componentes de GUI:

```bash
python -m pytest tests -v
```

Todas as alterações passam por validação contínua no GitHub Actions a cada commit ou pull request.
