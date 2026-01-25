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

* **FR-01 (Role Definition):** The system shall support four distinct user roles: **Customer, Manager (Lily), Florist, and Driver.**
* **FR-02 (Guest Checkout):** The system shall allow Customers to purchase items without creating an account (Guest Checkout), requiring only email and phone number for contact.
* **FR-03 (Customer Account):** The system shall allow Customers to register and log in to view Order History and save delivery addresses.
* **FR-04 (Staff Access):** The system shall restrict access to the Admin Dashboard based on roles:
* *Manager:* Full access (Sales, Inventory, Users).
* *Florist:* "Production View" only.
* *Driver:* "Logistics View" only.



## 2. Product Catalog & Upsells

*The system handles the display of finished goods and "add-on" logic.*

* **FR-05 (Categorization):** The system shall allow products to be categorized by Occasion (Birthday, Sympathy) and Season (Spring, Winter).
* **FR-06 (Filtering):** The system shall allow Customers to filter products by price range and category.
* **FR-07 (Upsell Visibility):** The system shall hide "Add-on" items (Candles, Greeting Cards) from the main product gallery.
* **FR-08 (Checkout Upsell):** The system shall display "Add-on" items only within the Cart or Checkout flow as suggested additions.
* **FR-09 (Dynamic Availability):** The system shall automatically mark a Product as "Out of Stock" if the associated Raw Materials (see FR-13) are insufficient.

## 3. Inventory Management (Raw Materials)

*The system tracks stems/supplies, not just finished bouquets.*

* **FR-10 (Raw Material Database):** The system shall maintain a database of Raw Materials (e.g., Red Roses, Ferns, Vases) with current stock counts.
* **FR-11 (Recipe Logic):** The system shall allow the Manager to define "Recipes" for Products (e.g., "1 Valentine Bouquet = 12 Red Roses + 1 Vase").
* **FR-12 (Stock Deduction):** Upon successful order placement, the system shall automatically deduct the required quantity of Raw Materials from the inventory based on the Product Recipe.
* **FR-13 (Low Stock Alerts):** The system shall display a visual warning in the Manager Dashboard when any Raw Material count falls below a defined threshold.
* **FR-14 (Manual Adjustments):** The system shall allow the Manager to manually add stock (restocking) or adjust counts (breakage/spoilage).

## 4. Ordering & Logistics

*The system handles the complexity of delivery times and zones.*

* **FR-15 (Fulfillment Method):** The system shall require the Customer to select "In-Store Pickup" or "Local Delivery" before checkout.
* **FR-16 (Delivery Zone Pricing):** The system shall calculate delivery fees based on the destination Zip Code:
* Zone A (Close): Fixed Low Rate.
* Zone B (Far): Fixed High Rate.
* Zone C: Block order (No delivery available).


* **FR-17 (Same-Day Cutoff):** The system shall disable the "Today" option in the delivery date picker if the current server time is past 11:00 AM.
* **FR-18 (Card Message):** The system shall provide a text field for a custom "Card Message" (max 200 characters) associated with the order.

## 5. Payments & Loyalty

*The system handles money and rewards.*

* **FR-19 (Payment Gateway):** The system shall integrate with the **Square API** to process credit card payments securely.
* **FR-20 (Loyalty Points Accrual):** The system shall calculate 1 point per $1 spent for registered Customers.
* **FR-21 (Loyalty Redemption):** The system shall allow registered Customers to redeem points for a discount during checkout.

## 6. Staff Workflows (Admin Views)

*Specific interface requirements for internal operations.*

* **FR-22 (Manager Dashboard):** The system shall provide a dashboard displaying Total Sales, Low Stock Alerts, and Pending Orders.
* **FR-23 (Florist Production View):** The system shall display a list of "To-Make" orders that shows the **Recipe** (ingredients) rather than just the Product Name.
* **FR-24 (Driver Logistics View):** The system shall display a list of "Ready" orders containing **only** Recipient Name, Address, Phone, and Special Instructions (Sales totals and billing info must be hidden).
* **FR-25 (Status Workflow):** The system shall allow orders to be moved through states: `PENDING` -> `PREPARING` -> `READY` -> `OUT_FOR_DELIVERY` -> `DELIVERED`.

## 7. Non-Functional Requirements

*Performance and Quality Constraints.*

* **NFR-01 (Responsiveness):** The web application must be fully responsive, specifically optimized for Mobile usage for Customers and Drivers.
* **NFR-02 (Security):** All payment data must be tokenized via Square; no credit card numbers shall be stored in the application database.
* **NFR-03 (Performance):** The "Availability Check" (querying recipes vs. stock) must execute in under 200ms to prevent lag when adding items to the cart.
* **NFR-04 (Scalability):** The database schema must support up to 500 concurrent orders (peak holiday load).

---

### **Next Steps for Development**

This document now serves as your "Contract" for the code.

1. **Database Migration:** Create tables based on the Schema provided earlier.
2. **Seed Data:** Populate the DB with 5 test Raw Materials and 3 test Products (Recipes) to test the inventory logic immediately.

