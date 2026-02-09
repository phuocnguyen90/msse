# User Stories for Lily's Florist Web Application

**Version:** 2.0  
**Date:** February 9, 2026  
**Total Stories:** 22 (categorized by priority and persona)

---

## Priority Legend
- **P0 (Critical)**: Must have for MVP launch - addresses core pain points
- **P1 (High)**: Important for customer experience and operations
- **P2 (Medium)**: Enhances functionality, can be phased
- **P3 (Low)**: Nice-to-have, Phase 2 consideration

---

## Epic 1: Customer Shopping Experience

### **US-01: Browse Product Gallery by Category** [P0]

> **As a** potential customer,  
> **I want** to browse bouquets organized by occasion (Birthday, Sympathy, Wedding) and season (Valentine's, Mother's Day, Spring),  
> **So that** I can quickly find an appropriate arrangement for my specific need without scrolling through unrelated products.

**Acceptance Criteria:**
- Products display with high-quality photos, name, and price
- Filter by multiple categories simultaneously
- "In Season" badge shows on seasonal arrangements
- Mobile-optimized grid layout

**Interview Source:** *"filter products by occasion... and season"*

---

### **US-02: View Seasonal Availability** [P1]

> **As a** customer,  
> **I want** to see which flowers are currently in season and readily available,  
> **So that** I can choose arrangements using fresh, peak-season blooms and feel confident about quality.

**Acceptance Criteria:**
- "Fresh & In Season" badge visible on applicable products
- Optional filter: "Show only seasonal items"
- Homepage banner highlights current seasonal collection

**Interview Source:** *"I love when sites show real-time availability so customers know what's in season"*

---

### **US-03: Select Delivery or Pickup** [P0]

> **As a** customer,  
> **I want** to choose between local delivery or in-store pickup early in my shopping flow,  
> **So that** I know the service is available for my location before I invest time customizing an order.

**Acceptance Criteria:**
- Selection required before adding items to cart
- System validates delivery zip code against service zones
- Clear messaging if address is out of delivery range
- Pickup shows shop address and hours

**Interview Source:** *"Customers should be able to choose delivery or pickup"*

---

### **US-04: Schedule Delivery Date with Cutoff Enforcement** [P0]

> **As a** customer,  
> **I want** to select a specific delivery date and time window,  
> **So that** flowers arrive when the recipient is available, and I have realistic expectations about same-day availability.

**Acceptance Criteria:**
- Calendar picker shows next 7 days
- "Today" option disabled after 1:00 PM
- Time slots: Morning (9-12), Afternoon (12-5), Evening (5-8)
- Clear message: "Same-day orders must be placed before 1:00 PM"

**Interview Source:** *"for same-day delivery I usually cut it off around 1:00 pm... I'd like the website to clearly enforce that cutoff"*

---

### **US-05: See Automatic Delivery Fee by Distance** [P0]

> **As a** customer,  
> **I want** to see my delivery fee calculated automatically when I enter my address,  
> **So that** I know the total cost upfront without having to call the shop or guess.

**Acceptance Criteria:**
- Fee displays immediately after zip code entry
- Different rates for zones (e.g., Downtown: $5, Suburbs: $12)
- Error message for out-of-range addresses: "Sorry, we don't deliver to this area"
- Fee included in order total preview

**Interview Source:** *"I charge different delivery rates based on distance from the shop... having the website handle it automatically would save time"*

---

### **US-06: Add Personalized Card Message** [P0]

> **As a** customer,  
> **I want** to write a custom message that will be included on a card with the flowers,  
> **So that** the recipient knows who sent the gift and feels the personal touch.

**Acceptance Criteria:**
- Text field with 200 character limit and counter
- Supports basic punctuation and line breaks
- Preview shows how card will look
- Field is optional but encouraged with placeholder

**Interview Source:** *"recipient details, address, and a card message"*

---

### **US-07: Add Complementary Items During Checkout** [P1]

> **As a** customer,  
> **I want** to be offered add-ons like candles, chocolates, or greeting cards after selecting my bouquet,  
> **So that** I can easily complete a thoughtful gift package without searching the site separately.

**Acceptance Criteria:**
- Add-ons appear in "Complete Your Gift" section during cart review
- Display thumbnail, name, price
- Quick "Add to Order" button
- Add-ons NOT shown in main product gallery

**Interview Source:** *"Customers should first choose their flowers, then be gently prompted to add items like candles, chocolates, or vases... keeps the bouquets clean and simple"*

---

### **US-08: Guest Checkout or Account Login** [P0]

> **As a** customer,  
> **I want** the option to checkout quickly as a guest or log into my account to save time,  
> **So that** I can complete urgent orders fast but also build a relationship with the shop for future purchases.

**Acceptance Criteria:**
- Prominent "Guest Checkout" and "Login" options before payment
- Guest requires only email and phone
- Registered users see saved addresses and loyalty points
- No forced registration

**Interview Source:** *"checkout as a guest for speed, or log in to save my details"*

---

### **US-09: View Order History and Reorder** [P1]

> **As a** registered customer,  
> **I want** to view my past orders and click "Reorder" to repeat a previous purchase,  
> **So that** I can quickly send flowers to recurring recipients (like my mother every Mother's Day) without searching again.

**Acceptance Criteria:**
- Order history shows date, product thumbnail, recipient name, total
- "Reorder" button pre-fills cart with same items
- Customer updates delivery date/address before completing
- Display order status for recent orders

**Interview Source:** *"quickly send the same arrangement to a recurring recipient... without searching for it again"*

---

### **US-10: Track Order Status in Real-Time** [P1]

> **As a** customer,  
> **I want** to see the current status of my order (Being Prepared, Out for Delivery, Delivered),  
> **So that** I know when to expect delivery and can plan accordingly or alert the recipient.

**Acceptance Criteria:**
- Status displayed in customer account: "Being prepared", "Ready for delivery", "Out for delivery", "Delivered"
- Email notification when status changes to "Delivered"
- Link in confirmation email goes to order tracking page
- Estimated completion time shown

**Interview Source:** *"order tracking are things I really wish I had now"*

---

### **US-11: Earn and Redeem Loyalty Points** [P1]

> **As a** repeat customer,  
> **I want** to see my loyalty points balance and apply points for a discount at checkout,  
> **So that** I feel rewarded for my continued business and have incentive to return to Lily's shop.

**Acceptance Criteria:**
- Earn 1 point per $1 spent (visible on order confirmation)
- Account dashboard shows current points balance
- Checkout shows redemption option: "Use 100 points = $10 off"
- Points deducted only after successful payment

**Interview Source:** *"Regular customers earn points for purchases... I'd love for the website to handle this automatically"*

---

### **US-12: Indicate Flower Substitution Preferences** [P2]

> **As a** customer ordering flowers,  
> **I want** to tell Lily my preferences if certain flowers aren't available (substitute freely vs. contact me first),  
> **So that** my order can be fulfilled smoothly even if my exact choice is out of stock, according to my comfort level.

**Acceptance Criteria:**
- Checkbox options during checkout:
  - "Contact me before substituting"
  - "Substitute with similar colors/style" (default)
  - "Substitute freely—I trust your expertise"
- Preference stored with order and visible to florists

**Interview Source:** *"I'll substitute flowers with something similar and call the customer if it's a big change"*

---

## Epic 2: Custom & Corporate Orders

### **US-13: Submit Custom Event Inquiry** [P2]

> **As a** wedding or corporate event planner,  
> **I want** to submit my event details (date, venue, budget, style preferences, flower types) through a dedicated inquiry form,  
> **So that** Lily can provide an accurate custom quote for large-scale arrangements without playing phone tag or multiple emails.

**Acceptance Criteria:**
- Form fields: Name, email, phone, event type, date, venue, estimated guest count, budget range, style/color preferences, additional notes
- Confirmation email sent to customer and Lily
- Inquiry stored in admin dashboard for Lily to review
- Not integrated with regular checkout (handled manually)

**Interview Source:** *"weddings, events, and repeat customers... a big part of my business"*

---

### **US-14: Read Care Tips and Seasonal Stories** [P3]

> **As a** site visitor interested in flowers,  
> **I want** to read blog posts about flower care tips and seasonal highlights,  
> **So that** I can make my bouquet last longer, learn about Lily's expertise, and feel connected to the shop's story.

**Acceptance Criteria:**
- Blog section with posts tagged by topic (Care Tips, Seasonal, Events)
- Recent posts displayed on homepage or dedicated blog page
- Each post has title, featured image, body content, publish date
- Search or filter by tag

**Interview Source:** *"learn how to make my bouquet last longer and feel connected to the florist's expertise"*

---

## Epic 3: Inventory & Order Management (Lily - Owner)

### **US-15: Define Product Recipes with Stem Counts** [P0]

> **As** Lily (Shop Owner),  
> **I want** to define exactly which flowers (by stem count) and supplies are required for each product,  
> **So that** the system can automatically track what I have available and prevent me from overselling during busy holidays.

**Acceptance Criteria:**
- Product creation interface includes "Recipe Builder"
- Add raw materials: e.g., "12 Red Roses, 5 Ferns, 1 Glass Vase"
- Recipe saved and associated with product
- Recipe viewable by Florist Assistants when preparing orders

**Interview Source:** *"I mostly think in terms of individual stems... For day-to-day work, I mentally translate that into how many arrangements I can realistically make. Right now that translation lives in my head, which is part of the problem"*

---

### **US-16: Automatic Stock Deduction on Sale** [P0]

> **As** Lily (Shop Owner),  
> **I want** the system to automatically deduct flower stems and supplies from inventory when an online order is paid,  
> **So that** I don't accidentally oversell items I don't have in stock, especially during Valentine's Day or Mother's Day rushes.

**Acceptance Criteria:**
- Upon payment confirmation, deduct quantities per product recipe
- Log transaction: order ID, timestamp, materials deducted
- Real-time availability updated across website
- Products automatically marked "Out of Stock" when ingredients insufficient

**Interview Source:** *"I don't accidentally sell items I don't have, preventing shortages during holidays"*

---

### **US-17: Receive Low Stock Alerts** [P0]

> **As** Lily (Shop Owner),  
> **I want** to see visual alerts when any flower or supply falls below a minimum threshold,  
> **So that** I can reorder from suppliers before running out and having to turn down customers.

**Acceptance Criteria:**
- Dashboard shows "Low Stock Alerts" section
- Each alert displays: material name, current count, threshold, deficit
- Sortable by urgency (most critical first)
- Threshold configurable per material (e.g., Red Roses: alert at 20 stems)

**Interview Source:** *"A system that warns me early... would really help"*

---

### **US-18: Manually Adjust Inventory Levels** [P0]

> **As** Lily (Shop Owner),  
> **I want** to manually add or subtract flower stems for restocking, breakage, spoilage, or manual sales,  
> **So that** my inventory stays accurate even when materials don't move through the normal online order flow.

**Acceptance Criteria:**
- Inventory management page lists all materials with current counts
- "Adjust Stock" button opens modal: Add or Subtract quantity, Reason field
- All adjustments logged with timestamp and user
- Adjustment immediately updates availability calculations

**Interview Source:** *"Sometimes I rush an order from my supplier"* + implied need for breakage/spoilage tracking

---

### **US-19: View Centralized Order Dashboard** [P0]

> **As** Lily (Shop Owner),  
> **I want** to view all incoming web orders in a single dashboard with filters by date, status, and delivery time,  
> **So that** I can prioritize which arrangements to prepare first and ensure nothing is missed during holiday rushes.

**Acceptance Criteria:**
- Dashboard shows: Today's orders, Pending production, Revenue summary
- Filterable by: Status (Paid, Preparing, Ready, Delivered), Date range, Delivery method
- Sortable by: Order time, Delivery date, Total amount
- Quick actions: View details, Update status

**Interview Source:** *"view all incoming orders... in a single dashboard... I stop 'juggling' multiple lists and ensure no order is missed during busy rushes"*

---

### **US-20: Send Automatic Order Confirmations** [P0]

> **As** Lily (Shop Owner),  
> **I want** the system to automatically email order confirmations to customers with their order summary and delivery date,  
> **So that** customers feel reassured their order was received and I don't get anxious phone calls asking "Did you get my order?"

**Acceptance Criteria:**
- Email sent immediately after successful payment
- Contains: Order number, itemized products, delivery date/time, recipient details, total, shop contact info
- Branded template with logo
- Link to order tracking (for registered users)

**Interview Source:** *"customers are reassured their order was received, reducing the need for them to call the shop to check"*

---

### **US-21: Create and Manage Promotional Discount Codes** [P1]

> **As** Lily (Shop Owner),  
> **I want** to create discount codes with specific amounts, date ranges, and usage limits (e.g., "MOTHER10" for 10% off, valid May 8-12),  
> **So that** I can run targeted holiday promotions and track which social media campaigns drive the most sales.

**Acceptance Criteria:**
- Code creation form: Code text, Discount type (% or $), Value, Valid dates, Minimum order, Usage limit
- Active codes listed in admin dashboard
- Customers enter code at checkout
- System validates: active dates, usage limit not exceeded, minimum met
- Report shows redemption count per code

**Interview Source:** *"create and manage discount codes (e.g., 'MOTHER10') for holidays... track the effectiveness of my social media promotions"*

---

### **US-22: Update Product Photos and Seasonal Specials** [P1]

> **As** Lily (Shop Owner),  
> **I want** to easily upload new product photos and update the "Seasonal Specials" banner on the homepage,  
> **So that** the website always looks fresh and reflects what's currently available without needing to call a developer.

**Acceptance Criteria:**
- Simple upload interface: drag-and-drop photos
- Add/edit product descriptions and pricing
- Homepage banner editor: upload image, add link, set display dates
- Photo gallery management: upload, reorder, caption, delete
- Changes publish immediately

**Interview Source:** *"the site always looks fresh and reflects what is currently growing/available without needing code changes"*

---

## Epic 4: Florist Assistant Operations

### **US-23: View Production Queue with Recipes** [P0]

> **As a** Florist Assistant,  
> **I want** to see a "To Prepare" queue showing each order's required flowers by stem count (the recipe),  
> **So that** I can gather exactly what I need from the cooler efficiently without guessing quantities or asking Lily.

**Acceptance Criteria:**
- Dashboard filtered to show orders with status: PAID
- Each order displays:
  - Order number and customer name
  - Product name with photo
  - **Recipe breakdown**: "Requires: 12 Red Roses, 5 Ferns, 1 Glass Vase"
  - Card message to include
  - Add-on items (candles, chocolates)
- Button: "Mark as Preparing"
- When complete: "Mark as Ready for Delivery"

**Interview Source:** *"Both assistants should be able to view orders, update statuses"* + *"that translation lives in my head"* (recipe logic)

---

### **US-24: Update Order Status Through Workflow** [P0]

> **As a** Florist Assistant,  
> **I want** to move orders through preparation stages (Preparing → Ready),  
> **So that** everyone on the team knows which orders are complete and ready for pickup or delivery.

**Acceptance Criteria:**
- Visible status buttons based on current state
- Status change requires confirmation click
- Timestamp logged for each transition
- Order automatically moves to appropriate queue (Driver queue when "Ready")

**Interview Source:** *"Both assistants should be able to view orders, update statuses"*

---

### **US-25: Check Current Inventory Levels** [P1]

> **As a** Florist Assistant,  
> **I want** to quickly check how many stems of each flower type are currently in stock,  
> **So that** I can alert Lily if we're running low mid-day and might need an emergency supplier order.

**Acceptance Criteria:**
- Inventory page accessible from assistant dashboard
- List shows: Material name, Current count, Status indicator (OK, Low, Critical)
- Read-only view (cannot adjust counts)
- Mobile-optimized for quick checks from cooler area

**Interview Source:** *"Both assistants should be able to... check inventory levels"*

---

## Epic 5: Delivery Driver Operations

### **US-26: View Daily Delivery Queue** [P1]

> **As a** Delivery Driver,  
> **I want** to see today's deliveries with addresses, recipient names, and special instructions,  
> **So that** I can plan my route efficiently and complete deliveries smoothly without accessing sensitive payment information.

**Acceptance Criteria:**
- Dashboard shows orders: status = READY, delivery_date = TODAY
- Display for each order:
  - Recipient name
  - Delivery address with "Get Directions" link (opens Google Maps)
  - Recipient phone number
  - Special instructions (gate codes, building details)
  - Card message (to verify correct order)
- **Hidden**: Order total, customer email, payment info
- Buttons: "Out for Delivery", "Confirm Delivered"

**Interview Source:** *"one part-time delivery helper"* + implied privacy/security need

---

### **US-27: Confirm Delivery Completion** [P1]

> **As a** Delivery Driver,  
> **I want** to mark an order as "Delivered" with a timestamp,  
> **So that** Lily and the customer know the delivery was completed successfully, and I'm accountable for my route.

**Acceptance Criteria:**
- "Confirm Delivered" button available after marking "Out for Delivery"
- Requires confirmation: "Confirm delivery to [Recipient Name] at [Address]?"
- System logs delivery timestamp
- Automatic email sent to customer: "Your flowers have been delivered!"
- Order removed from driver's active queue

**Interview Source:** Implied from delivery workflow discussion

---

## Priority Summary by Epic

| Epic | P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low) | Total |
|------|---------------|-----------|-------------|----------|-------|
| Customer Shopping | 4 | 5 | 1 | 0 | 10 |
| Custom Orders | 0 | 0 | 1 | 1 | 2 |
| Owner Operations | 6 | 2 | 0 | 0 | 8 |
| Florist Assistant | 2 | 1 | 0 | 0 | 3 |
| Delivery Driver | 0 | 2 | 0 | 0 | 2 |
| **Total** | **12** | **10** | **2** | **1** | **25** |

---

## Traceability to Requirements

Each user story maps to specific requirements in the SRS:

- US-15, US-16, US-17, US-18 → FR-11 through FR-18 (Inventory Management)
- US-04 → FR-23 (Same-day cutoff)
- US-05 → FR-24 (Delivery zone pricing)
- US-07 → FR-18 through FR-20 (Add-on logic)
- US-23, US-24, US-25 → FR-05, FR-56 (Florist Assistant role)
- US-26, US-27 → FR-06, FR-57 (Driver role)
- US-10 → FR-58, FR-59 (Order tracking)
- US-21 → FR-44 through FR-47 (Promotional codes)

---

## MVP Scope Recommendation (Phase 1)

**Include all P0 stories (12 total):**
- Core shopping flow (US-03, US-04, US-05, US-06, US-08)
- Inventory management (US-15, US-16, US-17, US-18)
- Order dashboard (US-19, US-20)
- Florist production (US-23, US-24)

**This addresses Lily's top pain points:**
1. ✅ Inventory overselling prevention
2. ✅ Centralized order management
3. ✅ Automatic order confirmations
4. ✅ Same-day cutoff enforcement
5. ✅ Recipe-based production workflow

---

## Story Sizing Estimates

**Small (1-3 days):** US-06, US-08, US-12, US-20, US-24, US-27  
**Medium (3-5 days):** US-01, US-03, US-04, US-05, US-07, US-09, US-10, US-11, US-14, US-21, US-22, US-25, US-26  
**Large (5-10 days):** US-15, US-16, US-17, US-18, US-19, US-23  
**Extra Large (10+ days, consider splitting):** US-02, US-13

