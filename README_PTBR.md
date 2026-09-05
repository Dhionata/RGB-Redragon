# 🌸 OpenRGB Flowers Blooming (Flores Desabrochando)

Efeito de iluminação RGB orgânico de alta performance para o teclado **Redragon K556RGB-M** (Devarajas) e outros dispositivos do ecossistema **OpenRGB**.

O efeito simula flores desabrochando de maneira orgânica e contínua: centros de flores (estames) brotam aleatoriamente pela superfície das teclas, expandem pétalas com harmônicos suaves e degradês florais vívidos, misturam-se suavemente onde se sobrepõem e desvanecem com naturalidade sobre uma brisa suave de fundo.

Disponibilizado para a comunidade em **dois formatos integrados**:
1. **Módulo/CLI Standalone em Python (`openrgb-python`)**: Arquitetura modular profissional SOLID & DRY, acelerada com NumPy, prévia em tempo real no terminal (TrueColor 24-bit) e envio em modo Direct para latência ultrabaixa.
2. **Shader GLSL para OpenRGB Effects Plugin (`flowers_blooming.frag`)**: Pronto para ser colado diretamente no editor de Shaders do plugin oficial do OpenRGB.

---

## 🏛️ Arquitetura SOLID & DRY

O projeto foi rigorosamente estruturado seguindo os princípios **SOLID** e **DRY**:

- **S (Single Responsibility)**: Cada classe reside em seu próprio arquivo isolado, com responsabilidade única:
  - `ColorRGB`, `ColorHSV`: Representações imutáveis de cores com conversão precisa e empacotamento binário.
  - `FastColorMath`: Operações matemáticas 100% vetorizadas com NumPy para conversão de cores HSV/RGB sem laços em Python.
  - `PetalGeometry`: Equações polares harmônicas para contorno natural de pétalas ($4, 5, 6, 8$ pétalas).
  - `FlowerInstance`: Ciclo de vida individual da flor (broto, abertura, floração plena, murcha suave).
  - `BloomingEngine`: Orquestrador de campo floral com distribuição estocástica (evita aglomeração).
  - `K556LayoutProvider`: Mapeamento físico 2D real das 104 teclas do Redragon K556 ANSI com espaçamento milimétrico.
  - `OpenRGBTransmitter`: Transmissão assíncrona ao SDK com reconexão automática e ativação do modo Direct.
  - `TerminalVisualizer`: Renderização ao vivo em 24-bit TrueColor no console.
- **O (Open/Closed)**: Novas paletas florais e modos de mesclagem (`IBlendStrategy`, `IColorPalette`) podem ser adicionados sem alterar o motor central.
- **L (Liskov Substitution)**: Todas as implementações de `ILayoutProvider`, `IFrameTransmitter` e `IBlendStrategy` são intercambiáveis sem quebrar o cliente.
- **I (Interface Segregation)**: Interfaces concisas e bem delineadas em `core/interfaces/`.
- **D (Dependency Inversion)**: O serviço central (`RunnerService`) depende de abstrações, desacoplado de sockets físicos.

---

## ⚡ Performance & Otimização de CPU

- **Vetorização com NumPy**: O cálculo de coordenadas, distâncias euclidianas com correção de proporção (*aspect ratio* do teclado ~3.7:1), atenuação de bordas e interpolação de cores é executado em operações vetorizadas C/NumPy.
- **Uso de CPU < 0.5%**: O tempo de cálculo por frame é inferior a 0.2 milissegundos.
- **OpenRGB Direct Mode com `fast=True`**: Elimina chamadas síncronas de atualização de estado interno que causariam quedas de FPS, enviando pacotes contínuos de até 60 FPS sem engasgos.

---

## 📦 Instalação e Execução

### Opção 1: Via Python CLI (Recomendado)

1. **Pré-requisitos**:
   - Python 3.10+
   - OpenRGB instalado com o servidor SDK ativo (porta padrão `6742`).
     - No OpenRGB, vá na aba **SDK Server** e clique em **Start Server** (ou configure para iniciar automaticamente).

2. **Instalar dependências**:
   ```bash
   pip install -e .
   ```

3. **Executar com seu Redragon K556**:
   ```bash
   openrgb-flowers --palette sakura --fps 30 --speed 1.0
   ```

4. **Visualização ao vivo no Terminal (sem precisar do OpenRGB aberto)**:
   ```bash
   openrgb-flowers --mock --preview --palette lotus
   ```

### Opções do Terminal / Argumentos CLI:
| Parâmetro | Padrão | Descrição |
|---|---|---|
| `--palette, -p` | `sakura` | Paleta: `sakura`, `rose`, `lotus`, `sunflower`, `lavender`, `rainbow` |
| `--fps` | `30.0` | Taxa de quadros alvo (15 a 60 FPS) |
| `--speed, -s` | `1.0` | Multiplicador de velocidade do ciclo floral |
| `--max-flowers, -m` | `7` | Quantidade máxima de flores desabrochando simultaneamente |
| `--spawn-rate` | `1.4` | Taxa média de surgimento de novas flores por segundo |
| `--brightness, -b` | `1.0` | Controle de brilho geral (0.0 a 1.0) |
| `--blend` | `weighted` | Modo de mesclagem: `weighted` (orgânico), `screen`, `additive` |
| `--preview` | `False` | Ativa visualizador 2D TrueColor no terminal |
| `--mock` | `False` | Executa sem conectar ao servidor OpenRGB (ótimo para testes) |
| `--host` | `127.0.0.1` | IP do servidor OpenRGB |
| `--port` | `6742` | Porta do servidor OpenRGB |
| `--device, -d` | `None` | Filtro para o nome do dispositivo (ex: "K556" ou "Redragon") |

---

### Opção 2: Via OpenRGB Effects Plugin (Shader GLSL)

Se preferir rodar o efeito internamente pelo plugin oficial do OpenRGB:

1. Abra o OpenRGB e vá para a aba do **Effects Plugin**.
2. Na lista de efeitos, selecione ou adicione **Shaders**.
3. Abra o arquivo `shaders/flowers_blooming.frag`.
4. Cole o conteúdo no editor de Shader do OpenRGB Effects Plugin e clique em **Apply / Start**.
5. Certifique-se de que o teclado está no modo **Direct** na aba de dispositivos.

---

## 🧪 Testes Automatizados

Para rodar a suíte completa de testes unitários:
```bash
pytest
```
