from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

app = Flask(__name__)

# Substitua com suas credenciais do Azure OpenAI
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

@app.route('/calculate-roi', methods=['POST'])
def calculate_roi():
    data = request.json

    # Valida input
    required_fields = ['budget', 'employees', 'duration', 'trainingCost', 'implementationCost', 'costSavings', 'revenueIncrease', 'discountRate', 'riskOfFailure']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Envia os dados para o Azure OpenAI
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {AZURE_OPENAI_API_KEY}'
    }
    payload = {
        "prompt": f"Calculate ROI with the following data: {data}",
        "max_tokens": 100
    }
    response = requests.post(f"{AZURE_OPENAI_ENDPOINT}/v1/engines/davinci-codex/completions", headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({"error": "Failed to get response from Azure OpenAI"}), 500

    result = response.json()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)