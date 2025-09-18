import requests
import asyncio

SERVER_URL = "http://localhost:8000"

def add_car(brand: str, model: str, price: float, rating: float):
    """Adiciona um carro ao servidor."""
    data = {
        "brand": brand,
        "model": model,
        "price": price,
        "rating": rating
    }
    response = requests.post(f"{SERVER_URL}/add_car", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to add car: {response.text}"}

def get_cars_by_brand(brand: str):
    """Obtém carros de uma marca específica do servidor."""
    response = requests.get(f"{SERVER_URL}/get_cars_by_brand", params={"brand": brand})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to get cars: {response.text}"}

def get_cars_by_model(model: str):
    """Obtém carros de um modelo específico do servidor."""
    response = requests.get(f"{SERVER_URL}/get_cars_by_model", params={"model": model})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to get cars: {response.text}"}

def get_all_cars():
    """Obtém todos os carros do servidor."""
    response = requests.get(f"{SERVER_URL}/get_all_cars")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to get cars: {response.text}"}

def add_car_with_date(brand: str, model: str, price: float, rating: float, launch_date: str):
    """Adiciona um carro ao servidor com data de lançamento."""
    data = {
        "brand": brand,
        "model": model,
        "price": price,
        "rating": rating,
        "launch_date": launch_date
    }
    response = requests.post(f"{SERVER_URL}/add_car_with_date", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to add car: {response.text}"}

def get_cars_filtered(brand: str = None, start_date: str = None, end_date: str = None, min_rating: float = None, limit: int = 10):
    """Obtém carros filtrados do servidor."""
    params = {}
    if brand:
        params["brand"] = brand
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if min_rating is not None:
        params["min_rating"] = min_rating
    params["limit"] = limit
    response = requests.get(f"{SERVER_URL}/get_cars_filtered", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to get cars: {response.text}"}

async def main():
    # Exemplo de uso do cliente
    print("Conectando ao servidor...")
    
    # Adicionar um carro
    result = add_car("Toyota", "Corolla", 80000.0, 4.5)
    print(f"Carro adicionado: {result}")
    
    # Buscar carros por marca
    cars = get_cars_by_brand("Toyota")
    print(f"Carros da marca Toyota: {cars}")
    
    # Buscar carros por modelo
    cars = get_cars_by_model("Corolla")
    print(f"Carros do modelo Corolla: {cars}")
    
    # Listar todos os carros
    cars = get_all_cars()
    print(f"Todos os carros: {cars}")

if __name__ == "__main__":
    asyncio.run(main())
