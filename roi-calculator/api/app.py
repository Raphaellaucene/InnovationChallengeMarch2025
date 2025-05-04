from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os
import logging

from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

app = Flask(__name__)

# Habilita CORS para as seguintes rotas
CORS(app, resources={r"/*": {"origins": ["https://raphaellaucene.github.io", "http://localhost:5000"]}}, methods=["POST"], allow_headers=["Content-Type", "Authorization"])

# env
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
INSTRUMENTATION_KEY = os.getenv("AZURE_INSTRUMENTATION_KEY")

# Configurar o logger para enviar logs ao Application Insights
logger = logging.getLogger(__name__)
connection_string = 'InstrumentationKey=6f8a879c-9567-44e1-9899-b49be41a80ec;IngestionEndpoint=https://eastus2-3.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus2.livediagnostics.monitor.azure.com/;ApplicationId=0fef1baa-886b-442d-9d47-3d78550cd06a'
logger.addHandler(AzureLogHandler(connection_string=connection_string))


# Configurar o tracer para enviar telemetria ao Application Insights
tracer = Tracer(exporter=AzureExporter(connection_string=f'InstrumentationKey={INSTRUMENTATION_KEY}'),
                sampler=ProbabilitySampler(1.0))

@app.route('/')
def sendMessage():
    try:
        with tracer.span(name='sendMessage') as span:
            span.add_attribute("http.method", "GET")
            span.add_attribute("endpoint", "/")
            logger.info('Message sent successfully!')
            span.add_annotation("Log message sent successfully.")
        return 'Message sent successfully!'
    except Exception as e:
        logger.exception("An error occurred: %s", str(e))
        return 'An error occurred', 500


@app.route('/calculate-roi', methods=['POST'])
def calculate_roi():
    data = request.json

    # Valida input
    required_fields = ['budget', 'employees', 'duration', 'trainingCost', 'implementationCost', 'costSavings', 'revenueIncrease', 'discountRate', 'riskOfFailure']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Cria o prompt
    prompt = (
        "Analyze the provided project data to determine the best project option, suggest corrections and improvements, "
        "identify potential problems, and deliver actionable recommendations. Ensure a detailed breakdown of all elements to support the analysis.\n\n"
        "## Instructions\n\n"
        "1. **Standardize Evaluation Criteria**:\n"
        "   - Identify which project performs best based on return on investment (ROI), net present value (NPV), or other suitable metrics derived from the provided data.\n"
        "   - Factor in financial components (e.g., budget, cost savings, revenue increase, training cost, implementation cost) and qualitative factors such as the number of impacted employees and risk of failure.\n\n"
        "2. **Suggest Corrections and Improvements**:\n"
        "   - Highlight areas where project inputs or assumptions could be improved, made more realistic, or optimized (e.g., cutting costs, reducing risk, reallocating resources).\n"
        "   - Suggest alternative approaches or solutions for achieving better results.\n\n"
        "3. **Identify Potential Problems and Risks**:\n"
        "   - Pinpoint risk areas such as exceeding the budget, unrealistic assumptions, or a high risk of failure.\n"
        "   - Evaluate whether the project duration, costs, or savings could be underestimated or overstated.\n\n"
        "4. **Add Insights and Recommendations**:\n"
        "   - Consider strategic impacts on the organization, employees, or operational goals beyond financial metrics.\n"
        "   - Highlight any additional opportunities or risks not explicitly stated in the data.\n\n"
        "# Steps\n\n"
        "1. **Financial Analysis**: Calculate and evaluate the financial performance for each project, including ROI, NPV, and payback period (if applicable). Use the provided discount rate to assess NPV and incorporate risk of failure into your analysis.\n"
        "2. **Comparative Analysis**: Compare results across projects or scenarios (use data placeholders or simplified data for single options if multiple projects aren't explicitly provided).\n"
        "3. **Identify Weaknesses**: Analyze cost structures, durations, and risk percentages to identify concerns or inefficiencies.\n"
        "4. **Provide Actionable Output**: Organize and present findings under clear categories (e.g., recommendations, risks) to ensure actionable insights.\n\n"
        "# Output Format\n\n"
        "The response must follow a structured format, with clear sections for analysis:\n\n"
        "1. **Best Project Option**: Provide a ranked recommendation on the project choice or suggest a 'go/no-go' decision.\n"
        "2. **Suggested Corrections and Improvements**:\n"
        "    - Clearly list specific suggestions for improving the input data, assumptions, or project feasibility.\n"
        "3. **Potential Problems and Risks**:\n"
        "    - Detail risks and potential problem areas with root causes identified and potential mitigations suggested.\n"
        "4. **Additional Insights and Recommendations**:\n"
        "    - Highlight strategic insights or opportunities that go beyond the provided data.\n"
        "5. **Detailed Reasoning Steps**: Show all calculations, steps, and assumptions to reach conclusions.\n\n"
        "# Example\n\n"
        "**Input**:\n"
        "```\n"
        "Project Budget: {budget}\n"
        "Number of Impacted Employees: {employees}\n"
        "Project Duration (months): {duration}\n"
        "Training Cost: {training_cost}\n"
        "Implementation Cost: {implementation_cost}\n"
        "Cost Savings: {cost_savings}\n"
        "Revenue Increase: {revenue_increase}\n"
        "Discount Rate (%): {discount_rate}\n"
        "Risk of Failure (%): {risk_of_failure}\n"
        "```\n\n"
        "**Output**:\n\n"
        "1. **Best Project Option**:\n"
        "   - Based on the data, this project yields strong financial returns with a positive NPV of $231,096 and an ROI of 75%. With modest risk, this is a viable option if training and implementation run on schedule.\n\n"
        "2. **Suggested Corrections and Improvements**:\n"
        "   - Reassess the budget's allocation for contingencies, as the project has a 10% risk of failure.\n"
        "   - Investigate whether training costs could be reduced by adopting alternative training methods.\n\n"
        "3. **Potential Problems and Risks**:\n"
        "   - The project’s revenue increase estimates could be overly optimistic, especially if market conditions shift.\n"
        "   - Implementation costs could rise by 10-20% if unforeseen challenges occur, which may strain the budget.\n\n"
        "4. **Additional Insights and Recommendations**:\n"
        "   - Beyond financial outcomes, this project has high strategic value due to the large number of impacted employees (150), which could improve morale and productivity.\n"
        "   - Monitor post-implementation performance closely to ensure cost savings and revenue gains are achieved.\n\n"
        "**Reasoning**:\n"
        "- The NPV was calculated using the formula: NPV = ∑ [(Revenue Increase + Cost Savings – Training/Implementation Cost) / (1 + Discount Rate)^n].\n"
        "- A risk of failure adjustment was factored by scaling expected outcomes by (1 - Risk of Failure%).\n\n"
        "# Notes\n\n"
        "- Ensure the analysis accounts for all significant elements provided in the input.\n"
        "- Emphasize actionable insights and realistic recommendations tailored to the data.\n"
        "- Adjust calculations or assumptions for missing data or uncertainties if needed."
    ).format(
        budget=data['budget'],
        employees=data['employees'],
        duration=data['duration'],
        training_cost=data['trainingCost'],
        implementation_cost=data['implementationCost'],
        cost_savings=data['costSavings'],
        revenue_increase=data['revenueIncrease'],
        discount_rate=data['discountRate'],
        risk_of_failure=data['riskOfFailure']
    )

    # Envia os dados para o Azure OpenAI
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are an assistant who analyzes project data."},
            {"role": "user", "content": prompt}
        ]
    }
    result = call_openai_api(payload)
    response = make_response(jsonify(result))
    return response

def call_openai_api(payload):
    headers = {
        'Content-Type': 'application/json',
        'api-key': f'{AZURE_OPENAI_API_KEY}'
    }
    response = requests.post(f"{AZURE_OPENAI_ENDPOINT}", headers=headers, json=payload)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)