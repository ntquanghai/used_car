let currentPage = 1;
let currentSearch = "";
let currentSort = "id";
let currentLimit = 25;

export function getCurrentPage() {
    return currentPage;
}

export function getCurrentSearch() {
    return currentSearch;
}

export function getCurrentLimit() {
    return currentLimit;
}

export function getCurrentSort() {
    return currentSort;
}

export async function loadVehicles(
    limit = currentLimit, 
    page = currentPage, 
    search = currentSearch,
    sort_by = currentSort
) {
    const vehicleTable = document.getElementById("vehicleTable");
    const response = await fetch(`http://127.0.0.1:8000/vehicles?limit=${limit}&page=${page}&search=${search}&sort_by=${sort_by}`);
    const data = await response.json();

    return data
}

export async function onSearch() {
    const searchForm = document.getElementById("search");
    
    searchForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        currentSearch = e.target[0].value;
        currentPage = 1;

        await reloadVehicles();
    });
}

export async function getVehiclePageLimit(
    limit = currentLimit,
    search = currentSearch
) {
    const response = await fetch(
        `http://127.0.0.1:8000/vehicles/vehicle_page_count?limit=${limit}&search=${search}`
    );

    const data = await response.json();

    return data;
}
export async function renderVehiclesTable(data) {
    const vehicleTable = document.getElementById("vehicleTable");
    vehicleTable.replaceChildren()

    const vehicle_keys = Object.keys(data[0])
    const tHead = document.createElement("thead")
    const tHeadRows = document.createElement("tr")

    const floatKeys = ["price","predicted_price","absolute_error","miles_per_year"]
    for (const vehicle_key of vehicle_keys) {
        const vehicle_key_normalized = vehicle_key.replaceAll("_"," ").toUpperCase()
        const th = document.createElement("th")
        th.classList = ""
        th.scope = "col"
        th.textContent = vehicle_key_normalized
        tHeadRows.appendChild(th)
    }
    tHead.appendChild(tHeadRows)
    vehicleTable.appendChild(tHead)

    const tBody = document.createElement("tbody")
    for (const vehicle of data) {
        const tr = document.createElement("tr");
        for (const vehicle_key of vehicle_keys) {
            const td = document.createElement("td")
            if (floatKeys.includes(vehicle_key)) {
                td.textContent = Math.ceil(vehicle[vehicle_key])
            }
            else {
                td.textContent = vehicle[vehicle_key]
            }
            tr.appendChild(td)
        }
        tBody.appendChild(tr)
    }
    vehicleTable.appendChild(tBody)
}

export async function reloadVehicles() {
    const data = await loadVehicles();
    const pageLimitData = await getVehiclePageLimit();

    renderVehiclesTable(data);
    renderPagination(pageLimitData);
}

export function renderPagination(pageLimit) {

    const paginationNavBar = document.getElementById("paginationNavBar");
    paginationNavBar.replaceChildren();

    const displayPage  = getCurrentPage();

    const ul = document.createElement("ul");
    ul.className = "pagination";

    function createButton(text, page, disabled = false, active = false, id = "", event) {

        const li = document.createElement("li");
        li.className = "page-item";

        if (disabled)
            li.classList.add("disabled");

        if (active)
            li.classList.add("active");

        const a = document.createElement("a");
        a.className = "page-link";
        a.href = "#";

        if (id)
            a.id = id;

        if (!disabled)
            a.dataset.page = page;

        a.textContent = text;

        li.appendChild(a);


        return li;
    }

    // First
    ul.appendChild(
        createButton("<<", 1, displayPage  === 1, false, "paginationFirst")
    );

    // Previous
    ul.appendChild(
        createButton("<", displayPage  - 1, displayPage  === 1, false, "paginationPrev")
    );

    // Current page window
    const start = Math.max(1, displayPage  - 1);
    const end = Math.min(pageLimit, start + 2);

    for (let page = start; page <= end; page++) {

        ul.appendChild(
            createButton(
                page,
                page,
                false,
                page === displayPage ,
                `pagination${page}`
            )
        );

    }

    // Page indicator
    ul.appendChild(
        createButton(
            `Page ${displayPage } / ${pageLimit}`,
            null,
            true
        )
    );

    // Next
    ul.appendChild(
        createButton(
            ">",
            displayPage  + 1,
            displayPage  === pageLimit,
            false,
            "paginationNext"
        )
    );

    // Last
    ul.appendChild(
        createButton(
            ">>",
            pageLimit,
            displayPage === pageLimit,
            false,
            "paginationLast"
        )
    );

    paginationNavBar.appendChild(ul);
    ul.addEventListener("click", async (e) => {

        e.preventDefault();

        const target = e.target;

        if (!target.classList.contains("page-link")) {
            return;
        }

        if (!target.dataset.page) {
            return;
        }

        currentPage = Number(target.dataset.page);

        await reloadVehicles();
    });
}

export async function onOrderBy() {
    const filters = ["id","manufacturer","model","price","odometer","condition"]
    const orderByFilter = document.getElementById("selectOrderBy");

    for (const filter of filters) {
        const option = document.createElement("option")
        if(filter == "id") {
            option.selected = true;
        }
        option.value = filter
        option.textContent = filter.toUpperCase()
        orderByFilter.appendChild(option)
    }

    orderByFilter.addEventListener('change', async (event) => {
    // 3. Log the selected value
        currentSort = event.target.value;
        console.log(currentSort)
        
        await reloadVehicles();
    });
}


