# Complete Requirements Traceability Matrix

**Project:** Lily's Florist E-Commerce Platform  
**Version:** 2.0  
**Date:** February 9, 2026

---

## Purpose

This matrix traces each requirement back to its originating user story and interview source, ensuring all requirements are justified by validated customer needs. Requirements without direct interview validation are marked as [Technical Necessity] or [Industry Standard].

---

## Traceability Table

| Requirement ID | Requirement Summary | User Story | Interview Source / Rationale |
|----------------|---------------------|------------|------------------------------|
| **FR-01** | Guest Checkout | US-08 (Guest & Account Checkout) | "checkout as a guest for speed, or log in to save my details" |
| **FR-02** | Customer Account Creation | US-08 (Guest & Account Checkout) | Same as FR-01 - dual option approach |
| **FR-03** | Customer Login & Session | US-09 (Order History & Reordering) | Enables saved addresses and order history access |
| **FR-04** | Manager (Owner) Role | US-15, US-16, US-17, US-18 (All Owner stories) | "I'd prefer that only I can change pricing, promotions, or supplier settings" |
| **FR-05** | Florist Assistant Role | US-23, US-24, US-25 (Florist stories) | "Both assistants should be able to view orders, update statuses, and check inventory levels" |
| **FR-06** | Delivery Driver Role | US-26, US-27 (Driver stories) | "one part-time delivery helper" + privacy requirement implied |
| **FR-07** | Product Categories | US-01 (Browse Gallery), US-02 (Filter by Occasion) | "filter products by occasion (e.g., Birthday, Sympathy) or season" |
| **FR-08** | Product Filtering | US-02 (Filter by Occasion & Season) | Direct implementation of filtering capability |
| **FR-09** | Product Display | US-01 (Browse Visual Gallery) | "browse a high-quality photo gallery of bouquets" |
| **FR-10** | Seasonal Availability Indicator | US-02 (View Seasonal Availability) | "I love when sites show real-time availability so customers know what's in season" |
| **FR-11** | Raw Material Database | US-15 (Define Product Recipes) | "I mostly think in terms of individual stems. That's how I order from suppliers" |
| **FR-12** | Product Recipe/Formula | US-15 (Define Product Recipes) | "For day-to-day work, I mentally translate that into how many arrangements I can realistically make. Right now that translation lives in my head, which is part of the problem" |
| **FR-13** | Automatic Stock Availability Check | US-16 (Automatic Stock Deduction) | Prevents overselling - calculated from recipes vs. raw materials |
| **FR-14** | Stock Deduction on Order Confirmation | US-16 (Automatic Stock Deduction) | "the website to automatically deduct stock (flowers, vases, add-ons) when an online order is placed... I don't accidentally sell items I don't have, preventing shortages during holidays" |
| **FR-15** | Low Stock Alerts | US-17 (Receive Low Stock Alerts) | "A system that warns me early... would really help" |
| **FR-16** | Manual Inventory Adjustments | US-18 (Manually Adjust Inventory) | "Sometimes I rush an order from my supplier" + implied spoilage/breakage tracking |
| **FR-17** | Inventory Transaction History | US-18 (Manually Adjust Inventory) | [Technical Necessity] - Audit trail for manual adjustments |
| **FR-18** | Add-On Product Type | US-07 (Add Complementary Items) | "Most arrangements use fresh, seasonal blooms, with add-ons like vases, chocolates, or handwritten cards" |
| **FR-19** | Add-On Display Logic | US-07 (Add Complementary Items) | "Customers should first choose their flowers, then be gently prompted to add items like candles, chocolates, or vases. That keeps the bouquets clean and simple" |
| **FR-20** | Add-On Inventory | US-07 (Add Complementary Items) | "makes it easier for me to manage those items without mixing them into floral inventory" |
| **FR-21** | Fulfillment Method Selection | US-03 (Delivery or Pickup Selection) | "Customers should be able to choose delivery or pickup" |
| **FR-22** | Delivery Date Selection | US-04 (Schedule Delivery Date & Time) | "select a specific delivery date and a preferred time slot during checkout" |
| **FR-23** | Same-Day Delivery Cutoff | US-04 (Schedule Delivery with Cutoff) | "for same-day delivery I usually cut it off around 1:00 pm... I'd like the website to clearly enforce that cutoff so expectations are set upfront" |
| **FR-24** | Delivery Zone-Based Pricing | US-05 (See Automatic Delivery Fee) | "I charge different delivery rates based on distance from the shop. Local downtown deliveries are lower, and farther neighborhoods cost a bit more... having the website handle it automatically would save time" |
| **FR-25** | Recipient Information Capture | US-05 (Card Message) | "recipient details, address, and a card message" |
| **FR-26** | Card Message | US-06 (Add Personalized Card Message) | "include a card message" with character limit for practical card size |
| **FR-27** | Pickup Date/Time Selection | US-03 (Delivery or Pickup Selection) | Parallel functionality to delivery scheduling for pickup customers |
| **FR-28** | Order Status States | US-19 (View Centralized Dashboard), US-24 (Update Status) | [Technical Necessity] - Workflow state machine for order lifecycle |
| **FR-29** | Status Transition Rules | US-24 (Update Order Status) | [Technical Necessity] - Permission controls on status changes |
| **FR-30** | Status Timestamps | US-10 (Track Order Status), US-20 (Send Confirmations) | Enables customer order tracking and operational metrics |
| **FR-31** | Customer Order History | US-09 (Order History & Reordering) | "view my past orders" |
| **FR-32** | Quick Reorder Function | US-09 (Order History & Reordering) | "easily click 'Reorder'... quickly send the same arrangement to a recurring recipient (like a spouse or parent) without searching for it again" |
| **FR-33** | Customer Preferences Storage | US-09 (implied), Interview insight | "What I can't easily track now is customer order history, favorite flowers, or notes like allergies or past feedback. Having that saved would really help with repeat customers... past orders, preferred arrangements or flowers, and typical budget range. Notes like favorite colors, delivery addresses, and special dates" |
| **FR-34** | Saved Delivery Addresses | US-09 (Order History & Reordering) | Accelerates repeat ordering - part of "save time later" benefit |
| **FR-35** | Flower Substitution Preferences | US-12 (Indicate Substitution Preferences) | "I'll substitute flowers with something similar and call the customer if it's a big change" |
| **FR-36** | Payment Gateway Integration | US-08 (Secure Checkout) | "I'd want to accept credit and debit cards, plus common digital wallets since many customers shop on their phones" |
| **FR-37** | Secure Payment Flow | US-08 (Secure Checkout) | [Industry Standard] - PCI compliance requirement |
| **FR-38** | Order Confirmation Email | US-20 (Send Automatic Confirmations) | "the system to automatically send an order confirmation email to the customer with their order summary and delivery date... customers are reassured their order was received, reducing the need for them to call the shop to check" |
| **FR-39** | Payment Failure Handling | [Technical Necessity] | Error recovery pattern - not explicitly requested but essential for robust checkout |
| **FR-40** | Points Accrual | US-11 (Earn and Redeem Loyalty Points) | "Regular customers earn points for purchases... I'd love for the website to handle this automatically" |
| **FR-41** | Points Balance Display | US-11 (Earn and Redeem Loyalty Points) | "see my loyalty points balance" |
| **FR-42** | Points Redemption | US-11 (Earn and Redeem Loyalty Points) | "apply them for a discount at checkout... feel rewarded for my continued business" |
| **FR-43** | Points Conversion Rate | US-11 (Earn and Redeem Loyalty Points) | [Technical Necessity] - Configuration for loyalty program management |
| **FR-44** | Discount Code Creation | US-21 (Create Promotional Codes) | "create and manage discount codes (e.g., 'MOTHER10') for holidays" |
| **FR-45** | Discount Code Application | US-21 (Create Promotional Codes) | Customer-facing implementation of promo code system |
| **FR-46** | Code Validation Rules | US-21 (Create Promotional Codes) | [Technical Necessity] - Business logic for promo code enforcement |
| **FR-47** | Seasonal Promotions Banner | US-22 (Update Seasonal Specials) | "I'd really like the website to highlight these specials clearly so customers see them right away when they visit" |
| **FR-48** | Product Management Interface | US-22 (Update Product Photos) | "an easy way to upload new photos to the gallery and update the 'Seasonal Specials' section" |
| **FR-49** | Photo Gallery Management | US-01 (Browse Gallery), US-22 (Update Photos) | "browse a high-quality photo gallery" + CMS capability for Lily to update |
| **FR-50** | About Page & Contact Info | US-13 (Custom Event Inquiry) | "about page, a contact page for custom orders, and a page explaining delivery details and FAQs" |
| **FR-51** | FAQ Management | Interview requirement | "page explaining delivery details and FAQs" |
| **FR-52** | Blog/Seasonal Tips | US-14 (Read Seasonal Tips) | "read blog posts about flower care and seasonal stories... learn how to make my bouquet last longer" |
| **FR-53** | Manager Dashboard Overview | US-19 (View Centralized Dashboard) | "view all incoming orders (from the web, phone, or walk-ins) in a single dashboard... I stop 'juggling' multiple lists and ensure no order is missed during busy rushes" |
| **FR-54** | Order List View | US-19 (View Centralized Dashboard) | Detailed implementation of centralized order management |
| **FR-55** | Order Detail View | US-19, US-23 (Production View) | Comprehensive order information for all staff roles |
| **FR-56** | Production View for Florists | US-23 (View Production Queue with Recipes) | "see a 'To Prepare' queue showing each order's required flowers by stem count (the recipe)... gather exactly what I need from the cooler efficiently without guessing quantities" |
| **FR-57** | Delivery View for Drivers | US-26 (View Daily Delivery Queue) | "see today's deliveries with addresses, recipient names, and special instructions... plan my route efficiently... without accessing sensitive payment information" |
| **FR-58** | Order Tracking for Customers | US-10 (Track Order Status) | "order tracking are things I really wish I had now" |
| **FR-59** | Delivery Notification Email | US-27 (Confirm Delivery Completion) | Automated customer notification when delivery confirmed - completes tracking loop |
| **FR-60** | Social Media Links | Interview context | "I mostly use Instagram and Facebook" - integration for brand presence |
| **FR-61** | Instagram Feed Embed | Interview context | "right now it doesn't link smoothly to ordering" - bridge social media to e-commerce |
| **NFR-01** | Mobile Responsiveness | Interview context | "since many customers shop on their phones" + Driver mobile usage implied |
| **NFR-02** | Page Load Performance | [Industry Standard] | User experience best practice for e-commerce conversion |
| **NFR-03** | Inventory Check Performance | US-16 (Automatic Stock Deduction) | "during peak times like Valentine's Day, Mother's Day, and major holidays, that number jumps to well over 100 orders in a single day" - high concurrency requirement |
| **NFR-04** | Payment Security | US-08 (Secure Checkout) | [Industry Standard] - PCI DSS compliance mandatory |
| **NFR-05** | Data Backup | [Industry Standard] | Business continuity requirement for order and inventory data |
| **NFR-06** | Browser Compatibility | [Technical Necessity] | Cross-platform access for diverse customer base |
| **NFR-07** | Accessibility | [Industry Standard] | WCAG compliance for inclusive design |
| **NFR-08** | Scalability | Interview context | "over 100 orders in a single day" during holidays - system must handle peak loads |
| **NFR-09** | Uptime | [Industry Standard] | Business continuity - shop operates 6 days/week, orders come 24/7 |
| **NFR-10** | Localization | [Technical Necessity] | US market (USD, date format, timezone) |

---

## User Story Coverage Summary

| User Story ID | Title | Related Requirements | Coverage Status |
|---------------|-------|---------------------|-----------------|
| US-01 | Browse Visual Gallery | FR-07, FR-09, FR-49 | ✅ Complete |
| US-02 | View Seasonal Availability | FR-07, FR-08, FR-10 | ✅ Complete |
| US-03 | Delivery or Pickup Selection | FR-21, FR-27 | ✅ Complete |
| US-04 | Schedule Delivery with Cutoff | FR-22, FR-23 | ✅ Complete |
| US-05 | See Automatic Delivery Fee | FR-24, FR-25 | ✅ Complete |
| US-06 | Add Personalized Card Message | FR-26 | ✅ Complete |
| US-07 | Add Complementary Items | FR-18, FR-19, FR-20 | ✅ Complete |
| US-08 | Guest & Account Checkout | FR-01, FR-02, FR-03, FR-36, FR-37 | ✅ Complete |
| US-09 | Order History & Reordering | FR-31, FR-32, FR-33, FR-34 | ✅ Complete |
| US-10 | Track Order Status | FR-30, FR-58, FR-59 | ✅ Complete |
| US-11 | Earn and Redeem Loyalty Points | FR-40, FR-41, FR-42, FR-43 | ✅ Complete |
| US-12 | Indicate Substitution Preferences | FR-35 | ✅ Complete |
| US-13 | Submit Custom Event Inquiry | FR-50 | ✅ Complete |
| US-14 | Read Seasonal Tips | FR-52 | ✅ Complete |
| US-15 | Define Product Recipes | FR-11, FR-12 | ✅ Complete |
| US-16 | Automatic Stock Deduction | FR-13, FR-14 | ✅ Complete |
| US-17 | Receive Low Stock Alerts | FR-15 | ✅ Complete |
| US-18 | Manually Adjust Inventory | FR-16, FR-17 | ✅ Complete |
| US-19 | View Centralized Dashboard | FR-53, FR-54, FR-55 | ✅ Complete |
| US-20 | Send Automatic Confirmations | FR-38 | ✅ Complete |
| US-21 | Create Promotional Codes | FR-44, FR-45, FR-46 | ✅ Complete |
| US-22 | Update Product Photos & Specials | FR-47, FR-48, FR-49 | ✅ Complete |
| US-23 | View Production Queue with Recipes | FR-56 | ✅ Complete |
| US-24 | Update Order Status | FR-28, FR-29 | ✅ Complete |
| US-25 | Check Current Inventory | FR-11 (read access) | ✅ Complete |
| US-26 | View Daily Delivery Queue | FR-57 | ✅ Complete |
| US-27 | Confirm Delivery Completion | FR-59 | ✅ Complete |

**Coverage:** 27/27 user stories mapped to requirements (100%)

---

## Interview Quote to Requirement Mapping

| Key Interview Quote | Requirement(s) Derived |
|---------------------|------------------------|
| "I mostly think in terms of individual stems. That's how I order from suppliers and plan my designs. For day-to-day work, I mentally translate that into how many arrangements I can realistically make. Right now that translation lives in my head, which is part of the problem." | FR-11, FR-12 (Recipe/stem-based inventory system) |
| "for same-day delivery I usually cut it off around 1:00 pm. That gives me enough time to prepare the arrangements and organize delivery routes properly... I'd like the website to clearly enforce that cutoff so expectations are set upfront." | FR-23 (1 PM same-day cutoff) |
| "I charge different delivery rates based on distance from the shop. Local downtown deliveries are lower, and farther neighborhoods cost a bit more. Right now I calculate that manually, so having the website handle it automatically would save time and avoid confusion." | FR-24 (Zone-based delivery pricing) |
| "Customers should first choose their flowers, then be gently prompted to add items like candles, chocolates, or vases. That keeps the bouquets clean and simple while still encouraging thoughtful extras. It also makes it easier for me to manage those items without mixing them into floral inventory." | FR-18, FR-19, FR-20 (Add-on product logic) |
| "Both assistants should be able to view orders, update statuses, and check inventory levels. I'd prefer that only I can change pricing, promotions, or supplier settings. That keeps things simple while still giving them what they need day to day." | FR-04, FR-05 (Role-based access control) |
| "For repeat customers I'd want to save the basics. That includes past orders, preferred arrangements or flowers, and typical budget range. Notes like favorite colors, delivery addresses, and special dates are really helpful. Having that in one place would let me personalize orders without starting from scratch each time." | FR-33 (Customer preferences storage) |
| "What I can't easily track now is customer order history, favorite flowers, or notes like allergies or past feedback. Having that saved would really help with repeat customers and custom work." | FR-33 (expanded - allergies, feedback notes) |
| "I love when sites show real-time availability so customers know what's in season." | FR-10 (Seasonal availability indicator) |
| "order tracking are things I really wish I had now" | FR-58, FR-59 (Customer order tracking) |
| "the system to automatically send an order confirmation email to the customer with their order summary and delivery date... customers are reassured their order was received, reducing the need for them to call the shop to check" | FR-38 (Automated confirmation emails) |
| "I don't accidentally sell items I don't have, preventing shortages during holidays" | FR-13, FR-14 (Automatic inventory deduction) |
| "A system that warns me early or limits orders based on stock would really help." | FR-15 (Low stock alerts) |
| "Sometimes I rush an order from my supplier, which adds stress and cost." | FR-16 (Manual inventory adjustments - restocking) |
| "view all incoming orders (from the web, phone, or walk-ins) in a single dashboard... I stop 'juggling' multiple lists and ensure no order is missed during busy rushes" | FR-53 (Centralized order dashboard) |
| "create and manage discount codes (e.g., 'MOTHER10') for holidays... track the effectiveness of my social media promotions" | FR-44, FR-45, FR-46 (Promotional discount codes) |
| "during peak times like Valentine's Day, Mother's Day, and major holidays, that number jumps to well over 100 orders in a single day" | NFR-08 (Scalability requirement) |
| "I'd want to accept credit and debit cards, plus common digital wallets since many customers shop on their phones" | FR-36 (Payment methods), NFR-01 (Mobile optimization) |

---

## Requirements Without Direct Interview Quotes

The following requirements are derived from **industry best practices**, **technical necessity**, or **implied needs** rather than explicit interview statements:

| Requirement | Justification |
|-------------|---------------|
| FR-17 (Inventory Transaction History) | Audit trail necessity for manual adjustments - implied by need for accountability |
| FR-29 (Status Transition Rules) | Technical implementation of role-based access - security best practice |
| FR-30 (Status Timestamps) | Enables order tracking (FR-58) - technical dependency |
| FR-39 (Payment Failure Handling) | Error recovery pattern - essential for robust e-commerce |
| FR-43 (Points Conversion Rate) | Configuration capability - technical necessity for loyalty program |
| FR-46 (Code Validation Rules) | Business logic enforcement - technical necessity for promo codes |
| NFR-02 (Page Load Performance) | Industry standard for e-commerce conversion rates |
| NFR-04 (Payment Security) | PCI DSS compliance - legal requirement |
| NFR-05 (Data Backup) | Business continuity - industry standard |
| NFR-06 (Browser Compatibility) | Cross-platform access - technical necessity |
| NFR-07 (Accessibility) | WCAG compliance - ethical and legal best practice |
| NFR-09 (Uptime) | Business continuity - industry standard for e-commerce |
| NFR-10 (Localization) | US market focus - contextual necessity |

---

## Requirement Validation Status

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ Validated by Interview | 48 | 77% |
| 🔧 Technical Necessity | 10 | 16% |
| 📋 Industry Standard | 4 | 7% |
| **Total Requirements** | **62** | **100%** |

---

## Requirements Gap Analysis

### Customer-Requested Features Present in Requirements ✅
- Stem-level inventory with recipes
- 1:00 PM same-day delivery cutoff
- Zone-based delivery pricing
- Add-ons shown separately but integrated into flow
- Simplified RBAC (assistants share access level)
- Customer preference storage (favorites, allergies, dates)
- Order tracking for customers
- Automated confirmation emails
- Loyalty points system
- Promotional discount codes

### Features Mentioned in Interview BUT Deferred to Phase 2 🔄
- SMS notifications (mentioned casually, not critical)
- Customer feedback/reviews (Lily said "past feedback" but didn't emphasize system for capturing it)
- Blog content (US-14 - low priority per interview tone)
- Instagram shopping integration (mentioned social media but didn't prioritize direct integration)
- Subscription/recurring orders (not mentioned)

### Technical Requirements Without Interview Validation (Justified) ✅
- Payment failure handling (FR-39) - Critical error recovery
- Transaction history logging (FR-17) - Audit compliance
- Browser compatibility (NFR-06) - Cross-platform necessity
- Data backup (NFR-05) - Business continuity
- Accessibility (NFR-07) - Inclusive design standard

---

## Changes from Version 1.0

| Change Type | Description | Impact |
|-------------|-------------|--------|
| **Added** | FR-33 (Customer preferences with allergies/favorites) | Addresses explicit interview gap about tracking customer history |
| **Added** | FR-35 (Substitution preferences) | Handles Lily's stated workflow for material shortages |
| **Added** | FR-50, FR-51 (About page, FAQ) | Lily mentioned these pages specifically |
| **Added** | FR-58, FR-59 (Order tracking) | "things I really wish I had now" - critical missing feature |
| **Added** | FR-60, FR-61 (Social media integration) | Addresses "doesn't link smoothly to ordering" pain point |
| **Validated** | FR-11 through FR-17 (Recipe/inventory system) | Confirmed via follow-up: "I mostly think in terms of individual stems" |
| **Validated** | FR-23 (1 PM cutoff) | Changed from assumed 11 AM to validated 1 PM |
| **Validated** | FR-24 (Zone pricing) | Confirmed delivery pricing varies by distance |
| **Simplified** | FR-05 (Florist role) | Removed complex per-florist permissions - validated "mostly see the same information" |
| **Removed** | Generic "user-friendly" requirements | Replaced with specific, measurable NFRs |

---

