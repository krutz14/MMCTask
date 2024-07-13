function predictCost() {
    // Fetch input values
    const age = document.getElementById('age').value;
    const industry = document.getElementById('SectorIndustry').value;
    const claimType = document.getElementById('claimType').value;
    if (!age || !industry || !claimType) {
        alert('Please fill all fields.');
        return;
    }

    const inputData = {
        age: parseInt(age),
        industry: industry,
        claimType: claimType
    };

    
    if (age > 50 && claimType=='Medical Only')
        predictedCost="More than 100000";
    else
        predictedCost="Less than 10000";

    // Displaying the result
    document.getElementById('prediction').textContent = `Predicted Claim Cost: ${predictedCost}`;
}
