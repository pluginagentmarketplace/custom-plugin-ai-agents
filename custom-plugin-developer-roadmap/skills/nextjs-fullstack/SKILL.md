---
name: nextjs-fullstack
description: Full-stack development with Next.js 14+ App Router, Server Components, Server Actions, data fetching, and caching strategies.
---

# Next.js Full-Stack Development

Build production-ready full-stack applications with Next.js. Master the App Router, Server Components, Server Actions, advanced data fetching patterns, and intelligent caching strategies.

## Quick Start

```typescript
// app/page.tsx - Server Component by default
import { Suspense } from 'react';
import { UserList } from './components/user-list';
import { UserListSkeleton } from './components/user-list-skeleton';

export default function Page() {
  return (
    <main>
      <h1>Users</h1>
      <Suspense fallback={<UserListSkeleton />}>
        <UserList />
      </Suspense>
    </main>
  );
}

// app/components/user-list.tsx - Server Component fetching data
import { db } from '@/lib/db';

interface User {
  id: string;
  name: string;
  email: string;
}

export async function UserList() {
  const users: User[] = await db.user.findMany();

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name} ({user.email})</li>
      ))}
    </ul>
  );
}

// app/actions.ts - Server Actions
'use server'

import { db } from '@/lib/db';
import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  const user = await db.user.create({ data: { name, email } });
  revalidatePath('/');

  return user;
}
```

## Key Concepts

### Server Components for Data Fetching

Server Components run only on the server and enable direct database access:

```typescript
// app/dashboard/page.tsx
import { db } from '@/lib/db';
import { cache } from 'react';

// Memoize database queries to avoid N+1 problems
const getUser = cache(async (userId: string) => {
  return await db.user.findUnique({ where: { id: userId } });
});

const getUserPosts = cache(async (userId: string) => {
  return await db.post.findMany({ where: { authorId: userId } });
});

interface DashboardPageProps {
  params: { userId: string };
}

export const revalidate = 60; // ISR: Revalidate every 60 seconds

export async function generateMetadata({ params }: DashboardPageProps) {
  const user = await getUser(params.userId);
  return { title: `${user.name}'s Dashboard` };
}

export default async function DashboardPage({ params }: DashboardPageProps) {
  const user = await getUser(params.userId);
  const posts = await getUserPosts(params.userId);

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Server Actions for Mutations

Server Actions handle form submissions and mutations securely:

```typescript
// app/actions.ts
'use server'

import { db } from '@/lib/db';
import { revalidatePath, revalidateTag } from 'next/cache';

// Form submission action
export async function updateUserProfile(formData: FormData) {
  const userId = formData.get('userId') as string;
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  try {
    const user = await db.user.update({
      where: { id: userId },
      data: { name, email },
    });

    // Revalidate cache after mutation
    revalidatePath(`/users/${userId}`);
    revalidateTag('user-profile');

    return { success: true, user };
  } catch (error) {
    return { success: false, error: 'Failed to update profile' };
  }
}

// Progressive enhancement with Client Component
// app/components/profile-form.tsx
'use client'

import { updateUserProfile } from '@/app/actions';
import { useActionState } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

export function ProfileForm({ user }: { user: User }) {
  const [state, formAction, isPending] = useActionState(updateUserProfile, null);

  return (
    <form action={formAction}>
      <input type="hidden" name="userId" value={user.id} />

      <label>
        Name:
        <input type="text" name="name" defaultValue={user.name} />
      </label>

      <label>
        Email:
        <input type="email" name="email" defaultValue={user.email} />
      </label>

      <button type="submit" disabled={isPending}>
        {isPending ? 'Saving...' : 'Save'}
      </button>

      {state?.error && <p style={{ color: 'red' }}>{state.error}</p>}
    </form>
  );
}
```

### Advanced Data Fetching and Caching

Implement sophisticated data fetching patterns:

```typescript
// lib/api.ts
const cache = new Map<string, { data: any; time: number }>();

export async function fetchWithCache<T>(
  url: string,
  options: { revalidate?: number; tags?: string[] } = {}
): Promise<T> {
  const cached = cache.get(url);
  const now = Date.now();

  if (cached && now - cached.time < (options.revalidate ?? 60000)) {
    return cached.data;
  }

  const response = await fetch(url, {
    next: { revalidate: options.revalidate, tags: options.tags },
  });

  if (!response.ok) throw new Error(`API error: ${response.status}`);

  const data = await response.json();
  cache.set(url, { data, time: now });
  return data;
}

// app/products/page.tsx - Using fetch with caching
import { fetchWithCache } from '@/lib/api';

interface Product {
  id: string;
  name: string;
  price: number;
}

export const revalidate = 3600; // Revalidate every hour

export async function generateStaticParams() {
  const products = await fetchWithCache<Product[]>('/api/products', {
    tags: ['products'],
  });

  return products.map((product) => ({ id: product.id }));
}

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await fetchWithCache<Product>(`/api/products/${params.id}`, {
    revalidate: 3600,
    tags: ['product', params.id],
  });

  return (
    <div>
      <h1>{product.name}</h1>
      <p>${product.price}</p>
    </div>
  );
}
```

## Common Patterns

### 1. API Routes for Backend Logic

```typescript
// app/api/users/route.ts - Endpoint for creating users
import { NextRequest, NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { name, email } = body;

    // Validate input
    if (!name || !email) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    const user = await db.user.create({
      data: { name, email },
    });

    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

// app/api/users/[id]/route.ts - Dynamic route
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await db.user.findUnique({
    where: { id: params.id },
  });

  if (!user) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  return NextResponse.json(user);
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await request.json();
  const user = await db.user.update({
    where: { id: params.id },
    data: body,
  });

  return NextResponse.json(user);
}
```

### 2. Middleware for Request Processing

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Check authentication
  const token = request.cookies.get('auth-token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Add custom headers
  const response = NextResponse.next();
  response.headers.set('X-Custom-Header', 'value');

  return response;
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};
```

### 3. Streaming with Suspense Boundaries

```typescript
// app/profile/page.tsx
import { Suspense } from 'react';
import { UserInfo } from './components/user-info';
import { UserPosts } from './components/user-posts';
import { UserInfoSkeleton, UserPostsSkeleton } from './components/skeletons';

export default function ProfilePage() {
  return (
    <div>
      <h1>Profile</h1>

      <Suspense fallback={<UserInfoSkeleton />}>
        <UserInfo />
      </Suspense>

      <Suspense fallback={<UserPostsSkeleton />}>
        <UserPosts />
      </Suspense>
    </div>
  );
}

// app/profile/components/user-info.tsx
import { db } from '@/lib/db';

export async function UserInfo() {
  await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate slow query
  const user = await db.user.findFirst();

  return (
    <div>
      <h2>{user?.name}</h2>
      <p>{user?.email}</p>
    </div>
  );
}
```

### 4. Client-Side Interactivity with 'use client'

```typescript
// app/components/counter.tsx
'use client'

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}

// app/page.tsx - Mix Server and Client Components
import { Counter } from './components/counter';
import { UserList } from './components/user-list'; // Server Component

export default function Home() {
  return (
    <main>
      <UserList />
      <Counter />
    </main>
  );
}
```

## Best Practices

✅ Use Server Components by default, opt-in to 'use client' only when needed
✅ Leverage `cache()` function to deduplicate requests within a single render
✅ Use `revalidatePath` and `revalidateTag` strategically to balance freshness and performance
✅ Implement proper error boundaries for resilient user experiences
✅ Use Suspense boundaries for progressive content loading
✅ Validate and sanitize all user input in Server Actions
✅ Use TypeScript for type-safe API routes and Server Actions

## Common Pitfalls

❌ Over-using 'use client' when Server Components would suffice
❌ Fetching data in loops instead of using batching or JOINs
❌ Forgetting to revalidate cache after mutations
❌ Using absolute timeouts instead of ISR for cache expiration
❌ Not handling errors in Server Actions gracefully
❌ Mixing Server and Client Component logic without clear boundaries

## Resources

- [Next.js App Router Documentation](https://nextjs.org/docs/app)
- [Server Components and Async Components](https://nextjs.org/docs/getting-started/react-essentials)
- [Data Fetching and Caching](https://nextjs.org/docs/app/building-your-application/data-fetching)
- [Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
- [Next.js Performance Optimization](https://nextjs.org/docs/app/building-your-application/optimizing)
