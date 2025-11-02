import requests
import json
import re
import datetime
from image_processing import analyze_image
from carregararctic import text_to_sql
import sqlite3

# URL do servidor MCP (ajuste conforme necessário)
SERVER_URL = "http://localhost:8000"

def add_car_to_server(brand: str, model: str, price: float, rating: float):
    """Adiciona um carro ao servidor."""
    payload = {
        "brand": brand,
        "model": model,
        "price": price,
        "rating": rating
    }
    response = requests.post(f"{SERVER_URL}/add_car", json=payload)
    return response.json()

def get_cars_by_brand(brand: str):
    """Obtém carros de uma marca específica do servidor."""
    response = requests.get(f"{SERVER_URL}/get_cars_by_brand?brand={brand}")
    return response.json()

def get_cars_by_model(model: str):
    """Obtém carros de um modelo específico do servidor."""
    response = requests.get(f"{SERVER_URL}/get_cars_by_model?model={model}")
    return response.json()

def get_all_cars():
    """Obtém todos os carros do servidor."""
    response = requests.get(f"{SERVER_URL}/get_all_cars")
    return response.json()

def process_image_and_add_car(image_path: str):
    """Processa a imagem e adiciona o carro ao servidor."""
    brand, model, price, rating = analyze_image(image_path)
    result = add_car_to_server(brand, model, price, rating)
    return result

def parse_add_prompt(prompt: str) -> dict:
    """Parse a prompt to add a car, e.g., 'o novo carro da Nissan lançado ontem é nota 9'."""
    # Extract brand
    brand_match = re.search(r'da (\w+)', prompt)
    brand = brand_match.group(1) if brand_match else "Desconhecida"

    # Extract rating
    rating_match = re.search(r'nota (\d+)', prompt)
    rating = float(rating_match.group(1)) if rating_match else 5.0

    # Extract launch date
    launch_date = None
    if "ontem" in prompt:
        launch_date = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    elif "hoje" in prompt:
        launch_date = datetime.date.today().isoformat()
    else:
        date_match = re.search(r'(\d{4})', prompt)
        if date_match:
            launch_date = f"{date_match.group(1)}-01-01"

    # Default model and price
    model = "Novo Modelo"
    price = 50000.0

    return {
        "brand": brand,
        "model": model,
        "price": price,
        "rating": rating,
        "launch_date": launch_date
    }

def parse_query_prompt(prompt: str) -> dict:
    """Parse a query prompt, e.g., 'quais os 10 melhores carros da Nissan lançados entre 2010 e hoje'."""
    # Extract brand
    brand_match = re.search(r'da (\w+)', prompt)
    brand = brand_match.group(1) if brand_match else None

    # Extract limit
    limit_match = re.search(r'(\d+) melhores', prompt)
    limit = int(limit_match.group(1)) if limit_match else 10

    # Extract date range
    start_date = None
    end_date = None
    date_match = re.search(r'entre (\d{4}) e (\w+)', prompt)
    if date_match:
        start_year = date_match.group(1)
        end_word = date_match.group(2)
        start_date = f"{start_year}-01-01"
        if end_word == "hoje":
            end_date = datetime.date.today().isoformat()
        else:
            end_date = f"{end_word}-12-31"

    return {
        "brand": brand,
        "start_date": start_date,
        "end_date": end_date,
        "min_rating": None,
        "limit": limit
    }

def chatbot():
    """Interface simples do chatbot."""
    print("Bem-vindo ao Chatbot de Análise de Carros!")
    print("Você pode enviar uma imagem de um carro para análise ou usar comandos de texto.")
    print("Comandos disponíveis:")
    print("1. 'analisar <caminho_da_imagem>' - Analisar uma imagem de carro")
    print("2. 'buscar marca <marca>' - Buscar carros por marca")
    print("3. 'buscar modelo <modelo>' - Buscar carros por modelo")
    print("4. 'listar todos' - Listar todos os carros")
    print("5. 'adicionar <descrição do carro>' - Adicionar carro via texto, ex: 'adicionar o novo carro da Nissan lançado ontem é nota 9'")
    print("6. 'consultar <consulta>' - Consultar carros via texto, ex: 'consultar quais os 10 melhores carros da Nissan lançados entre 2010 e hoje'")
    print("7. 'sair' - Sair do chatbot")
    
    while True:
        user_input = input("\nDigite seu comando: ").strip()
        
        if user_input.lower() == 'sair':
            print("Até logo!")
            break
        elif user_input.startswith('analisar '):
            image_path = user_input[9:]  # Remove 'analisar ' do início
            try:
                result = process_image_and_add_car(image_path)
                print(f"Carro adicionado: {result}")
            except Exception as e:
                print(f"Erro ao analisar a imagem: {e}")
        elif user_input.startswith('buscar marca '):
            brand = user_input[13:]  # Remove 'buscar marca ' do início
            try:
                cars = get_cars_by_brand(brand)
                if cars:
                    print(f"Carros da marca {brand}:")
                    for car in cars:
                        print(f"  - Modelo: {car['model']}, Preço: R${car['price']}, Nota: {car['rating']}")
                else:
                    print(f"Nenhum carro encontrado para a marca {brand}.")
            except Exception as e:
                print(f"Erro ao buscar carros: {e}")
        elif user_input.startswith('buscar modelo '):
            model = user_input[14:]  # Remove 'buscar modelo ' do início
            try:
                cars = get_cars_by_model(model)
                if cars:
                    print(f"Carros do modelo {model}:")
                    for car in cars:
                        print(f"  - Marca: {car['brand']}, Preço: R${car['price']}, Nota: {car['rating']}")
                else:
                    print(f"Nenhum carro encontrado para o modelo {model}.")
            except Exception as e:
                print(f"Erro ao buscar carros: {e}")
        elif user_input == 'listar todos':
            try:
                cars = get_all_cars()
                if cars:
                    print("Todos os carros:")
                    for car in cars:
                        print(f"  - Marca: {car['brand']}, Modelo: {car['model']}, Preço: R${car['price']}, Nota: {car['rating']}")
                else:
                    print("Nenhum carro cadastrado.")
            except Exception as e:
                print(f"Erro ao listar carros: {e}")
        elif user_input.startswith('adicionar '):
            prompt = user_input[9:]
            try:
                car_info = parse_add_prompt(prompt)
                # Use add_car_with_date endpoint
                payload = {
                    "brand": car_info["brand"],
                    "model": car_info["model"],
                    "price": car_info["price"],
                    "rating": car_info["rating"],
                    "launch_date": car_info["launch_date"]
                }
                response = requests.post(f"{SERVER_URL}/add_car_with_date", json=payload)
                if response.status_code == 200:
                    print("Carro adicionado com sucesso via texto!")
                else:
                    print(f"Erro ao adicionar carro: {response.text}")
            except Exception as e:
                print(f"Erro ao processar comando de adicionar: {e}")
        elif user_input.startswith('consultar '):
            prompt = user_input[9:]
            try:
                # Gera SQL a partir do prompt em linguagem natural
                sql_query = text_to_sql(prompt)
                print(f"\n🧠 SQL gerado pelo modelo:\n{sql_query}\n")

                # Executa a query diretamente no banco local
                conn = sqlite3.connect("cars.db")
                cursor = conn.cursor()
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                conn.close()

                if rows:
                    print("📊 Resultados da consulta:")
                    for row in rows:
                        print(row)
                else:
                    print("Nenhum resultado encontrado.")

            except Exception as e:
                print(f"Erro ao processar comando de consultar: {e}")

if __name__ == "__main__":
    chatbot()
