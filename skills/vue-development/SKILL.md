---
name: vue-development
description: Vue 3 development using Composition API, reactivity, Vue Router, Pinia state management, and composables.
---

# Vue 3 Development

Master Vue 3 with Composition API for building reactive, maintainable components. Learn state management with Pinia, routing with Vue Router, and best practices for composables.

## Quick Start

```vue
<!-- src/components/UserProfile.vue -->
<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

// Composition API with ref
const user = useUserStore();
const router = useRouter();
const isEditing = ref(false);
const formData = ref({ name: '', email: '' });

// Computed properties
const isFormValid = computed(() => {
  return formData.value.name && formData.value.email;
});

// Watch for changes
watch(
  () => user.currentUser,
  (newUser) => {
    if (newUser) {
      formData.value = { ...newUser };
    }
  },
  { immediate: true }
);

// Methods
async function saveProfile() {
  await user.updateProfile(formData.value);
  isEditing.value = false;
  router.push('/dashboard');
}

function cancel() {
  isEditing.value = false;
}
</script>

<template>
  <div class="profile-container">
    <h1>{{ user.currentUser?.name }}</h1>

    <template v-if="!isEditing">
      <p>{{ user.currentUser?.email }}</p>
      <button @click="isEditing = true">Edit Profile</button>
    </template>

    <form v-else @submit.prevent="saveProfile">
      <input v-model="formData.name" type="text" placeholder="Name" />
      <input v-model="formData.email" type="email" placeholder="Email" />

      <button type="submit" :disabled="!isFormValid">Save</button>
      <button type="button" @click="cancel">Cancel</button>
    </form>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
```

## Key Concepts

### Composition API and Reactivity

The Composition API provides granular control over component logic:

```vue
<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue';

// Reactive references
const count = ref(0);
const message = ref('Hello');

// Reactive object
const state = reactive({
  todos: [] as string[],
  filter: 'all' as 'all' | 'active' | 'completed',
});

// Computed properties with getters and setters
const filteredTodos = computed(() => {
  if (state.filter === 'all') return state.todos;
  // Filter logic here
  return state.todos;
});

// Lifecycle hooks
onMounted(() => {
  console.log('Component mounted');
});

onUnmounted(() => {
  console.log('Component unmounted');
});

// Methods
function increment() {
  count.value++;
}

function addTodo(todo: string) {
  state.todos.push(todo);
}
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <button @click="increment">Increment</button>

    <p>Todos: {{ filteredTodos }}</p>
    <select v-model="state.filter">
      <option value="all">All</option>
      <option value="active">Active</option>
      <option value="completed">Completed</option>
    </select>
  </div>
</template>
```

### Pinia State Management

Centralized state management with type-safe stores:

```typescript
// src/stores/user.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User } from '@/types';

export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref<User | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Computed
  const isAuthenticated = computed(() => !!currentUser.value);
  const userInitials = computed(() => {
    if (!currentUser.value) return '';
    return currentUser.value.name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase();
  });

  // Actions
  async function fetchUser(userId: string) {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) throw new Error('Failed to fetch user');
      currentUser.value = await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
    } finally {
      isLoading.value = false;
    }
  }

  async function updateProfile(data: Partial<User>) {
    if (!currentUser.value) return;

    try {
      const response = await fetch(`/api/users/${currentUser.value.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) throw new Error('Failed to update profile');
      currentUser.value = await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error';
    }
  }

  function logout() {
    currentUser.value = null;
  }

  return {
    currentUser,
    isLoading,
    error,
    isAuthenticated,
    userInitials,
    fetchUser,
    updateProfile,
    logout,
  };
});

// src/stores/todo.ts - Option API style
import { defineStore } from 'pinia';

interface Todo {
  id: number;
  text: string;
  completed: boolean;
}

export const useTodoStore = defineStore('todo', {
  state: () => ({
    todos: [] as Todo[],
    nextId: 1,
  }),

  getters: {
    completedCount(): number {
      return this.todos.filter(t => t.completed).length;
    },

    pendingCount(): number {
      return this.todos.filter(t => !t.completed).length;
    },
  },

  actions: {
    addTodo(text: string) {
      this.todos.push({
        id: this.nextId++,
        text,
        completed: false,
      });
    },

    toggleTodo(id: number) {
      const todo = this.todos.find(t => t.id === id);
      if (todo) todo.completed = !todo.completed;
    },

    removeTodo(id: number) {
      this.todos = this.todos.filter(t => t.id !== id);
    },
  },
});
```

### Vue Router for Navigation

Set up routing with type-safe navigation:

```typescript
// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/users/:id',
    name: 'UserProfile',
    component: () => import('@/views/UserProfile.vue'),
    beforeEnter: async (to) => {
      // Validate user exists before entering route
      const userId = to.params.id as string;
      try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) return '/404';
      } catch {
        return '/404';
      }
    },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
  },
];

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

// Navigation guards
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isUserLoggedIn()) {
    next('/login');
  } else {
    next();
  }
});

function isUserLoggedIn() {
  // Check authentication
  return !!localStorage.getItem('authToken');
}
```

## Common Patterns

### 1. Custom Composables for Logic Reuse

```typescript
// src/composables/useAsync.ts
import { ref, watchEffect } from 'vue';

export function useAsync<T>(
  asyncFunction: () => Promise<T>,
  immediate = true
) {
  const data = ref<T | null>(null);
  const loading = ref(false);
  const error = ref<Error | null>(null);

  const execute = async () => {
    loading.value = true;
    error.value = null;

    try {
      data.value = await asyncFunction();
    } catch (err) {
      error.value = err instanceof Error ? err : new Error(String(err));
    } finally {
      loading.value = false;
    }
  };

  if (immediate) {
    watchEffect(execute);
  }

  return { data, loading, error, execute };
}

// src/composables/useFetch.ts
import { useAsync } from './useAsync';

export function useFetch<T>(url: string) {
  const fetchData = async () => {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json() as Promise<T>;
  };

  return useAsync(fetchData);
}

// Usage in component
export default {
  setup() {
    const { data: users, loading, error } = useFetch('/api/users');

    return { users, loading, error };
  },
};
```

### 2. Form Handling with v-model

```vue
<script setup lang="ts">
import { reactive } from 'vue';

interface FormData {
  email: string;
  password: string;
  rememberMe: boolean;
}

const form = reactive<FormData>({
  email: '',
  password: '',
  rememberMe: false,
});

const errors = reactive<Record<string, string>>({});

function validateForm(): boolean {
  errors.email = '';
  errors.password = '';

  if (!form.email) {
    errors.email = 'Email is required';
  }

  if (!form.password) {
    errors.password = 'Password is required';
  }

  return Object.values(errors).every(e => !e);
}

async function handleSubmit() {
  if (!validateForm()) return;

  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });

    if (response.ok) {
      // Handle success
    }
  } catch (err) {
    // Handle error
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <div class="form-group">
      <label for="email">Email</label>
      <input
        id="email"
        v-model="form.email"
        type="email"
        @blur="validateForm"
      />
      <span v-if="errors.email" class="error">{{ errors.email }}</span>
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <input
        id="password"
        v-model="form.password"
        type="password"
        @blur="validateForm"
      />
      <span v-if="errors.password" class="error">{{ errors.password }}</span>
    </div>

    <label>
      <input v-model="form.rememberMe" type="checkbox" />
      Remember me
    </label>

    <button type="submit">Login</button>
  </form>
</template>
```

### 3. Conditional Rendering and Lists

```vue
<script setup lang="ts">
import { ref, computed } from 'vue';

interface Item {
  id: number;
  title: string;
  completed: boolean;
}

const items = ref<Item[]>([
  { id: 1, title: 'Learn Vue 3', completed: true },
  { id: 2, title: 'Build a project', completed: false },
]);

const activeTab = ref('all');

const filteredItems = computed(() => {
  switch (activeTab.value) {
    case 'active':
      return items.value.filter(i => !i.completed);
    case 'completed':
      return items.value.filter(i => i.completed);
    default:
      return items.value;
  }
});

function toggleItem(id: number) {
  const item = items.value.find(i => i.id === id);
  if (item) item.completed = !item.completed;
}

function deleteItem(id: number) {
  items.value = items.value.filter(i => i.id !== id);
}
</script>

<template>
  <div>
    <div class="tabs">
      <button
        v-for="tab in ['all', 'active', 'completed']"
        :key="tab"
        :class="{ active: activeTab === tab }"
        @click="activeTab = tab"
      >
        {{ tab }}
      </button>
    </div>

    <ul v-if="filteredItems.length > 0">
      <li v-for="item in filteredItems" :key="item.id">
        <input
          :checked="item.completed"
          type="checkbox"
          @change="toggleItem(item.id)"
        />
        <span :class="{ completed: item.completed }">
          {{ item.title }}
        </span>
        <button @click="deleteItem(item.id)">Delete</button>
      </li>
    </ul>

    <p v-else>No items to display</p>
  </div>
</template>

<style scoped>
.tabs button {
  padding: 0.5rem 1rem;
  margin-right: 0.5rem;
}

.tabs button.active {
  background-color: #007bff;
  color: white;
}

.completed {
  text-decoration: line-through;
  color: #999;
}
</style>
```

## Best Practices

✅ Use Composition API for better code organization and logic reuse
✅ Create reusable composables for common patterns
✅ Keep components small and focused on a single responsibility
✅ Use Pinia for centralized state management
✅ Implement proper loading and error states
✅ Use TypeScript for type-safe components and stores
✅ Leverage lazy loading for routes to improve performance

## Common Pitfalls

❌ Mutating state directly instead of using actions
❌ Creating too many deeply nested reactive objects
❌ Forgetting to unsubscribe from computed properties and watches
❌ Mixing reactive and non-reactive state
❌ Over-using watchers when computed properties would suffice
❌ Not properly typing Pinia stores

## Resources

- [Vue 3 Official Documentation](https://vuejs.org/)
- [Composition API Guide](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Vue Router Official Docs](https://router.vuejs.org/)
- [VueUse - Collection of Composables](https://vueuse.org/)
