# Application Feature Analysis

This document provides a comprehensive feature analysis of the **Flask-Ecommerce** application, evaluating each core feature against its implementation status in the codebase.

---

## 1. Feature Availability Overview

| Feature | Exists? | Status Summary |
| :--- | :---: | :--- |
| **Home Page** | ✅ | Fully implemented with banners, flash sale items, and layout components. |
| **Login** | ✅ | Implemented with Flask-Login and secure password verification. |
| **Registration** | ✅ | Implemented with WTForms, password hashing, and duplicate check. |
| **Product Details** | Card only | Product cards show basic information. A dedicated product page is a potential enhancement. |
| **Search** | ✅ | Filters products by name with case-insensitive matching. |
| **Cart** | ✅ | Supports adding items and calculating totals. AJAX handlers are present for quantity changes and removal. |
| **Checkout** | Partial | Order processing logic exists alongside a test-mode payment integration with placeholder credentials. |
| **Categories** | UI only | Displayed in the home page sidebar as static links. |

---

## 2. Detailed Feature Breakdown

### 🏠 Home Page (`✅`)
* **Route:** `/` (`website/views.py`)
* **Template:** `website/templates/home.html`
* **Details:**
  * Displays flash-sale products fetched from the SQLite database (`Product.query.filter_by(flash_sale=True)`).
  * Includes a promotional banner, promotional badges (Free Delivery, Tech Week, Food, etc.), and side widgets.
  * Renders an icon in the storefront navigation for the number of distinct entries in the signed-in customer's cart.

---

### 🔑 User Login (`✅`)
* **Route:** `/login` (`website/auth.py`)
* **Template:** `website/templates/login.html`
* **Details:**
  * Uses `Flask-Login` session management (`login_user`).
  * Validates credentials against salted password hashes using Werkzeug's `check_password_hash`.
  * Redirects to the home page after successful login and displays a flash message when credentials are rejected.

---

### 📝 User Registration (`✅`)
* **Route:** `/sign-up` (`website/auth.py`)
* **Template:** `website/templates/signup.html`
* **Details:**
  * Managed via `SignUpForm` (`website/forms.py`).
  * Uses an HTML email input for browser-side format checks. On the server, the form requires an email address, a username of at least two characters, and password fields of at least six characters.
  * The signup route checks that the passwords match. A mismatch redisplays the form without a dedicated message.
  * Hashes passwords before persisting to database (`generate_password_hash`).
  * The database enforces email uniqueness. The signup route displays a duplicate-email message if saving the new account raises an exception.

---

### 📦 Product Details (`✅` / Minimal)
* **Status:** Basic product information is visible on item cards.
* **Details:**
  * Product picture, product title, current price, previous price, and stock levels are rendered directly on product cards (`home.html` and `search.html`).
  * *Note:* There is currently no dedicated single-product details page (e.g., `/product/<id>`) for expanded product descriptions, specifications, or customer reviews.

---

### 🔍 Search (`✅`)
* **Route:** `/search` (`website/views.py`)
* **Template:** `website/templates/search.html`
* **Details:**
  * Accessible from the main navigation on pages that use the storefront layout.
  * Queries the database using `Product.query.filter(Product.product_name.ilike(f'%{search_query}%'))` for case-insensitive partial matching.
  * Displays matching products in a responsive grid with direct "Add to Cart" capability.

---

### 🛒 Shopping Cart (`✅`)
* **Routes:**
  * View Cart: `/cart` (`website/views.py`)
  * Add Item: `/add-to-cart/<int:item_id>`
  * Increase Quantity: `/pluscart` (AJAX GET)
  * Decrease Quantity: `/minuscart` (AJAX GET)
  * Remove Item: `/removecart` (AJAX GET)
* **Template:** `website/templates/cart.html`
* **Details:**
  * Tied to authenticated customer accounts via database foreign keys (`customer_link`).
  * Uses jQuery (`myScript.js`) to send asynchronous requests for quantity changes and removal. The Remove link retains its default navigation. Removal and the empty-cart state still need browser verification.
  * Calculates the cart subtotal from unit prices and quantities and adds a delivery fee of Ksh 200 to the displayed total for a nonempty cart.

---

### 💳 Checkout (Partial)
* **Route:** `/place-order` (`website/views.py`)
* **Details:**
  * The route calculates the total and calls IntaSend M-Pesa STK Push in test mode with placeholder credentials and a placeholder phone number.
  * After receiving the expected API response, the route creates order records, decrements inventory, and removes the purchased items from the customer's cart.
  * The cart links directly to the order route. A dedicated form for a shipping address, phone number, or delivery notes is a potential enhancement.
  * If order placement raises an exception, the route displays `Order not placed` and redirects to the home page.

---

### 🗂️ Categories (UI Only)
* **Template:** `website/templates/home.html`
* **Details:**
  * Displays a full sidebar of product categories:
    * *Supermarket, Health & Beauty, Home & Office, Fashion, Electronics, Gaming, Baby Products, Sporting Goods, Garden & Outdoor.*
  * *Note:* In the current version, these category links are static placeholders (`<a href="">`). Products in the database do not currently have a `category` column to filter by.

---

## 3. Additional Existing Features

The application also includes these workflows.

1. **Admin Management Dashboard (`website/admin.py`):**
   * Add shop items with image upload (`/add-shop-items`).
   * View all inventory products (`/shop-items`).
   * Edit existing products (`/update-item/<id>`).
   * Delete products (`/delete-item/<id>`).
   * View and update customer order statuses (`/view-orders`, `/update-order/<id>`).
2. **User Profile & Password Management (`website/auth.py`):**
   * View customer profile (`/profile/<id>`).
   * Change account password (`/change-password/<id>`).
3. **Customer Order History (`website/views.py`):**
   * View products, quantities, prices, and order statuses (`/orders`). Payment IDs are stored in the database.

---

## 4. Possible Future App Enhancements

The SQE plan focuses on automating login, registration, search, and cart. The following enhancements are outside that scope. See the [implementation plan](IMPLEMENTATION_PLAN.md).

1. **Checkout improvements:**
   * Read payment credentials from environment variables.
   * Add a checkout form to collect shipping address and customer phone number before payment trigger.
2. **Dynamic Categories:**
   * Add a `category` string column to `Product` model in `website/models.py`.
   * Create a `/category/<name>` route to enable filtering.
3. **Dedicated Product Details Page:**
   * Add `/product/<int:product_id>` route and `product_details.html` template for in-depth viewing.
