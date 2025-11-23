async function sendText() {
    const transcript = document.getElementById("inputText").value.trim();
    if (!transcript) {
        alert("Please enter a transcript.");
        return;
    }

    try {
        const response = await fetch("/score", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ transcript: transcript })
        });

        if (!response.ok) {
            const err = await response.json();
            document.getElementById("output").innerHTML = `<p style="color:red;">Error: ${err.error}</p>`;
            return;
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        document.getElementById("output").innerHTML = `<p style="color:red;">Error: ${error}</p>`;
    }
}

function displayResults(data) {
    let html = `<h3>Overall Score: ${data.overall_score} / 100</h3>`;
    html += `<p>Word Count: ${data.word_count}</p>`;
    html += `<table>
                <tr>
                    <th>Criterion Name</th>
                    <th>Metric</th>
                    <th>Score (0-100)</th>
                    <th>Feedback</th>
                </tr>`;

    data.criteria.forEach(c => {
        html += `<tr>
                    <td>${c.criterion_name}</td>
                    <td>${c.metric}</td>
                    <td>${c.score}</td>
                    <td>${c.feedback}</td>
                </tr>`;
    });

    html += `</table>`;
    document.getElementById("output").innerHTML = html;
}
