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

- [ ] Digitize restaurant order tracking
- [ ] Reduce order errors and staff miscommunication
- [ ] Show real-time order status
- [ ] Support role-based system access
- [ ] Provide daily sales and order analytics

## 4. Scope

### In Scope

- [ ] User authentication
- [ ] Role-based authorization
- [ ] Menu management
- [ ] Order placement
- [ ] Order tracking
- [ ] Order history
- [ ] Daily sales and order analytics

### Out of Scope

- [ ] Online payment gateway
- [ ] Delivery tracking
- [ ] Multi-branch management
- [ ] Native mobile application

## 5. User Roles and Permissions

### Customer / Table Session

- [ ] Browse menu
- [ ] Scan QR code at the table
- [ ] Place orders for the scanned table
- [ ] View current table order status
- [ ] Request cancellation only before kitchen starts preparation

### Staff

- [ ] View incoming and active orders
- [ ] Update order status
- [ ] Filter and search active orders
- [ ] Manage order workflow queue

### Owner

- [ ] Full CRUD for menu items
- [ ] View all orders
- [ ] View reports and analytics
- [ ] Manage restaurant data and staff accounts

## 6. Core Features

- [ ] Staff and owner authentication
- [ ] QR-based table access
- [ ] Table-based order placement
- [ ] Order status tracking
- [ ] Staff order status updates
- [ ] Owner menu management
- [ ] Owner reporting dashboard

## 7. Suggested Order Status Flow

- [ ] New
- [ ] Preparing
- [ ] Ready
- [ ] Completed
- [ ] Cancelled

Rules:

- [ ] Customer can cancel only when status is `New`
- [ ] Staff can move order from `New` to `Preparing`
- [ ] Staff can move order from `Preparing` to `Ready`
- [ ] Staff can move order from `Ready` to `Completed`
- [ ] Cancelled orders cannot be edited further

## 8. MVP Definition

Finish these first before adding advanced features:

- [ ] Login system for staff and owner
- [ ] User roles: staff, owner
- [ ] QR-based customer ordering flow
- [ ] Menu listing
- [ ] Create order
- [ ] View order status
- [ ] Staff updates order status
- [ ] Owner manages menu
- [ ] Basic daily sales summary

## 9. Database Planning

### Main Entities

- [ ] Users
- [ ] Tables
- [ ] Menu items
- [ ] Orders
- [ ] Order items

### Recommended Fields

#### Users

- [ ] id
- [ ] username
- [ ] email
- [ ] password_hash
- [ ] role
- [ ] created_at

#### Tables

- [ ] id
- [ ] number
- [ ] qr_token
- [ ] status

#### Menu Items

- [ ] id
- [ ] name
- [ ] description
- [ ] price
- [ ] category
- [ ] is_available
- [ ] created_at

#### Orders

- [ ] id
- [ ] table_id
- [ ] status
- [ ] payment_status
- [ ] total_amount
- [ ] created_at
- [ ] updated_at

#### Order Items

- [ ] id
- [ ] order_id
- [ ] menu_item_id
- [ ] quantity
- [ ] unit_price
- [ ] subtotal

## 10. Backend Checklist

### Project Setup

- [ ] Clean up `requirements.txt`
- [ ] Add all missing dependencies
- [ ] Configure `.env` support
- [ ] Choose final database: PostgreSQL or MySQL
- [ ] Replace SQLite if production DB is required for final delivery

### Architecture

- [ ] Keep layered structure: routes, services, repositories, schemas, models
- [ ] Separate business logic from API routes
- [ ] Add dependency injection for DB session and auth

### Authentication

- [ ] Create staff/owner registration or seed accounts
- [ ] Create login endpoint
- [ ] Hash passwords securely
- [ ] Generate JWT tokens
- [ ] Protect routes by role

### Menu Module

- [ ] Get all menu items
- [ ] Get menu item by id
- [ ] Create menu item
- [ ] Update menu item
- [ ] Delete menu item
- [ ] Restrict create/update/delete to owner

### Order Module

- [ ] Pre-create tables `1..20`
- [ ] Validate table exists before customer order access
- [ ] Validate QR token before customer order access
- [ ] Create or reuse active order for a table
- [ ] Customer/table views active order
- [ ] Customer/table cancels only `New` orders
- [ ] Staff views active orders
- [ ] Staff updates order status
- [ ] Owner views all orders

### Validation and Rules

- [ ] Validate order item quantities
- [ ] Prevent ordering unavailable menu items
- [ ] Calculate totals on the backend
- [ ] Restrict invalid status transitions

### Reporting

- [ ] Daily sales total
- [ ] Orders count by day
- [ ] Revenue by paid orders
- [ ] Orders by status
- [ ] Top-selling menu items

### Backend Quality

- [ ] Add seed data for demo users and menu
- [ ] Add API error handling
- [ ] Add logging
- [ ] Add unit tests for services
- [ ] Add API tests for routes

## 11. Frontend Checklist

### Project Setup

- [ ] Define page structure
- [ ] Set up router guards for auth and roles
- [ ] Create API service layer
- [ ] Add state management if needed

### Customer Pages

- [ ] Menu page
- [ ] QR landing route
- [ ] Read table number and QR token from URL
- [ ] Validate scanned table with backend
- [ ] Cart / order form
- [ ] Current table order page

### Staff Pages

- [ ] Staff login
- [ ] Active orders dashboard
- [ ] Order status update screen
- [ ] Order filter/search UI

### Owner Pages

- [ ] Owner dashboard
- [ ] Menu management page
- [ ] Reports / analytics page
- [ ] User management page if included

### Frontend Quality

- [ ] Handle loading states
- [ ] Handle empty states
- [ ] Handle API errors clearly
- [ ] Keep role-based navigation clean
- [ ] Make UI responsive for laptop and tablet

## 12. API Checklist

- [ ] `POST /auth/register`
- [ ] `POST /auth/login`
- [ ] `GET /tables`
- [ ] `GET /tables/{number}/active-order?qr_token=...`
- [ ] `GET /menus`
- [ ] `POST /menus`
- [ ] `PUT /menus/{id}`
- [ ] `DELETE /menus/{id}`
- [ ] `POST /orders`
- [ ] `GET /orders/active`
- [ ] `PATCH /orders/{id}/payment`
- [ ] `PATCH /orders/{id}/status`
- [ ] `GET /reports/daily-sales`

## 13. Suggested Milestones

### Milestone 1: Foundation

- [ ] Finalize requirements
- [ ] Finalize roles and permissions
- [ ] Finalize DB schema
- [ ] Set up backend and frontend environments

### Milestone 2: Authentication

- [ ] Register/login flow works
- [ ] JWT auth works
- [ ] Route protection works

### Milestone 3: Menu Management

- [ ] Owner can manage menu
- [ ] Customer can browse menu

### Milestone 4: Order Workflow

- [ ] Customer can enter through scanned QR link
- [ ] Table can create order
- [ ] Staff can view queue
- [ ] Staff can update status
- [ ] Table can track status
- [ ] Staff can mark order as paid and free the table

### Milestone 5: Reporting

- [ ] Owner can view daily summary
- [ ] Owner can view analytics

### Milestone 6: Finalization

- [ ] Test end-to-end workflow
- [ ] Fix bugs
- [ ] Improve UI
- [ ] Prepare final presentation/demo

## 14. Testing Checklist

- [ ] Test staff login
- [ ] Test owner login
- [ ] Test unauthorized access is blocked
- [ ] Test order creation
- [ ] Test table active-order flow
- [ ] Test cancel rule for `New` orders only
- [ ] Test staff status update flow
- [ ] Test payment closes order and frees table
- [ ] Test menu CRUD permissions
- [ ] Test analytics endpoints

## 15. Documentation Checklist

- [ ] Update README run instructions
- [ ] Add environment setup steps
- [ ] Document API endpoints
- [ ] Document QR code table access flow
- [ ] Document table-based customer flow
- [ ] Document user roles and permissions
- [ ] Document database schema
- [ ] Add screenshots for final submission

## 16. Recommended Build Order

1. [ ] Fix backend dependencies and startup
2. [ ] Finalize database models
3. [ ] Implement staff/owner authentication and roles
4. [ ] Implement menu CRUD
5. [ ] Implement QR-backed table model and active table order flow
6. [ ] Implement order status and payment workflow
7. [ ] Build frontend pages for each role
8. [ ] Add reporting and analytics
9. [ ] Add tests
10. [ ] Clean up README and prepare demo

## 17. Immediate Next Tasks For This Repo

- [ ] Fix backend dependency issues in `requirements.txt`
- [ ] Add missing auth module and JWT support
- [ ] Verify current models match project scope
- [ ] Add customer, staff, and owner role enforcement
- [ ] Add QR route and scanned-table frontend flow
- [ ] Add missing menu and order endpoints
- [ ] Add tests under `backend/tests`
- [ ] Connect frontend pages to backend API
- [ ] Update README with correct backend startup command
