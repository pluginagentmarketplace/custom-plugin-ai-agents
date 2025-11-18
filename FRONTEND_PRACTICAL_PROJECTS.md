# Frontend Practical Projects & Use Cases
## Real-World Applications for Claude Code Plugin Development

---

## 1. PROJECT CATEGORIZATION BY COMPLEXITY & LEARNING VALUE

### 1.1 Tier 1: Foundation Projects (1-2 weeks each)

These projects reinforce fundamental HTML, CSS, and JavaScript skills.

#### Project: Personal Portfolio Website
**Skills Developed:**
- HTML semantic structure
- Responsive CSS (Flexbox, Grid)
- CSS animations and transitions
- JavaScript for smooth scrolling and navigation
- Mobile-first design approach

**Requirements:**
- Hero section with CTA
- Project showcase gallery
- About section
- Contact form
- Responsive navigation menu
- Smooth scrolling functionality

**Technologies:**
- HTML5, CSS3, Vanilla JavaScript
- No framework required
- Optional: Lighthouse optimization

**Implementation Patterns:**
```
Structure:
├── index.html (semantic HTML)
├── styles/
│   ├── main.css (global styles)
│   ├── components.css (component styles)
│   └── responsive.css (media queries)
├── scripts/
│   ├── navigation.js (menu toggle)
│   ├── scroll.js (smooth scrolling)
│   └── contact.js (form handling)
└── assets/
    ├── images/
    └── fonts/
```

**Best Practices to Implement:**
- Semantic HTML with proper heading hierarchy
- Mobile-first CSS approach
- CSS variables for theming
- Keyboard accessible navigation
- Form validation without framework
- Lighthouse score > 90

---

#### Project: Interactive Todo Application
**Skills Developed:**
- JavaScript state management basics
- DOM manipulation
- Event handling
- Local storage persistence
- List rendering and filtering

**Requirements:**
- Add/delete todos
- Mark as complete/incomplete
- Filter by status (all/active/completed)
- Local storage persistence
- Clear completed button

**Technologies:**
- HTML5, CSS3, Vanilla JavaScript
- LocalStorage API

**Implementation Patterns:**
```javascript
// Core structure pattern
class TodoApp {
  constructor() {
    this.todos = this.loadFromStorage();
    this.init();
  }

  init() {
    this.render();
    this.attachEventListeners();
  }

  render() {
    // Filter todos based on current filter
    // Update DOM
  }

  saveToStorage() {
    // Persist state
  }
}
```

**Best Practices:**
- Separation of concerns (data, UI, events)
- DRY principle in event handling
- Proper error handling
- Accessibility for interactive elements
- Keyboard navigation support

---

#### Project: Weather Application
**Skills Developed:**
- REST API consumption with Fetch
- Async/await handling
- Error handling and loading states
- Dynamic content rendering
- API key management

**Requirements:**
- Search by city
- Display current weather
- 5-day forecast
- Temperature unit toggle
- API error handling with user feedback

**Technologies:**
- HTML5, CSS3, Vanilla JavaScript
- Fetch API
- OpenWeatherMap API (free tier)

**Implementation Patterns:**
```javascript
// API integration pattern
async function fetchWeather(city) {
  try {
    setLoading(true);
    const response = await fetch(`${API_URL}?q=${city}&appid=${API_KEY}`);
    if (!response.ok) throw new Error('City not found');

    const data = await response.json();
    renderWeather(data);
  } catch (error) {
    displayError(error.message);
  } finally {
    setLoading(false);
  }
}
```

**Best Practices:**
- Proper error handling
- Loading state management
- Rate limiting awareness
- Environment variable usage
- API response validation

---

### 1.2 Tier 2: Framework Foundation Projects (2-4 weeks each)

Introduce modern framework patterns and component architecture.

#### Project: Blog Platform with React
**Skills Developed:**
- React components and props
- State management with useState
- Effects and lifecycle with useEffect
- Component composition
- Conditional rendering
- List rendering with keys

**Requirements:**
- Display list of blog posts
- Create new blog post form
- Individual post view
- Search/filter posts
- Delete post functionality
- Local data storage

**Technologies:**
- React with Hooks
- Vite or Create React App
- CSS Modules or Tailwind CSS

**Component Structure:**
```
App/
├── components/
│   ├── PostList.jsx
│   ├── PostCard.jsx
│   ├── PostForm.jsx
│   ├── PostDetail.jsx
│   └── SearchBar.jsx
├── hooks/
│   └── usePosts.js (custom hook)
├── styles/
└── App.jsx
```

**Key Patterns:**
- Custom hooks for data management
- Prop drilling awareness
- Key usage in lists
- Conditional rendering patterns
- Form handling with useState

**Best Practices:**
- Components as pure functions
- Props validation with PropTypes
- Proper dependency arrays in useEffect
- Single responsibility per component

---

#### Project: E-Commerce Product Catalog with Vue
**Skills Developed:**
- Vue template syntax and directives
- Component props and events
- Computed properties
- List rendering and filtering
- Form handling with v-model
- Routing basics

**Requirements:**
- Product grid display
- Filter by category and price
- Shopping cart
- Product detail view
- Add to cart functionality
- Cart total calculation

**Technologies:**
- Vue 3 with Composition API
- Vue Router for navigation
- Tailwind CSS

**Component Structure:**
```
src/
├── components/
│   ├── ProductGrid.vue
│   ├── ProductCard.vue
│   ├── FilterPanel.vue
│   └── ShoppingCart.vue
├── views/
│   ├── ProductList.vue
│   └── ProductDetail.vue
├── composables/
│   └── useCart.js
└── App.vue
```

**Key Patterns:**
- Composition API for logic reuse
- Computed properties for filtering
- Event emission for component communication
- Provide/inject for shared state
- Scoped styles for component isolation

---

#### Project: Dashboard with Angular
**Skills Developed:**
- Angular components and services
- Dependency injection
- RxJS observables and operators
- HTTP client for data fetching
- Routing with parameters
- Reactive forms

**Requirements:**
- User authentication
- Dashboard with multiple widgets
- Real-time data refresh
- User profile management
- Logout functionality

**Technologies:**
- Angular 15+
- Angular Material
- RxJS for reactive programming

**Module Structure:**
```
src/
├── app/
│   ├── core/
│   │   ├── services/
│   │   │   ├── auth.service.ts
│   │   │   └── dashboard.service.ts
│   │   └── guards/
│   ├── shared/
│   │   └── components/
│   ├── features/
│   │   ├── dashboard/
│   │   │   ├── dashboard.component.ts
│   │   │   └── dashboard.module.ts
│   │   └── profile/
│   └── app.module.ts
```

**Key Patterns:**
- Service-based architecture
- Observable streams with RxJS
- Smart/dumb component pattern
- Route guards for authentication
- HTTP interceptors for auth tokens

---

### 1.3 Tier 3: Advanced Framework Projects (4-8 weeks each)

Complex features requiring advanced patterns and state management.

#### Project: Real-Time Chat Application with React
**Skills Developed:**
- Complex state management (Redux/Zustand)
- WebSocket integration
- Real-time data synchronization
- User authentication and authorization
- Message persistence
- Performance optimization with memoization

**Requirements:**
- User registration and login
- Real-time messaging
- Multiple chat rooms
- User presence indicators
- Message history
- Typing indicators
- Message search

**Technologies:**
- React with Hooks
- Redux Toolkit or Zustand
- WebSocket (Socket.io)
- Firebase or similar backend

**Architecture:**
```
State Management:
├── users slice
│   ├── currentUser
│   ├── onlineUsers
│   └── userActions
├── messages slice
│   ├── messagesByRoom
│   ├── unreadCount
│   └── messageActions
├── rooms slice
│   ├── selectedRoom
│   ├── roomList
│   └── roomActions
└── websocket middleware

Components:
├── ChatWindow
├── MessageList
├── MessageInput
├── UserList
├── RoomList
└── UserProfile
```

**Advanced Patterns:**
- Normalized state shape
- Message deduplication
- Offline support with optimistic updates
- WebSocket reconnection logic
- Memory leak prevention in cleanup

**Performance Considerations:**
- Virtualized lists for large message histories
- React.memo for message components
- useCallback for event handlers
- Message batching for real-time updates

---

#### Project: E-Commerce Platform with Next.js
**Skills Developed:**
- Server-side rendering and static generation
- API route development
- Database integration
- Authentication and authorization
- Payment processing
- Admin dashboard

**Requirements:**
- Product catalog with search
- Shopping cart and checkout
- Payment processing (Stripe)
- Order history
- Admin product management
- User authentication (NextAuth.js)
- Email notifications

**Technologies:**
- Next.js with App Router
- Prisma with PostgreSQL
- NextAuth.js for authentication
- Stripe for payments
- Tailwind CSS

**Project Structure:**
```
app/
├── (auth)/
│   ├── login/
│   ├── register/
│   └── layout.tsx
├── (shop)/
│   ├── products/
│   │   ├── page.tsx
│   │   └── [id]/
│   ├── cart/
│   └── layout.tsx
├── (admin)/
│   ├── products/
│   ├── orders/
│   └── layout.tsx
├── api/
│   ├── auth/[...nextauth]/
│   ├── products/
│   ├── orders/
│   └── stripe/
└── layout.tsx

lib/
├── db.ts (Prisma client)
├── auth.ts (NextAuth config)
└── stripe.ts

prisma/
├── schema.prisma
└── migrations/
```

**Architecture Patterns:**
- Server components for data fetching
- API routes for backend logic
- Database queries in server components
- Middleware for authentication
- Revalidation strategy (ISR)

**Database Schema:**
```prisma
model Product {
  id String @id @default(cuid())
  name String
  description String
  price Float
  category String
  inventory Int
  createdAt DateTime @default(now())
}

model Order {
  id String @id @default(cuid())
  userId String
  user User @relation(fields: [userId], references: [id])
  items Json
  total Float
  status String @default("pending")
  createdAt DateTime @default(now())
}

model User {
  id String @id @default(cuid())
  email String @unique
  orders Order[]
}
```

**Best Practices:**
- Server-side data fetching with revalidation
- Database connection pooling
- Type-safe database queries with Prisma
- Secure environment variable handling
- API error responses standardization

---

#### Project: Project Management Tool with Vue 3
**Skills Developed:**
- Advanced Composition API patterns
- Pinia state management
- Complex form validation
- Real-time collaboration features
- Performance optimization
- Testing strategies

**Requirements:**
- Create and manage projects
- Task creation and assignment
- Team member management
- Real-time task updates
- Comment system
- File attachments
- Activity tracking

**Technologies:**
- Vue 3 with Composition API
- Pinia for state management
- Vue Router
- Tailwind CSS
- Vite

**State Management Structure:**
```javascript
// projects.store.js (Pinia)
export const useProjectsStore = defineStore('projects', {
  state: () => ({
    projects: [],
    currentProject: null,
    tasks: [],
    teamMembers: [],
  }),

  getters: {
    projectById: (state) => (id) => {
      return state.projects.find(p => p.id === id);
    },
    tasksByProject: (state) => (projectId) => {
      return state.tasks.filter(t => t.projectId === projectId);
    },
  },

  actions: {
    async createProject(data) {
      // API call and state update
    },
    async updateTask(taskId, updates) {
      // API call and optimistic update
    },
  },
});
```

---

### 1.4 Tier 4: Full-Stack Advanced Projects (8+ weeks)

Enterprise-level applications with complex requirements.

#### Project: SaaS Analytics Dashboard
**Skills Developed:**
- Full-stack Next.js development
- Advanced database design
- Complex data visualizations
- Team collaboration features
- Multi-tenant architecture
- Advanced security patterns

**Requirements:**
- User and team management
- Analytics data ingestion
- Real-time dashboards
- Custom report generation
- Data export (CSV, PDF)
- Webhook integration
- API rate limiting
- Usage tracking and billing

**Architecture:**
```
Frontend:
- Next.js with App Router
- React Query for data fetching
- Recharts for visualizations
- Zustand for UI state

Backend:
- Next.js API routes
- PostgreSQL with Prisma
- Redis for caching
- Job queue for async tasks

Infrastructure:
- Vercel deployment
- Edge functions
- CDN for static assets
- S3 for file storage
```

**Key Features:**
- Multi-tenant data isolation
- WebSocket for real-time updates
- Complex analytics queries optimization
- CSV/PDF generation
- Webhook system for integrations

---

#### Project: AI-Powered Content Platform
**Skills Developed:**
- AI/ML API integration
- Streaming responses
- Advanced caching strategies
- User authentication and authorization
- Content moderation
- Analytics and monitoring

**Requirements:**
- AI content generation
- User content library
- Collaboration on content
- Version history
- Export options
- Usage analytics
- Admin moderation

**Technologies:**
- Next.js with Server Components
- OpenAI API integration
- Prisma with PostgreSQL
- TanStack Query for data
- Tailwind CSS + shadcn/ui

**Features:**
- Streaming AI responses to UI
- Optimistic updates
- Offline support
- Real-time collaboration cursors
- Content versioning system

---

## 2. PROJECT SELECTION MATRIX

| Project | Duration | Level | Best Framework | Key Skills | Team Size |
|---------|----------|-------|-----------------|------------|-----------|
| Portfolio | 1 week | Beginner | None | HTML, CSS, JS | 1 |
| Todo App | 1 week | Beginner | None | JS, DOM, Storage | 1 |
| Weather App | 2 weeks | Beginner | None | JS, APIs, Async | 1-2 |
| Blog Platform | 3 weeks | Intermediate | React | Components, Hooks | 1-2 |
| E-Commerce | 4 weeks | Intermediate | Vue | Routing, Forms | 2 |
| Dashboard | 4 weeks | Intermediate | Angular | DI, RxJS, Routing | 2 |
| Chat App | 6 weeks | Advanced | React | State, WebSocket | 2-3 |
| E-Commerce (Full) | 8 weeks | Advanced | Next.js | SSR, Auth, Payments | 3-4 |
| Project Manager | 6 weeks | Advanced | Vue | Composition, Pinia | 2-3 |
| Analytics Dashboard | 10+ weeks | Expert | Next.js | Full-stack, Architecture | 4+ |
| Content Platform | 12+ weeks | Expert | Next.js | AI, Streaming, Collab | 4+ |

---

## 3. COMMON DESIGN PATTERNS IN PROJECTS

### 3.1 Component Patterns

#### Pattern: Container/Presentational Components
**Use Case:** Separating business logic from UI

```javascript
// Container Component (React)
function UserListContainer() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsers().then(data => {
      setUsers(data);
      setLoading(false);
    });
  }, []);

  return <UserListPresentation users={users} loading={loading} />;
}

// Presentational Component
function UserListPresentation({ users, loading }) {
  if (loading) return <LoadingSpinner />;
  return (
    <ul>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </ul>
  );
}
```

---

#### Pattern: Compound Components
**Use Case:** Complex components with interdependent parts

```javascript
// Define component namespace
const Dropdown = {
  Root: DropdownRoot,
  Trigger: DropdownTrigger,
  Menu: DropdownMenu,
  Item: DropdownItem,
};

// Usage
<Dropdown.Root>
  <Dropdown.Trigger>Open Menu</Dropdown.Trigger>
  <Dropdown.Menu>
    <Dropdown.Item>Option 1</Dropdown.Item>
    <Dropdown.Item>Option 2</Dropdown.Item>
  </Dropdown.Menu>
</Dropdown.Root>
```

---

#### Pattern: Render Props
**Use Case:** Sharing logic between components

```javascript
function DataFetcher({ url, children }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(data => setData(data))
      .catch(err => setError(err));
  }, [url]);

  return children({ data, error });
}

// Usage
<DataFetcher url="/api/users">
  {({ data, error }) => (
    error ? <Error /> : <UserList users={data} />
  )}
</DataFetcher>
```

---

### 3.2 State Management Patterns

#### Pattern: Redux Slice Pattern
```javascript
// createSlice (Redux Toolkit)
const tasksSlice = createSlice({
  name: 'tasks',
  initialState,
  reducers: {
    addTask: (state, action) => {
      state.items.push(action.payload);
    },
    removeTask: (state, action) => {
      state.items = state.items.filter(t => t.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTasks.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchTasks.fulfilled, (state, action) => {
        state.items = action.payload;
        state.loading = false;
      });
  },
});
```

---

#### Pattern: Zustand Store Pattern
```javascript
const useStore = create((set) => ({
  tasks: [],
  addTask: (task) => set((state) => ({
    tasks: [...state.tasks, task]
  })),
  removeTask: (id) => set((state) => ({
    tasks: state.tasks.filter(t => t.id !== id)
  })),
}));
```

---

### 3.3 Data Fetching Patterns

#### Pattern: React Query Pattern
```javascript
function UserProfile({ userId }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  if (isLoading) return <Skeleton />;
  if (error) return <Error error={error} />;

  return <Profile user={data} />;
}
```

---

#### Pattern: Next.js Server Component
```javascript
// Async component (no client state needed)
export default async function PostList() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 } // ISR
  }).then(res => res.json());

  return (
    <ul>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </ul>
  );
}
```

---

### 3.4 Form Patterns

#### Pattern: Controlled Components
```javascript
function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await login({ email, password });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
}
```

---

#### Pattern: React Hook Form
```javascript
import { useForm } from 'react-hook-form';

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('email', { required: 'Email is required' })}
        type="email"
      />
      {errors.email && <span>{errors.email.message}</span>}
      <button type="submit">Login</button>
    </form>
  );
}
```

---

## 4. API INTEGRATION PATTERNS

### 4.1 REST API Integration
```javascript
// Base fetch wrapper
async function apiCall(endpoint, options = {}) {
  const response = await fetch(`/api${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message);
  }

  return response.json();
}

// Usage
const users = await apiCall('/users');
const newUser = await apiCall('/users', {
  method: 'POST',
  body: JSON.stringify({ name: 'John' }),
});
```

---

### 4.2 GraphQL Integration
```javascript
import { ApolloClient, gql } from '@apollo/client';

const GET_USERS = gql`
  query GetUsers {
    users {
      id
      name
      email
    }
  }
`;

function UserList() {
  const { loading, data } = useQuery(GET_USERS);

  if (loading) return <Spinner />;

  return (
    <ul>
      {data.users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

---

### 4.3 WebSocket Integration
```javascript
class WebSocketManager {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.handlers = {};

    this.ws.onmessage = (event) => {
      const { type, payload } = JSON.parse(event.data);
      this.handlers[type]?.(payload);
    };
  }

  on(type, handler) {
    this.handlers[type] = handler;
  }

  send(type, payload) {
    this.ws.send(JSON.stringify({ type, payload }));
  }
}

// Usage
const ws = new WebSocketManager('ws://localhost:8080');
ws.on('message', (message) => {
  console.log('New message:', message);
});
ws.send('message', { text: 'Hello!' });
```

---

## 5. AUTHENTICATION PATTERNS

### 5.1 JWT Authentication
```javascript
// Login
async function login(email, password) {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });

  const { token } = await response.json();
  localStorage.setItem('token', token);
}

// Protected request
function apiCall(endpoint) {
  const token = localStorage.getItem('token');
  return fetch(`/api${endpoint}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
}
```

---

### 5.2 Session-Based Authentication (NextAuth.js)
```javascript
// app/api/auth/[...nextauth]/route.js
export const { handlers, auth } = NextAuth({
  providers: [
    Credentials({
      async authorize(credentials) {
        const user = await db.user.findUnique({
          where: { email: credentials.email },
        });

        if (user && await verifyPassword(credentials.password, user.password)) {
          return user;
        }
        return null;
      },
    }),
  ],
});

// Protected page
export default async function Dashboard() {
  const session = await auth();

  if (!session) {
    redirect('/login');
  }

  return <div>Welcome, {session.user.name}!</div>;
}
```

---

## 6. TESTING PATTERNS

### 6.1 Component Testing (React Testing Library)
```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('LoginForm', () => {
  it('submits form with email and password', async () => {
    const mockLogin = jest.fn();
    render(<LoginForm onSubmit={mockLogin} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'password123');
    await userEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(mockLogin).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });
});
```

---

### 6.2 E2E Testing (Cypress)
```javascript
describe('User Login Flow', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
  });

  it('should log in successfully', () => {
    cy.get('[data-testid=email-input]').type('test@example.com');
    cy.get('[data-testid=password-input]').type('password123');
    cy.get('[data-testid=submit-button]').click();

    cy.url().should('include', '/dashboard');
    cy.get('[data-testid=welcome-message]').should('contain', 'Welcome');
  });
});
```

---

## 7. PERFORMANCE OPTIMIZATION PATTERNS

### 7.1 Code Splitting
```javascript
// React.lazy with Suspense
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

---

### 7.2 Memoization
```javascript
// useMemo for expensive computations
function FilteredList({ items, filter }) {
  const filtered = useMemo(() => {
    return items.filter(item => item.includes(filter));
  }, [items, filter]);

  return <List items={filtered} />;
}

// useCallback for stable references
const handleClick = useCallback(() => {
  doSomething();
}, [dependencies]);
```

---

### 7.3 Image Optimization
```javascript
// Next.js Image component
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // Load eagerly for LCP
  quality={75} // Compression
/>
```

---

## 8. ERROR HANDLING PATTERNS

### 8.1 Error Boundary Pattern
```javascript
class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <MyComponent />
</ErrorBoundary>
```

---

### 8.2 Async Error Handling
```javascript
async function fetchData() {
  try {
    const response = await fetch('/api/data');

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof TypeError) {
      // Network error
      logError('Network error', error);
      throw new Error('Failed to connect to server');
    }

    // Syntax error or other
    logError('Unknown error', error);
    throw error;
  }
}
```

---

## 9. ACCESSIBILITY PATTERNS

### 9.1 Semantic HTML
```html
<!-- Good -->
<nav>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
</main>

<footer>
  <p>&copy; 2024</p>
</footer>
```

---

### 9.2 ARIA Attributes
```javascript
// Accessible dropdown
function Dropdown({ isOpen, onToggle }) {
  return (
    <div>
      <button
        aria-haspopup="true"
        aria-expanded={isOpen}
        onClick={onToggle}
      >
        Menu
      </button>
      {isOpen && (
        <ul role="menu">
          <li role="menuitem">Option 1</li>
          <li role="menuitem">Option 2</li>
        </ul>
      )}
    </div>
  );
}
```

---

### 9.3 Keyboard Navigation
```javascript
function MenuItem({ onSelect }) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onSelect();
    }
  };

  return (
    <li
      role="menuitem"
      tabIndex={0}
      onKeyDown={handleKeyDown}
      onClick={onSelect}
    >
      Option
    </li>
  );
}
```

---

## 10. DEPLOYMENT PATTERNS

### 10.1 Next.js Deployment
```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  compress: true,
  productionBrowserSourceMaps: false,
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'example.com' },
    ],
  },
  headers: async () => {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
```

---

### 10.2 Docker Containerization
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Build application
COPY . .
RUN npm run build

# Production
ENV NODE_ENV=production
EXPOSE 3000

CMD ["npm", "start"]
```

---

## 11. PROJECT MILESTONES & DELIVERABLES

### Standard Project Milestones

#### Phase 1: Planning (Week 1)
- [ ] Requirements gathering
- [ ] Wireframes and mockups
- [ ] Technology selection
- [ ] Architecture design
- [ ] Project setup

#### Phase 2: Core Development (Weeks 2-4)
- [ ] Basic component structure
- [ ] Data model design
- [ ] Core functionality
- [ ] Basic styling
- [ ] Unit tests

#### Phase 3: Advanced Features (Weeks 5-6)
- [ ] State management
- [ ] API integration
- [ ] Advanced interactions
- [ ] Performance optimization
- [ ] Integration tests

#### Phase 4: Polish & Testing (Weeks 7-8)
- [ ] Bug fixes
- [ ] E2E testing
- [ ] Accessibility audit
- [ ] Performance audit
- [ ] Documentation

#### Phase 5: Deployment & Monitoring (Week 9+)
- [ ] Staging deployment
- [ ] Production deployment
- [ ] Monitoring setup
- [ ] Error tracking
- [ ] Analytics setup

---

## Document Summary

This practical guide covers:
- **11 progressive projects** from beginner to expert
- **Project selection matrix** for skill/duration matching
- **Common design patterns** with real code examples
- **API integration strategies**
- **Authentication patterns**
- **Testing approaches**
- **Performance techniques**
- **Accessibility implementation**
- **Deployment strategies**
- **Project milestones**

Use this for:
1. Guiding learners through realistic projects
2. Code generation examples in Claude Code plugin
3. Best practice recommendations
4. Architecture suggestions
5. Testing strategy definitions
6. Deployment guidance

