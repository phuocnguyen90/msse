### **Database Schema Strategy**

#### **1. The "Recipe" Problem (Inventory)**

We cannot just have a `Products` table. We need three tables to handle her request:

* `Products` (The Bouquet she sells)
* `Raw_Materials` (The Roses/Vases she buys)
* `Product_Recipes` ( The bridge: "This Bouquet uses 5 of those Roses")

#### **2. The "Upsell" Problem (Add-ons)**

Since add-ons aren't standalone, we can flag them in the `Products` table as `is_addon = true` so they don't show up in the main gallery, or create a separate table. A flag is faster to build.

#### **3. The "RBAC" Problem (Roles)**

We need a `role` enum in the Users table to filter views for Drivers vs. Florists.

---

### **Proposed Database Tables (SQL Structure)**

#### **A. Users & Authentication**

* **Users**
* `id` (PK)
* `email` (Unique)
* `password_hash`
* `role` (Enum: 'CUSTOMER', 'MANAGER', 'FLORIST', 'DRIVER')
* `loyalty_points` (Integer, default 0)
* `phone_number`



#### **B. Products & Inventory (The Complex Part)**

* **Raw_Materials** (What Lily has in stock)
* `id` (PK)
* `name` (e.g., "Red Rose", "Glass Vase", "Ribbon")
* `stock_quantity` (Integer)
* `unit` (e.g., "stems", "units", "meters")
* `low_stock_threshold` (Integer - triggers warning)


* **Products** (What the Customer buys)
* `id` (PK)
* `name` (e.g., "Valentine's Special")
* `slug` (for URL)
* `price` (Decimal)
* `is_addon` (Boolean - *If true, only show at checkout upsell*)
* `image_url`
* `category` (Enum: 'Birthday', 'Wedding', 'Sympathy')


* **Product_Recipes** (The Link)
* `id` (PK)
* `product_id` (FK -> Products)
* `raw_material_id` (FK -> Raw_Materials)
* `quantity_required` (Integer - e.g., 5)
* *(Logic: When Product is ordered, system queries this table and subtracts `quantity_required` from `Raw_Materials`)*



#### **C. Orders & Delivery**

* **Orders**
* `id` (PK)
* `user_id` (FK -> Users, nullable for Guest)
* `total_price`
* `status` (Enum: 'PENDING', 'PAID', 'PREPARING', 'OUT_FOR_DELIVERY', 'DELIVERED')
* `payment_method` (Enum: 'SQUARE', 'CASH')
* `stripe_payment_intent_id` (or Square ID)
* `delivery_type` (Enum: 'PICKUP', 'DELIVERY')
* `delivery_fee` (Calculated based on distance)
* `delivery_date` (Date)
* `delivery_time_slot` (String - e.g., "Morning")
* `card_message` (Text)


* **Order_Items**
* `id` (PK)
* `order_id` (FK -> Orders)
* `product_id` (FK -> Products)
* `quantity`
* `price_at_purchase` (Snapshotted price)


* **Delivery_Info** (For the Driver View)
* `order_id` (FK -> Orders)
* `recipient_name`
* `recipient_phone`
* `address_line_1`
* `city`
* `distance_km` (Stored from API calculation)
* `delivery_instructions` (e.g., "Gate code 1234")



---

### **New Logic Flows (Code Implications)**

Since you are the sole developer, here is how you should tackle the complex logic:

**1. The "Can I make this?" Check (Inventory Logic)**

* *Before* a user can add "Valentine's Special" to the cart, your backend must:
1. Check `Product_Recipes` for that bouquet.
2. Check `Raw_Materials` to see if you have enough stems.
3. If `Raw_Materials.stock` < `Recipe.required`, mark Product as **Out of Stock**.



**2. The "Cutoff Time" Logic**

* Create a simple utility function:
```javascript
function isSameDayAvailable() {
   const now = new Date();
   const cutoff = new Date();
   cutoff.setHours(11, 0, 0); // 11:00 AM
   return now < cutoff;
}

```


* If `false`, disable today's date in the date picker UI.

**3. Distance Pricing**

* Since she wants dynamic pricing, you will likely need to integrate the **Google Maps Distance Matrix API** (or Mapbox).
* *Simpler Alternative for MVP:* Define 3 sets of Zip Codes/Postcodes in your code.
* Zone A (Close): $5
* Zone B (Medium): $10
* Zone C (Far): $15
* *This saves you from building a real-time GPS distance calculator.*


