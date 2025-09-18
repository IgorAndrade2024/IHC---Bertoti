# Manual do Sistema de Análise de Carros

## Introdução

Este sistema é uma aplicação completa para análise de imagens de carros, extração de informações via OCR (Reconhecimento Óptico de Caracteres) e gerenciamento de um banco de dados de carros. O sistema utiliza visão computacional para processar imagens, extrair dados como marca, modelo, preço e avaliação, e oferece interfaces para interação via chatbot e API HTTP.

## Arquitetura do Sistema

O sistema é composto por vários módulos interconectados:

### 1. Servidor MCP (server.py)
- **Função**: Servidor principal que gerencia o banco de dados e fornece ferramentas MCP
- **Tecnologias**: Python, Flask, SQLite, MCP (Model Context Protocol)
- **Responsabilidades**:
  - Gerenciamento do banco de dados SQLite
  - Exposição de ferramentas MCP para manipulação de dados
  - API HTTP REST para integração com outros sistemas
  - Validação de entrada e tratamento de erros

### 2. Processamento de Imagens (image_processing.py)
- **Função**: Análise de imagens de carros para extração de informações
- **Tecnologias**: OpenCV, Pytesseract, NumPy
- **Responsabilidades**:
  - Pré-processamento de imagens (conversão para escala de cinza, thresholding)
  - Extração de texto via OCR usando Tesseract
  - Parsing inteligente do texto extraído para identificar marca, modelo, preço e avaliação
  - Fallback para valores padrão em caso de falha

### 3. Chatbot (chatbot.py)
- **Função**: Interface de usuário baseada em texto
- **Tecnologias**: Python
- **Responsabilidades**:
  - Interpretação de comandos de texto do usuário
  - Análise de imagens enviadas pelo usuário
  - Consulta ao banco de dados
  - Adição de novos carros via texto natural

### 4. Cliente MCP (mcp_client.py)
- **Função**: Cliente para comunicação com o servidor
- **Tecnologias**: Python, Requests
- **Responsabilidades**:
  - Comunicação HTTP com o servidor
  - Execução de operações CRUD nos dados dos carros
  - Demonstração de uso programático do sistema

### 5. Banco de Dados
- **Tipo**: SQLite
- **Estrutura**:
  - Tabela `cars` com campos: id, brand, model, price, rating, launch_date
- **Características**:
  - Persistência local
  - Suporte a consultas complexas com filtros
  - Migração automática de schema

## Pré-requisitos do Sistema

### Requisitos Mínimos de Hardware
- **Processador**: Intel Core i3 ou equivalente
- **Memória RAM**: 4 GB
- **Armazenamento**: 500 MB de espaço livre
- **Sistema Operacional**: Windows 10+, Linux (Ubuntu 18.04+), macOS 10.14+

### Software Necessário

#### Python 3.8+
```bash
# Verificar versão do Python
python --version
# Deve mostrar Python 3.8 ou superior
```

#### Tesseract OCR
**Windows:**
1. Baixe o instalador do [site oficial](https://github.com/UB-Mannheim/tesseract/wiki)
2. Execute o instalador
3. Adicione o diretório de instalação ao PATH do sistema

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-por
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

## Instalação do Sistema

### 1. Clonagem/Preparação do Projeto
```bash
# Navegue até o diretório do projeto
cd /caminho/para/o/projeto
```

### 2. Criação do Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

### 3. Instalação das Dependências Python
```bash
pip install opencv-python numpy mcp flask requests pytesseract
```

### 4. Verificação da Instalação
```bash
# Verificar se todas as bibliotecas foram instaladas
python -c "import cv2, numpy, mcp, flask, requests, pytesseract; print('Todas as dependências instaladas com sucesso')"
```

## Como Executar o Sistema

### 1. Inicialização do Servidor
```bash
# Ativar ambiente virtual (se não estiver ativado)
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Executar o servidor
python server.py
```

**Saída esperada:**
```
Servidor iniciado...
 * Running on http://127.0.0.1:8000
```

### 2. Uso do Chatbot (em outro terminal)
```bash
# Em outro terminal, ativar ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Executar o chatbot
python chatbot.py
```

### 3. Teste dos Endpoints HTTP
```bash
# Adicionar um carro
curl -X POST http://localhost:8000/add_car \
  -H "Content-Type: application/json" \
  -d '{"brand":"Toyota","model":"Corolla","price":80000,"rating":4.5}'

# Listar todos os carros
curl http://localhost:8000/get_all_cars

# Buscar por marca
curl "http://localhost:8000/get_cars_by_brand?brand=Toyota"
```

### 4. Uso do Cliente MCP
```bash
python mcp_client.py
```

## Exemplos de Uso

### Análise de Imagem
```python
from image_processing import analyze_image

# Analisar uma imagem de carro
brand, model, price, rating = analyze_image("caminho/para/imagem.jpg")
print(f"Marca: {brand}, Modelo: {model}, Preço: {price}, Avaliação: {rating}")
```

### Uso do Chatbot
```
Digite seu comando: analisar /caminho/para/imagem.jpg
Digite seu comando: buscar marca Toyota
Digite seu comando: listar todos
Digite seu comando: sair
```

### API HTTP
```python
import requests

# Adicionar carro
response = requests.post("http://localhost:8000/add_car", json={
    "brand": "Honda",
    "model": "Civic",
    "price": 75000,
    "rating": 4.2
})

# Buscar carros
cars = requests.get("http://localhost:8000/get_cars_by_brand?brand=Honda").json()
```

## Especificações Técnicas

### Formatos de Imagem Suportados
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)

### Formatos de Texto Reconhecidos
- **Marca/Modelo**: "Marca: Toyota", "Brand: Honda", "Toyota Corolla"
- **Preço**: "R$ 80.000", "80000 reais", "Preço: 80000"
- **Avaliação**: "Nota: 4.5", "Rating: 4.5", "4.5/5"

### Limites do Sistema
- **Tamanho máximo da imagem**: 10 MB
- **Resolução recomendada**: 1920x1080 pixels
- **Idiomas suportados**: Português, Inglês
- **Precisão do OCR**: 85-95% (depende da qualidade da imagem)

### Endpoints da API HTTP

#### POST /add_car
- **Descrição**: Adiciona um novo carro
- **Parâmetros**: brand (string), model (string), price (float), rating (float 0-5)
- **Resposta**: {"message": "Car added successfully"}

#### POST /add_car_with_date
- **Descrição**: Adiciona um carro com data de lançamento
- **Parâmetros**: brand, model, price, rating, launch_date (string YYYY-MM-DD)
- **Resposta**: {"message": "Car added successfully"}

#### GET /get_all_cars
- **Descrição**: Lista todos os carros
- **Resposta**: Array de objetos carro

#### GET /get_cars_by_brand
- **Parâmetros**: brand (string)
- **Resposta**: Array de carros da marca especificada

#### GET /get_cars_filtered
- **Parâmetros**: brand, start_date, end_date, min_rating, limit
- **Resposta**: Array de carros filtrados

## Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
# Instalar dependências faltantes
pip install nome_do_modulo
```

### Erro: "Tesseract not found"
```bash
# Windows: Verificar se Tesseract está no PATH
tesseract --version

# Linux: Instalar Tesseract
sudo apt-get install tesseract-ocr
```

### Erro: "Porta 8000 já em uso"
```bash
# Matar processo na porta 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux:
sudo lsof -ti:8000 | xargs kill -9
```

### Imagens não sendo processadas corretamente
- Verificar se a imagem não está corrompida
- Garantir que o texto na imagem esteja legível
- Tentar imagens com melhor resolução
- Verificar se o Tesseract suporta o idioma do texto

### Chatbot não responde
- Verificar se o servidor está rodando
- Confirmar que o ambiente virtual está ativado
- Verificar logs do servidor para erros

## Logs e Depuração

### Logs do Servidor
O servidor gera logs automaticamente no console:
```
127.0.0.1 - - [Data] "GET /get_all_cars HTTP/1.1" 200 -
```

### Logs de Erro
Erros são exibidos no console com mensagens descritivas:
```
Erro ao analisar imagem: [mensagem de erro]. Usando valores padrão.
```

### Modo Debug
Para ativar modo debug no servidor, modificar server.py:
```python
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
```

## Manutenção e Atualização

### Backup do Banco de Dados
```bash
# Copiar arquivo do banco
cp cars.db cars_backup.db
```

### Atualização das Dependências
```bash
pip install --upgrade opencv-python numpy mcp flask requests pytesseract
```

### Limpeza de Dados
```bash
# Remover todos os registros (cuidado!)
sqlite3 cars.db "DELETE FROM cars;"
```

## Suporte e Contato

Para suporte técnico ou relatar bugs:
1. Verificar este manual
2. Consultar logs de erro
3. Testar com dados de exemplo
4. Abrir issue no repositório do projeto

## Conclusão

Este sistema oferece uma solução completa e robusta para análise de imagens de carros e gerenciamento de dados automotivos. Com sua arquitetura modular e interfaces múltiplas, pode ser facilmente integrado a outros sistemas ou usado como ferramenta independente para processamento de dados de veículos.
