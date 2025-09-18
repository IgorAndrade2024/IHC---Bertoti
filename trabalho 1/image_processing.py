import cv2
import numpy as np
import pytesseract
import re

def analyze_image(image_path: str) -> tuple:
    """Analisa a imagem e retorna a marca, modelo, preço e nota do carro."""
    try:
        # Carregar a imagem
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Imagem não pôde ser carregada.")

        # Pré-processamento da imagem para melhorar OCR
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Extrair texto da imagem usando OCR
        text = pytesseract.image_to_string(gray, lang='por+eng')  # Suporte para português e inglês

        # Parsear o texto extraído para encontrar marca, modelo, preço e nota
        brand = extract_value(text, ['marca', 'brand'], default="Desconhecida")
        model = extract_value(text, ['modelo', 'model'], default="Desconhecido")
        price = extract_price(text)
        rating = extract_rating(text)

        return brand, model, price, rating

    except Exception as e:
        print(f"Erro ao analisar imagem: {e}. Usando valores padrão.")
        # Fallback para valores fictícios
        brand = "Marca Exemplo"
        model = "Modelo Exemplo"
        price = 20000.0
        rating = 4.5
        return brand, model, price, rating

def extract_value(text: str, keywords: list, default: str) -> str:
    """Extrai valor baseado em palavras-chave."""
    text_lower = text.lower()
    for keyword in keywords:
        pattern = rf"{keyword}[:\s]*([^\n\r]+)"
        match = re.search(pattern, text_lower)
        if match:
            return match.group(1).strip().title()
    return default

def extract_price(text: str) -> float:
    """Extrai preço do texto."""
    # Procurar por padrões de preço, como R$ 50000 ou 50000 reais
    patterns = [
        r"R\$\s*(\d+(?:[.,]\d+)?)",
        r"(\d+(?:[.,]\d+)?)\s*reais?",
        r"preço[:\s]*(\d+(?:[.,]\d+)?)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            price_str = match.group(1).replace(',', '.')
            try:
                return float(price_str)
            except ValueError:
                pass
    return 50000.0  # Valor padrão

def extract_rating(text: str) -> float:
    """Extrai nota do texto."""
    # Procurar por padrões de nota, como nota 4.5 ou rating 4.5
    patterns = [
        r"nota[:\s]*(\d+(?:[.,]\d+)?)",
        r"rating[:\s]*(\d+(?:[.,]\d+)?)",
        r"(\d+(?:[.,]\d+)?)/5",
        r"(\d+(?:[.,]\d+)?)/10"
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            rating_str = match.group(1).replace(',', '.')
            try:
                rating = float(rating_str)
                if rating > 10:  # Se for /10, converter para /5
                    rating /= 2
                return min(max(rating, 0), 5)  # Limitar entre 0 e 5
            except ValueError:
                pass
    return 4.0  # Valor padrão
