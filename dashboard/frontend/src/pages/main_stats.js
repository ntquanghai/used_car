export async function loadManufacturerChart(limit = 20) {

    const response = await fetch(`http://127.0.0.1:8000/stats/manufacturer?limit=${limit}`);
    const data = await response.json();
    console.log(data);

    const labels = data.map(d => d.manufacturer);
    const counts = data.map(d => d.count);

    const colors = labels.map((_, i) =>
        `hsl(${(i * 360) / labels.length},70%,60%)`
    );

    new Chart(document.getElementById("manufacturerChart"), {
        type:"bar",
        // options:{
        //     maintainAspectRatio: false,
        // },
        data:{
            labels,
            datasets:[{
                label: "Listings",
                data:counts,
                backgroundColor:colors
            }]
        }
    });
}

export async function loadCondition() {

    const response = await fetch("http://127.0.0.1:8000/stats/condition");
    const data = await response.json();

    const labels = data.map(d => d.condition);
    const counts = data.map(d => d.count);

    const conditionColors = {
        "new": "#1B5E20",         // Dark Green
        "like new": "#2E7D32",    // Green
        "excellent": "#43A047",   // Medium Green
        "good": "#81C784",        // Light Green
        "fair": "#FDD835",        // Yellow
        "salvage": "#D32F2F",     // Red
        "unknown": "#9E9E9E"      // Gray
    };

    const colors = labels.map(label =>
        conditionColors[label.toLowerCase()] ?? "#9E9E9E"
    );
    new Chart(document.getElementById("conditionChart"), {
        type:"bar",
        // options:{
        //     maintainAspectRatio: false,
        // },
        data:{
            labels,
            datasets:[{
                label: "Conditions",
                data:counts,
                backgroundColor:colors
            }]
        }
    });

}

export async function loadPrice() {
    document.getElementById("priceHistogram").innerHTML = "Loading...";

    const response = await fetch("http://127.0.0.1:8000/stats/price");
    const data = await response.json();
    const priceList = document.getElementById("priceStats");

    const price_hist = data[0];
    const price_stats = data[1];

    const bins = price_hist.bins;
    const counts = price_hist.counts;

    const skipped_cols = ["min_price","max_price"]
    const label_map = {
        "avg_price": "Mean",
        "median":"Median",
        "q1": "1st Quartile",
        "q3": "3rd Quartile",
        "p05": "5% Percentile",
        "p90": "90% Percentile",
        "p95": "95% Percentile"
    }

    for (const stat in price_stats) {

        if (skipped_cols.includes(stat)) continue;

        const li = document.createElement("li");
        li.className = "price-stat";

        li.innerHTML = `
            <span class="price-stat-label">
                ${label_map[stat] ?? stat}
            </span>

            <span class="price-stat-value">
                $${Math.round(price_stats[stat]).toLocaleString()}
            </span>
        `;

        priceList.appendChild(li);
    }
    new Chart(
        document.getElementById("priceHistogram"),
        {
            type: "bar",
            data: {
                labels: bins.map(v => `$${Math.round(v).toLocaleString()}`),

                datasets: [{
                    label: "Number of Listings",
                    data: counts,
                    backgroundColor: "rgba(54,162,235,0.7)",
                    borderColor: "rgb(54,162,235)",
                    borderWidth: 1,
                    barPercentage: 1, 
                    categoryPercentage: 1,
                }]
            },

            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: "Vehicle Price Distribution"
                    },

                    legend: {
                        display: false
                    }
                },

                scales: {

                    x: {
                        title: {
                            display: true,
                            text: "Price"
                        },
                        ticks: {
                            maxTicksLimit: 6
                        }
                    },

                    y: {
                        beginAtZero: true,

                        title: {
                            display: true,
                            text: "Listings"
                        }
                    }

                }
            }
        }
    );



    return data;
}

