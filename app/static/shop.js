let products = [];
let cart = [];
let activeCategory = "Alle";

document.addEventListener("DOMContentLoaded", () => {
    bindUI();
    loadProducts();
    renderCart();
});

function bindUI() {
    const searchInput = document.getElementById("shop-search");
    const searchButton = document.getElementById("search-btn");
    const cartToggle = document.getElementById("cart-toggle");
    const checkoutBtn = document.getElementById("checkout-btn");

    if (searchInput) {
        searchInput.addEventListener("input", applyFilters);
    }

    if (searchButton) {
        searchButton.addEventListener("click", applyFilters);
    }

    document.querySelectorAll("[data-category]").forEach(button => {
        button.addEventListener("click", () => {
            activeCategory = button.dataset.category;
            applyFilters();

            document.querySelectorAll("[data-category]").forEach(btn => {
                btn.classList.remove("active-category");
            });
            button.classList.add("active-category");
        });
    });

    if (cartToggle) {
        cartToggle.addEventListener("click", () => {
            const cartSection = document.getElementById("warenkorb");
            if (cartSection) {
                cartSection.scrollIntoView({ behavior: "smooth" });
            }
        });
    }

    if (checkoutBtn) {
        checkoutBtn.addEventListener("click", checkout);
    }
}

async function loadProducts() {
    const feedback = document.getElementById("shop-feedback");
    if (feedback) {
        feedback.textContent = "Produkte werden geladen...";
    }

    try {
        const response = await fetch("/api/artikel");

        if (!response.ok) {
            throw new Error("Produkte konnten nicht geladen werden");
        }

        products = await response.json();

        if (feedback) {
            feedback.textContent = "";
        }

        applyFilters();
    } catch (error) {
        if (feedback) {
            feedback.textContent = "Fehler beim Laden der Produkte.";
        }
        console.error(error);
    }
}

function applyFilters() {
    const searchInput = document.getElementById("shop-search");
    const searchTerm = (searchInput?.value || "").trim().toLowerCase();

    const filtered = products.filter(item => {
        const matchesSearch =
            item.bezeichnung.toLowerCase().includes(searchTerm) ||
            (item.kategorie || "").toLowerCase().includes(searchTerm);

        const matchesCategory =
            activeCategory === "Alle" ||
            (item.kategorie || "").toLowerCase().includes(activeCategory.toLowerCase());

        return matchesSearch && matchesCategory;
    });

    renderProducts(filtered);
}

function renderProducts(items) {
    const grid = document.getElementById("product-grid");
    if (!grid) return;

    grid.innerHTML = "";

    if (items.length === 0) {
        grid.innerHTML = `
            <article class="product-card">
                <div class="product-body">
                    <h4>Keine Produkte gefunden</h4>
                    <p>Versuche eine andere Suche oder Kategorie.</p>
                </div>
            </article>
        `;
        return;
    }

    items.forEach(item => {
        const card = document.createElement("article");
        card.className = "product-card";

        const bestandText = Number(item.bestand) > 0
            ? `Bestand: ${item.bestand}`
            : "Aktuell nicht verfügbar";

        card.innerHTML = `
            <div class="product-media">${getEmojiForCategory(item.kategorie)}</div>
            <div class="product-body">
                <span class="product-tag">${item.kategorie || "Artikel"}</span>
                <h4>${escapeHtml(item.bezeichnung)}</h4>
                <p>${bestandText}</p>
            </div>
            <div class="product-footer">
                <strong>${formatPrice(item.preis)}</strong>
                <button
                    class="btn btn-primary small-btn"
                    type="button"
                    ${Number(item.bestand) <= 0 ? "disabled" : ""}
                    data-add-to-cart="${item.id}">
                    ${Number(item.bestand) <= 0 ? "Nicht verfügbar" : "In den Warenkorb"}
                </button>
            </div>
        `;

        grid.appendChild(card);
    });

    document.querySelectorAll("[data-add-to-cart]").forEach(button => {
        button.addEventListener("click", () => {
            addToCart(Number(button.dataset.addToCart));
        });
    });
}

function addToCart(id) {
    const product = products.find(p => Number(p.id) === id);
    if (!product) return;
    if (Number(product.bestand) <= 0) return;

    const existing = cart.find(item => item.artikel_id === id);

    if (existing) {
        if (existing.menge < Number(product.bestand)) {
            existing.menge += 1;
        }
    } else {
        cart.push({
            artikel_id: product.id,
            bezeichnung: product.bezeichnung,
            preis: Number(product.preis),
            menge: 1,
            maxBestand: Number(product.bestand)
        });
    }

    renderCart();
}

function changeQuantity(id, delta) {
    const item = cart.find(entry => entry.artikel_id === id);
    if (!item) return;

    item.menge += delta;

    if (item.menge <= 0) {
        cart = cart.filter(entry => entry.artikel_id !== id);
    } else if (item.menge > item.maxBestand) {
        item.menge = item.maxBestand;
    }

    renderCart();
}

function removeFromCart(id) {
    cart = cart.filter(item => item.artikel_id !== id);
    renderCart();
}

function renderCart() {
    const cartItems = document.getElementById("cart-items");
    const cartTotal = document.getElementById("cart-total");
    const cartCount = document.getElementById("cart-count");
    const cartCountSummary = document.getElementById("cart-count-summary");

    if (!cartItems || !cartTotal || !cartCount || !cartCountSummary) return;

    cartItems.innerHTML = "";

    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="cart-empty">
                <h4>Dein Warenkorb ist leer</h4>
                <p>Lege Produkte in den Warenkorb, um eine Bestellung vorzubereiten.</p>
            </div>
        `;
    } else {
        cart.forEach(item => {
            const row = document.createElement("div");
            row.className = "cart-item";
            row.innerHTML = `
                <div class="cart-item-info">
                    <strong>${escapeHtml(item.bezeichnung)}</strong>
                    <p>${formatPrice(item.preis)} pro Stück</p>
                </div>

                <div class="cart-qty-controls" aria-label="Menge für ${escapeHtml(item.bezeichnung)}">
                    <button type="button" class="qty-btn" data-qty-action="minus" data-id="${item.artikel_id}">−</button>
                    <span class="qty-value">${item.menge}</span>
                    <button type="button" class="qty-btn" data-qty-action="plus" data-id="${item.artikel_id}">+</button>
                </div>

                <div class="cart-item-price">
                    <strong>${formatPrice(item.preis * item.menge)}</strong>
                    <button type="button" class="remove-btn" data-remove-id="${item.artikel_id}">
                        Entfernen
                    </button>
                </div>
            `;
            cartItems.appendChild(row);
        });
    }

    document.querySelectorAll("[data-remove-id]").forEach(button => {
        button.addEventListener("click", () => {
            removeFromCart(Number(button.dataset.removeId));
        });
    });

    document.querySelectorAll("[data-qty-action]").forEach(button => {
        button.addEventListener("click", () => {
            const id = Number(button.dataset.id);
            const action = button.dataset.qtyAction;
            changeQuantity(id, action === "plus" ? 1 : -1);
        });
    });

    const itemCount = cart.reduce((sum, item) => sum + item.menge, 0);
    const total = cart.reduce((sum, item) => sum + (item.preis * item.menge), 0);

    cartCount.textContent = itemCount;
    cartCountSummary.textContent = itemCount;
    cartTotal.textContent = formatPrice(total);
}

async function checkout() {
    if (cart.length === 0) {
        alert("Dein Warenkorb ist leer.");
        return;
    }

    alert("Checkout-API kommt als Nächstes. Aktuell funktioniert der Warenkorb im Frontend.");
}

function formatPrice(value) {
    return `${Number(value).toFixed(2).replace(".", ",")} €`;
}

function getEmojiForCategory(category) {
    const value = (category || "").toLowerCase();

    if (value.includes("obst")) return "🍎";
    if (value.includes("gemüse")) return "🥦";
    if (value.includes("milch")) return "🥛";
    if (value.includes("back")) return "🍞";
    if (value.includes("bio")) return "🌿";
    return "🛍️";
}

function escapeHtml(text) {
    return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}