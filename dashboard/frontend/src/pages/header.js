export function renderHeader(activePage = "") {
    const header = document.getElementById("header");

    if (!header) {
        console.error("Header container not found.");
        return;
    }

    header.innerHTML = `
        <nav class="dashboard-header">
            <div class="dashboard-title">Used Car Price Dashboard</div>

            <div class="dashboard-nav">
                <a class="nav-button ${activePage === "statistics" ? "active" : ""}" href="index.html">
                    Statistics
                </a>

                <a class="nav-button ${activePage === "search" ? "active" : ""}" href="vehicles.html">
                    Search
                </a>

                <a class="nav-button ${activePage === "performance" ? "active" : ""}" href="results.html">
                    Model Performance
                </a>
            </div>
        </nav>
    `;
}