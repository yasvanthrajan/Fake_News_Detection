async function analyzeNews() {
  const newsInput = document.getElementById('newsInput').value;
  const resultDiv = document.getElementById('result');

  if (!newsInput.trim()) {
    resultDiv.innerHTML = '<p style="color: #dc3545;">Please enter a news article to analyze.</p>';
    resultDiv.className = 'show';
    return;
  }

  resultDiv.innerHTML = '<div class="loading">Analyzing content</div>';
  resultDiv.className = 'show';

  try {
    const response = await fetch('https://o2qkj1tq67.execute-api.us-east-1.amazonaws.com/prod/FakeNewsAnalysisLambda', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ news: newsInput })
    });

    if (!response.ok) {
      const errorMessage = await response.text();
      throw new Error(errorMessage);
    }

    const data = await response.json();
    
    // Determine result class
    const resultClass = data.result.toLowerCase().includes('fake') ? 'fake' : 'real';
    const confidenceScore = parseFloat(data.confidence_score) || 0;
    
    setTimeout(() => {
      resultDiv.className = `show ${resultClass}`;
      resultDiv.innerHTML = `
        <h3>Analysis Result</h3>
        <div class="result-item">
          <strong>Verdict:</strong> <span>${data.result}</span>
        </div>
        <div class="result-item">
          <strong>Confidence Score:</strong> <span>${data.confidence_score}</span>
          <div class="info-icon" data-tooltip="Higher is more confident">i</div>
          <div class="progress-bar">
            <div class="progress-bar-fill" style="width: ${confidenceScore * 100}%; background-color: ${getColorForConfidence(confidenceScore)};"></div>
          </div>
        </div>
        <div class="result-item">
          <strong>External Check:</strong> <span>${data.external_check}</span>
        </div>
      `;
      
      // Animate the progress bar
      setTimeout(() => {
        const progressFill = document.querySelector('.progress-bar-fill');
        if (progressFill) {
          progressFill.style.width = `${confidenceScore * 100}%`;
        }
      }, 100);
    }, 1000); // Added delay for effect
  } catch (error) {
    resultDiv.innerHTML = `<p style="color: #dc3545;">Error: ${error.message}</p>`;
    resultDiv.className = 'show';
  }
}

function getColorForConfidence(score) {
  // Generate color from red to green based on score
  if (score < 0.5) {
    // Red to yellow (low confidence)
    const g = Math.round(score * 2 * 255);
    return `rgb(255, ${g}, 0)`;
  } else {
    // Yellow to green (high confidence)
    const r = Math.round((1 - (score - 0.5) * 2) * 255);
    return `rgb(${r}, 255, 0)`;
  }
}