var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

function calculateROI() {
    return __awaiter(this, void 0, void 0, function* () {
        const budget = parseFloat(document.getElementById('budget').value);
        const employees = parseInt(document.getElementById('employees').value);
        const duration = parseInt(document.getElementById('duration').value);
        const trainingCost = parseFloat(document.getElementById('training-cost').value);
        const implementationCost = parseFloat(document.getElementById('implementation-cost').value);
        const costSavings = parseFloat(document.getElementById('cost-savings').value);
        const revenueIncrease = parseFloat(document.getElementById('revenue-increase').value);
        const discountRate = parseFloat(document.getElementById('discount-rate').value) / 100;
        let riskOfFailure = parseFloat(document.getElementById('risk-of-failure').value) / 100;
        // Define um valor default se riskOfFailure não for informado
        if (isNaN(riskOfFailure) || riskOfFailure < 0) {
            riskOfFailure = 0;
        }
        // Valida input
        if (isNaN(budget) || isNaN(employees) || isNaN(duration) || isNaN(trainingCost) || isNaN(implementationCost) || isNaN(costSavings) || isNaN(revenueIncrease) || isNaN(discountRate) || budget <= 0 || employees <= 0 || duration <= 0 || trainingCost < 0 || implementationCost < 0 || costSavings < 0 || revenueIncrease < 0 || discountRate < 0) {
            alert("Please enter valid values.");
            return;
        }
        const data = {
            budget: budget,
            employees: employees,
            duration: duration,
            trainingCost: trainingCost,
            implementationCost: implementationCost,
            costSavings: costSavings,
            revenueIncrease: revenueIncrease,
            discountRate: discountRate * 100, // converte devolta para porcentagem
            riskOfFailure: riskOfFailure * 100
        };
        try {
            console.log('Sending data to API:', data);
            const response = yield fetch('https://supraroiapi-hje5akbba9fha2cz.eastus2-01.azurewebsites.net/calculate-roi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            const result = yield response.json();
            console.log('Received result from API:', result);
            // Verifica se a resposta contém o campo esperado
            if (result.choices && result.choices[0] && result.choices[0].message && result.choices[0].message.content) {
                const messageContent = result.choices[0].message.content;
                const htmlContent = marked(messageContent); //transforma markdown em HTML
                const resultsElement = document.getElementById('results');
                if (resultsElement) {
                    resultsElement.innerHTML = yield htmlContent;
                }
                else {
                    throw new Error('Results element not found');
                }
            }
            else {
                throw new Error('Unexpected response format');
            }
        }
        catch (error) {
            console.error('There was a problem with the fetch operation:', error);
            alert('There was an error calculating the ROI. Please try again later.');
        }
    });
}
document.getElementById('roi-form').addEventListener('submit', function (event) {
    event.preventDefault();
    calculateROI();
});
