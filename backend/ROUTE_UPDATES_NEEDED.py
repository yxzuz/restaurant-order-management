"""
Multi-Tenant Completion: Remaining Route Updates

CRITICAL: All routes need to pass current_user.restaurant_id to services.
This file contains exact code changes needed for each route file.
"""

# ============================================================================
# FILE: app/api/routes/tables.py
# ============================================================================

# CHANGE 1: list_tables
# OLD:
def list_tables(current_user: User = Depends(require_staff_or_owner), db: Session = Depends(get_db)):
    return TableService(db).list_tables()

# NEW:
def list_tables(current_user: User = Depends(require_staff_or_owner), db: Session = Depends(get_db)):
    return TableService(db).list_tables(current_user.restaurant_id)

# CHANGE 2: create_table
# OLD:
    table = service.create_table(payload.number)
# NEW:
    table = service.create_table(payload.number, current_user.restaurant_id)

# CHANGE 3: delete_table
# OLD:
    success = service.delete_table(table_number)
# NEW:
    success = service.delete_table(table_number, current_user.restaurant_id)


# ============================================================================
# FILE: app/api/routes/menus.py
# ============================================================================

# CHANGE 1: list_menu_items
# OLD:
    return service.list_menu_items()
# NEW:
    return service.list_menu_items(current_user.restaurant_id)

# CHANGE 2: create_menu_item
# OLD:
    menu_item = service.create_menu_item(
        name=payload.name,
        price=payload.price,
        is_available=payload.is_available,
        category=payload.category,
        image_url=payload.image_url,
    )
# NEW:
    menu_item = service.create_menu_item(
        name=payload.name,
        price=payload.price,
        restaurant_id=current_user.restaurant_id,
        description=payload.description,
        is_available=payload.is_available,
        category=payload.category,
        image_url=payload.image_url,
    )

# CHANGE 3: upload_image
# OLD:
    image_url = service.upload_menu_image(image)
# NEW:
    image_url = service.upload_menu_image(image, current_user.restaurant_id)


# ============================================================================
# FILE: app/api/routes/orders.py
# ============================================================================

# CHANGE 1: list_orders
# OLD:
    return service.list_orders()
# NEW:
    return service.list_orders(current_user.restaurant_id)

# CHANGE 2: list_active_orders
# OLD:
    return service.list_active_orders()
# NEW:
    return service.list_active_orders(current_user.restaurant_id)

# NOTE: create_order (customer endpoint) doesn't have current_user, 
# it extracts restaurant_id from table ✅ Already handled in service


# ============================================================================
# FILE: app/api/routes/auth.py (already has register, needs staff fix)
# ============================================================================

# CHANGE 1: create_staff
# OLD:
    user = service.create_staff(payload)
# NEW:
    user = service.create_staff(payload, current_user.restaurant_id)


# ============================================================================
# VERIFICATION CHECKLIST
# ============================================================================

After making these changes, verify:

1. ✅ Services receive restaurant_id
2. ✅ Repositories filter by restaurant_id  
3. ✅ JWT includes restaurant_id
4. ✅ Registration creates restaurant + owner
5. ✅ Login works across restaurants
6. ✅ Staff creation scoped to owner's restaurant
7. ✅ Menu items scoped to restaurant
8. ✅ Orders scoped to restaurant  
9. ✅ Tables scoped to restaurant
10. ✅ S3 uploads to restaurant folder

# ============================================================================
# TESTING SCRIPT
# ============================================================================

# Test 1: Register Restaurant A
POST /api/auth/register
{
  "username": "ownerA",
  "password": "password123",
  "restaurant_name": "Pizza Palace"
}
# Should return token

# Test 2: Create menu item in Restaurant A
POST /api/menus
Headers: Authorization: Bearer <token_from_test_1>
{
  "name": "Margherita Pizza",
  "price": 12.99,
  "category": "Mains",
  "description": "Classic tomato and mozzarella"
}

# Test 3: Register Restaurant B
POST /api/auth/register
{
  "username": "ownerB",
  "password": "password456",
  "restaurant_name": "Burger Hub"
}

# Test 4: Check Restaurant B menu is empty
GET /api/menus
Headers: Authorization: Bearer <token_from_test_3>
# Should return [] (not Pizza Palace's items)

# Test 5: Login as Restaurant A owner
POST /api/auth/login
{
  "username": "ownerA",
  "password": "password123"
}
# Should return token

# Test 6: Verify Restaurant A menu still has pizza
GET /api/menus
Headers: Authorization: Bearer <token_from_test_5>
# Should return Margherita Pizza

SUCCESS = Data is fully isolated between restaurants!
