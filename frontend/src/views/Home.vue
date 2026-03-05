<template>
  <div class="home">
    <h1>Restaurant Order Management</h1>
    <p>Welcome to the restaurant order management system</p>
    <div class="features">
      <div class="feature-card">
        <h3>📋 Orders</h3>
        <p>Manage customer orders</p>
      </div>
      <div class="feature-card">
        <h3>🍽️ Menu</h3>
        <p>View and update menu items</p>
      </div>
      <div class="feature-card">
        <h3>👥 Customers</h3>
        <p>Customer management</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  text-align: center;
}

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 2.5rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 40px;
}

.feature-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}
</style>
