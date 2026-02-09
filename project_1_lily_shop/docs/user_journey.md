# User Journey Documentation for Lily's Florist Web Application

**Version:** 2.0  
**Date:** February 9, 2026  
**Personas Covered:** Customer, Florist Assistant, Delivery Driver, Manager (Lily)

---

## Overview

This document maps the complete user journeys for all personas interacting with Lily's Florist web application. Each journey includes:
- **Happy Path**: Ideal flow with no errors
- **Alternative Paths**: Different choices users might make
- **Error Scenarios**: What happens when things go wrong
- **Recovery Flows**: How users get back on track

---

## Journey 1: Customer Shopping & Ordering

### Primary Goal
Order flowers for a specific occasion and delivery date with confidence that items are available and delivery is possible.

### Secondary Goals
- Personalize the gift with card message and add-ons
- Understand total cost including delivery before payment
- Receive confirmation that order was received

---

### Stage 1: Discovery & Browsing

**Entry Point:** Customer lands on homepage from Google search or social media link

#### Happy Path

**Step 1.1:** Customer sees homepage with featured seasonal collection banner  
- **UI Elements:** Hero image, "Valentine's Collection" banner, navigation menu, product categories
- **User Thought:** "I need flowers for Valentine's Day"

**Step 1.2:** Customer clicks "Valentine's Collection" category  
- **System Action:** 
  - Query products tagged with "Valentine's" category
  - For each product, check raw materials inventory against recipe
  - Calculate available quantity per product
  - Display products with availability status
- **User Sees:** Grid of Valentine's bouquets with photos, names, prices, "In Stock" or "Only 3 left" badges

**Step 1.3:** Customer clicks on "Love Bouquet" product  
- **System Action:** Load product detail page
- **User Sees:** 
  - Large product photo gallery (5 images)
  - Product name, description, base price ($45)
  - Availability: "In Stock"
  - Customer reviews (future enhancement)
  - "Select Delivery or Pickup" buttons

#### Alternative Path 1A: Product Out of Stock

**Step 1.3a:** Customer clicks on "Red Romance Bouquet"  
- **System Displays:** "Currently Unavailable - This arrangement requires flowers that are temporarily out of stock"
- **UI Elements:** 
  - "Notify me when available" button (for registered users)
  - "View Similar Arrangements" section below showing 3 alternatives
- **User Action:** Customer clicks "Elegant Roses" from similar arrangements
- **Flow:** Returns to Step 1.3 (product detail page for alternative)

#### Alternative Path 1B: Searching Instead of Browsing

**Step 1.1b:** Customer uses search bar: "birthday flowers mom"  
- **System Action:** Search products by title, description, tags; filter to "Birthday" category
- **User Sees:** Search results page with 8 matching products
- **Flow:** Customer clicks product → proceeds to Step 1.3

#### Error Scenario 1: Website Loading Issues

**Problem:** Product images fail to load due to slow connection  
- **System Behavior:** Show placeholder images with product names and prices still visible
- **User Action:** Can still browse and select products using text information
- **Recovery:** Images lazy-load as connection improves

---

### Stage 2: Service Selection & Configuration

**Entry Requirement:** Customer has selected a product they want to order

#### Happy Path

**Step 2.1:** Customer clicks "Delivery" button on product page  
- **System Action:** Open delivery configuration modal
- **User Sees:** 
  - Zip code entry field
  - "Or choose In-Store Pickup instead" link

**Step 2.2:** Customer enters delivery zip code: "95110"  
- **System Action:** 
  - Validate zip code format
  - Check against delivery zone database
  - Calculate delivery fee based on zone
- **System Response:** "Delivery available to your area for $8.00"
- **User Sees:** 
  - Delivery fee displayed prominently
  - Calendar date picker (labeled "Select Delivery Date")
  - Time slot dropdown (Morning/Afternoon/Evening)

**Step 2.3:** Customer opens date picker  
- **System Action:** 
  - Check current server time: 10:30 AM (before 1 PM cutoff)
  - Generate available dates: Today through 7 days ahead
  - Enable "Today" option since before cutoff
- **User Sees:** Calendar with today highlighted and available

**Step 2.4:** Customer selects "Tomorrow (Feb 10)" and "Morning (9 AM - 12 PM)"  
- **System Stores:** delivery_date = 2026-02-10, time_slot = "Morning"
- **User Sees:** Selected date/time confirmed in summary box

**Step 2.5:** Customer fills in recipient details  
- **Fields:** 
  - Recipient Name: "Sarah Johnson"
  - Delivery Address: "123 Main St, San Jose, CA 95110"
  - Recipient Phone: "(408) 555-1234"
  - Special Instructions: "Leave with doorman if no answer"
  - Card Message: "Happy Birthday, Mom! Love, Alex"
- **System Validation:** All required fields present, phone format valid, address valid

**Step 2.6:** Customer clicks "Add to Cart"  
- **System Action:** 
  - Create cart session
  - Add product with selected configuration
  - Store delivery details
- **User Sees:** Success message: "Added to cart!" with cart icon showing (1) item

#### Alternative Path 2A: In-Store Pickup Instead

**Step 2.1a:** Customer clicks "In-Store Pickup" button  
- **System Action:** Open pickup configuration modal
- **User Sees:** 
  - Shop address: "456 Downtown Ave, San Jose, CA 95113"
  - "Get Directions" link (opens Google Maps)
  - Shop hours: Mon-Sat 9 AM - 6 PM, Sun 10 AM - 4 PM
  - Pickup date/time selector

**Step 2.2a:** Customer selects pickup date and time  
- **Available Slots:** Today (if before 1 PM), Tomorrow, Next 7 days
- **Time Slots:** 10 AM-12 PM, 12 PM-3 PM, 3 PM-6 PM
- **Customer Selects:** Tomorrow, 12 PM - 3 PM
- **System Stores:** fulfillment_type = "pickup", pickup_date = 2026-02-10, pickup_time = "12-3PM"

**Step 2.3a:** Customer enters their contact info for pickup notification  
- **Fields:** Name, Phone, Email (no address needed)
- **Card Message:** Still available (flowers come with card)
- **Flow:** Proceeds to Step 2.6 (Add to Cart)

#### Alternative Path 2B: Same-Day Order After Cutoff

**Step 2.3b:** Customer attempts to order at 2:30 PM  
- **System Action:** Check server time: 2:30 PM (past 1 PM cutoff)
- **Calendar Display:** "Today" option is DISABLED (grayed out)
- **User Sees:** Tooltip on hover: "Same-day orders must be placed before 1:00 PM. Please select tomorrow or later."
- **Available Dates:** Starting from tomorrow (Feb 10)
- **User Action:** Customer selects tomorrow instead
- **Flow:** Continues normally from Step 2.4

#### Error Scenario 2A: Invalid Zip Code

**Step 2.2 Error:** Customer enters "00000"  
- **System Response:** "Please enter a valid zip code"
- **UI:** Red border on input field, error message below field
- **User Action:** Customer corrects to valid zip code
- **Recovery:** Proceeds to Step 2.2 normally

#### Error Scenario 2B: Out of Delivery Range

**Step 2.2 Error:** Customer enters zip code "94000" (outside delivery zone)  
- **System Action:** Check zone database - no matching zone found
- **System Response:** 
  - Modal shows: "Sorry, we don't deliver to this area yet"
  - Offer alternatives:
    - "Try In-Store Pickup instead" button
    - "Notify me when delivery expands to my area" (email capture)
- **User Action Option 1:** Switch to pickup → proceeds to Alternative Path 2A
- **User Action Option 2:** Leave site (lost conversion)

#### Error Scenario 2C: Card Message Too Long

**Step 2.5 Error:** Customer types 250-character message (limit is 200)  
- **System Behavior:** 
  - Character counter turns red at 200
  - Input stops accepting text at 200 characters
  - Message below field: "Card message limited to 200 characters"
- **User Action:** Customer edits message to fit within limit
- **Recovery:** Proceeds to Step 2.6

---

### Stage 3: Cart Review & Upsells

**Entry Requirement:** Customer has added at least one product to cart

#### Happy Path

**Step 3.1:** Customer clicks cart icon or "View Cart" button  
- **System Action:** Load cart page
- **User Sees:** 
  - Cart summary:
    - "Love Bouquet" - $45.00
    - Delivery to 95110 - $8.00
    - Subtotal - $53.00 (before tax)
  - Delivery details summary
  - Card message preview

**Step 3.2:** System displays "Complete Your Gift" section  
- **UI:** Below cart items, prominent section with headline "Complete Your Gift"
- **Add-on Items Shown:**
  - Lavender Candle ($12) with thumbnail
  - Premium Chocolates ($18) with thumbnail  
  - Deluxe Vase Upgrade ($25) with thumbnail
  - Greeting Card ($5) with thumbnail
- **Each Item:** "Add to Order" button, brief description
- **Note:** These add-ons were NOT visible in main product gallery (per requirement)

**Step 3.3:** Customer clicks "Add to Order" on Lavender Candle  
- **System Action:** 
  - Add candle to cart
  - Check candle inventory (unit count, not stem-based)
  - Update cart total
- **User Sees:** 
  - Candle appears in cart items list
  - Subtotal updates: $65.00
  - Success indicator (green checkmark) on add-on item

**Step 3.4:** Customer reviews final cart and clicks "Proceed to Checkout"  
- **Cart Contents:**
  - Love Bouquet - $45.00
  - Lavender Candle - $12.00
  - Delivery Fee - $8.00
  - **Subtotal: $65.00**
- **System Action:** Route to checkout page

#### Alternative Path 3A: Promo Code Application

**Step 3.2a:** Customer notices "Have a promo code?" link and clicks it  
- **UI:** Expands to show promo code input field
- **Customer Enters:** "LOVE15"
- **Customer Clicks:** "Apply" button

**Step 3.3a:** System validates promo code  
- **System Checks:**
  - Code exists in database ✓
  - Code is active (current date within valid range) ✓
  - Discount type: 15% off
  - Minimum order: $40 ✓
  - Usage limit: Customer hasn't used it yet ✓
- **System Response:** Success! "LOVE15 applied - 15% off"
- **Cart Updates:**
  - Subtotal: $65.00
  - Promo Discount (LOVE15): -$9.75
  - **New Subtotal: $55.25**
- **Flow:** Proceeds to Step 3.4

#### Alternative Path 3B: Registered User Applies Loyalty Points

**Step 3.2b:** Customer (logged in, registered user) sees loyalty points balance  
- **UI Display:** "You have 250 loyalty points ($25.00 credit)"
- **Checkbox:** "Use 100 points for $10 off this order"
- **Customer Action:** Checks box

**Step 3.3b:** System applies points discount  
- **Cart Updates:**
  - Subtotal: $65.00
  - Loyalty Discount: -$10.00
  - **New Subtotal: $55.00**
- **Points Remaining:** 150 (deduction happens after payment)
- **Flow:** Proceeds to Step 3.4

#### Alternative Path 3C: Customer Edits Cart

**Step 3.1c:** Customer realizes they want different time slot  
- **UI:** "Edit delivery details" link under delivery summary
- **System Action:** Opens modal with date/time/address fields pre-filled
- **Customer Changes:** Time slot from "Morning" to "Afternoon"
- **System Saves:** Updated configuration
- **User Sees:** Updated delivery summary
- **Flow:** Can proceed to Step 3.4 or continue shopping

**Step 3.1d:** Customer wants to remove add-on  
- **UI:** Small "X" or "Remove" link next to each cart item
- **Customer Clicks:** Remove Lavender Candle
- **System Action:** Remove from cart, update total
- **Cart Updates:** Subtotal back to $53.00
- **Flow:** Customer can add different add-ons or proceed to checkout

#### Error Scenario 3A: Invalid Promo Code

**Step 3.3a Error:** Customer enters "EXPIRED20"  
- **System Checks:** Code valid_until date = 2026-02-01 (expired)
- **System Response:** Error message (red): "This promo code has expired"
- **User Action:** Customer can try different code or proceed without discount
- **Recovery:** Cart total remains unchanged

#### Error Scenario 3B: Item Goes Out of Stock While in Cart

**Problem:** Another customer bought the last "Love Bouquet" while this customer was browsing add-ons  
- **System Detection:** When customer clicks "Proceed to Checkout", system re-validates inventory
- **System Action:** 
  - Check product recipe against current raw materials
  - Find insufficient "Red Roses" (oversold by concurrent purchase)
- **System Response:** 
  - Display modal: "Sorry, 'Love Bouquet' is no longer available. Stock levels changed while you were shopping."
  - Offer alternatives:
    - "View Similar Arrangements"
    - "Remove from cart and continue with add-ons only" (if add-ons present)
- **User Action:** Customer selects alternative bouquet
- **Recovery:** Returns to product selection (Stage 1) with cart preserved (delivery details, add-ons saved)

---

### Stage 4: Checkout & Payment

**Entry Requirement:** Customer has valid cart and clicked "Proceed to Checkout"

#### Happy Path

**Step 4.1:** Customer lands on checkout page  
- **System Action:** Display secure checkout form
- **User Sees:**
  - Order summary sidebar (items, delivery, total)
  - Guest Checkout or Login options
  - Payment form (Square integration iframe)

**Step 4.2:** Customer selects "Guest Checkout"  
- **Required Fields:**
  - Email: "alex.smith@email.com"
  - Phone: "(408) 555-9876"
  - Confirm delivery address (pre-filled from Stage 2)
- **Note:** No password or account creation required

**Step 4.3:** Customer enters payment details in Square form  
- **Square Iframe Displays:**
  - Card number field
  - Expiration date
  - CVV
  - Zip code (billing)
- **Security Note:** Credit card data never touches Lily's server, handled entirely by Square
- **Customer Enters:** Valid credit card information

**Step 4.4:** Customer reviews final order summary  
- **Display:**
  - Love Bouquet - $45.00
  - Lavender Candle - $12.00
  - Delivery Fee (Zone 2) - $8.00
  - Tax (9.25%) - $6.01
  - **Total: $71.01**
  - Delivery Date: Feb 10, Morning (9 AM - 12 PM)
  - Recipient: Sarah Johnson, 123 Main St
  - Card Message: "Happy Birthday, Mom! Love, Alex"

**Step 4.5:** Customer clicks "Place Order" button  
- **System Action:**
  - Disable button, show loading spinner
  - Send payment request to Square API
  - Square processes payment
  - Square returns success token

**Step 4.6:** Payment successful - System processes order  
- **System Actions (in sequence):**
  1. Create order record with status = `PAID`
  2. Generate unique order number: #2026-0209-0047
  3. **Deduct raw materials from inventory:**
     - Love Bouquet recipe: -12 Red Roses, -5 Ferns, -1 Glass Vase
     - Lavender Candle: -1 unit from add-on inventory
  4. Log inventory transactions with order reference
  5. Update product availability calculations site-wide
  6. Send confirmation email to customer (alex.smith@email.com)
  7. Add order to Florist Assistant "To Prepare" queue
  8. If registered user: Award loyalty points (71 points for $71 spent)

**Step 4.7:** Customer sees order confirmation page  
- **Display:**
  - Success banner: "Order Confirmed!"
  - Order number: #2026-0209-0047
  - Confirmation message: "Check your email for order details"
  - Summary of order
  - Estimated preparation time: "Your order will be ready by 8:00 AM on Feb 10"
  - **For registered users:** "Track your order" link
  - **For guest users:** "Create an account to track this order" button

#### Alternative Path 4A: Registered User Login

**Step 4.2a:** Customer clicks "Login" instead of Guest Checkout  
- **System Action:** Show login form (email + password)
- **Customer Logs In:** Email: "returning@customer.com", Password: ****
- **System Loads:**
  - Saved delivery addresses (dropdown)
  - Current loyalty points balance: 250 points
  - Order history link
- **Customer Selects:** Saved address "Mom's House" (auto-fills recipient details)
- **Benefit:** Faster checkout, loyalty points visible
- **Flow:** Proceeds to Step 4.3 (payment)

#### Alternative Path 4B: Create Account During Checkout

**Step 4.2b:** Guest checkout form includes checkbox: "Create an account to save this order and track future orders"  
- **Customer Checks:** Checkbox
- **Additional Fields Appear:** Password, Confirm Password
- **Customer Completes:** Sets password
- **System Action (after payment):** 
  - Create user account with provided email/password
  - Associate this order with new account
  - Send welcome email with account details
- **Benefit:** Customer can track order and has account for future orders

#### Alternative Path 4C: Apply Substitution Preference

**Step 4.4c:** Checkout form includes flower substitution options  
- **UI Display:** "If certain flowers aren't available:"
- **Radio Options:**
  - ○ Contact me before substituting
  - ● Substitute with similar colors/style (selected by default)
  - ○ Substitute freely—I trust your expertise
- **Customer Selection:** Keeps default (similar colors/style)
- **System Stores:** substitution_preference with order
- **Use:** Florist Assistant will see this preference when preparing order

#### Error Scenario 4A: Payment Declined

**Step 4.5 Error:** Square returns payment declined error  
- **System Action:** 
  - Do NOT create order
  - Do NOT deduct inventory
  - Log failed payment attempt (fraud detection)
- **User Sees:**
  - Error message (red box): "Payment could not be processed. Please check your card details or try a different payment method."
  - Specific reason if provided: "Insufficient funds" or "Card expired"
  - "Try Again" button
- **Cart Preserved:** All items and details remain in cart
- **User Action:** Customer updates payment info or tries different card
- **Recovery:** Returns to Step 4.3 (payment entry)

#### Error Scenario 4B: Session Timeout During Checkout

**Problem:** Customer left checkout page open for 25 minutes while distracted  
- **System Behavior:** Session expires after 20 minutes of inactivity
- **User Action:** Customer clicks "Place Order"
- **System Response:**
  - Display modal: "Your session has expired for security"
  - "Your cart has been saved. Please refresh to continue."
  - Auto-refresh button
- **After Refresh:**
  - Cart contents preserved
  - Delivery details preserved (in session storage)
  - Must re-enter payment details (security requirement)
- **Recovery:** Customer re-enters payment info, proceeds from Step 4.3

#### Error Scenario 4C: Inventory Changed During Checkout

**Problem:** While customer is on checkout page, Florist Assistant manually adjusted Red Rose count (spoilage), making Love Bouquet unavailable  
- **System Detection:** Inventory validation runs when "Place Order" clicked
- **System Action:**
  - Check product recipe against current raw materials
  - Find insufficient inventory
  - **BEFORE** processing payment
- **System Response:**
  - Block payment submission
  - Display error: "We're sorry—'Love Bouquet' is no longer available due to a last-minute stock update."
  - Offer options:
    - "View Similar Bouquets"
    - "Contact us" (phone number shown)
- **User Action:** Customer selects alternative or abandons order
- **Recovery:** Returns to product selection (Stage 1) with preserved cart metadata

---

### Stage 5: Post-Purchase Experience

**Entry Requirement:** Order successfully placed and confirmed

#### Happy Path (Guest User)

**Step 5.1:** Customer receives confirmation email within 1 minute  
- **Email Contents:**
  - Subject: "Order Confirmation #2026-0209-0047 - Lily's Florist"
  - Order summary with itemized list
  - Delivery details (recipient, address, date/time)
  - Card message preview
  - Total charged
  - Shop contact info: phone, email, address
  - "Questions?" section with FAQ link
- **Customer Action:** Reviews email, feels assured order was received

**Step 5.2:** Customer saves email for reference  
- **Customer Thought:** "I'll forward this to my brother so he knows I sent flowers to Mom"
- **No further action needed from customer until delivery**

#### Happy Path (Registered User)

**Step 5.1:** Same confirmation email as guest user

**Step 5.2:** Customer logs into account to track order  
- **System Action:** Display account dashboard
- **User Sees:**
  - Order #2026-0209-0047 listed in "Active Orders"
  - Status: "Being Prepared"
  - Estimated ready time: Feb 10, 8:00 AM
  - Progress bar or timeline showing:
    - ✓ Order Received (Feb 9, 10:45 AM)
    - ● Being Prepared (current)
    - ○ Ready for Delivery
    - ○ Out for Delivery
    - ○ Delivered

**Step 5.3:** System updates status as order progresses (automated)  
- **10:30 AM Feb 10:** Florist marks order "Ready" → Status updates to "Ready for Delivery"
- **11:15 AM Feb 10:** Driver marks "Out for Delivery" → Status updates
- **11:45 AM Feb 10:** Driver confirms "Delivered" → Status updates

**Step 5.4:** Customer receives delivery confirmation email  
- **Trigger:** When driver clicks "Confirm Delivered"
- **Email Contents:**
  - Subject: "Your flowers have been delivered!"
  - Order number
  - Delivery timestamp: Feb 10, 11:45 AM
  - "Thank you for choosing Lily's Florist"
  - "Order again" button (links to website)
  - Future enhancement: "Rate your experience" button
- **Customer Satisfaction:** Knows exactly when flowers were delivered

#### Alternative Path 5A: Customer Wants to Modify Order

**Scenario:** Customer realizes wrong delivery date, calls shop  
- **Customer Action:** Calls Lily's shop (number from confirmation email)
- **Lily/Staff Action:** Looks up order #2026-0209-0047 in dashboard
- **System Capability:** 
  - If status = PAID (not yet PREPARING): Can modify details
  - If status = PREPARING or later: Too late, order in production
- **Resolution:**
  - If modifiable: Lily updates delivery date manually in system
  - If too late: Lily explains, offers to create new order for different date
- **Note:** This is manual staff intervention, not self-service (future enhancement)

#### Alternative Path 5B: Customer Wants Receipt for Reimbursement

**Step 5.2b:** Registered customer clicks "Download Receipt" in account dashboard  
- **System Action:** Generate PDF receipt
- **PDF Contents:**
  - Lily's Florist business information
  - Order number and date
  - Itemized list with prices
  - Tax breakdown
  - Total
  - Payment method (last 4 digits of card)
- **Use Case:** Customer submits for corporate expense reimbursement

---

## Journey 2: Florist Assistant Production Workflow

### Primary Goal
Efficiently prepare flower arrangements with correct quantities of materials, updating order status to keep team coordinated.

### Secondary Goals
- Avoid guessing how many stems to pull from cooler
- Identify when materials are running low
- Ensure card message is included correctly

---

### Stage 1: Viewing Production Queue

**Entry Point:** Florist Assistant (Maria) arrives at shop and logs into system on tablet

#### Happy Path

**Step 1.1:** Maria opens web browser and navigates to lilys-florist.com/admin  
- **System Action:** Detect user not authenticated, redirect to login
- **Login Form:** Email and password fields
- **Maria Enters:** maria@lilysflorist.com, password

**Step 1.2:** System authenticates Maria as Florist Assistant role  
- **System Action:** 
  - Check credentials against user database
  - Load role permissions (can view/update orders, view inventory; cannot change pricing)
  - Set session cookie
  - Redirect to Florist Assistant dashboard

**Step 1.3:** Maria sees her dashboard  
- **UI Layout:**
  - Top banner: "Welcome, Maria" + current time: 9:15 AM
  - Main section: "Orders to Prepare" (default view)
  - Sidebar: "Today's Deliveries" count, "Pickup Orders" count, "Low Stock Alerts" badge
  - Button: "Check Inventory Levels"
- **Orders to Prepare Section:**
  - Filtered automatically to show orders with status = PAID
  - Sorted by delivery_date/pickup_date (soonest first)
  - List displays:
    - Order #2026-0209-0047
    - Customer: Alex Smith
    - Delivery Date: Feb 10, Morning
    - Product: Love Bouquet
    - Add-ons: Lavender Candle
    - Status badge: PAID (blue)
    - "View Details" button

**Step 1.4:** Maria clicks "View Details" on order #2026-0209-0047  
- **System Action:** Load full order detail modal

---

### Stage 2: Reviewing Order Details & Recipe

**Entry Requirement:** Maria has opened specific order details

#### Happy Path

**Step 2.1:** Maria sees complete order information  
- **Order Detail Modal Display:**
  - **Header:** Order #2026-0209-0047, Status: PAID
  - **Product Section:**
    - Product name: "Love Bouquet"
    - Product photo
    - **RECIPE (Critical for Maria):**
      - 12 Red Roses (Long Stem)
      - 5 Ferns (Leather Leaf)
      - 1 Glass Vase (Medium Cylinder)
    - Quantity ordered: 1
  - **Add-ons Section:**
    - Lavender Candle (1x) - already packaged, just needs to be included
  - **Card Message Section:**
    - Display in box: "Happy Birthday, Mom! Love, Alex"
    - Instruction: "Include this message on gift card"
  - **Delivery Details:**
    - Recipient: Sarah Johnson
    - Address: 123 Main St, San Jose, CA 95110
    - Phone: (408) 555-1234
    - Date: Feb 10, Time: Morning (9 AM - 12 PM)
    - Special Instructions: "Leave with doorman if no answer"
  - **Substitution Preference:**
    - Customer selected: "Substitute with similar colors/style"
  - **Action Buttons:**
    - "Mark as Preparing" (green button)
    - "Print Work Order" (prints recipe + details)
    - "Back to Queue"

**Step 2.2:** Maria reviews recipe and checks mental inventory  
- **Maria's Thought:** "I need 12 red roses, 5 ferns, 1 medium vase. Let me check if we have enough in stock."
- **Maria Clicks:** "Check Inventory Levels" (sidebar link)

---

### Stage 3: Checking Inventory

**Entry Requirement:** Maria wants to verify materials available before starting

#### Happy Path

**Step 3.1:** Inventory page loads  
- **UI Display:**
  - Search bar: "Find material..."
  - Material list (scrollable):
    - Red Roses (Long Stem) - **78 stems** - Status: OK (green)
    - Ferns (Leather Leaf) - **45 stems** - Status: OK (green)
    - Glass Vase (Medium Cylinder) - **12 units** - Status: OK (green)
    - Yellow Tulips - **8 stems** - Status: LOW (orange, threshold: 15)
    - Purple Iris - **3 stems** - Status: CRITICAL (red, threshold: 10)
- **Maria Sees:** All materials needed for Love Bouquet are in good supply
- **Maria's Action:** Returns to order detail (browser back button or navigation)

#### Alternative Path 3A: Low Stock Alert Visible

**Step 3.1a:** Maria notices "Yellow Tulips - LOW" alert  
- **Maria's Thought:** "I should mention this to Lily when she comes in"
- **Maria Clicks:** Yellow Tulips row to see details
- **System Shows:**
  - Current count: 8 stems
  - Threshold: 15 stems
  - Used in products: "Sunshine Bouquet", "Spring Mix"
  - Deficit: 7 stems below threshold
- **Maria's Action:** Makes mental note or sends quick text to Lily
- **Flow:** Returns to order preparation

#### Error Scenario 3A: Inventory Critically Low for Current Order

**Problem:** Maria checks inventory and sees Red Roses at 10 stems (needs 12)  
- **System Should Have Prevented:** This order shouldn't have been accepted if recipe checking worked correctly
- **Maria's Action:**
  - Cannot complete order with available materials
  - Clicks "Report Issue" button in order detail
  - Modal opens: "What's the problem?"
  - Maria selects: "Insufficient materials"
  - Adds note: "Only 10 red roses available, need 12"
  - System changes order status to: BLOCKED
  - System emails Lily: "Order #2026-0209-0047 blocked - insufficient inventory"
- **Lily's Response:** 
  - Option 1: Emergency supplier order
  - Option 2: Contact customer for substitution approval
  - Option 3: Refund order

---

### Stage 4: Preparing the Arrangement

**Entry Requirement:** Maria confirmed materials available and ready to start assembly

#### Happy Path

**Step 4.1:** Maria clicks "Mark as Preparing" button  
- **System Action:**
  - Update order status: PAID → PREPARING
  - Timestamp logged: 9:25 AM
  - Order disappears from "To Prepare" queue
  - Order appears in "In Progress" section
- **UI Feedback:** Success toast message: "Order #2026-0209-0047 marked as Preparing"

**Step 4.2:** Maria physically gathers materials  
- **Maria's Actions (outside system):**
  - Goes to cooler
  - Pulls 12 red roses, inspects quality
  - Pulls 5 leather leaf ferns
  - Gets medium cylinder vase from supply shelf
  - Returns to workstation
  - **Note:** Maria doesn't need to count stems mentally or guess—recipe was explicit

**Step 4.3:** Maria assembles the Love Bouquet  
- **Physical work:** Trimming stems, arranging flowers, securing arrangement
- **Duration:** Approximately 15-20 minutes
- **System:** Order remains in PREPARING status
- **Optional:** Maria can reference order details on tablet if she forgets card message

**Step 4.4:** Maria writes card message  
- **Maria Writes:** "Happy Birthday, Mom! Love, Alex" on small card
- **Maria Attaches:** Card to vase with flower pick

**Step 4.5:** Maria packages add-on item  
- **Maria Gets:** Lavender Candle from add-ons shelf
- **Maria Packages:** Bouquet + candle in gift bag with tissue paper
- **Quality Check:** Verifies arrangement matches product photo aesthetically

**Step 4.6:** Maria marks order as ready  
- **Maria Returns to:** Tablet, opens order #2026-0209-0047
- **Maria Clicks:** "Mark as Ready for Delivery" button
- **System Actions:**
  - Update order status: PREPARING → READY
  - Timestamp logged: 9:50 AM
  - Order moves to "Ready for Pickup/Delivery" queue
  - **IF delivery:** Order appears in Driver dashboard (for deliveries on Feb 10)
  - **IF pickup:** Order appears in "Ready for Pickup" list visible at front desk
- **UI Feedback:** Success message: "Order ready! Moved to delivery queue."

#### Alternative Path 4A: Multiple Orders in Parallel

**Scenario:** Maria has 3 orders to prepare before lunch  

**Step 4.1a:** Maria reviews all 3 orders, notes recipes:
- Order A: Love Bouquet (12 roses, 5 ferns, 1 vase)
- Order B: Spring Sunrise (5 tulips, 3 daisies, 1 vase)
- Order C: Sympathy Arrangement (10 white lilies, 7 eucalyptus, 1 basket)

**Step 4.2a:** Maria batches material gathering  
- **Efficiency Strategy:** Pull all stems needed at once from cooler
- **Maria Gets:** 12 roses + 5 tulips + 10 lilies + ferns + daisies + eucalyptus
- **System:** All 3 orders marked PREPARING simultaneously

**Step 4.3a:** Maria assembles sequentially  
- Completes Order A → marks READY
- Completes Order B → marks READY
- Completes Order C → marks READY
- **Benefit of System:** Each order tracked independently, nothing gets lost

#### Alternative Path 4B: Need to Pause Mid-Order

**Step 4.2b:** Maria is gathering materials when Lily asks her to help with walk-in customer  
- **Maria's Action:** Leaves order in PREPARING status
- **System:** Order remains visible in "In Progress" section
- **After helping customer:** Maria returns, finds order in dashboard, continues work
- **Benefit:** Status tracking prevents forgetting which orders are started vs. not started

---

### Stage 5: Handling Edge Cases During Production

#### Error Scenario 5A: Material Quality Issue

**Step 4.2 Error:** Maria pulls 12 red roses but finds 3 have brown edges (unusable)  
- **Maria's Thought:** "I only have 9 good roses, but need 12"
- **Maria Checks:** Inventory count—system shows 78 stems (includes the bad ones)
- **Maria's Action:**
  - Clicks "Report Issue" on order detail
  - Selects issue type: "Material quality problem"
  - Note: "3 red roses have brown edges, can't use. Only 9 good stems available, need 12."
  - System sends alert to Lily
- **Maria's Options:**
  1. Wait for Lily's guidance
  2. If substitution preference allows: Use similar flowers (pink roses)
  3. If urgent: Call Lily directly
- **Lily's Response (via system):**
  - Logs into admin, sees Maria's alert
  - Checks substitution preference: "Substitute with similar colors/style" ✓
  - Replies via system: "Use pink roses instead, same count"
  - Updates order note: "Substituted pink roses for red due to quality issue"
- **Maria Continues:** Uses 12 pink roses instead, completes order

#### Error Scenario 5B: Forgot Card Message

**Step 4.6 Error:** Maria marks order READY but realizes she forgot to write the card  
- **Problem:** Order already in READY status, moved to driver queue
- **Maria's Action:**
  - Clicks order #2026-0209-0047 in READY queue
  - Clicks "Move Back to Preparing" button (status reversal)
  - System updates: READY → PREPARING
  - Order temporarily removed from driver queue
- **Maria Writes:** Card message
- **Maria Re-marks:** READY when complete
- **Recovery:** Simple status reversal capability prevents mistakes from shipping

---

## Journey 3: Delivery Driver Route Execution

### Primary Goal
Deliver all ready orders efficiently and on time while maintaining customer privacy and security.

### Secondary Goals
- Access delivery addresses and contact info without seeing payment details
- Navigate to addresses efficiently
- Confirm delivery completion for tracking

---

### Stage 1: Starting the Delivery Shift

**Entry Point:** Driver (Carlos) arrives at shop at 10:00 AM to pick up deliveries

#### Happy Path

**Step 1.1:** Carlos opens lilys-florist.com/admin on his phone  
- **Device:** Carlos uses personal smartphone (site is mobile-optimized)
- **System Action:** Redirect to login if not authenticated
- **Carlos Logs In:** carlos@lilysflorist.com, password

**Step 1.2:** System authenticates Carlos as Driver role  
- **System Action:**
  - Load driver permissions (view delivery orders only, no financial data access)
  - Redirect to Driver Dashboard (mobile view)

**Step 1.3:** Carlos sees his delivery queue  
- **Mobile UI Display:**
  - Header: "Today's Deliveries - Feb 10"
  - Count: "3 orders ready"
  - Filter tabs: "All" | "Morning" | "Afternoon" | "Evening"
  - Default filter: Shows all orders for today with status = READY or OUT_FOR_DELIVERY
  - **Order List Preview:**
    - Order #2026-0209-0047 - Sarah Johnson - 123 Main St - Morning
    - Order #2026-0209-0051 - Mike Chen - 789 Oak Ave - Morning  
    - Order #2026-0209-0055 - Lisa Park - 456 Elm St - Afternoon

**Step 1.4:** Carlos clicks on first order to see details  
- **System Action:** Open order detail view

---

### Stage 2: Reviewing Delivery Details

**Entry Requirement:** Carlos has selected a specific order to review

#### Happy Path

**Step 2.1:** Carlos sees delivery information (privacy-filtered)  
- **Mobile Order Detail Display:**
  - **Order Number:** #2026-0209-0047
  - **Status:** READY
  - **Recipient Information:**
    - Name: Sarah Johnson
    - Address: 123 Main St, San Jose, CA 95110
    - Phone: (408) 555-1234
    - **"Call" button** (initiates phone call)
  - **Delivery Time:** Morning (9 AM - 12 PM)
  - **Special Instructions:** "Leave with doorman if no answer"
  - **Card Message Preview:** "Happy Birthday, Mom! Love, Alex"
    - Purpose: Verify this is correct order when delivering
  - **Product (for reference):** Love Bouquet + Lavender Candle
    - Purpose: Know what to carry out, double-check completeness
  - **HIDDEN FIELDS (not visible to Carlos):**
    - ❌ Order total
    - ❌ Customer email (only recipient name shown)
    - ❌ Payment method
    - ❌ Customer (purchaser) phone number (only recipient phone shown)
  - **Action Buttons:**
    - "Get Directions" (large, green)
    - "Out for Delivery" (secondary button)
    - "Back to List"

**Step 2.2:** Carlos reviews all 3 morning deliveries  
- **Carlos's Mental Planning:** Determines efficient route order
- **Carlos Decides:** 
  1. 123 Main St (closest)
  2. 789 Oak Ave (north side)
  3. Come back for afternoon delivery later

---

### Stage 3: Loading Van and Starting Route

**Entry Requirement:** Carlos has reviewed orders and planned route

#### Happy Path

**Step 3.1:** Carlos physically collects orders from prep area  
- **Carlos Verifies:** 
  - Each arrangement matches product description
  - Card is attached
  - Add-ons are packaged together
- **Carlos Loads:** Arranges in van carefully to prevent tipping

**Step 3.2:** Carlos clicks "Out for Delivery" on first order  
- **UI:** Carlos opens order #2026-0209-0047 on his phone
- **Carlos Clicks:** "Out for Delivery" button
- **System Actions:**
  - Update status: READY → OUT_FOR_DELIVERY
  - Timestamp logged: 10:15 AM
  - Order marked as "in transit" in Lily's admin dashboard
  - **Optional (future):** Customer receives notification email "Your order is out for delivery"
- **UI Feedback:** Button changes to "Confirm Delivered" (grayed out until Carlos completes delivery)

**Step 3.3:** Carlos clicks "Get Directions"  
- **System Action:** 
  - Extract address: 123 Main St, San Jose, CA 95110
  - Generate navigation URL for Google Maps
  - Open Google Maps app (if installed) or Google Maps website
- **Google Maps:** Loads with destination set, shows route from current location (shop)
- **Carlos Drives:** Follows GPS to 123 Main St

#### Alternative Path 3A: Multiple Orders to Same Area

**Step 3.2a:** Carlos marks multiple orders OUT_FOR_DELIVERY at once  
- **UI Enhancement:** Checkbox next to each order in list
- **Carlos Selects:** Orders #0047 and #0051 (both morning, same neighborhood)
- **Carlos Clicks:** "Mark Selected as Out for Delivery" (bulk action)
- **System Updates:** Both orders → OUT_FOR_DELIVERY with same timestamp
- **Efficiency:** Carlos doesn't have to mark individually

---

### Stage 4: Executing Delivery

**Entry Requirement:** Carlos arrives at delivery address

#### Happy Path

**Step 4.1:** Carlos arrives at 123 Main St at 10:30 AM  
- **Carlos Parks:** Finds parking spot
- **Carlos Retrieves:** Love Bouquet + Lavender Candle from van
- **Carlos References:** Phone to double-check address and special instructions

**Step 4.2:** Carlos follows special instructions  
- **Special Instruction Read:** "Leave with doorman if no answer"
- **Carlos Enters:** Building lobby
- **Carlos Sees:** Doorman at desk
- **Carlos:** "Delivery for Sarah Johnson in [apartment/unit number if provided]"
- **Doorman:** "I can sign for it"

**Step 4.3:** Carlos hands over delivery  
- **Carlos Verifies:** Shows card message briefly: "Happy Birthday, Mom! Love, Alex"
- **Doorman Confirms:** "Yes, that's for Sarah, she's expecting it"
- **Carlos:** "Great, have a nice day!"
- **Doorman:** Signs or acknowledges (no signature capture in system currently)

**Step 4.4:** Carlos marks delivery complete  
- **Carlos Opens:** Order #2026-0209-0047 on phone
- **Carlos Clicks:** "Confirm Delivered" button
- **System Displays:** Confirmation modal: "Confirm delivery to Sarah Johnson at 123 Main St?"
- **Carlos Clicks:** "Yes, Delivered"
- **System Actions:**
  1. Update status: OUT_FOR_DELIVERY → DELIVERED
  2. Timestamp logged: 10:35 AM
  3. Order removed from Carlos's active delivery queue
  4. Order archived in completed deliveries
  5. **Automated email sent to customer:** "Your flowers have been delivered!"
  6. Customer account (if registered) shows delivery timestamp
- **UI Feedback:** Success message: "Delivery confirmed! 2 orders remaining."

**Step 4.5:** Carlos proceeds to next delivery  
- **Carlos Opens:** Delivery queue, now shows 2 remaining orders
- **Carlos Selects:** Order #2026-0209-0051 (next address)
- **Flow:** Repeats Stage 4 for next delivery

#### Alternative Path 4A: Recipient Home (Hand-to-Hand Delivery)

**Step 4.2a:** Carlos arrives at house address  
- **Carlos Rings:** Doorbell
- **Recipient (Sarah) Answers:** Door opens
- **Carlos:** "Flower delivery for Sarah Johnson!"
- **Sarah:** "That's me!"
- **Carlos Hands:** Bouquet directly to Sarah
- **Sarah (Optional):** "These are beautiful, thank you!"
- **Carlos:** "You're welcome, enjoy!"
- **Carlos Marks:** Delivered (same process as Step 4.4)

#### Alternative Path 4B: No One Home, No Safe Place

**Step 4.2b:** Carlos arrives at house, no doorman mentioned in instructions  
- **Carlos Rings:** Doorbell, no answer
- **Carlos Waits:** 1 minute, rings again, still no answer
- **Carlos Calls:** Recipient phone number (408) 555-1234 from order details
- **Phone:** Goes to voicemail
- **Carlos's Decision:** 
  - Cannot leave flowers outside (no instructions to do so, weather concerns)
  - Must bring back to shop

**Step 4.3b:** Carlos handles failed delivery  
- **Carlos Opens:** Order #2026-0209-0047 on phone
- **Carlos Sees:** "Confirm Delivered" button
- **Carlos Clicks:** "Report Issue" (alternative button)
- **System Shows:** Issue options:
  - "Recipient not home"
  - "Wrong address"
  - "Refused delivery"
  - "Other"
- **Carlos Selects:** "Recipient not home"
- **Carlos Adds Note:** "Called phone, no answer. Left voicemail. Returning to shop."
- **System Actions:**
  - Status changes: OUT_FOR_DELIVERY → DELIVERY_FAILED
  - Alert sent to Lily's dashboard
  - Order flagged for follow-up
- **Carlos Returns:** Bouquet to shop
- **Lily's Follow-up:** Contacts customer to reschedule delivery

#### Error Scenario 4A: Wrong Address or Can't Find Location

**Problem:** Carlos arrives at "123 Main St" but building doesn't exist or no such unit  
- **Carlos Calls:** Recipient phone: "Hi, this is Carlos from Lily's Florist with your delivery, but I'm having trouble finding 123 Main St..."
- **Recipient Clarifies:** "Oh, it's 123 Main Street COURT, not Main Street"
- **Carlos:** "Got it, I'll head there now"
- **Resolution:** Carlos navigates to correct address, completes delivery normally
- **Carlos Adds:** Note in system: "Address clarified - Main St Court"

**Alternative:** If Carlos can't reach recipient and can't find address:
- **Carlos Reports Issue:** "Wrong address - unable to locate"
- **System Alerts:** Lily
- **Lily Contacts:** Customer to verify address
- **Resolution:** Either redeliver later today or reschedule for tomorrow

---

### Stage 5: End of Shift & Reconciliation

**Entry Requirement:** Carlos has completed all deliveries or end of work hours

#### Happy Path

**Step 5.1:** Carlos finishes all deliveries by 12:30 PM  
- **Carlos's Delivery Queue:** Shows "0 orders remaining"
- **Carlos Sees:** "All deliveries complete!" message
- **Carlos Returns:** To shop

**Step 5.2:** Carlos reviews completed deliveries (optional)  
- **UI:** "Completed Today" tab in dashboard
- **Carlos Sees:**
  - Order #2026-0209-0047 - DELIVERED - 10:35 AM ✓
  - Order #2026-0209-0051 - DELIVERED - 11:10 AM ✓
  - Order #2026-0209-0055 - DELIVERED - 12:15 PM ✓
- **Use:** Carlos can verify all orders marked complete, no issues

**Step 5.3:** Carlos logs out  
- **Carlos Clicks:** Profile icon → "Logout"
- **System:** Clear session, return to login page
- **Carlos's Phone:** Closes browser

#### Alternative Path 5A: Afternoon Deliveries Later

**Scenario:** Carlos completed morning deliveries, will return for afternoon shift  
- **Step 5.1a:** Carlos's queue still shows 2 afternoon orders (delivery time 12-5 PM)
- **Carlos:** Returns to shop around 2:30 PM
- **Carlos Logs In:** Again on phone
- **System Shows:** 2 orders now ready for afternoon delivery
- **Carlos Loads:** Afternoon orders, repeats delivery process

---

## Journey 4: Manager (Lily) Inventory & Operations Management

### Primary Goal
Maintain accurate inventory levels, oversee daily operations, and ensure no orders are missed or blocked.

### Secondary Goals
- Receive low stock alerts before running out
- Restock materials when shipments arrive
- Monitor order flow and revenue
- Handle edge cases and customer issues escalated by staff

---

### Stage 1: Daily Operations Check-In

**Entry Point:** Lily arrives at shop at 8:00 AM and logs into admin dashboard on her desktop computer

#### Happy Path

**Step 1.1:** Lily opens lilys-florist.com/admin on desktop  
- **Browser:** Chrome on desktop PC behind counter
- **System:** Redirect to login
- **Lily Logs In:** lily@lilysflorist.com, password

**Step 1.2:** System authenticates Lily as Manager role  
- **System Action:** Load full admin permissions (pricing, inventory, users, all orders)
- **Redirect:** To Manager Dashboard (comprehensive view)

**Step 1.3:** Lily sees dashboard overview  
- **Dashboard Layout (Desktop):**
  - **Top Metrics Row:**
    - Today's Orders: 12 orders
    - Today's Revenue: $847.50
    - Week-to-Date Revenue: $3,245.80
    - Pending Production: 4 orders
  - **Alerts Section (prominent red/orange badges):**
    - 🔴 **CRITICAL:** Purple Iris (3 stems, threshold 10)
    - 🟠 **LOW:** Yellow Tulips (8 stems, threshold 15)
    - 🟠 **LOW:** Green Floral Foam (4 blocks, threshold 10)
  - **Today's Orders Timeline:**
    - Visual timeline showing orders by delivery time
    - Morning: 5 orders (2 DELIVERED, 2 OUT_FOR_DELIVERY, 1 READY)
    - Afternoon: 4 orders (3 READY, 1 PREPARING)
    - Evening: 3 orders (2 PAID, 1 PREPARING)
  - **Quick Actions Sidebar:**
    - "Manage Inventory"
    - "Create Promo Code"
    - "Upload New Products"
    - "View Sales Report"
    - "Manage Staff Users"

**Step 1.4:** Lily prioritizes critical alerts  
- **Lily's Thought:** "Purple Iris is critical—I need to order more immediately"
- **Lily Clicks:** Purple Iris alert row

---

### Stage 2: Handling Low Stock Alerts

**Entry Requirement:** Lily identified critical low stock item

#### Happy Path

**Step 2.1:** Lily opens inventory management page  
- **UI Display:**
  - Search/filter bar
  - Material list with columns: Name | Current Stock | Threshold | Status | Last Updated
  - Sorted by Status (Critical first, then Low, then OK)
  - **Purple Iris row highlighted:**
    - Current Stock: 3 stems
    - Threshold: 10 stems
    - Status: CRITICAL (red badge)
    - Deficit: -7 stems
    - Used in Products: "Sympathy Arrangement" (clickable link)

**Step 2.2:** Lily checks which products are affected  
- **Lily Clicks:** "Sympathy Arrangement" link
- **System Shows:** 
  - Sympathy Arrangement recipe requires 10 Purple Iris per unit
  - Current availability: 0 units can be made (insufficient inventory)
  - **Product Status:** Automatically marked "Out of Stock" on website
- **Lily's Thought:** "This is a popular sympathy arrangement, I need to fix this today"

**Step 2.3:** Lily calls supplier  
- **Action Outside System:** Lily picks up phone, calls flower supplier
- **Lily:** "Hi, I need an emergency order of Purple Iris, can you deliver today?"
- **Supplier:** "Yes, I can get you 50 stems by 2 PM"
- **Lily:** "Perfect, please deliver"

**Step 2.4:** Lily sets reminder to update inventory after delivery  
- **Action:** Lily writes post-it note: "Update Purple Iris inventory at 2 PM"
- **Alternative (future enhancement):** System could have "Expected Delivery" field to track pending shipments

---

### Stage 3: Restocking Inventory

**Entry Requirement:** Supplier arrives with shipment (2:15 PM same day)

#### Happy Path

**Step 3.1:** Supplier delivers 50 Purple Iris stems  
- **Physical Action:** Lily receives delivery, inspects quality, stores in cooler
- **Lily Returns:** To computer

**Step 3.2:** Lily opens inventory management page  
- **Lily Clicks:** "Manage Inventory" from dashboard
- **Lily Finds:** Purple Iris in list (still showing 3 stems)

**Step 3.3:** Lily adds stock  
- **Lily Clicks:** "Adjust Stock" button next to Purple Iris
- **Modal Opens:**
  - Current Stock: 3 stems
  - Adjustment Type: (●) Add Stock  ( ) Subtract Stock
  - Quantity: [input field]
  - Reason: [text field]
- **Lily Enters:**
  - Quantity: 50
  - Reason: "Supplier delivery from [Supplier Name]"
- **Lily Clicks:** "Save Adjustment"

**Step 3.4:** System updates inventory  
- **System Actions:**
  1. Update Purple Iris count: 3 + 50 = 53 stems
  2. Log transaction: "Added 50 stems - Supplier delivery - Lily - 2:17 PM"
  3. **Recalculate product availability:**
     - Sympathy Arrangement recipe needs 10 Purple Iris
     - 53 stems available ÷ 10 per unit = 5 units can be made
     - **Product status updated:** "Out of Stock" → "In Stock"
  4. Remove CRITICAL alert badge from Purple Iris
  5. Update dashboard: Low Stock Alerts now shows 2 items instead of 3
- **UI Feedback:** Success toast: "Inventory updated! Purple Iris now 53 stems. Sympathy Arrangement is back in stock on website."

**Step 3.5:** Lily verifies on public website  
- **Lily Opens:** New browser tab to lilys-florist.com (public view)
- **Lily Navigates:** To Sympathy category
- **Lily Sees:** "Sympathy Arrangement" now shows "In Stock" badge
- **Lily's Satisfaction:** "Good, customers can order it again"

#### Alternative Path 3A: Adjusting for Spoilage

**Scenario:** Lily inspects cooler and finds 8 Red Roses with wilted petals (must discard)

**Step 3.1a:** Lily opens inventory management  
**Step 3.2a:** Lily finds Red Roses (current count: 78 stems)  
**Step 3.3a:** Lily clicks "Adjust Stock"  
- **Modal:**
  - Adjustment Type: ( ) Add Stock  (●) Subtract Stock
  - Quantity: 8
  - Reason: "Spoilage - wilted petals"
- **Lily Saves:** Adjustment

**Step 3.4a:** System updates  
- Red Roses: 78 - 8 = 70 stems
- Recalculates availability for all products using Red Roses
- Logs transaction: "Subtracted 8 stems - Spoilage - Lily - 3:45 PM"

---

### Stage 4: Monitoring Order Flow

**Entry Requirement:** Lily wants to check on order status throughout the day

#### Happy Path

**Step 4.1:** Lily returns to dashboard after inventory update  
- **Dashboard Refreshes:** Shows updated metrics
- **Today's Orders:** Now 15 orders (3 more came in since morning)
- **Revenue:** $1,124.00

**Step 4.2:** Lily reviews orders by status  
- **Filter Options:** All | PAID | PREPARING | READY | OUT_FOR_DELIVERY | DELIVERED
- **Lily Clicks:** "PAID" filter
- **System Shows:** 2 orders currently paid but not yet being prepared
  - Order #2026-0209-0063 - Spring Bouquet - Pickup tomorrow
  - Order #2026-0209-0064 - Congratulations Arrangement - Delivery tomorrow morning
- **Lily's Thought:** "These are for tomorrow, Florists will handle them in the morning"

**Step 4.3:** Lily checks delivery progress  
- **Lily Clicks:** "OUT_FOR_DELIVERY" filter
- **System Shows:** 1 order
  - Order #2026-0209-0059 - Carlos (Driver) - Been out for delivery for 45 minutes
- **Lily's Thought:** "Carlos is probably almost done"
- **System Updates Live:** Status changes to DELIVERED (Carlos just confirmed)
- **Lily Sees:** Badge updates automatically, order moves to DELIVERED

**Step 4.4:** Lily reviews completed deliveries  
- **Lily Clicks:** "DELIVERED" filter
- **System Shows:** 8 orders delivered today with timestamps
- **Lily's Satisfaction:** "Good pace today"

#### Alternative Path 4A: Handling Escalated Issue

**Scenario:** Maria (Florist) reported an issue with Order #2026-0209-0047 (material quality problem) earlier

**Step 4.1a:** Lily sees notification badge: "1 Blocked Order"  
- **Alert Box:** Order #2026-0209-0047 flagged by Maria - "Material quality problem"
- **Lily Clicks:** Order number link

**Step 4.2a:** Lily reviews Maria's issue report  
- **System Shows:**
  - Order details
  - Maria's note: "3 red roses have brown edges, can't use. Only 9 good stems available, need 12."
  - Customer substitution preference: "Substitute with similar colors/style"
  - Order status: BLOCKED

**Step 4.3a:** Lily makes decision  
- **Lily's Analysis:** 
  - Customer allows substitution with similar colors
  - Pink roses are available and similar
  - No need to contact customer
- **Lily Adds:** Reply to Maria: "Use pink roses instead, same count"
- **Lily Clicks:** "Unblock Order" button
- **System Updates:**
  - Status: BLOCKED → PREPARING (returns to Maria's queue)
  - Notification sent to Maria: "Lily approved pink roses substitution for Order #2026-0209-0047"
  - Order note added: "Used pink roses instead of red due to quality issue - customer pre-approved substitutions"

**Step 4.4a:** Maria receives notification and continues preparation  
- **Flow:** Returns to Florist Journey Stage 4

---

### Stage 5: Creating Promotional Campaign

**Entry Requirement:** Lily wants to run a promotion for upcoming Mother's Day

#### Happy Path

**Step 5.1:** Lily clicks "Create Promo Code" from dashboard  
- **System Action:** Open promo code creation form

**Step 5.2:** Lily designs the promotion  
- **Form Fields:**
  - **Code:** MOM15
  - **Description (internal):** Mother's Day 15% off
  - **Discount Type:** (●) Percentage  ( ) Fixed Amount
  - **Discount Value:** 15%
  - **Valid From:** May 8, 2026
  - **Valid Until:** May 12, 2026 (Mother's Day weekend)
  - **Minimum Order Amount:** $30
  - **Usage Limit:** 
    - ( ) Single use per customer
    - (●) Unlimited uses
  - **Applicable Products:**
    - (●) All products
    - ( ) Specific categories: [dropdown]
- **Lily Fills In:** All fields as shown above

**Step 5.3:** Lily saves promo code  
- **Lily Clicks:** "Save Promo Code"
- **System Actions:**
  1. Validate: Code "MOM15" doesn't already exist ✓
  2. Create promo code record in database
  3. Set status: Active (since start date is in future, will auto-activate)
  4. Add to promo codes list
- **UI Feedback:** "Promo code MOM15 created! Active May 8-12."

**Step 5.4:** Lily plans marketing  
- **Lily's Next Actions (outside system):**
  - Post on Instagram: "Use code MOM15 for 15% off this Mother's Day!"
  - Post on Facebook with same message
  - Add to homepage banner (using content management feature)
- **System:** Promo code is now live and ready for customers to use during checkout

#### Alternative Path 5A: Creating Homepage Banner

**Step 5.1a:** Lily clicks "Upload New Products" → "Manage Homepage"  
**Step 5.2a:** Lily accesses banner editor  
- **UI:** Visual editor showing current homepage
- **Section:** "Hero Banner" with current image
- **Lily Clicks:** "Edit Banner"

**Step 5.3a:** Lily uploads Mother's Day banner  
- **Upload Image:** mother-day-promo.jpg (1920x600px)
- **Banner Link:** /products?category=mothers-day
- **Display Dates:** May 8 - May 12, 2026
- **Alt Text:** "Mother's Day Special - 15% off with code MOM15"

**Step 5.4a:** Lily saves and previews  
- **System:** Upload image, resize if needed, save to CDN
- **Lily Clicks:** "Preview" button
- **New Tab Opens:** Shows public homepage with new banner
- **Lily Confirms:** "Publish"
- **System:** Banner scheduled to auto-display May 8

---

### Stage 6: End of Day Reconciliation

**Entry Requirement:** End of business day (6:00 PM)

#### Happy Path

**Step 6.1:** Lily reviews daily summary  
- **Dashboard Metrics:**
  - Total Orders Today: 18
  - Total Revenue: $1,456.50
  - Completed Deliveries: 12
  - Pending Pickups: 2 (customers notified, will pick up tomorrow)
  - Orders for Tomorrow: 4 (all PAID, ready for morning prep)

**Step 6.2:** Lily checks low stock status before closing  
- **Low Stock Alerts:** 
  - Yellow Tulips: 8 stems (threshold 15) - Noted for tomorrow's supplier order
  - Green Floral Foam: 4 blocks (threshold 10) - Noted
- **Lily's Action:** Writes order list for tomorrow's supplier call

**Step 6.3:** Lily logs out  
- **Lily:** Closes admin dashboard
- **System:** Session terminates

---

## Error Recovery Patterns Summary

### Pattern 1: Inventory Mismatch
**Trigger:** System shows stock available, but physical count is lower  
**Detection:** Florist reports during preparation  
**Resolution:** 
1. Manager manually adjusts inventory
2. System recalculates availability
3. Affected product marked out of stock
4. Future orders prevented until restock

### Pattern 2: Failed Delivery
**Trigger:** Driver cannot complete delivery  
**Detection:** Driver reports issue via mobile dashboard  
**Resolution:**
1. Order status → DELIVERY_FAILED
2. Manager notified
3. Manager contacts customer to reschedule
4. New delivery attempt scheduled

### Pattern 3: Payment Declined
**Trigger:** Payment gateway returns error  
**Detection:** During checkout process  
**Resolution:**
1. Order creation prevented (no inventory deduction)
2. Cart preserved
3. Customer shown specific error
4. Customer retries with different payment method

### Pattern 4: Substitution Required
**Trigger:** Material quality issue or unexpected shortage  
**Detection:** Florist identifies during preparation  
**Resolution:**
1. Check customer substitution preference
2. If "Contact first" → Manager contacts customer for approval
3. If "Substitute freely" → Florist uses best judgment
4. Document substitution in order notes

### Pattern 5: Same-Day Cutoff Missed
**Trigger:** Customer attempts to order after 1 PM  
**Detection:** Frontend validates before cart  
**Resolution:**
1. "Today" disabled in date picker
2. Clear messaging about cutoff
3. Customer selects tomorrow or later
4. Prevention-based (no recovery needed)

---

## Journey Metrics & Success Criteria

### Customer Journey Success
- **Conversion Rate:** 70%+ (cart to completed order)
- **Time to Complete Order:** Under 5 minutes average
- **Checkout Abandonment:** Under 15%
- **Return Visit Rate:** 40%+ (registered users)

### Florist Assistant Success
- **Order Preparation Time:** 15-20 minutes per standard bouquet
- **Recipe Accuracy:** 100% (no stem count errors)
- **Status Update Timeliness:** Within 2 minutes of completion

### Driver Success
- **Deliveries Per Hour:** 4-6 (depending on distance)
- **Successful Delivery Rate:** 95%+ (first attempt)
- **Navigation Accuracy:** 100% (address validation)

### Manager Success
- **Low Stock Alert Response:** Within 4 hours
- **Inventory Accuracy:** 95%+ (physical vs. system)
- **Order Issue Resolution:** Within 1 hour of alert

---

**End of User Journey Documentation**