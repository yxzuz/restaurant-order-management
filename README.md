# Restaurant Order Tracking & Management System

## Overview

This project is a web-based system designed to replace paper-based order tracking in small and medium-sized restaurants.
It allows customers to place orders digitally, staff to manage order status, and restaurant owners to monitor operations and view analytics.

The system focuses on **order workflow management** rather than payment processing.

---

## Problem Statement

Many restaurants still rely on handwritten order slips to manage customer orders.
This manual process can lead to:

* Lost or misplaced order tickets
* Miscommunication between staff and kitchen
* Delayed order preparation
* Lack of real-time order visibility
* No structured sales data for analysis

This system digitizes the ordering workflow to improve operational efficiency and reduce human error.

---

## Objectives

The main goals of the system are:

* Digitize manual restaurant order tracking
* Implement structured order lifecycle management
* Enforce role-based access control
* Improve operational transparency
* Provide basic analytics for restaurant owners

---

## System Features

### Authentication & Authorization

* Secure login and logout
* User authentication
* Role-based access control
* Permission-based system actions

### Order Management

* Create and manage restaurant orders
* Track order lifecycle
* View order history

### Menu Management

* Create, update, and remove menu items
* Manage pricing and availability

### Reporting

* Daily order summary
* Order activity monitoring

---

## User Roles

### Customer

Responsibilities:

* Browse menu
* Place orders
* View order status
* Cancel pending orders

Permissions:

* Create orders
* View own orders
* Cancel own pending orders

---

### Staff (Server / Cashier)

Responsibilities:

* View incoming orders
* Update order preparation status
* Manage active order queue

Permissions:

* Read active orders
* Update order status

---

### Restaurant Owner

Responsibilities:

* Manage menu items
* Monitor orders
* View reports and analytics
* Manage staff accounts

Permissions:

* Full CRUD access to menu
* View all orders
* Manage users

---

## System Workflow

1. User logs into the system.
2. The system authenticates credentials and assigns role permissions.
3. Customer places an order.
4. The order is stored in the database with status **New**.
5. Staff updates order status:

   * New
   * Preparing
   * Ready
   * Completed
   * Cancelled
6. Restaurant owner monitors orders and views reports.

---

## Technology Stack

### Frontend

* Vue.js
* JavaScript
* Axios

### Backend

* FastAPI
* Python
* SQLAlchemy

### Database

* PostgreSQL / MySQL

### Authentication

* JWT (JSON Web Tokens)
* Password hashing with bcrypt

---

## Project Structure

```

restaurant-order-tracking-system
│
├── backend
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend
│   ├── index.html
│   ├── package.json
│   └── src/
│       ├── assets/
│       ├── components/
│       ├── router/
│       ├── services/
│       ├── stores/
│       ├── views/
│       ├── App.vue
│       └── main.js
│
├── docs
│   └── architecture-diagrams
│
├── .gitignore
└── README.md
```

---

## How to Run the Project

### Backend (FastAPI)

```
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

API documentation available at:

```
http://localhost:8000/docs
```

---

### Frontend (Vue)

```
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:3000
```

---

## Future Improvements

* Multi-restaurant platform support
* Inventory tracking
* Order analytics dashboard
* Real-time order updates
* Integration with payment systems

---

## Author

Software Architecture Project
Restaurant Order Tracking & Management System
