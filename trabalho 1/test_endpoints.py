import requests
import json

SERVER_URL = "http://localhost:8000"

def test_get_all_cars():
    response = requests.get(f"{SERVER_URL}/get_all_cars")
    print(f"GET /get_all_cars: {response.status_code}")
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.text)

def test_add_car():
    data = {
        "brand": "Toyota",
        "model": "Corolla",
        "price": 80000.0,
        "rating": 4.5
    }
    response = requests.post(f"{SERVER_URL}/add_car", json=data)
    print(f"POST /add_car: {response.status_code}")
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.text)

def test_get_cars_by_brand():
    response = requests.get(f"{SERVER_URL}/get_cars_by_brand?brand=Toyota")
    print(f"GET /get_cars_by_brand: {response.status_code}")
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.text)

def test_add_car_with_date():
    data = {
        "brand": "Honda",
        "model": "Civic",
        "price": 75000.0,
        "rating": 4.2,
        "launch_date": "2023-01-01"
    }
    response = requests.post(f"{SERVER_URL}/add_car_with_date", json=data)
    print(f"POST /add_car_with_date: {response.status_code}")
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.text)

def test_get_cars_filtered():
    response = requests.get(f"{SERVER_URL}/get_cars_filtered?brand=Toyota&min_rating=4.0&limit=5")
    print(f"GET /get_cars_filtered: {response.status_code}")
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    print("Testing endpoints...")
    test_get_all_cars()
    test_add_car()
    test_get_cars_by_brand()
    test_add_car_with_date()
    test_get_cars_filtered()
    print("Testing completed.")
