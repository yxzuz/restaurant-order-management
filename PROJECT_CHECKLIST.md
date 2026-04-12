# Restaurant Order Tracking Platform Checklist

## 1. Project Goal

Build a web-based restaurant order tracking and workflow management system that replaces paper-based ordering with a digital workflow for customers, staff, and restaurant owners.

## 2. Problem Summary

Current paper-based processes cause:

- Lost or misplaced orders
- Illegible handwriting
- Wrong or incomplete orders
- Slow communication between front-of-house and kitchen
- No reliable daily reporting

## 3. Project Objectives

- [x] Digitize restaurant order tracking
- [x] Reduce order errors and staff miscommunication
- [x] Show real-time order status
- [x] Support role-based system access
- [x] Provide daily sales and order analytics

## 4. Scope

### In Scope

- [x] User authentication
- [x] Role-based authorization
- [x] Menu management
- [x] Order placement
- [x] Order tracking
- [x] Order history
- [x] Daily sales and order analytics

### Out of Scope

- [ ] Online payment gateway
- [ ] Delivery tracking
- [ ] Multi-branch management
- [ ] Native mobile application

## 5. User Roles and Permissions

### Customer / Table Session

- [x] Browse menu
- [x] Scan QR code at the table
- [x] Place orders for the scanned table
- [x] View current table order status
- [x] Request cancellation only before kitchen starts preparation

### Staff

- [x] View incoming and active orders
- [x] Update order status (per-item)
- [ ] Filter and search active orders
- [x] Manage order workflow queue
- [x] Toggle menu item availability

### Owner

- [x] Full CRUD for menu items
- [x] View all orders
- [x] View reports and analytics (connected to backend)
- [x] Manage restaurant data and staff accounts

## 6. Core Features

- [x] Staff and owner authentication
- [x] QR-based table access
- [x] Table-based order placement
- [x] Order status tracking (per-item)
- [x] Staff order status updates
- [x] Owner menu management
- [x] Owner reporting dashboard (analytics with real data)

## 7. Suggested Order Status Flow

- [x] New
- [x] Preparing
- [x] Ready
- [x] Completed
- [x] Cancelled

Rules:

- [x] Customer can cancel only when status is `New` (per-item)
- [x] Staff can move order from `New` to `Preparing` (per-item)
- [x] Staff can move order from `Preparing` to `Ready` (per-item)
- [x] Staff can move order from `Ready` to `Completed` (per-item)
- [x] Cancelled items cannot be edited further
- [x] Cannot cancel items from paid orders

## 8. MVP Definition

Finish these first before adding advanced features:

- [x] Login system for staff and owner
- [x] User roles: staff, owner
- [x] QR-based customer ordering flow
- [x] Menu listing
- [x] Create order
- [x] View order status (real-time auto-refresh)
- [x] Staff updates order status (per-item)
- [x] Owner manages menu
- [x] Basic daily sales summary (comprehensive analytics)

## 9. Database Planning

### Main Entities

- [x] Users
- [x] Tables
- [x] Menu items
- [x] Orders
- [x] Order items

### Recommended Fields

#### Users

- [x] id
- [x] username
- [x] email
- [x] password_hash
- [x] role
- [x] created_at

#### Tables

- [x] id
- [x] number
- [x] qr_token
- [x] status

#### Menu Items

- [x] id
- [x] name
- [x] description
- [x] price
- [x] category
- [x] is_available
- [x] created_at
- [x] image_url (S3)

#### Orders

- [x] id
- [x] table_id
- [x] status
- [x] payment_status
- [x] total_amount
- [x] created_at
- [x] updated_at
- [x] closed_at

#### Order Items

- [x] id
- [x] order_id
- [x] menu_item_id
- [x] quantity
- [x] unit_price
- [x] subtotal
- [x] status (NEW/PREPARING/READY/COMPLETED per-item)

## 10. Backend Checklist

### Project Setup

- [x] Clean up `requirements.txt`
- [x] Add all missing dependencies
- [x] Configure `.env` support
- [x] Choose final database: SQLite (current)
- [ ] Replace SQLite if production DB is required for final delivery

### Architecture

- [x] Keep layered structure: routes, services, repositories, schemas, models
- [x] Separate business logic from API routes
- [x] Add dependency injection for DB session and auth

### Authentication

- [x] Create staff/owner registration or seed accounts
- [x] Create login endpoint
- [x] Hash passwords securely (bcrypt)
- [x] Generate JWT tokens (30-min expiration)
- [x] Protect routes by role (require_owner, require_staff_or_owner)
- [x] Auto-logout on token expiration

### Menu Module

- [x] Get all menu items
- [x] Get menu item by id
- [x] Create menu item (owner only)
- [x] Update menu item (owner full edit, staff availability toggle)
- [x] Delete menu item (owner only)
- [x] Restrict create/update/delete to owner
- [x] Image upload support (S3)

### Order Module

- [x] Pre-create tables `1..20`
- [x] Validate table exists before customer order access
- [x] Validate QR token before customer order access
- [x] Create or reuse active order for a table
- [x] Customer/table views active order (auto-refresh every 5s)
- [x] Customer/table cancels only `New` items (not paid orders)
- [x] Staff views active orders
- [x] Staff updates order status (per-item)
- [x] Owner views all orders
- [x] Per-item status tracking and advancement
- [x] Per-item cancellation (NEW items only)
- [x] Payment status tracking
- [x] Mark order as paid (requires ALL items COMPLETED)

### Validation and Rules

- [x] Validate order item quantities
- [x] Prevent ordering unavailable menu items
- [x] Calculate totals on the backend
- [x] Restrict invalid status transitions
- [x] Uppercase enum values (NEW/PREPARING/READY/COMPLETED)
- [x] Database migration for status column
- [x] Cannot cancel items from paid orders

### Reporting

- [x] Daily sales total
- [x] Orders count by day
- [x] Revenue by paid orders
- [x] Orders by status
- [x] Top-selling menu items
- [x] Revenue by category
- [x] Hourly order distribution

### Backend Quality

- [x] Add seed data for demo users and menu
- [x] Add API error handling
- [ ] Add logging
- [ ] Add unit tests for services
- [ ] Add API tests for routes

## 11. Frontend Checklist

### Project Setup

- [x] Define page structure
- [x] Set up router guards for auth and roles
- [x] Create API service layer
- [x] Add state management (localStorage for auth)

### Customer Pages

- [x] Menu page
- [x] QR landing route
- [x] Read table number and QR token from URL
- [x] Validate scanned table with backend
- [x] Cart / order form
- [x] Current table order page (auto-refresh)
- [x] Per-item status display
- [x] Item cancellation (NEW items only)

### Staff Pages

- [x] Staff login
- [x] Active orders dashboard
- [x] Order status update screen (per-item)
- [ ] Order filter/search UI
- [x] Menu availability toggle
- [x] Role-based sidebar (Orders, Menu only)

### Owner Pages

- [x] Owner dashboard
- [x] Menu management page (full CRUD)
- [x] Reports / analytics page (UI ready, needs data)
- [x] User management page (staff accounts)
- [x] Tables management page
- [x] Role-based sidebar (all features)

### Frontend Quality

- [x] Handle loading states
- [x] Handle empty states
- [x] Handle API errors clearly (401 auto-logout)
- [x] Keep role-based navigation clean
- [x] Make UI responsive for laptop and tablet
- [x] Token expiration handling
- [x] Role detection from route path

## 12. API Checklist

- [x] `POST /auth/register`
- [x] `POST /auth/login`
- [x] `GET /tables`
- [x] `GET /tables/{number}/active-order?qr_token=...`
- [x] `GET /menus`
- [x] `POST /menus` (owner only)
- [x] `PATCH /menus/{id}` (owner full, staff availability)
- [x] `DELETE /menus/{id}` (owner only)
- [x] `POST /orders`
- [x] `GET /orders` (all orders for owner/staff)
- [x] `PATCH /orders/{id}/payment`
- [x] `PATCH /orders/{id}/status`
- [x] `PATCH /orders/{order_id}/items/{item_id}/status` (per-item)
- [x] `DELETE /orders/{order_id}/items/{item_id}` (cancel item)
- [x] `GET /reports/daily-sales`
- [x] `GET /reports/top-items`
- [x] `GET /reports/analytics`

## 13. Suggested Milestones

### Milestone 1: Foundation

- [x] Finalize requirements
- [x] Finalize roles and permissions
- [x] Finalize DB schema
- [x] Set up backend and frontend environments

### Milestone 2: Authentication

- [x] Register/login flow works
- [x] JWT auth works (30-min expiration)
- [x] Route protection works
- [x] Auto-logout on token expiration

### Milestone 3: Menu Management

- [x] Owner can manage menu (full CRUD)
- [x] Staff can toggle menu availability
- [x] Customer can browse menu with descriptions
- [x] Image upload support (S3)

### Milestone 4: Order Workflow

- [x] Customer can enter through scanned QR link
- [x] Table can create order
- [x] Staff can view queue
- [x] Staff can update status (per-item)
- [x] Table can track status (auto-refresh 5s)
- [x] Staff can mark order as paid and free the table
- [x] Per-item status advancement
- [x] Per-item cancellation (NEW items only)
- [x] Payment validation (all items COMPLETED)

### Milestone 5: Reporting

- [x] Owner can view daily summary (UI ready)
- [x] Owner can view analytics (connected to real backend data)
- [x] Top selling items display
- [x] Revenue by category display

### Milestone 6: Finalization

- [ ] Test end-to-end workflow
- [ ] Fix bugs
- [ ] Improve UI
- [ ] Prepare final presentation/demo

## 14. Testing Checklist

- [x] Test staff login
- [x] Test owner login
- [x] Test unauthorized access is blocked
- [x] Test order creation
- [x] Test table active-order flow
- [x] Test cancel rule for `New` items only
- [x] Test staff status update flow (per-item)
- [x] Test payment closes order and frees table
- [x] Test menu CRUD permissions
- [ ] Test analytics endpoints
- [x] Test token expiration and auto-logout
- [x] Test role-based navigation
- [x] Test per-item cancellation (not paid orders)

## 15. Documentation Checklist

- [x] Update README run instructions
- [x] Add environment setup steps
- [ ] Document API endpoints
- [x] Document QR code table access flow
- [x] Document table-based customer flow
- [x] Document user roles and permissions
- [ ] Document database schema
- [ ] Add screenshots for final submission

## 16. Recommended Build Order

1. [x] Fix backend dependencies and startup
2. [x] Finalize database models
3. [x] Implement staff/owner authentication and roles
4. [x] Implement menu CRUD
5. [x] Implement QR-backed table model and active table order flow
6. [x] Implement order status and payment workflow
7. [x] Build frontend pages for each role
8. [ ] Add reporting and analytics
9. [ ] Add tests
10. [ ] Clean up README and prepare demo

## 17. Immediate Next Tasks For This Repo

- [x] Fix backend dependency issues in `requirements.txt`
- [x] Add missing auth module and JWT support
- [x] Verify current models match project scope
- [x] Add customer, staff, and owner role enforcement
- [x] Add QR route and scanned-table frontend flow
- [x] Add missing menu and order endpoints
- [ ] Add tests under `backend/tests`
- [x] Connect frontend pages to backend API
- [x] Update README with correct backend startup command

## 18. REMAINING TASKS

### High Priority

1. [x] **Analytics/Reporting Backend** - Implement `/reports/daily-sales` endpoint
   - Daily sales total
   - Orders count by day
   - Revenue by paid orders
   - Orders by status breakdown
   - Top-selling menu items

2. [x] **Connect Analytics Frontend** - Wire OwnerAnalytics.vue to real data
   - Replace mock data with API calls
   - Display sales charts
   - Show KPIs (revenue, orders, etc.)
   - Added top selling items section
   - Added revenue by category section

3. [ ] **Order Search/Filter** - Add filtering to staff/owner order views
   - Filter by status
   - Filter by date/time
   - Search by table number

### Medium Priority

4. [ ] **Logging** - Add structured logging throughout backend
   - Request/response logging
   - Error tracking
   - Performance monitoring

5. [ ] **Testing** - Add unit and integration tests
   - Service layer unit tests
   - API endpoint tests
   - Frontend component tests

6. [ ] **API Documentation** - Generate OpenAPI/Swagger docs
   - Document all endpoints
   - Include request/response examples
   - Authentication flow documentation

### Low Priority

7. [ ] **Database Migration** - Consider PostgreSQL for production
   - Current: SQLite (development)
   - Production: PostgreSQL/MySQL recommended

8. [ ] **Screenshots & Demo** - Prepare final presentation materials
   - Owner dashboard screenshots
   - Staff workflow screenshots
   - Customer ordering flow screenshots
   - Demo video/walkthrough
