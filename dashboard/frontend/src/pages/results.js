export async function loadResults() {

    const response = await fetch(`http://127.0.0.1:8000/performance`);
    const data = await response.json();
    return data;
}

export async function loadErrorDistribution() {
    const response = await fetch(`http://127.0.0.1:8000/performance/error_distribution`);
    const data = await response.json();
    return data;
}

export async function loadErrorQuartiles() {
    const response = await fetch(`http://127.0.0.1:8000/performance/error_quartiles`);
    const data = await response.json();
    return data;
}

export async function loadTopErrors(limit = 50) {
    const response = await fetch(`http://127.0.0.1:8000/performance/top_errors?limit=${limit}`);
    const data = await response.json();
    return data;
}

export async function loadShap(limit = 20) {
    const response = await fetch(`http://127.0.0.1:8000/shap_values?limit=${limit}`);
    const data = await response.json();
    return data;
}

export async function renderResultsTable(data) {
    const resultsTable = document.getElementById("resultsTable");

    if (!resultsTable) {
        console.error("resultsTable element not found.");
        return;
    }

    const thresholdValue = data.threshold_value ?? 1000;
    const filteredCount = data.filtered_count ?? data.counts ?? 0;
    const totalCount = data.total_count ?? 0;

    const metrics = [
        {
            label: "Evaluated listings",
            value: `${filteredCount.toLocaleString()} / ${totalCount.toLocaleString()}`,
            note: `Only listings above $${thresholdValue.toLocaleString()} were used.`
        },
        {
            label: "MAE",
            value: `$${Number(data.mae).toLocaleString(undefined, { maximumFractionDigits: 0 })}`,
            note: "Average dollar error."
        },
        {
            label: "RMSE",
            value: `$${Number(data.rmse).toLocaleString(undefined, { maximumFractionDigits: 0 })}`,
            note: "Large errors penalized more heavily."
        },
        {
            label: "R² score",
            value: Number(data.r2_score).toFixed(3),
            note: `Explains about ${(Number(data.r2_score) * 100).toFixed(1)}% of price variation.`
        },
        {
            label: "MAPE",
            value: `${Number(data.mean_absolute_percentage_error).toFixed(1)}%`,
            note: "Average percentage error."
        },
        {
            label: "Within 5%",
            value: `${Number(data.accuracy_within_5_percent).toFixed(1)}%`,
            note: "Predictions within 5% of actual price."
        },
        {
            label: "Within 10%",
            value: `${Number(data.accuracy_within_10_percent).toFixed(1)}%`,
            note: "Predictions within 10% of actual price."
        },
        {
            label: "Within 20%",
            value: `${Number(data.accuracy_within_20_percent).toFixed(1)}%`,
            note: "Predictions within 20% of actual price."
        }
    ];

    resultsTable.innerHTML = `
        <div class="metrics-list">
            ${metrics.map(metric => `
                <div class="metric-row">
                    <div>
                        <div class="metric-label">${metric.label}</div>
                        <div class="metric-note">${metric.note}</div>
                    </div>
                    <div class="metric-value">${metric.value}</div>
                </div>
            `).join("")}
        </div>
    `;
}

export async function renderErrorDistributionBarChart(data) {
    const labels = data.map(d => d.error_range);
    const counts = data.map(d => d.frequency);

    const colors = labels.map((_, i) =>
        `hsl(${(i * 360) / labels.length},70%,60%)`
    );

    new Chart(document.getElementById("errorDistribution"), {
        type:"bar",
        data:{
            labels,
            datasets:[{
                label: "Listings",
                data: counts,
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
        }
    });

}

export async function renderErrorQuartilesTable(data) {
    console.log("Rendering error quartiles table with data:", data);
    const titleMap = {
        "q1": "1st Quartile (25th percentile)",
        "q2": "2nd Quartile (Median, 50th percentile)",
        "q3": "3rd Quartile (75th percentile)",
        "median": "Median",
        "p90": "90th Percentile",
        "p95": "95th Percentile",
    }
    const errorQuartiles = document.getElementById("errorQuartiles");
    errorQuartiles.innerHTML = `
        <div class="metrics-list">
            <table class = "table table-sm border-bottom-0" id = "errorQuartilesTable">
            <thead>
                <tr>
                    <th scope="col">Quartile</th>
                    <th scope="col">Absolute Error</th>
                </tr>
            </thead>
            <tbody>
                ${Object.entries(data).map(([quartile, value]) => `
                    <tr>
                        <td class = "fw-bold">${titleMap[quartile] || quartile}</td>
                        <td>$${Number(value).toFixed(2)}</td>
                    </tr>
                `).join("")}
            </tbody>
            </table>
        </div>
    `;

}

export async function renderTopShapFeatures(data) {
    console.log(data);

    const labels = data.map(row => row.feature.replaceAll("_", " ").toUpperCase());
    const values = data.map(row => row.importance);

    const canvas = document.getElementById("explainability");

    new Chart(canvas, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Mean absolute SHAP value",
                data: values,
                backgroundColor: "rgba(54, 99, 181, 0.75)",
                borderColor: "rgba(54, 99, 181, 1)",
                borderWidth: 1,
                barThickness: 18,
                maxBarThickness: 24
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    right: 12
                }
            },
        }
    });
}