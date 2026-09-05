# 🌸 OpenRGB Flowers Blooming & Mosaico Cromático

Efeitos de iluminação RGB orgânicos de alta performance para o teclado **Redragon K556RGB-M** (Devarajas) e outros dispositivos do ecossistema **OpenRGB**.

O projeto conta com **dois efeitos principais**, **8 paletas de cores**, **suporte nativo USB HID** e uma **interface gráfica interativa (GUI)** completa com pré-visualização em tempo real do teclado.

---

## 🎨 Efeitos Disponíveis

### 1. 🌸 Flores Desabrochando (`blooming`)
- **Comportamento**: Centros florais (estames) brotam aleatoriamente pela superfície das teclas, expandem pétalas com harmônicos suaves e degradês florais vívidos, misturam-se onde se sobrepõem e desvanecem com naturalidade sobre uma brisa suave de fundo.
- **Configuração**: Permite ajustar quantidade de flores simultâneas (`max_flowers`), taxa de brotamento (`spawn_rate`), velocidade e modos de mesclagem (`weighted`, `screen`, `additive`).

### 2. ✨ Mosaico de Cores Aleatórias (`random_blend`)
- **Comportamento**: **100% das teclas permanecem iluminadas simultaneamente**. Cada tecla faz uma transição de cor suave e contínua (*smoothstep cubic hermite*) em direção a novas cores aleatórias da paleta escolhida (ou espectro total), com velocidades e fases individuais assíncronas.
- **Visual**: Cria um espetáculo hipnótico e vibrante onde o teclado inteiro brilha continuamente em um degradê colorido que se transforma de forma orgânica e constante sem engasgos.

---

## 🖥️ Interface Gráfica Interativa (GUI)

O projeto inclui uma interface moderna em modo escuro com visualizador do teclado físico em tempo real:

```bash
python -m openrgb_flowers --gui
```

### Recursos da Interface:
- **Prévia do Teclado em Tempo Real**: Animação contínua ao vivo mesmo com o efeito parado. Ao mover qualquer controle, o teclado na tela responde instantaneamente.
- **Ajustes a Quente ("✓ Aplicar" e "⟲ Desfazer")**: Modifique velocidade, saturação, brilho, paleta ou efeito enquanto o teclado físico estiver funcionando e clique em "✓ Aplicar" para atualizar sem desconectar do USB, ou "⟲ Desfazer" para reverter.
- **Comboboxes em Alto Contraste**: Caixas de seleção com texto branco brilhante e fundo escuro em todos os estados, totalmente legíveis.
- **Seletores Interativos**:
  - Escolha de Efeito (*Flores Desabrochando* vs *Mosaico Aleatório*).
  - Escolha de Paleta (8 paletas disponíveis).
  - Seleção de Driver de Hardware (*Auto*, *Redragon K556 Nativo*, *OpenRGB SDK*, *Simulação*).
- **Controles Deslizantes Dinâmicos**:
  - Velocidade de transição (`0.2x` a `4.0x`).
  - Brilho global (`10%` a `100%`) com escala de hardware no nível 4 máximo.
  - Saturação de cores (`0%` monocromático a `200%` ultra saturado).
  - FPS Alvo (`15` a `60` FPS).
  - Máximo de flores simultâneas (no modo Blooming).
- **Botões de Ação**: Iniciar e Parar sem travar a interface (execução em thread separada com consumo desprezível de CPU).
- **Barra de Status**: Indicador de conexão de hardware e contador de FPS em tempo real.

---

## 🌈 Paletas de Cores Disponíveis

| Paleta | Nome | Tons e Características |
|---|---|---|
| 🌸 **Sakura** | `sakura` | Estame dourado, rosa cerejeira, magenta suave e pontas marfim |
| 🌈 **Rainbow** | `rainbow` | Arco-íris espectral completo vívido e contínuo |
| ⚡ **Cyberpunk** | `cyberpunk` | Ciano elétrico `#00F0FF`, Magenta neon `#FF007F`, Amarelo ácido `#FFE600` e Violeta |
| 🌌 **Aurora** | `aurora` | Verde polar `#00FF87`, Turquesa boreal, Índigo e Violeta real |
| 💜 **Lavender** | `lavender` | Lilás, violeta floral, azul celeste e púrpura suave |
| 🪷 **Lotus** | `lotus` | Rosa lótus aquático, azul piscina e toques de esmeralda |
| 🌻 **Sunflower** | `sunflower` | Âmbar profundo, amarelo ouro brilhante e reflexos quentes |
| 🌹 **Rose** | `rose` | Vermelho carmim profundo, rubi vibrante e rosa aveludado |

---

## 🚀 Como Executar via Terminal (CLI)

```bash
# Iniciar a Interface Gráfica interativa:
python -m openrgb_flowers --gui

# Efeito Mosaico de Cores Aleatórias (todas as teclas acesas misturando cores):
python -m openrgb_flowers --effect random_blend --palette rainbow --speed 1.3

# Efeito Flores Desabrochando com paleta Cyberpunk e prévia no terminal:
python -m openrgb_flowers --effect blooming --palette cyberpunk --speed 1.0 --preview

# Mosaico com paleta Aurora Nórdica:
python -m openrgb_flowers --effect random_blend --palette aurora --speed 1.5

# Flores com paleta Sakura:
python -m openrgb_flowers --effect blooming --palette sakura --speed 1.2
```

### Todos os Parâmetros do CLI:
| Parâmetro | Padrão | Descrição |
|---|---|---|
| `--gui` | `False` | Abre a interface gráfica interativa |
| `--effect, -e` | `blooming` | Tipo de efeito: `blooming` ou `random_blend` |
| `--palette, -p` | `sakura` | Paleta: `sakura`, `rainbow`, `cyberpunk`, `aurora`, `lavender`, `lotus`, `sunflower`, `rose` |
| `--driver` | `auto` | Driver: `auto` (K556 ou OpenRGB), `redragon` (USB HID nativo), `openrgb`, `mock` |
| `--speed, -s` | `1.0` | Multiplicador de velocidade da animação |
| `--brightness, -b` | `1.0` | Fator de brilho global (0.0 a 1.0) |
| `--saturation` | `1.0` | Saturação de cores (0.0 a 2.5) |
| `--fps` | `30.0` | Taxa de quadros alvo (15 a 60 FPS) |
| `--max-flowers, -m` | `7` | Máximo de flores simultâneas (no efeito blooming) |
| `--spawn-rate` | `1.4` | Taxa média de surgimento de novas flores por segundo |
| `--blend` | `weighted` | Modo de mesclagem: `weighted`, `screen`, `additive` |
| `--preview` | `False` | Exibe animação em 24-bit TrueColor no próprio terminal |
| `--mock` | `False` | Modo de simulação sem enviar comandos ao hardware |
| `--config, -c` | `None` | Caminho para arquivo de configuração JSON customizado |
| `--max-frames` | `None` | Limite opcional de quadros antes de encerrar automaticamente |

---

## 🏛️ Arquitetura SOLID & DRY

O projeto segue estritamente as melhores práticas de engenharia de software:
- **Single Responsibility (SRP)**: Cada abstração, modelo, motor, paleta e componente de interface possui seu próprio arquivo dedicado.
- **Open/Closed (OCP)**: Novos efeitos e paletas são integrados via `EffectEngineFactory` e `PaletteRegistry` sem modificar as classes existentes.
- **Liskov Substitution (LSP)**: `BloomingEngine` e `RandomBlendEngine` implementam `IEffectEngine` de forma totalmente intercambiável.
- **Zero-Allocation**: A renderização vetorizada via NumPy calcula frames em menos de 0.1ms, permitindo taxas de quadros altíssimas com menos de 0.5% de CPU.
- **Redragon WebHID Nativo**: Comunicação direta via USB HID (`2E3C:C365`) no Modo 10 com o comando `0x09` em 8 chunks de 64 bytes e nível de brilho 4 máximo.

---

## 🧪 Testes Automatizados

O projeto possui suíte completa de testes com **59 testes unitários**:

```bash
python -m pytest tests -v
```

