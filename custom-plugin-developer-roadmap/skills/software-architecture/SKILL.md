---
name: software-architecture
description: Master design patterns, SOLID principles, and architectural styles like clean architecture, DDD, and microservices. Use when designing application structure and implementing scalable system components.
---

# Software Architecture

Master fundamental design patterns, SOLID principles, and modern architectural approaches to build maintainable and scalable systems.

## Quick Start

### Design Patterns Overview

Design patterns are reusable solutions to common design problems in software.

```
┌─────────────────────────────────────────────────┐
│          Design Patterns Categories             │
├─────────────────────────────────────────────────┤
│ Creational: Object creation mechanisms          │
│ Structural: Object composition and relationships │
│ Behavioral: Object interaction and responsibility│
└─────────────────────────────────────────────────┘
```

## Creational Patterns

### Factory Pattern

Encapsulates object creation without specifying classes directly.

```typescript
// Abstract product
interface DataSource {
  connect(): void;
  execute(query: string): any;
}

// Concrete products
class PostgresDatabase implements DataSource {
  connect() { console.log('Connected to PostgreSQL'); }
  execute(query: string) { /* ... */ }
}

class MongoDatabase implements DataSource {
  connect() { console.log('Connected to MongoDB'); }
  execute(query: string) { /* ... */ }
}

// Factory
class DatabaseFactory {
  static create(type: 'postgres' | 'mongo'): DataSource {
    switch (type) {
      case 'postgres':
        return new PostgresDatabase();
      case 'mongo':
        return new MongoDatabase();
      default:
        throw new Error('Unknown database type');
    }
  }
}

// Usage
const db = DatabaseFactory.create('postgres');
db.connect();
```

### Singleton Pattern

Ensures a class has only one instance with global access.

```typescript
class Logger {
  private static instance: Logger;
  private logs: string[] = [];

  private constructor() {}

  static getInstance(): Logger {
    if (!Logger.instance) {
      Logger.instance = new Logger();
    }
    return Logger.instance;
  }

  log(message: string) {
    this.logs.push(message);
    console.log(message);
  }

  getLogs(): string[] {
    return [...this.logs];
  }
}

// Usage
const logger1 = Logger.getInstance();
const logger2 = Logger.getInstance();
logger1.log('Message');
console.log(logger1 === logger2); // true
```

## Behavioral Patterns

### Observer Pattern

Defines a one-to-many dependency between objects where state change triggers notifications.

```typescript
interface Observer {
  update(data: any): void;
}

class EventEmitter {
  private subscribers: Map<string, Observer[]> = new Map();

  subscribe(event: string, observer: Observer) {
    if (!this.subscribers.has(event)) {
      this.subscribers.set(event, []);
    }
    this.subscribers.get(event)!.push(observer);
  }

  unsubscribe(event: string, observer: Observer) {
    const observers = this.subscribers.get(event);
    if (observers) {
      const index = observers.indexOf(observer);
      if (index > -1) observers.splice(index, 1);
    }
  }

  emit(event: string, data: any) {
    const observers = this.subscribers.get(event);
    if (observers) {
      observers.forEach(obs => obs.update(data));
    }
  }
}

// Concrete observers
class EmailNotifier implements Observer {
  update(data: any) {
    console.log(`Sending email: ${data.message}`);
  }
}

class SlackNotifier implements Observer {
  update(data: any) {
    console.log(`Posting to Slack: ${data.message}`);
  }
}

// Usage
const emitter = new EventEmitter();
emitter.subscribe('order.created', new EmailNotifier());
emitter.subscribe('order.created', new SlackNotifier());
emitter.emit('order.created', { message: 'Order #123 created' });
```

### Strategy Pattern

Encapsulates algorithms in separate classes to make them interchangeable.

```typescript
interface PaymentStrategy {
  pay(amount: number): void;
}

class CreditCardPayment implements PaymentStrategy {
  pay(amount: number) {
    console.log(`Processing $${amount} via Credit Card`);
    // Process credit card payment
  }
}

class PayPalPayment implements PaymentStrategy {
  pay(amount: number) {
    console.log(`Processing $${amount} via PayPal`);
    // Process PayPal payment
  }
}

class CryptoPayment implements PaymentStrategy {
  pay(amount: number) {
    console.log(`Processing $${amount} via Cryptocurrency`);
    // Process crypto payment
  }
}

class Order {
  private strategy: PaymentStrategy;

  constructor(strategy: PaymentStrategy) {
    this.strategy = strategy;
  }

  setPaymentStrategy(strategy: PaymentStrategy) {
    this.strategy = strategy;
  }

  checkout(amount: number) {
    this.strategy.pay(amount);
  }
}

// Usage
const order = new Order(new CreditCardPayment());
order.checkout(99.99);
order.setPaymentStrategy(new PayPalPayment());
order.checkout(49.99);
```

## SOLID Principles

### Single Responsibility Principle (SRP)

A class should have only one reason to change.

```typescript
// Bad: Mixing responsibilities
class User {
  name: string;
  email: string;

  save() { /* Save to DB */ }
  sendEmail() { /* Send email */ }
  generateReport() { /* Generate report */ }
}

// Good: Single responsibility
class User {
  name: string;
  email: string;
}

class UserRepository {
  save(user: User) { /* Save to DB */ }
}

class EmailService {
  send(email: string, message: string) { /* Send email */ }
}

class UserReportGenerator {
  generate(user: User) { /* Generate report */ }
}
```

### Open/Closed Principle (OCP)

Software entities should be open for extension, closed for modification.

```typescript
// Bad: Must modify shape handler for new shapes
class AreaCalculator {
  calculateArea(shape: any): number {
    if (shape instanceof Circle) return Math.PI * shape.radius ** 2;
    if (shape instanceof Rectangle) return shape.width * shape.height;
    throw new Error('Unknown shape');
  }
}

// Good: Extension without modification
interface Shape {
  area(): number;
}

class Circle implements Shape {
  constructor(private radius: number) {}
  area() { return Math.PI * this.radius ** 2; }
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  area() { return this.width * this.height; }
}

class Triangle implements Shape {
  constructor(private base: number, private height: number) {}
  area() { return (this.base * this.height) / 2; }
}

class AreaCalculator {
  calculateArea(shapes: Shape[]): number {
    return shapes.reduce((sum, shape) => sum + shape.area(), 0);
  }
}
```

### Liskov Substitution Principle (LSP)

Derived classes should be substitutable for their base classes.

```typescript
// Bad: Circle doesn't fit Rectangle contract
class Rectangle {
  setWidth(w: number) { this.width = w; }
  setHeight(h: number) { this.height = h; }
  area() { return this.width * this.height; }
}

class Circle extends Rectangle {
  setRadius(r: number) { this.radius = r; }
  // Violates contract - setting width/height doesn't make sense for circle
}

// Good: Use composition or proper inheritance
interface Shape {
  area(): number;
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  area() { return this.width * this.height; }
}

class Circle implements Shape {
  constructor(private radius: number) {}
  area() { return Math.PI * this.radius ** 2; }
}
```

### Interface Segregation Principle (ISP)

Clients shouldn't depend on interfaces they don't use.

```typescript
// Bad: Forcing unnecessary method implementations
interface Worker {
  work(): void;
  eat(): void;
}

class Robot implements Worker {
  work() { /* ... */ }
  eat() { /* Robot doesn't eat - forced to implement */ }
}

// Good: Segregated interfaces
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

class Robot implements Workable {
  work() { /* ... */ }
}

class Human implements Workable, Eatable {
  work() { /* ... */ }
  eat() { /* ... */ }
}
```

### Dependency Inversion Principle (DIP)

High-level modules shouldn't depend on low-level modules; both should depend on abstractions.

```typescript
// Bad: High-level depends on low-level
class EmailService {
  send(to: string, message: string) { /* ... */ }
}

class UserRegistration {
  constructor(private emailService: EmailService) {}
  register(email: string) {
    this.emailService.send(email, 'Welcome!');
  }
}

// Good: Both depend on abstraction
interface NotificationService {
  send(to: string, message: string): void;
}

class EmailService implements NotificationService {
  send(to: string, message: string) { /* ... */ }
}

class SMSService implements NotificationService {
  send(to: string, message: string) { /* ... */ }
}

class UserRegistration {
  constructor(private notificationService: NotificationService) {}
  register(email: string) {
    this.notificationService.send(email, 'Welcome!');
  }
}
```

## Architectural Styles

### Clean Architecture

```
┌──────────────────────────────────────┐
│        Presentation Layer            │
│    (Controllers, Views, UI)          │
├──────────────────────────────────────┤
│         Application Layer            │
│       (Use Cases, Services)          │
├──────────────────────────────────────┤
│         Domain Layer                 │
│    (Entities, Business Rules)        │
├──────────────────────────────────────┤
│        Infrastructure Layer          │
│  (DB, APIs, External Services)       │
└──────────────────────────────────────┘

Dependencies flow INWARD
```

### Domain-Driven Design (DDD)

```
┌─────────────────────────────────────────────┐
│           Bounded Contexts                  │
├─────────────────────────────────────────────┤
│ Orders     │ Inventory │ Shipping │ Billing│
│ Aggregate  │ Aggregate │ Aggregate│Aggregate│
│            │           │          │        │
│ Entity     │ Entity    │ Entity   │Entity  │
│ Value Obj  │ Value Obj │ Value Obj│Value O │
└─────────────────────────────────────────────┘
```

Key concepts:
- **Entity**: Object with identity that persists over time
- **Value Object**: Immutable object with no identity
- **Aggregate**: Cluster of entities/value objects treated as single unit
- **Bounded Context**: Explicit boundary around model
- **Repository**: Abstraction for data access

### Microservices Architecture

```
┌──────────────────────────────────────────────────┐
│                  API Gateway                     │
└──────────────────────────────────────────────────┘
  │              │              │              │
  ▼              ▼              ▼              ▼
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│ Auth   │  │ Order  │  │Inventory│ │Shipping│
│Service │  │Service │  │Service  │ │Service │
└────────┘  └────────┘  └────────┘  └────────┘
  │ DB        │ DB       │ DB       │ DB
  │           │          │          │
┌─────────────────────────────────────────┐
│    Message Broker (Event Bus)           │
└─────────────────────────────────────────┘
```

### Monolithic Architecture

```
┌──────────────────────────────────────┐
│           Single Application         │
├──────────────────────────────────────┤
│ Auth │ Orders │ Inventory │ Shipping │
├──────────────────────────────────────┤
│         Single Database              │
└──────────────────────────────────────┘
```

## Microservices vs Monolith

| Aspect | Microservices | Monolith |
|--------|---------------|----------|
| Scalability | Individual service scaling | Entire app scaling |
| Deployment | Independent deployment | Full app redeployment |
| Technology | Mix and match stacks | Single tech stack |
| Complexity | High operational complexity | Lower operational complexity |
| Communication | Network calls (latency) | In-process (fast) |
| Development | Distributed development | Centralized development |
| Testing | Complex integration tests | Simpler testing |

## Best Practices

✅ **Prioritize cohesion** - Related functionality stays together
✅ **Keep boundaries clear** - Well-defined interfaces and contracts
✅ **Use dependency injection** - Decouple dependencies
✅ **Document architecture** - ADRs (Architecture Decision Records)
✅ **Regular refactoring** - Keep code quality high
✅ **Test at multiple levels** - Unit, integration, E2E tests
✅ **Measure and monitor** - Understand system behavior

## Common Pitfalls

❌ Mixing concerns - Violating SRP
❌ Tight coupling - Hard to test and maintain
❌ Over-engineering - Too much abstraction
❌ Inconsistent patterns - Unclear code intent
❌ Ignoring scalability - Problems emerge at scale
❌ Poor documentation - Hard to understand design decisions

## Resources

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns)
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design by Eric Evans](https://domainlanguage.com/ddd/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Microservices Patterns](https://microservices.io/)
