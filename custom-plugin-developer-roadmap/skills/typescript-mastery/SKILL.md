---
name: typescript-mastery
description: Advanced TypeScript patterns including generics, utility types, strict mode, and type inference for production code.
---

# TypeScript Mastery

Master advanced TypeScript features to build type-safe, maintainable applications. Learn to leverage generics, utility types, and strict mode for robust type inference and error prevention.

## Quick Start

```typescript
// Generic function with constraints
function merge<T extends object, U extends object>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}

const result = merge({ name: 'John' }, { age: 30 });
// result type: { name: string } & { age: number }

// Utility types for common transformations
type User = { id: number; name: string; email: string };
type UserPreview = Pick<User, 'id' | 'name'>;
type PartialUser = Partial<User>;
type ReadonlyUser = Readonly<User>;

// Conditional types for type inference
type IsString<T> = T extends string ? true : false;
type A = IsString<'hello'>; // true
type B = IsString<42>; // false
```

## Key Concepts

### Generics and Type Parameters

Generics allow you to write reusable code that works with multiple types while maintaining type safety:

```typescript
// Generic interface
interface Repository<T> {
  getAll(): Promise<T[]>;
  getById(id: string): Promise<T | null>;
  create(item: T): Promise<T>;
  update(id: string, item: Partial<T>): Promise<T>;
}

// Generic class implementation
class UserRepository implements Repository<User> {
  async getAll(): Promise<User[]> {
    // implementation
    return [];
  }

  async getById(id: string): Promise<User | null> {
    // implementation
    return null;
  }

  async create(item: User): Promise<User> {
    // implementation
    return item;
  }

  async update(id: string, item: Partial<User>): Promise<User> {
    // implementation
    return { id: 1, name: '', email: '', ...item };
  }
}

// Generic constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user: User = { id: 1, name: 'John', email: 'john@example.com' };
const name = getProperty(user, 'name'); // string
```

### Utility Types for Type Transformation

Built-in utility types help transform types for common patterns:

```typescript
// Record: Map keys to values
type UserRole = 'admin' | 'user' | 'guest';
const permissions: Record<UserRole, string[]> = {
  admin: ['read', 'write', 'delete'],
  user: ['read', 'write'],
  guest: ['read'],
};

// Mapped types for creating new types
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type UserGetters = Getters<User>;
// Results in: {
//   getId: () => number;
//   getName: () => string;
//   getEmail: () => string;
// }

// Template literal types for string unions
type HttpMethod = 'get' | 'post' | 'put' | 'delete';
type URLPath = `/${string}`;
type ApiRoute = `${HttpMethod} ${URLPath}`;

const route: ApiRoute = 'get /users'; // valid
// const invalid: ApiRoute = 'patch /users'; // error
```

### Strict Mode and Type Inference

Enable strict mode and leverage type inference for safer code:

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}

// Type inference with const
const user = { id: 1, name: 'John' } as const;
// type user = {
//   readonly id: 1;
//   readonly name: "John";
// }

// Infer types from values
const createUser = (data: { name: string; age: number }) => ({
  ...data,
  id: Math.random(),
  createdAt: new Date(),
});

type NewUser = ReturnType<typeof createUser>;
// type NewUser = {
//   name: string;
//   age: number;
//   id: number;
//   createdAt: Date;
// }
```

## Common Patterns

### 1. Function Overloading

```typescript
// Overload signatures
function process(data: string): string;
function process(data: number): number;
function process(data: boolean): boolean;

// Implementation
function process(data: string | number | boolean): string | number | boolean {
  if (typeof data === 'string') {
    return data.toUpperCase();
  } else if (typeof data === 'number') {
    return data * 2;
  }
  return !data;
}

const strResult = process('hello'); // string
const numResult = process(5); // number
```

### 2. Discriminated Unions

```typescript
type Success<T> = {
  status: 'success';
  data: T;
};

type Error = {
  status: 'error';
  message: string;
};

type Result<T> = Success<T> | Error;

function handleResult<T>(result: Result<T>): void {
  switch (result.status) {
    case 'success':
      console.log(result.data); // T
      break;
    case 'error':
      console.log(result.message); // string
      break;
  }
}
```

### 3. Generic Constraints with Conditional Types

```typescript
// Extract return type from function
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

// Filter object keys by value type
type KeysOfType<T, U> = {
  [K in keyof T]: T[K] extends U ? K : never;
}[keyof T];

type StringKeys = KeysOfType<User, string>; // 'name' | 'email'

// Async operation handler
type AsyncFunction<T> = () => Promise<T>;
type Awaited<T> = T extends Promise<infer U> ? U : T;

const fetchUser = async (): Promise<User> => ({ id: 1, name: 'John', email: 'john@example.com' });
type FetchResult = Awaited<ReturnType<typeof fetchUser>>; // User
```

### 4. Builder Pattern with Generics

```typescript
class QueryBuilder<T> {
  private filters: ((item: T) => boolean)[] = [];

  where(predicate: (item: T) => boolean): QueryBuilder<T> {
    this.filters.push(predicate);
    return this;
  }

  execute(items: T[]): T[] {
    return items.filter(item => this.filters.every(f => f(item)));
  }
}

const users: User[] = [
  { id: 1, name: 'John', email: 'john@example.com' },
  { id: 2, name: 'Jane', email: 'jane@example.com' },
];

const results = new QueryBuilder<User>()
  .where(u => u.name.includes('J'))
  .where(u => u.id > 1)
  .execute(users);
```

## Best Practices

✅ Use `strict: true` in tsconfig.json to catch errors at compile time
✅ Leverage `as const` for literal type inference with immutable data
✅ Create reusable generic utilities and share them across your codebase
✅ Use discriminated unions for type-safe handling of multiple states
✅ Prefer `keyof` and type inference over manual union types
✅ Document generic type parameters with meaningful names (T, K, V, etc.)

## Common Pitfalls

❌ Using `any` type to bypass type checking - reduces safety and IDE support
❌ Over-constraining generics making them less reusable
❌ Forgetting that conditional types are evaluated at compile time only
❌ Ignoring strict mode settings - allows unsafe code patterns to slip through

## Resources

- [TypeScript Handbook - Advanced Types](https://www.typescriptlang.org/docs/handbook/2/types-from-types.html)
- [TypeScript Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)
- [Effective TypeScript by Dan Vanderkam](https://effectivetypescript.com/)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
