<template>
    <DashboardLayout role="owner">
        <div class="space-y-6">
            <div>
                <h1 class="font-heading text-3xl font-bold text-foreground">Menu Management</h1>
                <p class="mt-1 text-sm text-muted-foreground">Add, edit, or remove menu items</p>
            </div>

            <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
                <OwnerMenuItemCard
                    v-for="item in menuItems"
                    :key="item.id"
                    :item="item"
                    @edit="openEdit"
                    @delete="deleteItem"
                    @toggle-availability="toggleAvailability"
                />
            </div>
        </div>
    </DashboardLayout>
</template>
<script setup>
import DashboardLayout from '@/components/DashboardLayout.vue'
import OwnerMenuItemCard from '@/components/OwnerMenuItemCard.vue'
import { mockMenuItems } from '@/data/mock-data'

const menuItems = mockMenuItems
function openEdit(item) {
  console.log('edit', item)
}

function deleteItem(item) {
  console.log('delete', item)
}

function toggleAvailability(item) {
  console.log('toggle availability', item)
}
//   const [items, setItems] = useState<MenuItem>(mockMenuItems);
//   const [editItem, setEditItem] = useState<MenuItem | null>(null);
//   const [isDialogOpen, setIsDialogOpen] = useState(false);

//   const [form, setForm] = useState({ name: '', description: '', price: '', category: 'Mains', is_available: true });

//   const openNew = () => {
//     setEditItem(null);
//     setForm({ name: '', description: '', price: '', category: 'Mains', is_available: true });
//     setIsDialogOpen(true);
//   };

//   const openEdit = (item) => {
//     setEditItem(item);
//     setForm({ name: item.name, description: item.description, price: item.price.toString(), category: item.category, is_available: item.is_available });
//     setIsDialogOpen(true);
//   };

//   const save = () => {
//     if (!form.name || !form.price) { toast.error('Name and price required'); return; }
//     if (editItem) {
//       setItems(prev => prev.map(i => i.id === editItem.id ? { ...i, ...form, price: parseFloat(form.price) } : i));
//       toast.success('Menu item updated');
//     } else {
//       const newItem = { id: `new-${Date.now()}`, ...form, price: parseFloat(form.price) };
//       setItems(prev => [...prev, newItem]);
//       toast.success('Menu item created');
//     }
//     setIsDialogOpen(false);
//   };

//   const deleteItem = (id) => {
//     setItems(prev => prev.filter(i => i.id !== id));
//     toast.success('Menu item deleted');
//   };

//   const toggleAvailability = (id) => {
//     setItems(prev => prev.map(i => i.id === id ? { ...i, is_available: !i.is_available } : i));
//   };


</script>
