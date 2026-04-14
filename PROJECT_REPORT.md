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

**Multi-tenant requirement (Restaurants):**

- Each owner account is associated with exactly one restaurant.
- Staff accounts are created under (and restricted to) the owner’s restaurant.
- All restaurant data (menu items, tables, orders, reports) is scoped by `restaurant_id` to ensure tenant isolation.

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
- JWT-based authentication with configurable expiration (default: 30 minutes)
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

Non-functional requirements represent stakeholder needs and constraints that define **how** the system should perform, rather than **what** it should do. These requirements drive the selection of architecture characteristics and technical design decisions.

#### NFR-1: Security & Data Isolation

**Stakeholder requirement:**

- The system must protect sensitive data (credentials, payment records, revenue analytics)
- One restaurant's data must never be accessible to another restaurant
- Staff members must not access owner-only features
- Customer ordering must work without exposing personal data

**Measurable criteria:**

- All passwords must be encrypted at rest
- Authentication tokens must expire within a reasonable timeframe
- Cross-restaurant data access must be prevented at database level
- Authorization checks must occur on every protected endpoint

#### NFR-2: Usability

**Stakeholder requirement:**

- Customers must be able to order without technical knowledge or account creation
- Staff must process orders quickly during peak hours
- System must provide clear visual feedback on order status
- Interfaces must work on both desktop computers and mobile devices

**Measurable criteria:**

- QR code scan → menu view requires ≤ 2 clicks
- Order status updates visible within 5 seconds of change
- Mobile screens must render without horizontal scrolling
- Error messages must be actionable (not technical jargon)

#### NFR-3: Performance

**Stakeholder requirement:**

- System must handle typical restaurant workload (20 tables, concurrent ordering)
- Menu browsing and order status checks must feel instantaneous
- Reports must load without noticeable delay for typical date ranges

**Measurable criteria:**

- Page load time acceptable for Wi-Fi conditions
- Database queries complete within reasonable time for dataset size
- Image loading does not block menu browsing

#### NFR-4: Maintainability & Evolvability

**Stakeholder requirement:**

- Code must be understandable for academic assessment and future maintenance
- Adding new features (reports, menu fields) should not require rewriting unrelated code
- System structure must be evident from file organization

**Measurable criteria:**

- New developers can locate feature code within minutes
- Adding a new endpoint touches ≤ 3 layers (route, service, repository)
- Automated tests prevent regression when making changes

#### NFR-5: Localization

**Stakeholder requirement:**

- System must support Thai restaurant operations (timezone, currency)
- Times must reflect Bangkok local time, not server time
- Prices must display in Thai Baht

**Measurable criteria:**

- All timestamps use Asia/Bangkok timezone (UTC+7)
- Currency formatted as THB
- Date/time displays match Thai business expectations

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
   - **How it is implemented:** Multi-tenant data model (`restaurant_id` foreign keys) supports many restaurants in one deployment; database configuration is environment-driven (`DATABASE_URL`) with PostgreSQL as the primary database; and image storage is externalized to AWS S3.

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
    - `report_service.py`: Analytics orchestration and response shaping
    - `report_repository.py`: Analytics query composition
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

### 3.3 NFR to Architecture Characteristic Mapping

This section demonstrates how **non-functional requirements** (stakeholder needs) drove the selection and implementation of **architecture characteristics** (technical design qualities).

| Non-Functional Requirement                | Architecture Characteristics             | Implementation Evidence                                                                                                                                                                        |
| ----------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **NFR-1: Security & Data Isolation**      | Security, Testability                    | JWT Bearer authentication, bcrypt password hashing, `restaurant_id` scoping in all queries, role-based dependencies (`require_owner`), architecture fitness tests for authorization boundaries |
| **NFR-2: Usability**                      | Simplicity, Responsiveness               | QR-based customer access (no registration), 5-second auto-refresh, mobile-responsive Tailwind layout, color-coded status badges, user-friendly validation messages                             |
| **NFR-3: Performance**                    | Efficiency, Scalability                  | PostgreSQL with indexes on foreign keys, S3 for image offloading, repository-based query composition, multi-tenant support without N+1 queries                                                 |
| **NFR-4: Maintainability & Evolvability** | Modularity, Testability, Maintainability | Layered architecture (routes/services/repositories/models), single-responsibility services, dependency injection, 34 automated backend tests, architecture fitness checks                      |
| **NFR-5: Localization**                   | Configurability                          | Timezone utilities (`THAI_TZ`), currency formatters (THB), environment-driven config, `now_thai()` helper functions                                                                            |

**Key insight:** Architecture characteristics are not arbitrary—they are **trade-off decisions** made to satisfy specific requirements. For example:

- **Security vs. Usability:** Customers can order without authentication (usability), but this required QR token validation and table-scoped access controls (security).
- **Modularity vs. Simplicity:** Layered architecture adds abstraction overhead but enables independent testing and feature additions without cross-contamination.
- **Performance vs. Maintainability:** Externalizing images to S3 improves performance but adds operational complexity.

### 3.4 Scalability Considerations

#### Current Implementation (Development)

- PostgreSQL database for realistic multi-tenant behavior
- Single-server deployment
- In-memory sessions

#### Production-Ready Upgrades

1. **Database:** Switch to PostgreSQL or MySQL for concurrent access
2. **Caching:** Add Redis for session storage and frequently accessed data
3. **Load Balancing:** Deploy multiple backend instances behind load balancer
4. **WebSocket:** Replace polling with WebSocket or SSE for real-time updates
5. **Microservices:** Split into separate services (Order Service, Menu Service, Analytics Service)

### 3.5 Security Architecture

#### Authentication Flow

1. User submits credentials → `/api/auth/login`
2. Backend validates against database (bcrypt check)
3. Generate JWT with role and user ID embedded
4. Return token to client (expiration controlled by configuration)
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
│  │  - ReportRepository                                 │    │
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
    │ PostgreSQL DB  │      │   AWS S3         │
    │   (Orders,     │      │   (Menu Item     │
    │    Users,      │      │    Images)       │
    │    Menus)      │      │                  │
    └────────────────┘      └──────────────────┘
```

### 4.2 High-Level Architecture Overview

The system follows a **client-server architecture** with a clear **layered architecture pattern** on the backend. This structure separates concerns across multiple tiers to achieve modularity, maintainability, and scalability.

**Overall Structure:**

- **Client Tier (Frontend):** Single-page application (SPA) built with Vue 3 that runs entirely in the user's browser. The frontend communicates with the backend exclusively through HTTP REST APIs. Three distinct user interfaces are provided: QR-based customer ordering (no authentication), staff dashboard (order management), and owner dashboard (full administrative control including analytics).

- **Server Tier (Backend):** FastAPI-based REST API server implementing a strict **four-layer architecture**:
  - **Presentation Layer (Routes):** HTTP endpoints that handle request/response formatting and input validation
  - **Business Logic Layer (Services):** Domain-specific workflow orchestration, business rule enforcement, and multi-repository coordination
  - **Data Access Layer (Repositories):** Database query composition and transaction management
  - **Domain Layer (Models):** SQLAlchemy ORM entities defining database schema and relationships

- **Data Tier:** PostgreSQL relational database providing persistent storage with multi-tenant isolation via `restaurant_id` scoping. AWS S3 serves as external object storage for menu item images, offloading binary data from the primary database.

- **Integration Tier:** RESTful HTTP communication between frontend and backend using JSON payloads. JWT tokens (stored in browser localStorage) authenticate and authorize requests. The frontend polls backend endpoints every 5 seconds for real-time order status updates.

**Architectural Style:** The backend implements a **closed layered architecture** where each layer communicates only with the layer directly below it (Routes → Services → Repositories → Models). This unidirectional dependency flow prevents layer-skipping and ensures business logic remains centralized in the service layer rather than being scattered across routes or repositories. Architecture fitness tests enforce these boundaries automatically.

**Multi-Tenancy:** The system is designed as a multi-tenant application where multiple restaurants share the same application instance and database. Data isolation is enforced at the database level through `restaurant_id` foreign keys on all tenant-scoped entities (users, tables, menu items, orders). Each restaurant's data remains completely isolated from other restaurants.

---

### 4.3 Components and Responsibilities

This section documents the major components/modules in each architectural layer, their roles, and interfaces.

#### 4.3.1 Presentation Layer (API Routes)

**Name:** `auth.py` (Authentication Routes)

**Description:** Handles user authentication endpoints for login and logout operations.

**Inputs/Outputs:**

- Input: Login credentials (username, password) via POST request body
- Output: JWT access token and user profile (role, username, restaurant_id)

**Interfaces/APIs:**

- `POST /api/auth/login` - Authenticate user and return JWT token
- `POST /api/auth/logout` - Client-side logout (token invalidation)

---

**Name:** `menus.py` (Menu Routes)

**Description:** Exposes HTTP endpoints for menu item management including CRUD operations and image uploads.

**Inputs/Outputs:**

- Input: Menu item data (name, price, category, image file), JWT token for authentication
- Output: Menu item objects with image URLs, category lists

**Interfaces/APIs:**

- `GET /api/menus/` - List all menu items for authenticated user's restaurant
- `GET /api/menus/{item_id}` - Get single menu item details
- `POST /api/menus/` - Create new menu item with optional image upload (owner only)
- `PATCH /api/menus/{item_id}` - Update menu item (owner for full update, staff for availability toggle)
- `DELETE /api/menus/{item_id}` - Delete menu item (owner only)
- `GET /api/menus/categories` - List available menu categories

---

**Name:** `orders.py` (Order Routes)

**Description:** Provides endpoints for order lifecycle management including creation, status updates, and item management.

**Inputs/Outputs:**

- Input: Order data (table number, QR token, items), status updates, JWT token
- Output: Order objects with items, statuses, and timestamps

**Interfaces/APIs:**

- `GET /api/orders/` - List all orders (staff/owner) or active order (customer via QR)
- `GET /api/orders/{order_id}` - Get specific order details
- `POST /api/orders/` - Create new order (customer via QR)
- `PATCH /api/orders/{order_id}/payment-status` - Update payment status (staff/owner)
- `PATCH /api/orders/{order_id}/items/{item_id}/status` - Update individual item status (staff/owner)
- `DELETE /api/orders/{order_id}/items/{item_id}` - Cancel order item (if NEW status and UNPAID)

---

**Name:** `tables.py` (Table Routes)

**Description:** Manages restaurant tables and QR code generation for customer access.

**Inputs/Outputs:**

- Input: Table numbers, QR tokens, JWT token
- Output: Table objects with QR tokens and status information

**Interfaces/APIs:**

- `GET /api/tables/` - List all tables for restaurant (owner only)
- `GET /api/tables/{table_id}` - Get specific table details
- `POST /api/tables/` - Create new table with QR token (owner only)
- `DELETE /api/tables/{table_id}` - Delete table (owner only)

---

**Name:** `reports.py` (Analytics Routes)

**Description:** Exposes analytics and reporting endpoints for business intelligence.

**Inputs/Outputs:**

- Input: Date ranges, restaurant_id from JWT
- Output: Aggregated analytics data (revenue, sales trends, top items, time distributions)

**Interfaces/APIs:**

- `GET /api/reports/overall` - Overall statistics (total revenue, order count, averages)
- `GET /api/reports/daily-sales` - Daily sales summary for date range
- `GET /api/reports/top-items` - Top selling items by quantity or revenue
- `GET /api/reports/category-revenue` - Revenue breakdown by menu category
- `GET /api/reports/hourly-distribution` - Order distribution by hour of day

---

#### 4.3.2 Business Logic Layer (Services)

**Name:** `auth_service.py` (AuthService)

**Description:** Handles authentication logic including password verification, JWT token generation, and user validation.

**Inputs/Outputs:**

- Input: Username, password, database session
- Output: JWT token string, user object

**Interfaces/APIs:**

- `authenticate(username, password) -> dict` - Verify credentials and generate token
- `create_access_token(data, expires_delta) -> str` - Generate JWT token
- `verify_password(plain, hashed) -> bool` - Compare passwords using bcrypt

---

**Name:** `menu_service.py` (MenuService)

**Description:** Orchestrates menu item operations including image upload to S3 and menu item lifecycle management.

**Inputs/Outputs:**

- Input: Menu item data, image files, restaurant_id
- Output: MenuItem objects with resolved S3 image URLs

**Interfaces/APIs:**

- `list_menu_items(restaurant_id) -> list[MenuItem]` - Get all menu items
- `get_menu_item(item_id) -> MenuItem` - Get single item
- `create_menu_item(name, price, category, ...) -> MenuItem` - Create new item
- `update_menu_item(item_id, **changes) -> MenuItem` - Update existing item
- `delete_menu_item(item_id) -> bool` - Delete item
- `upload_menu_image(image, restaurant_id) -> str` - Upload image to S3
- `list_categories() -> list[MenuCategory]` - Get available categories

---

**Name:** `order_service.py` (OrderService)

**Description:** Implements order workflow business rules including status transitions, payment validation, and multi-repository coordination.

**Inputs/Outputs:**

- Input: Order data, QR tokens, status transitions, restaurant_id
- Output: Order objects with items and validation results

**Interfaces/APIs:**

- `list_orders(restaurant_id) -> list[Order]` - Get all orders
- `list_active_orders(restaurant_id) -> list[Order]` - Get active orders only
- `create_order(order_data) -> Order` - Create order with QR validation
- `get_order(order_id) -> Order` - Get specific order
- `get_active_order_for_table(table_number, qr_token) -> Order` - QR-based order lookup
- `update_order_status(order_id, new_status) -> Order` - Validate and update order status
- `update_payment_status(order_id, payment_status) -> Order` - Process payment with completion checks
- `update_order_item_status(order_id, item_id, new_status) -> Order` - Update individual item status
- `cancel_order_item(order_id, item_id) -> Order` - Cancel item if eligible

---

**Name:** `table_service.py` (TableService)

**Description:** Manages table operations and QR token generation for customer access.

**Inputs/Outputs:**

- Input: Table numbers, restaurant_id
- Output: Table objects with QR tokens

**Interfaces/APIs:**

- `list_tables(restaurant_id) -> list[Table]` - Get all tables
- `get_table(table_id) -> Table` - Get specific table
- `create_table(number, restaurant_id) -> Table` - Create table with unique QR token
- `delete_table(table_id) -> bool` - Delete table if no active orders

---

**Name:** `report_service.py` (ReportService)

**Description:** Orchestrates analytics queries and formats reporting data for API responses.

**Inputs/Outputs:**

- Input: Restaurant_id, date ranges
- Output: Formatted analytics dictionaries

**Interfaces/APIs:**

- `get_overall_stats(restaurant_id) -> dict` - Calculate overall metrics
- `get_daily_sales(restaurant_id, days) -> list[dict]` - Daily sales trend
- `get_top_items(restaurant_id, limit) -> list[dict]` - Top selling items
- `get_category_revenue(restaurant_id) -> list[dict]` - Revenue by category
- `get_hourly_distribution(restaurant_id) -> list[dict]` - Orders by hour

---

**Name:** `s3_service.py` (S3Service)

**Description:** Handles AWS S3 interactions for menu item image uploads and URL generation.

**Inputs/Outputs:**

- Input: File streams, object keys, bucket configuration
- Output: Public S3 URLs for uploaded images

**Interfaces/APIs:**

- `upload_file(file_stream, filename, content_type) -> str` - Upload to S3
- `get_presigned_url(object_key, expiration) -> str` - Generate temporary access URL

---

#### 4.3.3 Data Access Layer (Repositories)

**Name:** `user_repository.py` (UserRepository)

**Description:** Encapsulates all database queries related to user management.

**Inputs/Outputs:**

- Input: Database session, user data, filters
- Output: User model instances

**Interfaces/APIs:**

- `get_by_username(username) -> User` - Find user by username
- `get_by_id(user_id) -> User` - Find user by ID
- `create(username, hashed_password, role, ...) -> User` - Create new user
- `delete(user_id) -> bool` - Delete user account

---

**Name:** `menu_item_repository.py` (MenuItemRepository)

**Description:** Manages database operations for menu items.

**Inputs/Outputs:**

- Input: Database session, menu item data, restaurant_id
- Output: MenuItem model instances

**Interfaces/APIs:**

- `list_all(restaurant_id) -> list[MenuItem]` - Get all items for restaurant
- `get_by_id(item_id) -> MenuItem` - Get specific item
- `create(name, price, category, ...) -> MenuItem` - Insert new item
- `update(item_id, **changes) -> MenuItem` - Update existing item
- `delete(item_id) -> bool` - Delete item

---

**Name:** `order_repository.py` (OrderRepository)

**Description:** Handles all order and order item database operations.

**Inputs/Outputs:**

- Input: Database session, order data, filters, status updates
- Output: Order and OrderItem model instances

**Interfaces/APIs:**

- `list_all(restaurant_id) -> list[Order]` - Get all orders
- `list_active(restaurant_id) -> list[Order]` - Get active (unpaid) orders
- `get_by_id(order_id) -> Order` - Get specific order
- `get_active_by_table_id(table_id) -> Order` - Find active order for table
- `create_order(table_id, restaurant_id) -> Order` - Create new order
- `add_item(order_id, menu_item_id, quantity, unit_price) -> OrderItem` - Add item to order
- `get_order_item(order_id, item_id) -> OrderItem` - Get specific order item
- `update_status(order, new_status) -> Order` - Update order status
- `update_payment_status(order, payment_status) -> Order` - Update payment status
- `update_item_status(item, new_status) -> OrderItem` - Update item status
- `delete_item(item) -> bool` - Delete order item

---

**Name:** `table_repository.py` (TableRepository)

**Description:** Manages database queries for restaurant tables.

**Inputs/Outputs:**

- Input: Database session, table data, restaurant_id
- Output: Table model instances

**Interfaces/APIs:**

- `list_all(restaurant_id) -> list[Table]` - Get all tables
- `get_by_id(table_id) -> Table` - Get specific table
- `get_by_number(number, restaurant_id) -> Table` - Find table by number
- `get_by_qr_token(qr_token) -> Table` - Find table by QR token
- `create(number, qr_token, restaurant_id) -> Table` - Create new table
- `update_status(table, status) -> Table` - Update table availability
- `delete(table_id) -> bool` - Delete table

---

**Name:** `report_repository.py` (ReportRepository)

**Description:** Composes complex analytics queries for reporting endpoints.

**Inputs/Outputs:**

- Input: Database session, restaurant_id, date filters
- Output: Aggregated query results (dictionaries, tuples)

**Interfaces/APIs:**

- `get_overall_counts(restaurant_id) -> dict` - Total orders, revenue, averages
- `get_daily_sales(restaurant_id, days) -> list` - Daily aggregated sales
- `get_top_items_by_quantity(restaurant_id, limit) -> list` - Most ordered items
- `get_top_items_by_revenue(restaurant_id, limit) -> list` - Highest revenue items
- `get_category_breakdown(restaurant_id) -> list` - Revenue per category
- `get_hourly_counts(restaurant_id) -> list` - Order count per hour

---

#### 4.3.4 Domain Layer (Models)

**Name:** `user.py` (User Model)

**Description:** Represents system users (owners and staff) with authentication data.

**Attributes:**

- `id` (PK), `username`, `hashed_password`, `role` (owner/staff)
- `restaurant_id` (FK), `created_by_id` (FK for staff), `created_at`

**Relationships:**

- `restaurant` - Many-to-one with Restaurant
- `created_by` - Self-referencing for staff accounts

---

**Name:** `restaurant.py` (Restaurant Model)

**Description:** Represents the multi-tenant restaurant entity.

**Attributes:**

- `id` (PK), `name`, `created_at`

**Relationships:**

- `users` - One-to-many with User
- `tables` - One-to-many with Table
- `menu_items` - One-to-many with MenuItem
- `orders` - One-to-many with Order

---

**Name:** `menu_item.py` (MenuItem Model)

**Description:** Represents dishes available for ordering.

**Attributes:**

- `id` (PK), `name`, `description`, `price`, `category`, `image_url`
- `is_available`, `restaurant_id` (FK), `created_at`, `updated_at`

**Relationships:**

- `restaurant` - Many-to-one with Restaurant
- `order_items` - One-to-many with OrderItem

---

**Name:** `order.py` (Order Model)

**Description:** Represents customer orders with status and payment tracking.

**Attributes:**

- `id` (PK), `table_id` (FK), `restaurant_id` (FK)
- `status` (NEW/PREPARING/READY/COMPLETED/CANCELLED)
- `payment_status` (UNPAID/PAID), `created_at`, `updated_at`, `closed_at`

**Relationships:**

- `table` - Many-to-one with Table
- `restaurant` - Many-to-one with Restaurant
- `items` - One-to-many with OrderItem

---

**Name:** `order_item.py` (OrderItem Model)

**Description:** Represents individual dishes within an order with per-item status tracking.

**Attributes:**

- `id` (PK), `order_id` (FK), `menu_item_id` (FK, nullable)
- `quantity`, `unit_price`, `status` (NEW/PREPARING/READY/COMPLETED)
- `created_at`, `updated_at`

**Relationships:**

- `order` - Many-to-one with Order
- `menu_item` - Many-to-one with MenuItem (nullable for deleted items)

---

**Name:** `table.py` (Table Model)

**Description:** Represents physical restaurant tables with QR code access.

**Attributes:**

- `id` (PK), `number`, `qr_token` (unique), `restaurant_id` (FK)
- `status` (AVAILABLE/OCCUPIED), `created_at`

**Relationships:**

- `restaurant` - Many-to-one with Restaurant
- `orders` - One-to-many with Order

---

### 4.4 Component Interaction Diagrams

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

### 4.5 Data Flow Example: Per-Item Status Update

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

[ER Diagram](docs/diagrams/schema.png)

### 5.2 Table Schemas

### 5.2.1 Current Implementation Alignment (Important)

The running backend is multi-tenant and extends the conceptual schema above as follows:

- A `restaurants` table exists and is the tenant root.
- `users`, `tables`, `menu_items`, and `orders` include `restaurant_id` foreign keys.
- `order_items.menu_item_id` is nullable with `ON DELETE SET NULL` to preserve order history when menu items are deleted.
- `orders` contains both `status` and `payment_status`, plus `closed_at` for completion/payment lifecycle tracking.

This alignment ensures tenant isolation and historical integrity while preserving layered service/repository flows.

### 5.2.2 Conceptual Table Schemas

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
- Good performance for this project scope

**Alternatives considered:**

- Django: Too heavyweight for this project
- Flask: Less built-in features, more boilerplate

#### Frontend: Vue 3 (Composition API)

**Chosen for:**

- Reactive and component-based
- Composition API provides better code organization
- Strong developer experience
- Lightweight compared to Angular

**Alternatives considered:**

- React: More verbose, JSX syntax
- Angular: Overkill for this scale

#### Database: PostgreSQL

**Chosen for:**

- Reliable relational database for multi-tenant deployments
- Better concurrency support than SQLite
- Strong SQL feature set for reporting/analytics queries

**Testing approach:** The automated test suite uses a temporary SQLite database for fast, isolated tests.

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
def get_top_selling_items(db: Session, restaurant_id: int, limit: int = 10):
    # Aggregate order items grouped by menu item
    results = (
        db.query(
            MenuItem.name,
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.quantity * OrderItem.unit_price).label('total_revenue')
        )
        .join(OrderItem, MenuItem.id == OrderItem.menu_item_id)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(Order.payment_status == PaymentStatus.PAID)  # Only paid orders
        .filter(Order.restaurant_id == restaurant_id)  # Tenant scoping
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
  // English UI but Thai currency
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "THB",
  }).format(value);
}

// Example output (browser-dependent): THB 350.00
```

#### Frontend Date/Time Formatting (Bangkok)

```javascript
function formatThaiTime(isoString) {
  return new Intl.DateTimeFormat("en-US", {
    timeZone: "Asia/Bangkok",
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  }).format(new Date(isoString));
}
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

### 7.7 Automated Testing (pytest)

The backend includes an automated test suite to validate both **business rules** and **security boundaries**.

- **Framework:** `pytest` + FastAPI `TestClient`
- **Isolation:** tests run against a temporary SQLite database file, and the schema is recreated per test for clean state.
- **Coverage focus:** multi-tenant data isolation, role-based access control, QR-token customer flows, menu/table rules, order lifecycle, and reporting access.

**Current suite size:** 34 backend tests passing.

Architecture fitness functions are included to enforce layered boundaries and coupling constraints, including:

- Routes must not import repositories directly
- Services must not import route modules
- Repositories must not import services/routes
- Services avoid direct ORM query composition (`.query(...)`) to reduce sinkhole risk

---

## 8. Conclusion

### 8.1 Project Summary

This Restaurant Order Management System addresses key inefficiencies of paper-based order tracking through a digital workflow. The current implementation uses a **layered architecture** with three user roles (Customer, Staff, Owner), each with defined permissions and responsibilities.

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

---

**End of Report**
