---
name: react-development
description: Build modern React applications with hooks, state management, and best practices. Use when working with React components, JSX, or React-specific patterns.
---

# React Development

Master modern React development with hooks, component patterns, and ecosystem best practices.

## Quick Start

### Functional Component with Hooks
```typescript
import { useState, useEffect } from 'react';

interface User {
  id: number;
  name: string;
}

export function UserProfile({ userId }: { userId: number }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => {
        setUser(data);
        setLoading(false);
      });
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (!user) return <div>User not found</div>;

  return (
    <div className="user-profile">
      <h1>{user.name}</h1>
    </div>
  );
}
```

## Essential Hooks

### useState - State Management
```typescript
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<string[]>([]);

// Functional updates
setCount(prev => prev + 1);
setItems(prev => [...prev, 'new item']);
```

### useEffect - Side Effects
```typescript
// Run once on mount
useEffect(() => {
  fetchData();
}, []);

// Run when dependency changes
useEffect(() => {
  const subscription = subscribe(userId);
  return () => subscription.unsubscribe(); // Cleanup
}, [userId]);
```

### useMemo - Expensive Computations
```typescript
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);
```

### useCallback - Memoized Callbacks
```typescript
const handleClick = useCallback(() => {
  doSomething(a, b);
}, [a, b]);
```

### useRef - DOM References & Mutable Values
```typescript
const inputRef = useRef<HTMLInputElement>(null);
const countRef = useRef(0); // Persists without re-render

useEffect(() => {
  inputRef.current?.focus();
}, []);
```

### Custom Hooks
```typescript
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}

// Usage
const [name, setName] = useLocalStorage('name', '');
```

## State Management

### Context API
```typescript
// Create context
const ThemeContext = createContext<'light' | 'dark'>('light');

// Provider
function App() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  return (
    <ThemeContext.Provider value={theme}>
      <YourApp />
    </ThemeContext.Provider>
  );
}

// Consumer
function ThemedButton() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Click me</button>;
}
```

### Redux Toolkit (Recommended)
```typescript
import { createSlice, configureStore } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: state => { state.value += 1; },
    decrement: state => { state.value -= 1; },
  },
});

export const { increment, decrement } = counterSlice.actions;
export const store = configureStore({ reducer: counterSlice.reducer });
```

### Zustand (Lightweight Alternative)
```typescript
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));

function Counter() {
  const { count, increment } = useStore();
  return <button onClick={increment}>{count}</button>;
}
```

## Component Patterns

### Compound Components
```typescript
interface TabsContextType {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

export function Tabs({ children }: { children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState('');

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

Tabs.List = function TabList({ children }: { children: React.ReactNode }) {
  return <div className="tab-list">{children}</div>;
};

Tabs.Tab = function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  return (
    <button onClick={() => context?.setActiveTab(id)}>
      {children}
    </button>
  );
};
```

### Render Props
```typescript
function DataFetcher({ url, render }: {
  url: string;
  render: (data: any) => JSX.Element
}) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(url).then(res => res.json()).then(setData);
  }, [url]);

  return data ? render(data) : <div>Loading...</div>;
}

// Usage
<DataFetcher url="/api/users" render={(users) => (
  <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
)} />
```

## Performance Optimization

### React.memo
```typescript
const ExpensiveComponent = React.memo(({ data }: { data: Data }) => {
  return <div>{/* Expensive render */}</div>;
}, (prevProps, nextProps) => {
  return prevProps.data.id === nextProps.data.id; // Custom comparison
});
```

### Code Splitting & Lazy Loading
```typescript
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Virtualization for Large Lists
```typescript
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }: { items: string[] }) {
  return (
    <FixedSizeList
      height={500}
      itemCount={items.length}
      itemSize={35}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>{items[index]}</div>
      )}
    </FixedSizeList>
  );
}
```

## Testing

### React Testing Library
```typescript
import { render, screen, fireEvent } from '@testing-library/react';

test('counter increments on click', () => {
  render(<Counter />);

  const button = screen.getByRole('button');
  fireEvent.click(button);

  expect(screen.getByText('1')).toBeInTheDocument();
});
```

### Vitest + React
```typescript
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';

describe('UserProfile', () => {
  it('renders user name', () => {
    const { getByText } = render(<UserProfile name="John" />);
    expect(getByText('John')).toBeTruthy();
  });
});
```

## Best Practices

✅ **Use functional components** with hooks (not class components)
✅ **TypeScript** for type safety
✅ **Custom hooks** for reusable logic
✅ **Memoization** (useMemo, useCallback, React.memo) for performance
✅ **Code splitting** for faster initial load
✅ **Error boundaries** for graceful error handling
✅ **Proper dependency arrays** in useEffect
✅ **Keys** in lists (unique and stable)
✅ **Accessibility** (ARIA, semantic HTML, keyboard navigation)

## Common Pitfalls

❌ Missing dependencies in useEffect
❌ Mutating state directly
❌ Using index as key in dynamic lists
❌ Not cleaning up useEffect subscriptions
❌ Excessive re-renders (missing memoization)
❌ Prop drilling (use Context or state management)

## Resources

- [React Docs (Beta)](https://react.dev)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [React Patterns](https://reactpatterns.com/)
