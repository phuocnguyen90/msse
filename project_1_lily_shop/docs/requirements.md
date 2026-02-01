This **Software Requirements Specification (SRS)** document outlines the functional and non-functional requirements for the **Lily’s Florist Web Application**.

This document is tailored for a **sole developer** working on a **2–3 week timeline**, prioritizing critical business logic (Raw Material Inventory & Role-Based Access) while keeping scope manageable.

---

# Software Requirements Specification (SRS)

**Project:** Lily’s Florist E-Commerce Platform
**Version:** 1.0
**Date:** January 25, 2026

---

## 1. User Authentication & Roles (RBAC)

*The system must handle multiple user types with strict permission boundaries.*

* **FR-01 (Role Definition):** The system shall support four distinct user roles: **Customer, Manager (Lily), Florist, and Driver.** *(Traces to US-15, US-16)*
* **FR-02 (Guest Checkout):** The system shall allow Customers to purchase items without creating an account (Guest Checkout), requiring only email and phone number for contact. *(Traces to US-06)*
* **FR-03 (Customer Account):** The system shall allow Customers to register and log in to view Order History and save delivery addresses. *(Traces to US-08, US-06)*
* **FR-04 (Staff Access):** The system shall restrict access to the Admin Dashboard based on roles:
* *Manager:* Full access (Sales, Inventory, Users).
* *Florist:* "Production View" only.
* *Driver:* "Logistics View" only. *(Traces to US-15)*



## 2. Product Catalog & Upsells

*The system handles the display of finished goods and "add-on" logic.*

* **FR-05 (Categorization):** The system shall allow products to be categorized by 5 predefined Occasions: **Birthday, Romance, Sympathy, Thank you, Just because**, and 4 Seasons: **Spring, Summer, Fall, Winter**. *(Traces to US-02)*
* **FR-06 (Filtering):** The system shall allow Customers to filter products by price range ($0-$100 in $10 increments) and up to 2 categories simultaneously. *(Traces to US-02)*
* **FR-07 (Upsell Visibility):** The system shall hide "Add-on" items (Candles, Greeting Cards, Vases, Teddy Bears) from the main product gallery. These items are flagged with `is_addon=true` and shall never appear in the main gallery. *(Traces to US-15)*
* **FR-08 (Checkout Upsell):** The system shall display "Add-on" items only within the Cart or Checkout flow as suggested additions, showing a maximum of 3 most relevant add-ons per order. *(Traces to US-15)*
* **FR-09 (Dynamic Availability):** The system shall automatically mark a Product as "Out of Stock" if the associated Raw Materials (see FR-13) are insufficient, calculated using: `Min(Raw_Material_Stock / Recipe_Requirement) < 1`. *(Traces to US-15)*

## 3. Inventory Management (Raw Materials)

*The system tracks stems/supplies, not just finished bouquets.*

* **FR-10 (Raw Material Database):** The system shall maintain a database of Raw Materials with support for 100+ unique materials (e.g., "Red Roses", "Ferns", "Vases"), each with current stock counts and unit tracking (stems, bunches, units). *(Traces to US-12)*
* **FR-11 (Recipe Logic):** The system shall allow the Manager to define "Recipes" for Products with up to 10 ingredients per recipe (e.g., "1 Valentine Bouquet = 12 Red Roses + 1 Vase"), using a many-to-many relationship table. *(Traces to US-12)*
* **FR-12 (Stock Deduction):** Upon successful order placement, the system shall automatically deduct the required quantity of Raw Materials from the inventory based on the Product Recipe, with transactional integrity to prevent overselling. *(Traces to US-12, US-15)*
* **FR-13 (Low Stock Alerts):** The system shall display a visual warning in the Manager Dashboard (red/yellow badges) when any Raw Material count falls below 20% of its typical weekly usage level, with automatic email alerts for critical items (<5 remaining). *(Traces to US-12)*
* **FR-14 (Manual Adjustments):** The system shall allow the Manager to manually adjust stock quantities by ±1000 units per transaction, with audit logging of all changes including timestamp, user, and quantity delta. *(Traces to US-12)*

## 4. Ordering & Logistics

*The system handles the complexity of delivery times and zones.*

* **FR-15 (Fulfillment Method):** The system shall require the Customer to select "In-Store Pickup" (free) or "Local Delivery" (additional fee) before proceeding to checkout, with delivery availability validated based on distance from store. *(Traces to US-03)*
* **FR-16 (Delivery Zone Pricing):** The system shall calculate delivery fees based on 3 predefined zones using Zip Code matching:
* Zone A (0-5 miles): Fixed $5.00 rate
* Zone B (6-15 miles): Fixed $15.00 rate
* Zone C (>15 miles): Block order with message "Sorry, we do not deliver to this area." *(Traces to US-03, US-04)*
* **FR-17 (Same-Day Cutoff):** The system shall disable the "Today" option in the delivery date picker if the current server time is past 11:00 AM, and prevent same-day orders placed after cutoff. *(Traces to US-04)*
* **FR-18 (Card Message):** The system shall provide a text field for a custom "Card Message" (max 200 characters) with real-time character counter, supporting UTF-8 characters including emojis. *(Traces to US-05)*

## 5. Payments & Loyalty

*The system handles money and rewards.*

* **FR-19 (Payment Gateway):** The system shall integrate with the **Square API** to process credit card payments securely, supporting card-present and card-not-present transactions with PCI DSS compliance. All payment data must be tokenized; no raw credit card numbers shall be stored. *(Traces to US-07)*
* **FR-20 (Loyalty Points Accrual):** The system shall calculate 1 loyalty point per $1 spent (rounded to nearest dollar) for registered Customers, with points awarded only after successful payment and capped at 1000 points per order. *(Traces to US-07)*
* **FR-21 (Loyalty Redemption):** The system shall allow registered Customers to redeem points at 100 points = $1 discount, with a maximum discount of 50% of order value per transaction. Points shall be deducted immediately upon successful redemption. *(Traces to US-07)*

## 6. Staff Workflows (Admin Views)

*Specific interface requirements for internal operations.*

* **FR-22 (Manager Dashboard):** The system shall provide a dashboard displaying real-time metrics: Today's Sales (at least $0), Low Stock Alerts (highlighted in red), Pending Orders (count), with data refresh every 30 seconds. *(Traces to US-11, US-15)*
* **FR-23 (Florist Production View):** The system shall display a list of "To-Make" orders filtered by status (`PENDING`, `PREPARING`), showing the **Recipe** (ingredients) with quantities rather than just the Product Name, organized by delivery time priority. *(Traces to US-11)*
* **FR-24 (Driver Logistics View):** The system shall display a list of "Ready" orders containing **only** Recipient Name, Address, Phone, and Special Instructions - with all financial data (Price, Total, Payment Method) completely hidden for privacy. *(Traces to US-15)*
* **FR-25 (Status Workflow):** The system shall allow orders to be moved through 5 states: `PENDING` -> `PAID` -> `PREPARING` -> `OUT_FOR_DELIVERY` -> `DELIVERED`, with automatic status transitions and timestamp logging. *(Traces to US-11)*

## 7. Non-Functional Requirements

*Performance and Quality Constraints.*

* **NFR-01 (Responsiveness):** The web application must be fully responsive, supporting breakpoints: mobile (320px-768px), tablet (769px-1024px), desktop (1025px+), with touch-optimized interfaces for Customers and Drivers achieving 100% Lighthouse performance score. *(Traces to US-15, US-11)*
* **NFR-02 (Security):** All payment data must be tokenized via Square API; no credit card numbers shall be stored in the application database. Implement HTTPS, CORS restrictions, and input validation for all user data with OWASP compliance. *(Traces to US-06, US-07)*
* **NFR-03 (Performance):** The "Availability Check" (querying recipes vs. stock) must execute in under 200ms (95th percentile) to prevent lag when adding items to the cart, with lazy loading for product images and CDN integration for static assets. *(Traces to US-15)*
* **NFR-04 (Scalability):** The database schema must support up to 500 concurrent orders during peak holiday load, with connection pooling, read replicas for reporting, and automatic failover for critical services. *(Traces to US-11)*

---

### **Appendix: Requirements Traceability Matrix**

This matrix traces each requirement back to its corresponding user story and ensures complete coverage of business needs.

| Requirement | User Story | Description |
|-------------|------------|-------------|
| **FR-01** | US-15 | Role Definition for authentication |
| **FR-02** | US-06 | Guest Checkout functionality |
| **FR-03** | US-08 | Customer Account registration/history |
| **FR-04** | US-15 | Staff access controls |
| **FR-05** | US-02 | Product categorization by occasion/season |
| **FR-06** | US-02 | Product filtering capabilities |
| **FR-07** | US-15 | Upsell item visibility control |
| **FR-08** | US-15 | Checkout upsell logic |
| **FR-09** | US-15 | Dynamic availability calculation |
| **FR-10** | US-12 | Raw material database structure |
| **FR-11** | US-12 | Recipe definition for products |
| **FR-12** | US-12, US-15 | Stock deduction on order |
| **FR-13** | US-12 | Low stock alert system |
| **FR-14** | US-12 | Manual stock adjustment |
| **FR-15** | US-03 | Fulfillment method selection |
| **FR-16** | US-03, US-04 | Delivery zone pricing |
| **FR-17** | US-04 | Same-day cutoff logic |
| **FR-18** | US-05 | Card personalization |
| **FR-19** | US-07 | Secure payment processing |
| **FR-20** | US-07 | Loyalty points accrual |
| **FR-21** | US-07 | Loyalty points redemption |
| **FR-22** | US-11, US-15 | Manager dashboard metrics |
| **FR-23** | US-11 | Florist production view |
| **FR-24** | US-15 | Driver logistics privacy |
| **FR-25** | US-11 | Order status workflow |
| **NFR-01** | US-15, US-11 | Mobile responsiveness |
| **NFR-02** | US-06, US-07 | Payment security |
| **NFR-03** | US-15 | Performance optimization |
| **NFR-04** | US-11 | Scalability requirements |

---

### **Next Steps for Development**

This document now serves as your "Contract" for the code.

1. **Database Migration:** Create tables based on the Schema provided earlier.
2. **Seed Data:** Populate the DB with 5 test Raw Materials and 3 test Products (Recipes) to test the inventory logic immediately.
3. **Implementation Priority:** Focus on FR-09 (Dynamic Availability) and FR-12 (Stock Deduction) first as they are critical to preventing overselling.

