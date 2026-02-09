# Software Requirements Specification (SRS)

**Project:** Lily's Florist E-Commerce Platform  
**Version:** 2.0  
**Date:** February 9, 2026  
**Interview Date:** January 25, 2026

---

## Document Organization

Requirements are organized by functional area and numbered sequentially. Each requirement includes:
- **Traceability**: Reference to source (interview quote or user story)
- **Priority**: P0 (Critical), P1 (High), P2 (Medium)
- **Type**: Functional (FR) or Non-Functional (NFR)

---

## 1. User Authentication & Account Management

### 1.1 Guest & Registered Customers

**FR-01: Guest Checkout** [P0]  
*Source: Interview - "I'd want to accept credit and debit cards, plus common digital wallets"*  
The system shall allow customers to complete purchases without creating an account, requiring only:
- Email address (for confirmation)
- Phone number (for delivery coordination)
- Delivery/billing address

**FR-02: Customer Account Creation** [P1]  
*Source: User Story #8 - Order History & Reordering*  
The system shall allow customers to create an account with:
- Email and password
- Profile information (name, phone, default delivery addresses)
- The system shall send email verification upon registration

**FR-03: Customer Login & Session** [P1]  
*Source: User Story #6 - Secure Guest & Account Checkout*  
The system shall maintain authenticated sessions for registered customers and allow them to:
- View order history
- Access saved delivery addresses
- View and redeem loyalty points
- Manage account preferences

### 1.2 Staff Access Control

**FR-04: Manager (Owner) Role** [P0]  
*Source: Interview - "I'd prefer that only I can change pricing, promotions, or supplier settings"*  
The system shall provide a Manager role (Lily) with exclusive access to:
- Pricing and product configuration
- Promotional tools and discount codes
- Supplier and inventory restocking management
- User role assignment
- Sales reports and analytics

**FR-05: Florist Assistant Role** [P1]  
*Source: Interview - "Both assistants should be able to view orders, update statuses, and check inventory levels"*  
The system shall provide a Florist Assistant role with access to:
- View all orders (status: PAID, PREPARING, READY)
- Update order status through workflow stages
- View current inventory levels (stems and supplies)
- Mark orders as complete
- **Restriction**: Cannot modify pricing, promotions, or user permissions

**FR-06: Delivery Driver Role** [P2]  
*Source: Interview - "one part-time delivery helper"*  
The system shall provide a Driver role with access to:
- View orders with status READY and delivery_date = TODAY
- View delivery details: recipient name, address, phone, special instructions, card message
- Update delivery status (OUT_FOR_DELIVERY, DELIVERED)
- **Privacy restriction**: Driver role shall NOT see order totals, payment information, or customer email addresses

---

## 2. Product Catalog & Browsing

**FR-07: Product Categories** [P1]  
*Source: User Story #2 - Filter by Occasion & Season*  
The system shall categorize products by:
- **Occasion**: Wedding, Funeral/Sympathy, Birthday, Anniversary, Corporate Event, Just Because
- **Season**: Spring, Summer, Fall, Winter, Holiday (Valentine's, Mother's Day, Christmas)
- Products may belong to multiple categories

**FR-08: Product Filtering** [P1]  
*Source: User Story #2*  
The system shall allow customers to filter the product catalog by:
- Price range (configurable min/max sliders)
- Occasion category
- Season/holiday category
- Availability (in stock vs. pre-order)

**FR-09: Product Display** [P0]  
*Source: User Story #1 - Browse Visual Gallery*  
Each product listing shall display:
- High-resolution product photo
- Product name and brief description
- Base price
- Availability status
- "Quick view" option for larger image and full details

**FR-10: Seasonal Availability Indicator** [P1]  
*Source: Interview - "I love when sites show real-time availability so customers know what's in season"*  
The system shall display a "In Season Now" badge for products featuring currently abundant seasonal flowers, as configured by the Manager.

---

## 3. Inventory Management (Stem-Level Tracking)

**FR-11: Raw Material Database** [P0]  
*Source: Interview - "I mostly think in terms of individual stems. That's how I order from suppliers"*  
The system shall maintain an inventory database of raw materials including:
- Flower types (e.g., Red Roses, Tulips, Ferns) tracked by stem count
- Supplies (e.g., Vases, Ribbons, Floral Foam) tracked by unit count
- Current stock quantity
- Reorder threshold (minimum stock level)
- Unit cost (for internal tracking)

**FR-12: Product Recipe/Formula** [P0]  
*Source: Interview - "For day-to-day work, I mentally translate that into how many arrangements I can realistically make. Right now that translation lives in my head"*  
The system shall allow the Manager to define a "recipe" for each product specifying:
- Required raw materials (e.g., "12 Red Roses")
- Required supplies (e.g., "1 Glass Vase")
- The recipe represents what is consumed when one unit of this product is sold

**FR-13: Automatic Stock Availability Check** [P0]  
*Source: User Story #12 - Automated Inventory Tracking*  
When a customer attempts to add a product to cart, the system shall:
1. Check current raw material stock levels against the product recipe
2. Calculate maximum quantity available based on limiting ingredient
3. If insufficient stock: display "Out of Stock" or "Only X available"
4. Update availability status dynamically across the site

**FR-14: Stock Deduction on Order Confirmation** [P0]  
*Source: User Story #12*  
Upon successful payment processing, the system shall automatically:
1. Deduct required raw materials from inventory based on product recipes
2. Log the deduction with timestamp and order reference
3. Update product availability calculations site-wide

**FR-15: Low Stock Alerts** [P1]  
*Source: Interview - "A system that warns me early... would really help"*  
The system shall display visual alerts in the Manager Dashboard when:
- Any raw material falls below its configured reorder threshold
- Alert shall show: material name, current count, threshold, deficit amount
- Alerts shall be sortable by urgency (most critical first)

**FR-16: Manual Inventory Adjustments** [P0]  
*Source: Interview - "I rush an order from my supplier"*  
The system shall allow the Manager to:
- Add stock (restocking from suppliers)
- Subtract stock (spoilage, breakage, manual sales)
- Enter adjustment reason as free text note
- All adjustments shall be logged with timestamp and user

**FR-17: Inventory Transaction History** [P2]  
The system shall maintain a log of all inventory changes including:
- Type (order deduction, manual add, manual subtract)
- Quantity changed
- Timestamp
- Associated order ID (if applicable)
- User who made the change

---

## 4. Add-On Products & Upselling

**FR-18: Add-On Product Type** [P1]  
*Source: Interview - "I'd like add-ons shown separately but clearly tied into the bouquet ordering"*  
The system shall support an "Add-On" product type for items such as:
- Candles
- Chocolates
- Greeting cards
- Premium vases (upgrades)

**FR-19: Add-On Display Logic** [P1]  
*Source: Interview - "Customers should first choose their flowers, then be gently prompted to add items"*  
Add-on products shall:
- NOT appear in main product gallery or category pages
- Appear in a dedicated "Complete Your Gift" section during cart review or checkout
- Display with thumbnail, name, price, and brief description
- Allow quantity selection

**FR-20: Add-On Inventory** [P1]  
*Source: Interview - "makes it easier for me to manage those items without mixing them into floral inventory"*  
Add-on products shall:
- Track simple unit inventory (not stem-based)
- Deduct stock upon order completion
- Display "Out of Stock" if unavailable

---

## 5. Order Workflow & Fulfillment

### 5.1 Customer Order Placement

**FR-21: Fulfillment Method Selection** [P0]  
*Source: Interview - "Customers should be able to choose delivery or pickup"*  
Before checkout, the system shall require customers to select:
- **In-Store Pickup**: Customer collects from shop address
- **Local Delivery**: Shop delivers to customer-specified address

**FR-22: Delivery Date Selection** [P0]  
*Source: Interview - "select a date and time window"*  
For delivery orders, the system shall:
- Display a date picker showing available delivery dates
- Allow selection from 7 days into the future (configurable)
- Display time slots: Morning (9 AM - 12 PM), Afternoon (12 PM - 5 PM), Evening (5 PM - 8 PM)

**FR-23: Same-Day Delivery Cutoff** [P0]  
*Source: Interview - "for same-day delivery I usually cut it off around 1:00 pm"*  
The system shall:
- Compare current server time against cutoff (default: 1:00 PM, configurable by Manager)
- If current time > cutoff: disable "Today" option in date picker
- Display message: "Same-day delivery orders must be placed before 1:00 PM"

**FR-24: Delivery Zone-Based Pricing** [P0]  
*Source: Interview - "I charge different delivery rates based on distance from the shop. Local downtown deliveries are lower"*  
The system shall:
- Allow Manager to configure delivery zones by zip code or radius from shop
- Assign delivery fee to each zone (e.g., Zone 1: $5, Zone 2: $12, Zone 3: $20)
- Calculate delivery fee automatically when customer enters delivery address
- Display delivery fee before payment
- Support "No Delivery Available" for out-of-range addresses

**FR-25: Recipient Information Capture** [P0]  
*Source: Interview - "recipient details, address, and a card message"*  
For delivery orders, the system shall capture:
- Recipient full name
- Delivery address (street, city, state, zip)
- Recipient phone number
- Special delivery instructions (e.g., "Gate code 1234", "Leave with doorman")
- Maximum 500 characters for instructions

**FR-26: Card Message** [P0]  
*Source: Interview - "include a card message"*  
The system shall provide a text field for customers to enter a personalized card message:
- Maximum 200 characters
- Display character counter
- Support basic punctuation
- Field is optional but encouraged with placeholder text

**FR-27: Pickup Date/Time Selection** [P1]  
For pickup orders, the system shall:
- Allow date selection (today through 7 days, respecting same-day cutoff)
- Display pickup time slots: 10 AM - 12 PM, 12 PM - 3 PM, 3 PM - 6 PM
- Show shop address and phone number

### 5.2 Order Status Workflow

**FR-28: Order Status States** [P0]  
*Source: User Story #11 - Centralized Order Dashboard*  
The system shall track orders through the following states:
1. **PENDING**: Payment processing
2. **PAID**: Payment confirmed, awaiting production
3. **PREPARING**: Florist is assembling
4. **READY**: Complete, awaiting pickup/delivery
5. **OUT_FOR_DELIVERY**: Driver has collected order
6. **DELIVERED**: Confirmed delivery/pickup
7. **CANCELLED**: Order cancelled (before PREPARING)

**FR-29: Status Transition Rules** [P1]  
The system shall enforce:
- Only Florist Assistants and Manager can move orders to PREPARING
- Only Florist Assistants and Manager can move orders to READY
- Only Driver and Manager can move orders to OUT_FOR_DELIVERY
- Only Driver and Manager can confirm DELIVERED
- Customers cannot see statuses PENDING/PAID (show as "Order Confirmed")

**FR-30: Status Timestamps** [P2]  
The system shall log timestamp for each status transition for internal tracking.

---

## 6. Customer Profiles & Personalization

**FR-31: Customer Order History** [P1]  
*Source: User Story #8; Interview - "past orders"*  
Registered customers shall view a list of past orders showing:
- Order date
- Product thumbnail and name
- Recipient name (if delivery)
- Total amount
- Order status
- Link to full order details

**FR-32: Quick Reorder Function** [P1]  
*Source: User Story #8 - "easily click 'Reorder'"*  
From order history, customers shall:
- Click "Reorder" button
- System pre-fills cart with same products and add-ons
- Customer reviews, updates delivery details, and completes checkout

**FR-33: Customer Preferences Storage** [P1]  
*Source: Interview - "preferred arrangements or flowers, favorite colors, delivery addresses, special dates"*  
The system shall allow Manager/Florists to add internal notes to customer profiles:
- Favorite flowers/color schemes
- Typical budget range
- Allergies or dislikes
- Important dates (anniversaries, birthdays)
- Maximum 1000 characters per note field
- **Privacy**: These notes are visible only to staff, not to customers

**FR-34: Saved Delivery Addresses** [P1]  
*Source: User Story #8*  
Registered customers shall:
- Save multiple delivery addresses with labels (e.g., "Mom's House", "Office")
- Select from saved addresses during checkout
- Edit or delete saved addresses from account settings

**FR-35: Flower Substitution Preferences** [P2]  
*Source: Interview - "I'll substitute flowers with something similar and call the customer if it's a big change"*  
During checkout, customers shall optionally indicate substitution preferences:
- "Contact me before substituting"
- "Substitute with similar colors/style"
- "Substitute freely, I trust your expertise"
- Default: "Contact me before substituting"

---

## 7. Payment Processing

**FR-36: Payment Gateway Integration** [P0]  
*Source: Interview - "credit and debit cards, plus common digital wallets"*  
The system shall integrate with Square Payment API to process:
- Credit cards (Visa, Mastercard, Amex, Discover)
- Debit cards
- Digital wallets (Apple Pay, Google Pay)

**FR-37: Secure Payment Flow** [P0]  
The system shall:
- Load Square payment form via embedded iframe
- Never store raw credit card numbers in application database
- Use tokenized payment data only
- Comply with PCI DSS Level 1 requirements through Square

**FR-38: Order Confirmation Email** [P0]  
*Source: Interview - "automatic confirmation email... customers are reassured their order was received"*  
Upon successful payment, the system shall automatically send email to customer containing:
- Order number
- Itemized list of products and add-ons
- Delivery/pickup date and time
- Recipient details (if delivery)
- Order total breakdown (subtotal, delivery, tax, discount)
- Shop contact information
- Link to order tracking (if customer has account)

**FR-39: Payment Failure Handling** [P1]  
If payment is declined, the system shall:
- Display clear error message from payment processor
- Retain cart contents
- Allow customer to retry with different payment method
- Log failed attempt (for fraud detection)

---

## 8. Loyalty Program

**FR-40: Points Accrual** [P1]  
*Source: Interview - "Regular customers earn points for purchases"*  
The system shall:
- Award 1 loyalty point per $1 spent (pre-tax, post-discount)
- Apply points only to registered customer accounts
- Display points earned on order confirmation

**FR-41: Points Balance Display** [P1]  
*Source: User Story #7*  
Registered customers shall see:
- Current points balance in account dashboard
- Points earned per historical order
- Points expiration policy (if implemented)

**FR-42: Points Redemption** [P1]  
*Source: User Story #7*  
During checkout, registered customers shall:
- View points balance
- Enter points to redeem (e.g., 100 points = $10 discount)
- See discount applied to order total
- System shall deduct redeemed points from balance upon payment confirmation

**FR-43: Points Conversion Rate** [P2]  
The system shall allow Manager to configure:
- Points-to-dollar conversion rate (default: 100 points = $10)
- Minimum redemption threshold (e.g., 50 points minimum)

---

## 9. Promotional Tools

**FR-44: Discount Code Creation** [P1]  
*Source: User Story #15 - "create and manage discount codes (e.g., 'MOTHER10')"*  
The system shall allow Manager to create promotional codes with:
- Code string (alphanumeric, 4-20 characters)
- Discount type: Percentage off or Fixed amount off
- Discount value
- Valid date range (start and end date)
- Minimum order amount (optional)
- Usage limit: Single-use per customer, or unlimited uses
- Applicable products: All products, or specific categories

**FR-45: Discount Code Application** [P1]  
During checkout, customers shall:
- Enter discount code in designated field
- Click "Apply"
- See validation message (success or error)
- See discount reflected in order total
- Discount shall apply before tax calculation

**FR-46: Code Validation Rules** [P1]  
The system shall validate that:
- Code exists and is active
- Current date is within valid range
- Order meets minimum amount (if specified)
- Customer hasn't exceeded usage limit
- Display specific error messages for each failure type

**FR-47: Seasonal Promotions Banner** [P2]  
*Source: Interview - "I'd really like the website to highlight these specials clearly"*  
The system shall allow Manager to:
- Create homepage banner promoting current special
- Upload banner image and link to category/product
- Set display schedule (start/end dates)
- Banner auto-hides when end date passes

---

## 10. Content Management

**FR-48: Product Management Interface** [P0]  
The Manager shall be able to:
- Create new products with name, description, base price, category tags
- Upload up to 5 photos per product
- Define product recipe (raw materials required)
- Set product as active/inactive
- Mark product as "seasonal" with season tag

**FR-49: Photo Gallery Management** [P1]  
*Source: User Story #13 - "upload new photos to the gallery"*  
The Manager shall be able to:
- Upload photos to a portfolio gallery (separate from product catalog)
- Add captions describing occasion/event type
- Reorder gallery images via drag-and-drop
- Mark photos as "featured" for homepage display

**FR-50: About Page & Contact Info** [P1]  
*Source: Interview - "about page, a contact page"*  
The system shall include:
- About page with shop story, hours, and location (editable by Manager)
- Contact page with phone, email, address, and embedded map
- Custom event inquiry form for weddings/corporate (name, email, event date, details field)

**FR-51: FAQ Management** [P2]  
*Source: Interview - "page explaining delivery details and FAQs"*  
The Manager shall be able to:
- Create FAQ items with question and answer
- Organize FAQs by category (Delivery, Care Tips, Custom Orders)
- Reorder FAQ display sequence

**FR-52: Blog/Seasonal Tips** [P2]  
*Source: User Story #10 - "read blog posts about flower care and seasonal stories"*  
The Manager shall be able to:
- Create blog posts with title, body content, and featured image
- Publish or save as draft
- Display recent posts on homepage or dedicated blog page
- Tag posts by topic (Care Tips, Seasonal Highlights, Events)

---

## 11. Order Management Dashboard (Staff)

**FR-53: Manager Dashboard Overview** [P0]  
*Source: Interview - "view all incoming orders... in a single dashboard"*  
The Manager Dashboard shall display:
- **Today's Orders**: Count and list of orders for today's delivery/pickup
- **Pending Production**: Orders in PAID status requiring attention
- **Low Stock Alerts**: Raw materials below threshold (from FR-15)
- **Revenue Summary**: Today's sales, week-to-date, month-to-date

**FR-54: Order List View** [P0]  
*Source: User Story #11*  
Staff users shall view a filterable/sortable order list showing:
- Order number
- Customer name
- Order date/time
- Delivery/pickup date
- Status
- Order total (hidden for Driver role)
- Quick action buttons (View Details, Update Status)

**FR-55: Order Detail View** [P0]  
Clicking an order shall display full details:
- Customer information
- Recipient information (if delivery)
- Itemized products and add-ons
- Card message
- Special delivery instructions
- Payment status
- Status history timeline
- Action button: Update Status

**FR-56: Production View for Florists** [P1]  
*Source: Interview context about assistants needing to "view and update orders"*  
Florist Assistants viewing an order in PAID or PREPARING status shall see:
- Product name and photo
- **Recipe breakdown**: "Requires: 12 Red Roses, 5 Ferns, 1 Glass Vase" (from FR-12)
- Quantity ordered
- Card message to include
- Add-on items (non-floral)
- Button: "Mark as Preparing" or "Mark as Ready"

**FR-57: Delivery View for Drivers** [P1]  
*Source: FR-06*  
Driver role viewing orders with status READY shall see:
- Recipient name
- Delivery address (with "Get Directions" link to Google Maps)
- Recipient phone number
- Special delivery instructions
- Card message (so driver can verify correct order)
- Button: "Out for Delivery" and "Confirm Delivered"
- **Hidden**: Order total, customer email, payment details

---

## 12. Customer Order Tracking

**FR-58: Order Tracking for Registered Customers** [P1]  
*Source: Interview - "order tracking are things I really wish I had now"*  
Registered customers viewing order details shall see:
- Current status translated to customer-friendly language:
  - PAID/PREPARING → "Being prepared"
  - READY → "Ready for pickup" or "Ready for delivery"
  - OUT_FOR_DELIVERY → "Out for delivery - arriving soon"
  - DELIVERED → "Delivered on [date/time]"
- Estimated preparation time (configurable, e.g., "2-3 hours")
- Status shall update automatically when staff changes backend status

**FR-59: Delivery Notification Email** [P2]  
When order status changes to DELIVERED, the system shall automatically send email to customer:
- Subject: "Your flowers have been delivered!"
- Order number
- Delivery confirmation timestamp
- Thank you message with link to leave feedback (future enhancement)

---

## 13. Social Media Integration

**FR-60: Social Media Links** [P2]  
*Source: Interview - "I mostly use Instagram and Facebook"*  
The website footer shall display clickable icons linking to:
- Instagram profile
- Facebook page
- Links shall be configurable by Manager in settings

**FR-61: Instagram Feed Embed** [P2]  
*Source: Interview - "it doesn't link smoothly to ordering"*  
The homepage or gallery page shall optionally embed:
- Recent Instagram posts (via Instagram Basic Display API)
- Clicking a post links to full Instagram post
- This provides inspiration while main ordering happens on site

---

## 14. Non-Functional Requirements

**NFR-01: Mobile Responsiveness** [P0]  
The web application shall be fully responsive and optimized for:
- Mobile phones (320px - 767px width)
- Tablets (768px - 1024px width)
- Desktops (1025px+ width)
Priority layout for mobile: Customer storefront and Driver delivery view

**NFR-02: Page Load Performance** [P1]  
- Homepage shall load in under 2 seconds on 4G connection
- Product catalog pages shall load in under 2.5 seconds
- Checkout flow pages shall load in under 1.5 seconds
- Performance measured via Google Lighthouse score target: 85+

**NFR-03: Inventory Check Performance** [P0]  
*Source: High-traffic concern during holidays*  
The availability check (comparing recipes to raw stock) when adding items to cart shall:
- Execute in under 200ms for single product
- Cache calculation results for 30 seconds to handle concurrent traffic
- Support up to 100 concurrent "add to cart" actions without degradation

**NFR-04: Payment Security** [P0]  
- All payment data must be transmitted via HTTPS (TLS 1.2 minimum)
- Credit card data shall be tokenized via Square API only
- Application shall never store CVV codes
- Application shall comply with PCI DSS Level 1 via Square SAQ-A

**NFR-05: Data Backup** [P1]  
- Database shall be backed up nightly at 2:00 AM local time
- Backup retention: 30 days rolling
- Backup storage: Encrypted, off-site
- Recovery time objective (RTO): 4 hours
- Recovery point objective (RPO): 24 hours

**NFR-06: Browser Compatibility** [P1]  
The application shall function correctly on:
- Chrome (latest 2 versions)
- Safari (latest 2 versions)
- Firefox (latest 2 versions)
- Edge (latest version)
- iOS Safari (iOS 14+)
- Chrome Mobile (Android 10+)

**NFR-07: Accessibility** [P2]  
The application shall meet WCAG 2.1 Level AA standards:
- Proper heading hierarchy
- Alt text for all product images
- Keyboard navigation support
- Sufficient color contrast (4.5:1 minimum)
- Screen reader compatibility

**NFR-08: Scalability** [P1]  
*Source: Interview - "over 100 orders in a single day" during holidays*  
The system shall support:
- Up to 500 concurrent active sessions
- Up to 200 orders per day processing capacity
- Database indexing optimized for read-heavy workloads
- Horizontal scaling capability via load balancer (future)

**NFR-09: Uptime** [P1]  
The application shall maintain:
- 99.5% uptime measured monthly
- Planned maintenance windows: Tuesdays 2:00 AM - 4:00 AM
- Status page displaying current system health

**NFR-10: Localization** [P2]  
The system shall:
- Display prices in USD with appropriate formatting ($12.50)
- Display dates in US format (MM/DD/YYYY)
- Use 12-hour time format with AM/PM
- Support future expansion to additional currencies/locales

---

## 15. Future Enhancements (Out of Scope for v1.0)

The following were discussed but deferred to post-launch iterations:

- **SMS notifications** for order status updates
- **Customer feedback/review system** post-delivery
- **Subscription flower service** (weekly/monthly recurring orders)
- **Wholesale ordering portal** for corporate clients
- **Advanced analytics dashboard** (customer segmentation, sales trends)
- **Multi-location support** if Lily opens additional shops
- **Integration with accounting software** (QuickBooks, Xero)

---

## Traceability Matrix Summary

| Requirement ID | Source Interview Quote / User Story |
|---|---|
| FR-11 to FR-17 | "I mostly think in terms of individual stems" + "translation lives in my head" |
| FR-23 | "I usually cut it off around 1:00 pm" |
| FR-24 | "I charge different delivery rates based on distance" |
| FR-18 to FR-20 | "add-ons shown separately but clearly tied into the bouquet ordering" |
| FR-05 | "only I can change pricing, promotions, or supplier settings" |
| FR-33 | "past orders, preferred arrangements, favorite colors, special dates" |
| FR-58 | "order tracking are things I really wish I had now" |
| FR-44 to FR-47 | User Story #15 - Promotional tools |

*(Full detailed matrix available in separate traceability document)*
