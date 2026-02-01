This **Product Requirements Document (PRD)** translates the agreed-upon features into a formal specification for development.

### **Product Requirements Document (PRD)**

**Project Name:** Lily’s Florist Web Application
**Version:** 1.0
**Status:** Ready for Development
**Date:** January 25, 2026
**Target Audience:** Customers, Lily (Manager), Florist Staff, Delivery Drivers

---

### **1. Executive Summary**

Lily’s Florist is transitioning from manual, pen-and-paper operations to a digital-first web platform. The core objective is to automate inventory management (preventing overselling) and streamline the order fulfillment pipeline by providing role-specific tools for staff.

**Key Success Metrics:**

* **Zero Inventory Conflicts:** System prevents ordering if raw materials (stems) are unavailable.
* **Operational Efficiency:** Eliminates the need for Lily to manually transcribe phone orders into production lists.
* **Delivery Accuracy:** Drivers access digital manifests, reducing delivery errors.

---

### **2. User Personas & Problems**

| Persona | Role | Core Problem | Solution |
| --- | --- | --- | --- |
| **The Customer** | Shopper | Unsure if items are in stock; wants convenient delivery. | Real-time stock checks; Easy Zone/Time selection. |
| **Lily** | Manager | Constant fear of overselling flowers she doesn't have. | "Recipe-based" inventory deduction. |
| **The Florist** | Staff | Confused by product names (e.g., "Love Bouquet") without knowing ingredients. | "Production View" showing the exact recipe (e.g., 12 Roses). |
| **The Driver** | Staff | Overwhelmed by paperwork containing sensitive sales data. | "Logistics View" showing only addresses and routing info. |

---

### **3. Functional Requirements**

#### **3.1 Inventory & Product Management (Critical Path)**

The system must manage stock at the **Raw Material** level, not the Product level.

* **FR-INV-01 (Recipe System):** The system shall link every Product to a "Recipe" of Raw Materials (e.g., 1 Bouquet = 5 Roses + 3 Ferns).
* **FR-INV-02 (Dynamic Availability):** Before adding to cart, the system must calculate: `Min(Raw_Material_Stock / Recipe_Requirement)`. If the result is < 1, the product is "Out of Stock".
* **FR-INV-03 (Deduction):** Upon payment, the system shall deduct the required Raw Materials from the inventory, not just the finished product count.

#### **3.2 Ordering & Checkout Logic**

* **FR-ORD-01 (Zone Pricing):** Delivery fees are calculated by Zip Code matching against three Zones (Local, Remote, Out-of-Range).
* **FR-ORD-02 (Time Logic):** The Date Picker must disable "Today" if the server time > 11:00 AM (Cutoff Time).
* **FR-ORD-03 (Upsell Module):** Items flagged as `is_addon` (Cards, Candles) shall only appear in the Cart/Checkout modal, never in the main gallery.

#### **3.3 Role-Based Access Control (RBAC)**

The application must render different views based on the logged-in user's role.

* **FR-ROLE-01 (Manager):** Full CRUD access to Inventory, Products, Users, and Financials.
* **FR-ROLE-02 (Florist):** Read-only access to a "To-Make List." This view must display **Ingredients** (Recipe), not just product names.
* **FR-ROLE-03 (Driver):** Read-only access to a "Delivery Manifest." This view must **hide** all financial data (Price, Total) and show only Logistics data (Address, Phone, Gate Code).

---

### **4. Technical Specifications**

#### **4.1 Stack Recommendations**

* **Frontend:** React (Vite) - For fast, responsive mobile views for Drivers.
* **Backend:** Node.js (Express) - Lightweight and fast for the single developer.
* **Database:** PostgreSQL - Required for the relational integrity of the Recipe system.
* **Payments:** Square API.

#### **4.2 Database Schema Overview**

* **`users`**: Stores Role (`enum: customer, manager, florist, driver`).
* **`raw_materials`**: The source of truth for stock (e.g., 'Red Rose', 'qty: 500').
* **`products`**: The catalog items.
* **`product_recipes`**: The junction table linking Products to Raw Materials.
* **`orders`**: Stores delivery status and zone info.

---

### **5. Implementation Roadmap (2-Week Sprint)**

#### **Phase 1: Foundation (Days 1-5)**

* **Day 1:** Setup PostgreSQL & Express Server. Define Database Migrations.
* **Day 2:** Build Auth System (Login + Role Middleware).
* **Day 3-4:** Build Inventory Logic (The "Recipe" calculation engine). **(Most Critical)**
* **Day 5:** Build Manager Dashboard (CRUD for Inventory).

#### **Phase 2: User Experience (Days 6-10)**

* **Day 6-7:** Customer Storefront & Cart (API integration with Inventory Logic).
* **Day 8:** Checkout Flow (Square Payment + Address/Zone Logic).
* **Day 9:** Staff Views (Florist "Recipe View" & Driver "Manifest").
* **Day 10:** Testing & Bug Fixes.

#### **Phase 3: Launch (Days 11-14)**

* **Day 11:** UI Polish & Mobile Responsiveness check.
* **Day 12:** Deployment (Heroku/Vercel/Render).
* **Day 13:** Training Lily on how to input initial stock.
* **Day 14:** Go Live.

---

### **6. Risks & Mitigation**

| Risk | Impact | Mitigation Strategy |
| --- | --- | --- |
| **Scope Creep** | High | Strictly adhere to Zip Code lists for delivery (no Google Maps API for distance). |
| **Data Entry** | Medium | Lily must manually input all recipes. Provide a "Clone Recipe" feature to speed this up. |
| **Complexity** | High | If Recipe logic is too hard, fallback to "Simple Product Counting" (MVP Contingency). |

---
