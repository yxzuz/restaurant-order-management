# Restaurant Order Management System

## Software Architecture Project Report

**Course:** Software Architecture  
**Submission Date:** April 16, 2026  
**Project Type:** From-Scratch Development

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Requirements](#2-system-requirements)
3. [Architecture Characteristics](#3-architecture-characteristics)
4. [Architecture Design](#4-architecture-design)
5. [Database Design](#5-database-design)
6. [Role & Permission Structure](#6-role--permission-structure)
7. [Implementation Details](#7-implementation-details)
8. [Conclusion](#8-conclusion)

---

## 1. Project Overview

### 1.1 Problem Statement

Many restaurants continue to rely on handwritten order slips to manage customer orders. This manual, paper-based approach leads to several operational challenges:

- **Lost or misplaced order tickets** causing delays and customer dissatisfaction
- **Miscommunication** between front-of-house staff and kitchen
- **Delayed order preparation** due to unclear handwriting or missing information
- **Lack of real-time visibility** into order status for both customers and staff
- **No structured sales data** for business analysis and decision-making
- **Inefficient resource allocation** without insights into peak hours or popular items

These issues directly impact customer satisfaction, operational efficiency, and the restaurant's ability to scale.

### 1.2 Solution

This project develops a comprehensive web-based order management system that digitizes the entire restaurant ordering workflow. The system replaces paper order slips with a modern, real-time digital solution accessible via QR codes for customers and role-based dashboards for staff and owners.

### 1.3 Key Objectives

1. **Digitize Order Tracking**
   - Eliminate paper-based order management
   - Provide real-time order status visibility
   - Enable independent tracking of each dish in an order

2. **Implement Role-Based Access Control**
   - Define clear responsibilities for each user type (Owner, Staff, Customer)
   - Enforce permission-based feature access
   - Secure sensitive operations (analytics, staff management)

3. **Improve Operational Transparency**
   - Real-time order status for customers
   - Kitchen workflow management for staff
   - Business intelligence for owners

4. **Enable Data-Driven Decision Making**
   - Track sales trends and patterns
   - Identify top-selling items
   - Analyze revenue by category and time

### 1.4 Key Features

#### Customer Features

- **QR Code Ordering**: Scan table QR code to access menu without login
- **Real-Time Updates**: Auto-refresh order status every 5 seconds
- **Item Cancellation**: Cancel items before kitchen starts preparation
- **Visual Feedback**: Color-coded status badges (NEW, PREPARING, READY, COMPLETED)

#### Staff Features

- **Order Management**: View and update all orders in real-time
- **Per-Item Status Control**: Advance each dish independently through workflow
- **Menu Availability Toggle**: Enable/disable menu items temporarily
- **Payment Processing**: Mark orders as paid after customer settles bill

#### Owner Features

- **Full Menu Management**: Create, edit, delete menu items with AWS S3 image upload
- **Staff Account Management**: Create and remove staff accounts
- **Table Management**: Configure tables and generate QR codes
- **Comprehensive Analytics**: Revenue tracking, top items, category performance, hourly distribution

---

## 2. System Requirements

### 2.1 Functional Requirements

#### FR-1: Multi-User Role System ✅

The system must support three distinct user roles:

**Customer Role:**

- Access menu via QR code without authentication
- Browse menu items with images and descriptions
- Add items to cart and place orders
- View real-time order status updates
- Cancel NEW items in UNPAID orders

**Staff Role:**

- Authenticate via username/password
- View all active and historical orders
- Update per-item status (NEW → PREPARING → READY → COMPLETED)
- Toggle menu item availability
- Mark orders as paid
- Cannot access analytics, staff management, or table management

**Owner Role:**

- Full CRUD operations on menu items
- Create and delete staff accounts
- Manage restaurant tables and QR codes
- Access comprehensive analytics dashboard
- All staff capabilities

#### FR-2: Database Operations (CRUD) ✅

Each user role must perform at least one CRUD operation:

**Owner:**

- Menu Items: CREATE, READ, UPDATE, DELETE
- Staff Accounts: CREATE, READ, DELETE
- Tables: CREATE, READ, DELETE
- Orders: READ, UPDATE

**Staff:**

- Orders: READ, UPDATE (item status, payment)
- Menu Items: READ, UPDATE (availability only)
- Order Items: DELETE (cancel NEW items)

**Customer:**

- Orders: CREATE, READ
- Order Items: CREATE, DELETE (cancel NEW items)

#### FR-3: Authentication & Authorization ✅

- Secure login/logout functionality
- JWT-based authentication with 30-minute expiration
- Password hashing using bcrypt
- Role-based route protection (frontend and backend)
- Automatic token expiration handling

#### FR-4: Order Workflow Management

- Per-item status tracking through defined lifecycle
- Status transitions: NEW → PREPARING → READY → COMPLETED
- Business rules:
  - Items can only progress forward (no backward transitions)
  - Items can be cancelled only if status is NEW and order is UNPAID
  - Payment requires ALL items to be COMPLETED
  - Each dish tracked independently

#### FR-5: Menu Management

- Full CRUD operations for menu items
- AWS S3 integration for image storage
- Category organization (appetizers, mains, desserts, beverages)
- Availability toggle for temporary item disabling
- Price management in Thai Baht (฿)

#### FR-6: Table & QR Code Management

- Pre-configured tables (1-20)
- Unique QR token for each table
- QR code generation for customer access
- Active order tracking per table
- Token validation on order creation

#### FR-7: Analytics & Reporting (Owner Only)

- Overall statistics (revenue, order count, average values)
- Daily sales summary (past 7 days)
- Top selling items by quantity and revenue
- Revenue breakdown by category
- Hourly distribution of orders
- Order status visualization

### 2.2 Non-Functional Requirements

#### NFR-1: Security

- JWT tokens with Bearer authentication scheme
- Bcrypt password hashing (cost factor 12)
- CORS configuration for cross-origin requests
- Role-based API endpoint protection
- Input validation and sanitization

#### NFR-2: Usability

- Responsive UI design (mobile and desktop)
- User-friendly error messages
- Real-time feedback (5-second auto-refresh)
- Intuitive status badges with color coding
- Clear navigation with role-based menus

#### NFR-3: Performance

- Lightweight SQLite database for development
- Efficient database queries with proper indexing
- Image storage offloaded to AWS S3
- Minimal page load times

#### NFR-4: Maintainability

- Layered architecture with clear separation
- Modular code organization
- Consistent naming conventions
- Comprehensive README documentation

#### NFR-5: Localization

- Thai timezone support (Asia/Bangkok, UTC+7)
- Thai Baht (฿) currency formatting
- Locale-aware date/time displays

### 2.3 User Stories

**As a Customer:**

- I want to scan a QR code to view the menu without creating an account
- I want to see real-time updates on my order status
- I want to cancel items before the kitchen starts preparing them
- I want to see which dishes are ready and which are still being prepared

**As a Staff Member:**

- I want to view all active orders in one place
- I want to update each dish's status independently
- I want to temporarily disable menu items that are out of stock
- I want to mark orders as paid when customers settle their bills

**As an Owner:**

- I want to add new menu items with photos
- I want to see analytics on top-selling items and revenue trends
- I want to create accounts for staff members
- I want to generate QR codes for new tables
- I want to control what staff members can access

---

## 3. Architecture Characteristics

### 3.1 Layered Architecture Pattern

The system implements a **classic layered architecture** with four distinct layers:

```
┌─────────────────────────────────────────────┐
│   Presentation Layer (API Routes)          │
│   - FastAPI endpoints                       │
│   - Request/response handling               │
│   - Input validation                        │
├─────────────────────────────────────────────┤
│   Business Logic Layer (Services)          │
│   - Order workflow management               │
│   - Authentication/authorization            │
│   - Business rule validation                │
├─────────────────────────────────────────────┤
│   Data Access Layer (Repositories)         │
│   - Database queries                        │
│   - Data transformation                     │
│   - Transaction management                  │
├─────────────────────────────────────────────┤
│   Domain Layer (Models)                    │
│   - SQLAlchemy ORM models                   │
│   - Database schema definition              │
│   - Entity relationships                    │
└─────────────────────────────────────────────┘
```

### 3.2 Architecture Benefits

#### Requirement-Driven Architecture Characteristics

The system’s architecture was selected and evolved based on concrete requirements (multi-role access, QR ordering, payment rules, analytics), and is best explained through the following architecture characteristics in priority order.

1. **Security (highest priority)**
    - **Requirement:** Protect staff credentials, payment records, and enforce strict tenant isolation between restaurants.
    - **How it is implemented:** JWT authentication (`Authorization: Bearer <token>`), bcrypt password hashing, role-based backend dependencies (`require_owner`, `require_staff_or_owner`), QR token validation for customer access, and **`restaurant_id` scoping** for data access so one restaurant cannot read or modify another restaurant’s data.
    - **Why it matters:** Without tenant isolation, an owner could view another restaurant’s revenue or orders.

2. **Modularity**
    - **Requirement:** Support ongoing feature growth (multi-tenant restaurants, analytics, QR customer flow) without rewriting unrelated code.
    - **How it is implemented:** Layering (Routes → Services → Repositories → Models) and domain-focused modules (`auth_service`, `order_service`, `menu_service`, `table_service`). This keeps HTTP concerns out of business rules and database queries.

3. **Maintainability**
    - **Requirement:** Keep the system understandable and change-friendly for an academic project under time constraints.
    - **How it is implemented:** Pydantic schemas validate at boundaries, consistent naming conventions for dependencies and routes, and small focused services. Changes (e.g., adding multi-tenancy or new menu fields like descriptions) have clear “homes” in the codebase.

4. **Testability**
    - **Requirement:** Validate business rules and security boundaries without manual testing.
    - **How it is implemented:** Business logic is centralized in services and repositories accept injected DB sessions, allowing tests to exercise rules like “payment requires all items completed” and “restaurant B cannot read restaurant A’s menu items” using FastAPI’s `TestClient`.

5. **Reliability**
    - **Requirement:** Prevent invalid state transitions and ensure consistent workflow behavior.
    - **How it is implemented:** Strict order and item status transition rules, payment gating (cannot mark PAID until all items are COMPLETED), and table state updates (table becomes AVAILABLE when an order is paid). These rules are enforced in the service layer.

6. **Scalability (moderate priority)**
    - **Requirement:** Support growth from a single restaurant to multiple restaurants with minimal redesign.
    - **How it is implemented:** Multi-tenant data model (`restaurant_id` foreign keys) supports many restaurants in one deployment; swapping SQLite→PostgreSQL is configuration-driven; and image storage is externalized to AWS S3.

#### Low Coupling

- **Interface-based communication:** Layers interact through well-defined interfaces
- **Dependency injection:** Database sessions passed as parameters, not global state
- **Service isolation:** Each service handles a single domain (auth, orders, menu, reports)
- **HTTP details abstracted:** Services don't know about FastAPI-specific concerns

**Example:**

```python
# Service doesn't know about HTTP
class OrderService:
    def __init__(self, db: Session):
        self.repository = OrderRepository(db)

    def create_order(self, order_data: CreateOrderSchema) -> Order:
        # Pure business logic
        ...

# Route uses service
@router.post("/orders")
def create_order_endpoint(
    payload: CreateOrderSchema,
    db: Session = Depends(get_db)
):
    service = OrderService(db)
    return service.create_order(payload)
```

#### High Cohesion

- **Single Responsibility:** Each module has one clear purpose
  - `auth_service.py`: Authentication and JWT management only
  - `order_service.py`: Order workflow and validation only
  - `report_service.py`: Analytics calculations only
- **Domain-based organization:** Files grouped by business domain, not technical layer
- **Focused classes:** Each service class handles operations for one entity type

#### Separation of Concerns

- **Routes:** Handle HTTP concerns (request parsing, response formatting)
- **Services:** Implement business rules and workflow logic
- **Repositories:** Perform database operations
- **Models:** Define data structure and relationships

#### Unidirectional Dependency Flow

```
Routes → Services → Repositories → Models
```

- **No circular dependencies:** Lower layers never import from higher layers
- **Clear flow:** Dependencies always point downward
- **Easy testing:** Can test each layer independently
- **Flexible replacement:** Can swap implementations within a layer

### 3.3 Scalability Considerations

#### Current Implementation (Development)

- SQLite database for simplicity
- Single-server deployment
- In-memory sessions

#### Production-Ready Upgrades

1. **Database:** Switch to PostgreSQL or MySQL for concurrent access
2. **Caching:** Add Redis for session storage and frequently accessed data
3. **Load Balancing:** Deploy multiple backend instances behind load balancer
4. **WebSocket:** Replace polling with WebSocket or SSE for real-time updates
5. **Microservices:** Split into separate services (Order Service, Menu Service, Analytics Service)

### 3.4 Security Architecture

#### Authentication Flow

1. User submits credentials → `/api/auth/login`
2. Backend validates against database (bcrypt check)
3. Generate JWT with role and user ID embedded
4. Return token to client (30-minute expiration)
5. Client stores in localStorage
6. All subsequent requests include `Authorization: Bearer <token>` header
7. Backend validates token on each request
8. Auto-logout on token expiration

#### Authorization Layers

- **Frontend Route Guards:** Prevent navigation to unauthorized pages
- **Backend Dependencies:** Validate JWT and check role before processing request
- **Service-Level Checks:** Additional business rule validation (e.g., staff can't delete menu items)

---

## 4. Architecture Design

### 4.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Browser    │  │   Browser    │  │   Browser    │     │
│  │  (Customer)  │  │   (Staff)    │  │   (Owner)    │     │
│  │  QR Access   │  │  Dashboard   │  │  Dashboard   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
                    HTTP/REST API (Axios)
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                  Frontend (Vue 3)                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Router (Route Guards)                               │    │
│  │  - Role-based navigation                             │    │
│  │  - Token validation                                  │    │
│  └──────────────────────┬───────────────────────────────┘    │
│                         │                                     │
│  ┌─────────────┬────────┴────────┬────────────────────┐     │
│  │   Views/    │   Components    │    Services        │     │
│  │   Pages     │   (Reusable)    │   (API Clients)    │     │
│  └─────────────┴─────────────────┴────────────────────┘     │
└───────────────────────────┬──────────────────────────────────┘
                            │
                    HTTP REST Requests
                            │
┌───────────────────────────┼──────────────────────────────────┐
│                  Backend (FastAPI)                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Middleware                                          │    │
│  │  - CORS                                              │    │
│  │  - Validation Error Handler                          │    │
│  └──────────────────────┬───────────────────────────────┘    │
│                         │                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  API Routes (Presentation Layer)                     │    │
│  │  /auth, /menus, /orders, /tables, /reports          │    │
│  └──────────────────────┬───────────────────────────────┘    │
│                         │                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Services (Business Logic Layer)                     │    │
│  │  - AuthService, MenuService, OrderService           │    │
│  │  - TableService, ReportService, S3Service           │    │
│  └──────────────────────┬───────────────────────────────┘    │
│                         │                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Repositories (Data Access Layer)                    │    │
│  │  - UserRepository, MenuItemRepository               │    │
│  │  - OrderRepository, TableRepository                 │    │
│  └──────────────────────┬───────────────────────────────┘    │
│                         │                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Models (Domain Layer)                               │    │
│  │  - User, MenuItem, Order, OrderItem, Table          │    │
│  └──────────────────────┬───────────────────────────────┘    │
└────────────────────────┼──────────────────────────────────────┘
                         │
            ┌────────────┴─────────────┐
            │                          │
    ┌───────▼────────┐      ┌─────────▼────────┐
    │   SQLite DB    │      │   AWS S3         │
    │   (Orders,     │      │   (Menu Item     │
    │    Users,      │      │    Images)       │
    │    Menus)      │      │                  │
    └────────────────┘      └──────────────────┘
```

### 4.2 Component Interaction Diagrams

#### Customer Ordering Sequence

```
Customer    Frontend      Backend       Database      S3
   │           │            │              │          │
   │  Scan QR  │            │              │          │
   ├──────────>│            │              │          │
   │           │ Validate   │              │          │
   │           │  Token     │              │          │
   │           ├───────────>│              │          │
   │           │            │ Query Table  │          │
   │           │            ├─────────────>│          │
   │           │            │<─────────────┤          │
   │           │<───────────┤              │          │
   │           │            │              │          │
   │  Browse   │            │              │          │
   │   Menu    │            │              │          │
   ├──────────>│ Get Menu   │              │          │
   │           ├───────────>│              │          │
   │           │            │ Query Items  │          │
   │           │            ├─────────────>│          │
   │           │            │<─────────────┤          │
   │           │<───────────┤              │          │
   │           │ Display    │              │          │
   │           │ with S3    │              │          │
   │           │ Images─────┼──────────────┼─────────>│
   │           │<───────────┼──────────────┼──────────┤
   │           │            │              │          │
   │  Place    │            │              │          │
   │  Order    │            │              │          │
   ├──────────>│ Create     │              │          │
   │           │  Order     │              │          │
   │           ├───────────>│              │          │
   │           │            │ Validate     │          │
   │           │            │ Business     │          │
   │           │            │ Rules        │          │
   │           │            │              │          │
   │           │            │ Insert Order │          │
   │           │            ├─────────────>│          │
   │           │            │<─────────────┤          │
   │           │<───────────┤              │          │
   │           │            │              │          │
   │  Auto     │            │              │          │
   │  Refresh  │            │              │          │
   │ (Every 5s)│            │              │          │
   ├──────────>│ Get Order  │              │          │
   │           ├───────────>│              │          │
   │           │            │ Query Order  │          │
   │           │            ├─────────────>│          │
   │           │            │<─────────────┤          │
   │           │<───────────┤              │          │
   │  Status   │            │              │          │
   │  Update   │            │              │          │
   │<──────────┤            │              │          │
```

#### Staff Order Management Sequence

```
Staff      Frontend      Backend       Database
  │           │            │              │
  │  Login    │            │              │
  ├──────────>│            │              │
  │           │ Auth       │              │
  │           ├───────────>│              │
  │           │            │ Verify       │
  │           │            │ Credentials  │
  │           │            ├─────────────>│
  │           │            │<─────────────┤
  │           │            │ Generate JWT │
  │           │<───────────┤              │
  │  JWT      │            │              │
  │<──────────┤            │              │
  │           │            │              │
  │  View     │            │              │
  │  Orders   │            │              │
  ├──────────>│ Get Orders │              │
  │           │ (with JWT) │              │
  │           ├───────────>│              │
  │           │            │ Verify Token │
  │           │            │ & Role       │
  │           │            │              │
  │           │            │ Query Orders │
  │           │            ├─────────────>│
  │           │            │<─────────────┤
  │           │<───────────┤              │
  │           │            │              │
  │  Update   │            │              │
  │  Item     │            │              │
  │  Status   │            │              │
  ├──────────>│ Update     │              │
  │           │  Status    │              │
  │           ├───────────>│              │
  │           │            │ Validate     │
  │           │            │ - Can progress?
  │           │            │ - Is paid?   │
  │           │            │              │
  │           │            │ Update DB    │
  │           │            ├─────────────>│
  │           │            │<─────────────┤
  │           │<───────────┤              │
  │  Success  │            │              │
  │<──────────┤            │              │
  │           │            │              │
  │  Mark     │            │              │
  │  Paid     │            │              │
  ├──────────>│ Update     │              │
  │           │  Payment   │              │
  │           ├───────────>│              │
  │           │            │ Validate     │
  │           │            │ - All items  │
  │           │            │   COMPLETED? │
  │           │            │              │
  │           │            │ Update DB    │
  │           │            ├─────────────>│
  │           │            │<─────────────┤
  │           │<───────────┤              │
  │  Success  │            │              │
  │<──────────┤            │              │
```

### 4.3 Data Flow Example: Per-Item Status Update

1. **Staff clicks "Start Preparing" on a dish**
2. Frontend sends PATCH `/api/orders/{order_id}/items/{item_id}/status`
3. Auth dependency validates JWT token and role (staff or owner)
4. OrderService validates business rules:
   - Order exists and is UNPAID
   - Item exists and belongs to the order
   - Current status is NEW (can transition to PREPARING)
5. OrderRepository updates order_item.status in database
6. Backend returns updated order
7. Frontend refreshes order display
8. Customer's auto-refresh (within 5 seconds) shows updated status

---

## 5. Database Design

### 5.1 Entity-Relationship Diagram

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │───┐
│ username        │   │
│ hashed_password │   │
│ role            │   │ (Owner who created staff)
│ created_by_id   │───┘
│ created_at      │
└─────────────────┘

┌─────────────────┐
│     tables      │
├─────────────────┤
│ id (PK)         │──────────────┐
│ number (UNIQUE) │              │
│ qr_token        │              │ (1)
│ created_at      │              │
└─────────────────┘              │
                                 │
                                 │
┌─────────────────┐              │
│   menu_items    │              │
├─────────────────┤              │
│ id (PK)         │───┐          │
│ name            │   │          │
│ description     │   │          │
│ price           │   │          │
│ category        │   │          │
│ image_url       │   │          │
│ is_available    │   │          │
│ created_at      │   │          │
│ updated_at      │   │          │
└─────────────────┘   │          │
                      │          │
                      │ (Many)   │
                      │          │
┌─────────────────┐   │          │
│     orders      │   │          │
├─────────────────┤   │          │
│ id (PK)         │───┼──┐       │
│ table_id (FK)   │───┘  │       │
│ table_number    │      │       │
│ payment_status  │      │ (1)   │
│ created_at      │      │       │
│ updated_at      │      │       │
└─────────────────┘      │       │
        │                │       │
        │ Has Many       │       │
        │                │       │
┌────────────────┐       │       │
│  order_items   │       │       │
├────────────────┤       │       │
│ id (PK)        │───────┘       │
│ order_id (FK)  │               │
│ menu_item_id   │───────────────┘
│ quantity       │
│ price          │
│ status         │ (NEW/PREPARING/READY/COMPLETED)
│ created_at     │
│ updated_at     │
└────────────────┘
```

### 5.2 Table Schemas

#### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL, -- 'owner' or 'staff'
    created_by_id INTEGER, -- FK to users(id) for staff accounts
    created_at TIMESTAMP DEFAULT (datetime('now', '+7 hours')),
    FOREIGN KEY (created_by_id) REFERENCES users(id)
);
```

#### Tables Table

```sql
CREATE TABLE tables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER UNIQUE NOT NULL,
    qr_token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT (datetime('now', '+7 hours'))
);
```

#### Menu Items Table

```sql
CREATE TABLE menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    image_url VARCHAR(500),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT (datetime('now', '+7 hours')),
    updated_at TIMESTAMP DEFAULT (datetime('now', '+7 hours'))
);
```

#### Orders Table

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_id INTEGER NOT NULL,
    table_number INTEGER NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'UNPAID', -- 'UNPAID' or 'PAID'
    created_at TIMESTAMP DEFAULT (datetime('now', '+7 hours')),
    updated_at TIMESTAMP DEFAULT (datetime('now', '+7 hours')),
    FOREIGN KEY (table_id) REFERENCES tables(id)
);
```

#### Order Items Table

```sql
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'NEW', -- 'NEW', 'PREPARING', 'READY', 'COMPLETED'
    created_at TIMESTAMP DEFAULT (datetime('now', '+7 hours')),
    updated_at TIMESTAMP DEFAULT (datetime('now', '+7 hours')),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);
```

### 5.3 Relationships

1. **Users → Users (Self-Referencing)**
   - Type: One-to-Many
   - Owner creates multiple staff accounts
   - `users.created_by_id` references `users.id`

2. **Tables → Orders**
   - Type: One-to-Many
   - One table can have multiple orders over time (but only one active order)
   - `orders.table_id` references `tables.id`

3. **Orders → Order Items**
   - Type: One-to-Many
   - One order contains multiple dishes
   - `order_items.order_id` references `orders.id`
   - CASCADE DELETE: Deleting an order deletes its items

4. **Menu Items → Order Items**
   - Type: One-to-Many
   - One menu item can appear in many orders
   - `order_items.menu_item_id` references `menu_items.id`

### 5.4 Indexes (for Performance)

```sql
-- Frequently queried columns
CREATE INDEX idx_orders_table_id ON orders(table_id);
CREATE INDEX idx_orders_payment_status ON orders(payment_status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_status ON order_items(status);
CREATE INDEX idx_menu_items_category ON menu_items(category);
CREATE INDEX idx_menu_items_is_available ON menu_items(is_available);
```

---

## 6. Role & Permission Structure

### 6.1 Role Definitions

#### Customer (QR Code User)

- **Access Method:** Scan QR code at table (no login required)
- **Identifier:** Temporary session associated with table QR token
- **Persistence:** None (no account creation)

#### Staff (Kitchen/Server)

- **Access Method:** Username/password login
- **Creation:** Created by Owner via Staff Management page
- **Identifier:** User account with role='staff'

#### Owner (Restaurant Manager)

- **Access Method:** Username/password login
- **Creation:** Bootstrap endpoint (one-time setup) or self-registration
- **Identifier:** User account with role='owner'

### 6.2 Permission Matrix

| Feature                            | Customer | Staff | Owner |
| ---------------------------------- | -------- | ----- | ----- |
| **Authentication**                 |
| Login/Logout                       | ❌       | ✅    | ✅    |
| Create Staff Account               | ❌       | ❌    | ✅    |
| Delete Staff Account               | ❌       | ❌    | ✅    |
| **Menu Operations**                |
| View Menu                          | ✅       | ✅    | ✅    |
| Create Menu Item                   | ❌       | ❌    | ✅    |
| Edit Menu Item (Full)              | ❌       | ❌    | ✅    |
| Edit Menu Item (Availability Only) | ❌       | ✅    | ✅    |
| Delete Menu Item                   | ❌       | ❌    | ✅    |
| Upload Menu Image                  | ❌       | ❌    | ✅    |
| **Order Operations**               |
| Create Order                       | ✅       | ❌    | ❌    |
| View Own Order                     | ✅       | ❌    | ❌    |
| View All Orders                    | ❌       | ✅    | ✅    |
| Update Item Status                 | ❌       | ✅    | ✅    |
| Cancel Item (NEW only)             | ✅       | ✅    | ✅    |
| Mark Order as Paid                 | ❌       | ✅    | ✅    |
| **Table Operations**               |
| View Table QR Code                 | ❌       | ❌    | ✅    |
| Create Table                       | ❌       | ❌    | ✅    |
| Delete Table                       | ❌       | ❌    | ✅    |
| **Analytics**                      |
| View Analytics Dashboard           | ❌       | ❌    | ✅    |
| Access Reports API                 | ❌       | ❌    | ✅    |

### 6.3 Access Control Implementation

#### Frontend (Vue Router Guards)

```javascript
router.beforeEach((to, from, next) => {
  const requiredRole = to.meta.requiredRole;
  const userRole = localStorage.getItem("user_role");

  if (requiredRole && userRole !== requiredRole) {
    // Redirect to home or show error
    next("/");
  } else {
    next();
  }
});
```

#### Backend (Dependency Functions)

```python
# auth.py
def require_owner(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    user = db.query(User).filter(User.id == payload['sub']).first()
    if user.role != 'owner':
        raise HTTPException(status_code=403, detail="Owner access required")
    return user

def require_staff_or_owner(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    user = db.query(User).filter(User.id == payload['sub']).first()
    if user.role not in ['owner', 'staff']:
        raise HTTPException(status_code=403, detail="Staff or owner access required")
    return user
```

#### Route Protection Examples

```python
# Owner-only endpoint
@router.post("/menus", dependencies=[Depends(require_owner)])
def create_menu_item(...):
    ...

# Staff or owner can access
@router.get("/orders", dependencies=[Depends(require_staff_or_owner)])
def get_orders(...):
    ...

# Public (customer) endpoint
@router.post("/orders")
def create_order(...):
    # No authentication required for customer orders
    ...
```

### 6.4 Business Rules Enforcement

#### Per-Item Cancellation Rules

```python
def cancel_order_item(order_id: int, item_id: int, db: Session) -> Order:
    order = get_order(order_id, db)
    item = get_order_item(item_id, db)

    # Business rule checks
    if order.payment_status == PaymentStatus.PAID:
        raise ValueError("Cannot cancel items from paid orders")

    if item.status != ItemStatus.NEW:
        raise ValueError("Can only cancel items with NEW status")

    if item.order_id != order_id:
        raise ValueError("Item does not belong to this order")

    # Safe to cancel
    db.delete(item)
    db.commit()
    return get_order(order_id, db)
```

#### Payment Validation Rules

```python
def mark_order_as_paid(order_id: int, db: Session) -> Order:
    order = get_order(order_id, db)

    # Business rule: All items must be COMPLETED
    incomplete_items = [
        item for item in order.items
        if item.status != ItemStatus.COMPLETED
    ]

    if incomplete_items:
        raise ValueError(
            f"Cannot mark as paid. {len(incomplete_items)} items not completed."
        )

    order.payment_status = PaymentStatus.PAID
    db.commit()
    return order
```

---

## 7. Implementation Details

### 7.1 Technology Stack Justification

#### Backend: FastAPI

**Chosen for:**

- Modern async Python framework
- Automatic OpenAPI documentation
- Built-in validation with Pydantic
- Easy dependency injection
- Excellent performance

**Alternatives considered:**

- Django: Too heavyweight for this project
- Flask: Less built-in features, more boilerplate

#### Frontend: Vue 3 (Composition API)

**Chosen for:**

- Reactive and component-based
- Composition API provides better code organization
- Excellent developer experience
- Lightweight compared to Angular

**Alternatives considered:**

- React: More verbose, JSX syntax
- Angular: Overkill for this scale

#### Database: SQLite

**Chosen for:**

- Zero configuration for development
- File-based (easy to reset and demo)
- Sufficient for prototype/MVP
- Easy migration path to PostgreSQL

**Production alternative:** PostgreSQL for concurrent access

#### Authentication: JWT

**Chosen for:**

- Stateless authentication
- Works well with RESTful APIs
- Frontend can store and manage tokens
- Includes expiration handling

**Alternatives considered:**

- Session-based: Requires server-side storage
- OAuth: Overkill for internal system

#### Image Storage: AWS S3

**Chosen for:**

- Scalable and reliable
- Offloads storage from application server
- Industry-standard solution
- CDN integration available

**Alternatives considered:**

- Local filesystem: Not scalable
- Database BLOBs: Poor performance

### 7.2 Key Algorithms and Business Logic

#### Per-Item Status Progression Algorithm

```python
def update_item_status(order_id: int, item_id: int, new_status: ItemStatus) -> OrderItem:
    # State machine validation
    ALLOWED_TRANSITIONS = {
        ItemStatus.NEW: [ItemStatus.PREPARING],
        ItemStatus.PREPARING: [ItemStatus.READY],
        ItemStatus.READY: [ItemStatus.COMPLETED],
        ItemStatus.COMPLETED: []  # Terminal state
    }

    item = get_order_item(item_id)
    current_status = item.status

    # Validate transition
    if new_status not in ALLOWED_TRANSITIONS[current_status]:
        raise ValueError(f"Cannot transition from {current_status} to {new_status}")

    # Validate order not paid
    order = get_order(order_id)
    if order.payment_status == PaymentStatus.PAID:
        raise ValueError("Cannot update items in paid order")

    # Apply transition
    item.status = new_status
    item.updated_at = now_thai()
    db.commit()
    return item
```

#### Analytics Calculations

```python
def get_top_selling_items(db: Session, limit: int = 10):
    # Aggregate order items grouped by menu item
    results = (
        db.query(
            MenuItem.name,
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue')
        )
        .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(Order.payment_status == PaymentStatus.PAID)  # Only paid orders
        .group_by(MenuItem.id, MenuItem.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            'name': r.name,
            'quantity_sold': int(r.total_quantity),
            'revenue': float(r.total_revenue)
        }
        for r in results
    ]
```

### 7.3 Security Measures

#### Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

#### JWT Token Generation

```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

#### Input Validation

```python
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=4, max_length=72)

# FastAPI automatically validates and returns user-friendly errors
```

#### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 7.4 Error Handling

#### User-Friendly Validation Errors

```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        field = error['loc'][-1]
        if error['type'] == 'string_too_short':
            min_length = error['ctx']['min_length']
            errors.append(f"{field.capitalize()} must be at least {min_length} characters long")

    return JSONResponse(
        status_code=400,
        content={
            "detail": "Validation error",
            "errors": errors,
            "message": " | ".join(errors)
        }
    )
```

#### Frontend Error Display

```javascript
try {
  await api.post("/auth/login", payload);
} catch (error) {
  const validationMessage = error?.response?.data?.message;
  const detail = error?.response?.data?.detail;

  if (validationMessage) {
    errorMessage.value = validationMessage;
  } else if (status === 401) {
    errorMessage.value = "Invalid username or password.";
  } else {
    errorMessage.value = detail || "Request failed. Please try again.";
  }
}
```

### 7.5 Thai Localization Implementation

#### Timezone Utilities

```python
from datetime import datetime, timezone, timedelta

THAI_TZ = timezone(timedelta(hours=7))

def now_thai() -> datetime:
    """Get current datetime in Thai timezone"""
    return datetime.now(THAI_TZ)

def utc_to_thai(dt: datetime) -> datetime:
    """Convert UTC datetime to Thai timezone"""
    return dt.replace(tzinfo=timezone.utc).astimezone(THAI_TZ)
```

#### Currency Formatting

```javascript
function formatCurrency(value) {
  return new Intl.NumberFormat("th-TH", {
    style: "currency",
    currency: "THB",
  }).format(value);
}

// Example output: ฿350.00
```

### 7.6 Real-Time Updates Implementation

#### Frontend Auto-Refresh

```javascript
let refreshInterval = null;

onMounted(() => {
  fetchOrder();
  refreshInterval = setInterval(fetchOrder, 5000); // Refresh every 5 seconds
});

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval);
  }
});
```

#### Optimistic Future Upgrade: WebSocket

```python
# Future implementation with WebSocket
from fastapi import WebSocket

@app.websocket("/ws/orders/{order_id}")
async def websocket_endpoint(websocket: WebSocket, order_id: int):
    await websocket.accept()
    while True:
        # Push updates when order changes
        order = get_order(order_id)
        await websocket.send_json(order.dict())
```

---

## 8. Conclusion

### 8.1 Project Summary

This Restaurant Order Management System successfully addresses the inefficiencies of paper-based order tracking by providing a comprehensive digital solution. The system implements a clear **layered architecture** with three distinct user roles (Customer, Staff, Owner), each with appropriate permissions and responsibilities.

Key achievements include:

- **Per-item status tracking** enabling independent dish lifecycle management
- **QR code-based ordering** for frictionless customer experience
- **Real-time order updates** for immediate feedback to customers
- **Comprehensive analytics** for data-driven business decisions
- **Role-based access control** ensuring security and appropriate feature access

### 8.2 Architecture Strengths

1. **Layered Architecture**: Clear separation between Presentation, Business Logic, Data Access, and Domain layers
2. **Low Coupling**: Services don't depend on HTTP details; layers communicate through interfaces
3. **High Cohesion**: Each service handles a single domain with focused responsibilities
4. **Unidirectional Dependencies**: Clean dependency flow prevents circular references
5. **Scalability**: Architecture supports future upgrades (PostgreSQL, WebSocket, microservices)

### 8.3 Learning Outcomes

Through this project, I gained practical experience in:

- Designing and implementing layered architecture patterns
- Building RESTful APIs with FastAPI
- Creating reactive frontends with Vue 3 Composition API
- Implementing JWT-based authentication and authorization
- Designing normalized database schemas with proper relationships
- Applying business rules and validation logic
- Integrating third-party services (AWS S3)
- Localizing applications for specific markets (Thai timezone/currency)

### 8.4 Future Enhancements

While the current MVP is fully functional, potential improvements include:

1. **WebSocket/SSE** for real-time updates instead of polling
2. **Unit and integration tests** for code reliability
3. **PostgreSQL migration** for production deployment
4. **Order filtering and search** for better order management
5. **Print integration** for kitchen receipt printing
6. **Inventory tracking** to manage stock levels
7. **Multi-language support** (English and Thai)
8. **Mobile applications** for better mobile experience

### 8.5 Reflection

This project demonstrates how thoughtful architecture design can create maintainable, scalable systems that solve real-world problems. The layered architecture pattern proved effective for organizing code, enabling independent development of each layer, and providing clear upgrade paths for future enhancements.

The system successfully meets all functional requirements while maintaining clean code structure and following software engineering best practices.

---

**End of Report**
