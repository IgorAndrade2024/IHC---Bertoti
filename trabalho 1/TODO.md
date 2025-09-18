# TODO List for Car Info Parsing and Query System

## 1. Extend Database Schema
- [x] Modify server.py to add 'launch_date' column to the 'cars' table.

## 2. Add MCP Server Tools
- [x] Add 'add_car_with_date' tool in server.py to insert car with launch_date.
- [x] Add 'get_cars_filtered' tool in server.py to query with filters (brand, date_range, rating).

## 3. Implement Text Prompt Parser
- [x] Create a new function in chatbot.py or a separate module to parse user text prompts and extract brand, rating, launch_date.

## 4. Extend Chatbot Interface
- [x] Modify chatbot.py to accept text prompts for adding cars (e.g., "add car: o novo carro da Nissan lançado ontem é nota 9").
- [x] Modify chatbot.py to accept query prompts (e.g., "query: quais os 10 melhores carros da Nissan lançados entre 2010 e hoje").
- [x] Update chatbot.py to use HTTP requests with new endpoints.

## 5. Update MCP Client
- [x] Extend mcp_client.py with new async functions for add_car_with_date and get_cars_filtered.

## 6. Testing
- [x] Syntax check passed for server.py, chatbot.py, mcp_client.py.
- [x] Code compiles without errors.
- [x] HTTP endpoints tested successfully: add_car, add_car_with_date, get_all_cars, get_cars_by_brand, get_cars_filtered.
- [x] MCP client import issue: Fixed by replacing with HTTP requests.
- [x] Chatbot interactive testing: Started successfully, commands recognized.
- [x] Image processing function: Implemented with OCR using pytesseract.

## 7. Documentation
- [x] Provide explanation of how the system works.
