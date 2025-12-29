---
name: performance-optimization
description: Web performance optimization including Core Web Vitals, code splitting, image optimization, lazy loading, and memoization.
---

# Performance Optimization

Build high-performance web applications by mastering Core Web Vitals, code splitting, image optimization, lazy loading, and memoization techniques.

## Quick Start

```typescript
// React component with performance optimization
import React, { useMemo, useCallback, lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

interface User {
  id: number;
  name: string;
}

interface Props {
  users: User[];
  onSelect: (user: User) => void;
}

export const UserList = React.memo(function UserList({ users, onSelect }: Props) {
  // Memoize expensive computation
  const sortedUsers = useMemo(() => {
    return [...users].sort((a, b) => a.name.localeCompare(b.name));
  }, [users]);

  // Memoize callback to prevent unnecessary re-renders
  const handleSelect = useCallback(
    (user: User) => {
      onSelect(user);
    },
    [onSelect]
  );

  return (
    <ul>
      {sortedUsers.map(user => (
        <li key={user.id} onClick={() => handleSelect(user)}>
          {user.name}
        </li>
      ))}
    </ul>
  );
});

// Lazy load components for code splitting
export function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}

// Image optimization
export function OptimizedImage({ src, alt }: { src: string; alt: string }) {
  return (
    <picture>
      <source srcSet={`${src}?w=400&q=80&fmt=webp`} type="image/webp" />
      <img
        src={`${src}?w=400&q=80`}
        alt={alt}
        width="400"
        height="300"
        loading="lazy"
      />
    </picture>
  );
}
```

## Key Concepts

### Core Web Vitals Metrics

Monitor and optimize the three key metrics that affect user experience:

```typescript
// Measure Core Web Vitals
class WebVitalsTracker {
  private metrics: Record<string, number> = {};

  // Largest Contentful Paint (LCP)
  // Measures loading performance
  measureLCP(): void {
    if ('PerformanceObserver' in window) {
      try {
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          this.metrics['LCP'] = lastEntry.renderTime || lastEntry.loadTime;
        });

        observer.observe({ entryTypes: ['largest-contentful-paint'] });
      } catch (e) {
        // Observer not supported
      }
    }
  }

  // First Input Delay (FID) / Interaction to Next Paint (INP)
  // Measures interactivity
  measureINP(): void {
    if ('PerformanceObserver' in window) {
      try {
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const longestEntry = entries.reduce((prev, current) =>
            (current.duration > prev.duration) ? current : prev
          );
          this.metrics['INP'] = longestEntry.duration;
        });

        observer.observe({ entryTypes: ['event'] });
      } catch (e) {
        // Observer not supported
      }
    }
  }

  // Cumulative Layout Shift (CLS)
  // Measures visual stability
  measureCLS(): void {
    if ('PerformanceObserver' in window) {
      try {
        let clsValue = 0;
        const observer = new PerformanceObserver((list) => {
          for (const entry of list.getEntries()) {
            if ((entry as any).hadRecentInput) continue;
            clsValue += (entry as any).value;
          }
          this.metrics['CLS'] = clsValue;
        });

        observer.observe({ entryTypes: ['layout-shift'] });
      } catch (e) {
        // Observer not supported
      }
    }
  }

  getMetrics(): Record<string, number> {
    return this.metrics;
  }

  reportMetrics(): void {
    console.log('Core Web Vitals:', this.metrics);
    // Send to analytics service
  }
}

// Usage
const tracker = new WebVitalsTracker();
tracker.measureLCP();
tracker.measureINP();
tracker.measureCLS();
```

### Code Splitting and Lazy Loading

Split your bundles to load only what's needed:

```typescript
// Next.js code splitting
import dynamic from 'next/dynamic';

// Lazy load component with loading state
const DynamicComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>,
  ssr: false, // Load only on client side if needed
});

export default function Page() {
  return <DynamicComponent />;
}

// Route-based code splitting in React Router
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

export function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

// Webpack bundle splitting configuration
// webpack.config.js
export default {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10,
        },
        common: {
          minChunks: 2,
          priority: 5,
          reuseExistingChunk: true,
        },
      },
    },
  },
};
```

### Image Optimization and Responsive Images

Optimize images for better performance:

```typescript
// Responsive images with srcset
interface ResponsiveImageProps {
  src: string;
  alt: string;
  maxWidth?: number;
}

export function ResponsiveImage({
  src,
  alt,
  maxWidth = 800,
}: ResponsiveImageProps) {
  // Generate different image sizes
  const imageSizes = [320, 640, 960, 1280];
  const srcSet = imageSizes
    .filter(size => size <= maxWidth)
    .map(size => `${src}?w=${size}&q=80 ${size}w`)
    .join(', ');

  return (
    <img
      src={`${src}?w=800&q=80`}
      srcSet={srcSet}
      alt={alt}
      sizes={`(max-width: 768px) 100vw, (max-width: 1200px) 80vw, ${maxWidth}px`}
      width={maxWidth}
      height="auto"
      loading="lazy"
      decoding="async"
    />
  );
}

// Picture element with WebP format
export function ModernImage({ src, alt }: { src: string; alt: string }) {
  return (
    <picture>
      {/* WebP format for modern browsers */}
      <source
        srcSet={`${src}?fmt=webp&w=400 400w, ${src}?fmt=webp&w=800 800w`}
        type="image/webp"
      />

      {/* JPEG fallback */}
      <source
        srcSet={`${src}?fmt=jpg&w=400 400w, ${src}?fmt=jpg&w=800 800w`}
        type="image/jpeg"
      />

      <img
        src={`${src}?fmt=jpg&w=800`}
        alt={alt}
        loading="lazy"
        decoding="async"
      />
    </picture>
  );
}
```

## Common Patterns

### 1. Memoization for Expensive Computations

```typescript
// React memoization
import { useMemo, useCallback, memo } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
}

interface Props {
  users: User[];
  selectedUserId: number;
  onSelect: (id: number) => void;
}

// Memoize component to prevent unnecessary re-renders
export const UserSelector = memo(function UserSelector({
  users,
  selectedUserId,
  onSelect,
}: Props) {
  // Memoize expensive sorting operation
  const sortedUsers = useMemo(() => {
    console.log('Sorting users...');
    return [...users].sort((a, b) => a.name.localeCompare(b.name));
  }, [users]);

  // Memoize callback
  const handleSelect = useCallback(
    (id: number) => {
      onSelect(id);
    },
    [onSelect]
  );

  return (
    <select value={selectedUserId} onChange={e => handleSelect(Number(e.target.value))}>
      {sortedUsers.map(user => (
        <option key={user.id} value={user.id}>
          {user.name}
        </option>
      ))}
    </select>
  );
});

// Vue 3 memoization
import { computed, shallowRef } from 'vue';

export function useUsers(users: Ref<User[]>) {
  // Memoized computation in Vue
  const sortedUsers = computed(() => {
    console.log('Sorting users...');
    return [...users.value].sort((a, b) => a.name.localeCompare(b.name));
  });

  return { sortedUsers };
}
```

### 2. Intersection Observer for Lazy Loading

```typescript
// Lazy load images and content as they enter viewport
export function useLazyLoad(ref: RefObject<HTMLElement>) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.unobserve(entry.target);
        }
      },
      { threshold: 0.1 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, [ref]);

  return isVisible;
}

// Usage
export function LazyImage({ src, alt }: { src: string; alt: string }) {
  const ref = useRef<HTMLImageElement>(null);
  const isVisible = useLazyLoad(ref);

  return (
    <img
      ref={ref}
      src={isVisible ? src : 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'}
      alt={alt}
      loading="lazy"
    />
  );
}

// Virtual scrolling for large lists
import { FixedSizeList as List } from 'react-window';

interface Item {
  id: number;
  name: string;
}

export function VirtualList({ items }: { items: Item[] }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      {items[index].name}
    </div>
  );

  return (
    <List
      height={600}
      itemCount={items.length}
      itemSize={35}
      width="100%"
    >
      {Row}
    </List>
  );
}
```

### 3. Service Worker for Caching

```typescript
// service-worker.ts
const CACHE_NAME = 'v1';
const urlsToCache = [
  '/',
  '/styles/main.css',
  '/scripts/main.js',
];

// Install event
self.addEventListener('install', (event: ExtendableEvent) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Fetch event with cache-first strategy
self.addEventListener('fetch', (event: FetchEvent) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      // Return cached version if available
      if (response) {
        return response;
      }

      return fetch(event.request).then((response) => {
        // Cache new requests
        if (!response || response.status !== 200) {
          return response;
        }

        const responseToCache = response.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });

        return response;
      });
    })
  );
});

// Register service worker in main app
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js')
    .then(registration => console.log('SW registered:', registration))
    .catch(error => console.log('SW registration failed:', error));
}
```

### 4. Debouncing and Throttling

```typescript
// Debounce function for expensive operations
function debounce<T extends (...args: any[]) => any>(
  func: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>;

  return function (...args: Parameters<T>) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}

// Usage in React search component
export function SearchUsers() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<User[]>([]);

  // Debounce search to avoid excessive API calls
  const debouncedSearch = useMemo(
    () => debounce(async (q: string) => {
      if (!q) return;
      const response = await fetch(`/api/users?q=${q}`);
      const data = await response.json();
      setResults(data);
    }, 300),
    []
  );

  return (
    <div>
      <input
        value={query}
        onChange={e => {
          setQuery(e.target.value);
          debouncedSearch(e.target.value);
        }}
        placeholder="Search users..."
      />
      <ul>
        {results.map(user => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}

// Throttle function for frequent events
function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;

  return function (...args: Parameters<T>) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// Usage for scroll events
const handleScroll = throttle(() => {
  console.log('Scroll event - throttled');
}, 1000);

window.addEventListener('scroll', handleScroll);
```

## Best Practices

✅ Monitor Core Web Vitals with real user monitoring (RUM)
✅ Use code splitting to deliver only necessary JavaScript
✅ Optimize images with proper formats, sizes, and lazy loading
✅ Implement memoization for expensive computations
✅ Use Service Workers for offline caching strategies
✅ Debounce/throttle expensive event handlers
✅ Measure performance improvements with Lighthouse and WebPageTest
✅ Enable HTTP/2 Server Push for critical resources

## Common Pitfalls

❌ Not measuring actual user performance with RUM data
❌ Over-memoizing trivial computations (adds overhead)
❌ Loading all images eagerly instead of lazy loading
❌ Large bundle sizes without code splitting
❌ Syncing state unnecessarily causing excessive renders
❌ Not caching static assets properly
❌ Ignoring third-party script performance impact

## Resources

- [Web Vitals by Google](https://web.dev/vitals/)
- [Lighthouse Documentation](https://developers.google.com/web/tools/lighthouse)
- [MDN Performance Guide](https://developer.mozilla.org/en-US/docs/Web/Performance)
- [WebPageTest Performance Testing](https://www.webpagetest.org/)
- [Bundle Analyzer - Webpack](https://github.com/webpack-bundle-analyzer/webpack-bundle-analyzer)
