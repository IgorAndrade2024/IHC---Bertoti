from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "Snowflake/Arctic-Text2SQL-R1-7B"

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)

# Modelo
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # melhora performance se tiver GPU
    device_map="auto",
    use_auth_token=True
)

# Função de inferência
def text_to_sql(prompt):
    schema = """
    Tabela: cars
    Colunas: id, brand, model, price, rating, launch_date
    """
    full_prompt = f"{schema}\n\nUsuário: {prompt}\nSQL:"
    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_length=512)
    sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return sql