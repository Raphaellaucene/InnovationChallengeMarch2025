function calculateROI() {
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

    const disengagementCost = employees * 1000; // Custo de desengajamento de funcionários
    const productivityIncrease = budget * 0.15; // 15% do orçamento para aumento de produtividade
    const totalCost = budget + trainingCost + implementationCost + disengagementCost;
    const riskAdjustedCost = totalCost * (1 + riskOfFailure); // Custo ajustado para risco (opcional)
    const totalBenefits = costSavings + revenueIncrease + productivityIncrease;

    const roi = ((totalBenefits - riskAdjustedCost) / riskAdjustedCost) * 100;

    let recommendation = "";
    if (roi > 0) {
        recommendation = "The project is financially viable. Consider proceeding.";
    } else {
        recommendation = "The project may not be viable. Evaluate the risks and costs.";
    }

    document.getElementById('roi-output').innerHTML = `ROI: ${roi.toFixed(2)}%`;
    document.getElementById('recommendations-output').innerHTML = recommendation;
}

document.getElementById('roi-form').addEventListener('submit', function(event) {
    event.preventDefault();
    calculateROI();
});