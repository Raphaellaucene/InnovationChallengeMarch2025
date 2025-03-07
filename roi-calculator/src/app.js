function calculateROI() {
    const budget = parseFloat(document.getElementById('budget').value);
    const employees = parseInt(document.getElementById('employees').value);
    const duration = parseInt(document.getElementById('duration').value);
    const trainingCost = parseFloat(document.getElementById('training-cost').value);
    const implementationCost = parseFloat(document.getElementById('implementation-cost').value);
    const costSavings = parseFloat(document.getElementById('cost-savings').value);
    const revenueIncrease = parseFloat(document.getElementById('revenue-increase').value);
    const discountRate = parseFloat(document.getElementById('discount-rate').value) / 100;

    if (isNaN(budget) || isNaN(employees) || isNaN(duration) || isNaN(trainingCost) || isNaN(implementationCost) || isNaN(costSavings) || isNaN(revenueIncrease) || isNaN(discountRate) || budget <= 0 || employees <= 0 || duration <= 0 || trainingCost < 0 || implementationCost < 0 || costSavings < 0 || revenueIncrease < 0 || discountRate < 0) {
        alert("Por favor, insira valores válidos.");
        return;
    }

    const riskOfFailure = 0.2; // 20% risco do projeto falhar
    const disengagementCost = employees * 1000; // Custos de desligamento de funcionários
    const productivityIncrease = budget * 0.15; // 15% de aumento na produtividade
    const totalCost = budget + trainingCost + implementationCost + disengagementCost;
    const totalBenefits = costSavings + revenueIncrease + productivityIncrease;

    const roi = ((totalBenefits - totalCost) / totalCost) * 100;

    let recommendation = "";
    if (roi > 0) {
        recommendation = "O projeto é financeiramente viável. Considere prosseguir.";
    } else {
        recommendation = "O projeto pode não ser viável. Avalie os riscos e custos.";
    }

    document.getElementById('roi-output').innerHTML = `ROI: ${roi.toFixed(2)}%`;
    document.getElementById('recommendations-output').innerHTML = recommendation;
}

document.getElementById('roi-form').addEventListener('submit', function(event) {
    event.preventDefault();
    calculateROI();
});