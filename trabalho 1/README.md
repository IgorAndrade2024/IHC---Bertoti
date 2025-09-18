# Sistema de Análise de Carros com Chatbot

Este projeto implementa um sistema que utiliza visão computacional para analisar imagens de carros e extrair informações como marca, modelo, preço e nota. O sistema inclui um servidor MCP, um módulo de processamento de imagem e um chatbot para interação com o usuário.

## Estrutura do Projeto

- `server.py`: Servidor MCP que gerencia o banco de dados de carros e fornece ferramentas para manipulação dos dados.
- `image_processing.py`: Módulo responsável por analisar imagens de carros e extrair informações.
- `chatbot.py`: Interface de chatbot para interação com o usuário.
- `mcp_client.py`: Cliente MCP para se comunicar com o servidor.

## Instalação

### Dependências Python

```bash
pip install opencv-python numpy mcp flask requests pytesseract
```

### Tesseract OCR

Para o processamento de imagens com OCR, instale o Tesseract:

- **Windows**: Baixe e instale do [site oficial](https://github.com/UB-Mannheim/tesseract/wiki). Adicione ao PATH.
- **Linux**: `sudo apt-get install tesseract-ocr tesseract-ocr-por`
- **macOS**: `brew install tesseract tesseract-lang`

## Como Usar

### 1. Iniciar o Servidor

```bash
python server.py
```

O servidor criará um banco de dados SQLite chamado `cars.db` e estará pronto para receber requisições.

### 2. Usar o Chatbot

```bash
python chatbot.py
```

O chatbot oferece os seguintes comandos:
- `analisar <caminho_da_imagem>`: Analisa uma imagem de carro e adiciona ao banco de dados.
- `buscar marca <marca>`: Busca carros por marca.
- `buscar modelo <modelo>`: Busca carros por modelo.
- `listar todos`: Lista todos os carros cadastrados.
- `sair`: Encerra o chatbot.

### 3. Usar o Cliente MCP

```bash
python mcp_client.py
```

O cliente MCP demonstra como se comunicar diretamente com o servidor para adicionar e buscar carros.

### 4. Usar a API HTTP

O servidor também fornece endpoints HTTP para integração com outras aplicações:

- `POST /add_car`: Adiciona um carro (JSON: brand, model, price, rating)
- `POST /add_car_with_date`: Adiciona um carro com data (JSON: brand, model, price, rating, launch_date)
- `GET /get_all_cars`: Lista todos os carros
- `GET /get_cars_by_brand?brand=<marca>`: Busca por marca
- `GET /get_cars_filtered?brand=<marca>&min_rating=<nota>&limit=<limite>`: Busca filtrada

Exemplo com curl:
```bash
curl -X POST http://localhost:8000/add_car -H "Content-Type: application/json" -d '{"brand":"Toyota","model":"Corolla","price":80000,"rating":4.5}'
```

## Personalização

### Processamento de Imagem

O arquivo `image_processing.py` contém uma implementação fictícia da função `analyze_image`. Para um sistema real, você deve substituir esta função por um modelo de visão computacional treinado para reconhecer carros e extrair as informações relevantes.

### Banco de Dados

O servidor utiliza um banco de dados SQLite chamado `cars.db`. Você pode modificar o esquema do banco de dados editando a função `init_db` em `server.py`.

## Dependências

- Python 3.x
- OpenCV (cv2)
- NumPy
- Biblioteca MCP (mcp.server.fastmcp e mcp.client.fastmcp)
- Pytesseract (para OCR)
- Tesseract OCR (deve ser instalado separadamente no sistema)
- Flask
- Requests
- Pillow (instalado com pytesseract)

## Limitações

- A implementação atual do processamento de imagem é fictícia e retorna valores fixos.
- O chatbot é um exemplo simples de interface de texto e pode ser expandido para suportar outros tipos de entrada e saída.
- O sistema não inclui autenticação ou medidas de segurança avançadas, o que seria necessário em um ambiente de produção.
