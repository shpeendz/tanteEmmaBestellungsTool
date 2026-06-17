let products = [];
let cart = [];

async function loadProducts() {
    const response = await fetch("/api/artikel");
    if (!response.ok) {
        throw new Error("Produkte konnten nicht geladen werden");
    }

    products = await response.json();
    renderProducts(products);
}

function renderProducts(items) {
    const grid = document.getElementById("product-grid");
    grid.innerHTML = "";

    items.forEach(item => {
        const card = document.createElement("article");
        card.className = "product-card";
        card.innerHTML = `
            <div class="product-media">🛍️</div>
            <div class="product-body">
                <span class="product-tag">${item.kategorie || "Artikel"}</span>
                <h4>${item.bezeichnung}</h4>
                <p>Bestand: ${item.bestand}</p>
            </div>
            <div class="product-footer">
                <strong>${item.preis.toFixed(2)} €</strong>
                <button class="btn btn-primary small-btn" onclick="addToCart(${item.id})">
                    In den Warenkorb
                </button>
            </div>
        `;
        grid.appendChild(card);
    });
}

function addToCart(id) {
    const product = products.find(p => p.id === id);
    if (!product) return;

    const existing = cart.find(item => item.artikel_id === id);

    if (existing) {
        existing.menge += 1;
    } else {
        cart.push({
            artikel_id: product.id,
            bezeichnung: product.bezeichnung,
            preis: product.preis,
            menge: 1
        });
    }

    renderCart();
}

function renderCart() {
    const cartItems = document.getElementById("cart-items");
    const cartTotal = document.getElementById("cart-total");
    const cartCount = document.getElementById("cart-count");

    cartItems.innerHTML = "";

    let total = 0;

    cart.forEach(item => {
        total += item.preis * item.menge;

        const row = document.createElement("div");
        row.className = "cart-item";
        row.innerHTML = `
            <div>
                <strong>${item.bezeichnung}</strong>
                <p>${item.menge} × ${item.preis.toFixed(2)} €</p>
            </div>
            <button onclick="removeFromCart(${item.artikel_id})">X</button>
        `;
        cartItems.appendChild(row);
    });

    cartTotal.textContent = total.toFixed(2) + " €";
    cartCount.textContent = cart.reduce((sum, item) => sum + item.menge, 0);
}

function removeFromCart(id) {
    cart = cart.filter(item => item.artikel_id !== id);
    renderCart();
}