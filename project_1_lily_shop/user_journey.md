This covers the four key personas we identified: **The Customer**, **The Florist** (Staff), **The Driver** (Staff), and **Lily** (Manager).

---

### **1. The Customer Journey (The Shopping Experience)**

*Goal: Order a bouquet for a specific date without hitting "Out of Stock" errors later.*

#### **Stage 1: Discovery & Availability (The "Recipe" Logic)**

1. **User Action:** Customer lands on the homepage and clicks the "Valentine’s Collection" category.
2. **System Action (Backend):**
* Query `Product_Recipes` for all bouquets in this category.
* Check `Raw_Materials` stock levels.
* *Logic:* If "Red Roses" count is low, automatically disable the "Love Bouquet" or mark it as "Sold Out" before the user even clicks it.


3. **User Action:** Customer clicks on the "Spring Sunrise" bouquet.

#### **Stage 2: Configuration (The "Cutoff" Logic)**

4. **User Action:** Customer selects "Delivery" (vs. Pickup).
5. **User Action:** Customer opens the Date Picker.
6. **System Action (Frontend/Backend):**
* *Logic:* Check current server time.
* If Time > 11:00 AM, **disable "Today"** in the calendar.
* User selects tomorrow's date.


7. **User Action:** Customer types a personalized card message: *"Happy Birthday, Mom!"*
8. **User Action:** Clicks "Add to Cart."

#### **Stage 3: The Upsell (The "Add-on" Logic)**

9. **System Action:** A modal or interstitial section appears: *"Complete the gift? Add a Candle or Greeting Card for $5."*
* *Note:* These items were hidden from the main store gallery as requested.


10. **User Action:** Customer adds a "Lavender Candle" and proceeds to Checkout.

#### **Stage 4: Logistics & Payment (The "Zone" Logic)**

11. **User Action:** Customer selects "Guest Checkout" (skips login).
12. **User Action:** Enters Delivery Address.
13. **System Action:**
* *Logic:* Compare Zip Code/Distance against the predefined Zones.
* If Zone A (Local): Add **$5.00** shipping.
* If Zone B (Far): Add **$15.00** shipping.
* If Zone C (Too far): Show error *"Sorry, we do not deliver to this area."*


14. **User Action:** Enters Credit Card details via the Square integration form.
15. **User Action:** Submits Order.

---

### **2. The Florist Journey (Production View)**

*Goal: Know exactly what to build without guessing inventory.*

1. **User Action:** Florist logs in and selects the **"To Make"** dashboard.
2. **System Display:** Shows a filtered list of Orders with status `PAID`.
* *Crucial View:* The Florist sees the **Recipe**, not just the product name.
* *Display:* "Order #101: Spring Sunrise (Needs: 5 Tulips, 3 Ferns, 1 Glass Vase)."


3. **User Action:** Florist assembles the bouquet.
4. **User Action:** Florist clicks **"Mark Ready for Delivery."**
5. **System Action:**
* Updates Order Status to `PREPARING` -> `READY`.
* Moves the order to the **Driver's Queue**.



---

### **3. The Driver Journey (Logistics View)**

*Goal: Deliver efficiently without seeing sensitive sales data.*

1. **User Action:** Driver logs in on mobile.
2. **System Display:** Sees a list of orders with status `READY` and `delivery_date = TODAY`.
* *Security:* Sales totals and customer email are **hidden**. Only Name, Address, Phone, and "Gate Code" are visible.


3. **User Action:** Driver loads the van and clicks **"Start Route."**
* *Optional Integration:* Clicking the address opens Google Maps.


4. **User Action:** Driver drops off flowers.
5. **User Action:** Driver clicks **"Confirm Delivery."**
6. **System Action:**
* Updates Order Status to `DELIVERED`.
* Triggers an automated email to the Customer: *"Your flowers have been delivered!"*



---

### **4. The Manager Journey (Lily's Admin)**

*Goal: Inventory control and overview.*

1. **User Action:** Lily logs in to the **Admin Dashboard**.
2. **System Display:**
* **Alert:** "Low Stock Warning: Red Roses (Only 15 stems left)."


3. **User Action:** Lily receives a fresh shipment from her supplier. She inputs: `+100 Red Roses`.
4. **System Action:**
* Updates `Raw_Materials` table.
* *Effect:* The "Love Bouquet" (which was sold out) automatically becomes purchasable on the website again.


