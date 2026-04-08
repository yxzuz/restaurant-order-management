export const mockMenuItems = [
  {
    id: 1,
    name: 'Grilled Salmon',
    description: 'Char-grilled salmon fillet with lemon butter sauce and seasonal vegetables.',
    image_url: '/src/assets/hero-restaurant.jpg',
    price: 24.99,
    category: 'Main Course',
    is_available: true,
  },
  {
    id: 2,
    name: 'Margherita Pizza',
    description: 'Wood-fired pizza topped with tomato sauce, fresh mozzarella, and basil.',
    image_url: '/src/assets/hero-restaurant.jpg',
    price: 18.5,
    category: 'Pizza',
    is_available: true,
  },
  {
    id: 3,
    name: 'Caesar Salad',
    description: 'Crisp romaine lettuce, parmesan, croutons, and creamy Caesar dressing.',
    image_url: '/src/assets/hero-restaurant.jpg',
    price: 12.0,
    category: 'Salad',
    is_available: true,
  },
  {
    id: 4,
    name: 'Truffle Pasta',
    description: 'Creamy handmade pasta finished with mushroom ragout and truffle oil.',
    image_url: '/src/assets/hero-restaurant.jpg',
    price: 21.75,
    category: 'Pasta',
    is_available: true,
  },
  {
    id: 5,
    name: 'Lemon Tart',
    description: 'Tangy lemon curd tart with a buttery crust and lightly whipped cream.',
    image_url: '/src/assets/hero-restaurant.jpg',
    price: 8.5,
    category: 'Dessert',
    is_available: true,
  },
]

export const mockOrders = [
  {
    id: 1,
    table_number: 3,
    status: 'New',
    total_amount: 59.97,
    created_at: '2026-04-09T10:15:00Z',
    items: [
      { id: 1, quantity: 2, subtotal: 37.0, menu_item: { name: 'Margherita Pizza' } },
      { id: 2, quantity: 1, subtotal: 22.97, menu_item: { name: 'Truffle Pasta' } },
    ],
  },
  {
    id: 2,
    table_number: 5,
    status: 'Preparing',
    total_amount: 36.99,
    created_at: '2026-04-09T09:50:00Z',
    items: [
      { id: 3, quantity: 1, subtotal: 24.99, menu_item: { name: 'Grilled Salmon' } },
      { id: 4, quantity: 1, subtotal: 12.0, menu_item: { name: 'Caesar Salad' } },
    ],
  },
  {
    id: 3,
    table_number: 7,
    status: 'Ready',
    total_amount: 42.5,
    created_at: '2026-04-09T09:35:00Z',
    items: [
      { id: 5, quantity: 2, subtotal: 17.0, menu_item: { name: 'Lemon Tart' } },
      { id: 6, quantity: 1, subtotal: 25.5, menu_item: { name: 'House Special' } },
    ],
  },
  {
    id: 4,
    table_number: 2,
    status: 'Completed',
    total_amount: 52.41,
    created_at: '2026-04-09T08:45:00Z',
    items: [
      { id: 7, quantity: 2, subtotal: 24.0, menu_item: { name: 'Bruschetta' } },
      { id: 8, quantity: 1, subtotal: 28.41, menu_item: { name: 'Seafood Risotto' } },
    ],
  },
]
