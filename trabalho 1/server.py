import sqlite3
from mcp.server.fastmcp import FastMCP
from flask import Flask, request, jsonify

# Inicializa o servidor MCP
mcp = FastMCP("car-analysis-server")

# Cria a tabela de carros se não existir
def init_db():
    conn = sqlite3.connect("cars.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            model TEXT,
            price REAL,
            rating REAL,
            launch_date TEXT
        )
    """)
    # Add launch_date column if it doesn't exist (for existing databases)
    try:
        conn.execute("ALTER TABLE cars ADD COLUMN launch_date TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.commit()
    conn.close()

# Ferramenta para adicionar dados de um carro ao banco de dados
@mcp.tool()
def add_car(brand: str, model: str, price: float, rating: float) -> bool:
    """Adiciona um carro ao banco de dados."""
    try:
        # Validação de entrada
        if not brand or not model:
            raise ValueError("Marca e modelo são obrigatórios.")
        if price <= 0:
            raise ValueError("Preço deve ser positivo.")
        if not (0 <= rating <= 5):
            raise ValueError("Nota deve estar entre 0 e 5.")

        conn = sqlite3.connect("cars.db")
        conn.execute(
            "INSERT INTO cars (brand, model, price, rating) VALUES (?, ?, ?, ?)",
            (brand, model, price, rating)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
        return False
    except ValueError as e:
        print(f"Erro de validação: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

@mcp.tool()
def add_car_with_date(brand: str, model: str, price: float, rating: float, launch_date: str) -> bool:
    """Adiciona um carro ao banco de dados com data de lançamento."""
    conn = sqlite3.connect("cars.db")
    conn.execute(
        "INSERT INTO cars (brand, model, price, rating, launch_date) VALUES (?, ?, ?, ?, ?)",
        (brand, model, price, rating, launch_date)
    )
    conn.commit()
    conn.close()
    return True

# Ferramenta para buscar carros por marca
@mcp.tool()
def get_cars_by_brand(brand: str) -> list:
    """Retorna uma lista de carros de uma determinada marca."""
    conn = sqlite3.connect("cars.db")
    cursor = conn.execute("SELECT brand, model, price, rating, launch_date FROM cars WHERE brand = ?", (brand,))
    cars = cursor.fetchall()
    conn.close()
    return [{"brand": row[0], "model": row[1], "price": row[2], "rating": row[3], "launch_date": row[4]} for row in cars]

# Ferramenta para buscar carros por modelo
@mcp.tool()
def get_cars_by_model(model: str) -> list:
    """Retorna uma lista de carros de um determinado modelo."""
    conn = sqlite3.connect("cars.db")
    cursor = conn.execute("SELECT brand, model, price, rating, launch_date FROM cars WHERE model = ?", (model,))
    cars = cursor.fetchall()
    conn.close()
    return [{"brand": row[0], "model": row[1], "price": row[2], "rating": row[3], "launch_date": row[4]} for row in cars]

# Ferramenta para buscar todos os carros
@mcp.tool()
def get_all_cars() -> list:
    """Retorna uma lista de todos os carros."""
    conn = sqlite3.connect("cars.db")
    cursor = conn.execute("SELECT brand, model, price, rating, launch_date FROM cars")
    cars = cursor.fetchall()
    conn.close()
    return [{"brand": row[0], "model": row[1], "price": row[2], "rating": row[3], "launch_date": row[4]} for row in cars]

@mcp.tool()
def get_cars_filtered(brand: str = None, start_date: str = None, end_date: str = None, min_rating: float = None, limit: int = 10) -> list:
    """Retorna uma lista de carros filtrados por marca, data de lançamento, nota mínima e limite."""
    conn = sqlite3.connect("cars.db")
    query = "SELECT brand, model, price, rating, launch_date FROM cars WHERE 1=1"
    params = []
    if brand:
        query += " AND brand = ?"
        params.append(brand)
    if start_date:
        query += " AND launch_date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND launch_date <= ?"
        params.append(end_date)
    if min_rating is not None:
        query += " AND rating >= ?"
        params.append(min_rating)
    query += " ORDER BY rating DESC LIMIT ?"
    params.append(limit)
    cursor = conn.execute(query, params)
    cars = cursor.fetchall()
    conn.close()
    return [{"brand": row[0], "model": row[1], "price": row[2], "rating": row[3], "launch_date": row[4]} for row in cars]

# Flask app for HTTP endpoints
app = Flask(__name__)

@app.route('/add_car', methods=['POST'])
def add_car_http():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Dados JSON obrigatórios"}), 400

        brand = data.get('brand')
        model = data.get('model')
        price = data.get('price')
        rating = data.get('rating')

        if not all([brand, model, price is not None, rating is not None]):
            return jsonify({"error": "Campos obrigatórios: brand, model, price, rating"}), 400

        success = add_car(brand, model, float(price), float(rating))
        if success:
            return jsonify({"message": "Car added successfully"})
        else:
            return jsonify({"error": "Falha ao adicionar carro"}), 500
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Erro de validação: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/add_car_with_date', methods=['POST'])
def add_car_with_date_http():
    data = request.json
    brand = data.get('brand')
    model = data.get('model')
    price = data.get('price')
    rating = data.get('rating')
    launch_date = data.get('launch_date')
    add_car_with_date(brand, model, price, rating, launch_date)
    return jsonify({"message": "Car added successfully"})

@app.route('/get_cars_by_brand', methods=['GET'])
def get_cars_by_brand_http():
    brand = request.args.get('brand')
    cars = get_cars_by_brand(brand)
    return jsonify(cars)

@app.route('/get_cars_by_model', methods=['GET'])
def get_cars_by_model_http():
    model = request.args.get('model')
    cars = get_cars_by_model(model)
    return jsonify(cars)

@app.route('/get_all_cars', methods=['GET'])
def get_all_cars_http():
    cars = get_all_cars()
    return jsonify(cars)

@app.route('/get_cars_filtered', methods=['GET'])
def get_cars_filtered_http():
    brand = request.args.get('brand')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    min_rating = request.args.get('min_rating')
    if min_rating:
        min_rating = float(min_rating)
    limit = request.args.get('limit', 10)
    limit = int(limit)
    cars = get_cars_filtered(brand, start_date, end_date, min_rating, limit)
    return jsonify(cars)

if __name__ == "__main__":
    # Inicializa o banco de dados
    init_db()
    print("Servidor iniciado...")
    app.run(host='0.0.0.0', port=8000)
