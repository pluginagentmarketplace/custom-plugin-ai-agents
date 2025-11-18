---
name: nodejs-api-development
description: Build scalable REST APIs with Node.js. Use when creating Express.js backends with proper error handling, validation, and database integration.
---

# Node.js API Development

Master modern Node.js backend development using Express.js with type-safe validation, ORM integration, and professional error handling patterns.

## Quick Start

```javascript
import express, { Express, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { prisma } from './db';

const app: Express = express();

app.use(express.json());

// Validation middleware
const validateBody = (schema: z.ZodSchema) =>
  (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ errors: result.error.issues });
    }
    req.body = result.data;
    next();
  };

// Error handling middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

## Key Concepts

### Async/Await Error Handling
```javascript
app.get('/users/:id', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const user = await prisma.user.findUniqueOrThrow({
      where: { id: req.params.id }
    });
    res.json(user);
  } catch (error) {
    if (error instanceof prisma.PrismaClientKnownRequestError) {
      return res.status(404).json({ error: 'User not found' });
    }
    next(error);
  }
});
```

### Middleware Composition
```javascript
const asyncHandler = (fn: Function) =>
  (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };

app.post('/users',
  validateBody(userSchema),
  asyncHandler(async (req: Request, res: Response) => {
    const user = await prisma.user.create({
      data: req.body
    });
    res.status(201).json(user);
  })
);
```

### Zod Validation with Prisma Integration
```javascript
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().min(18).optional()
});

type CreateUser = z.infer<typeof createUserSchema>;

app.post('/users',
  validateBody(createUserSchema),
  asyncHandler(async (req: Request<{}, {}, CreateUser>, res: Response) => {
    const user = await prisma.user.create({ data: req.body });
    res.status(201).json(user);
  })
);
```

## Common Patterns

### Repository Pattern with Prisma
```javascript
class UserRepository {
  async findById(id: string) {
    try {
      return await prisma.user.findUniqueOrThrow({ where: { id } });
    } catch (error) {
      throw new NotFoundError('User not found');
    }
  }

  async create(data: CreateUser) {
    return await prisma.user.create({ data });
  }

  async update(id: string, data: Partial<CreateUser>) {
    return await prisma.user.update({ where: { id }, data });
  }

  async delete(id: string) {
    return await prisma.user.delete({ where: { id } });
  }
}
```

### Request/Response Wrapper
```javascript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

const sendSuccess = <T>(res: Response, data: T, status = 200) => {
  res.status(status).json({ success: true, data } as ApiResponse<T>);
};

const sendError = (res: Response, error: string, status = 500) => {
  res.status(status).json({ success: false, error } as ApiResponse<null>);
};

app.get('/users/:id', asyncHandler(async (req: Request, res: Response) => {
  const user = await userRepository.findById(req.params.id);
  sendSuccess(res, user);
}));
```

### Database Transaction Pattern
```javascript
app.post('/orders', asyncHandler(async (req: Request, res: Response) => {
  const result = await prisma.$transaction(async (tx) => {
    const order = await tx.order.create({
      data: { userId: req.body.userId, status: 'pending' }
    });

    await tx.inventory.updateMany({
      where: { id: { in: req.body.itemIds } },
      data: { quantity: { decrement: 1 } }
    });

    return order;
  });

  sendSuccess(res, result, 201);
}));
```

## Best Practices

✅ Always wrap async route handlers with error handling middleware
✅ Use Zod schemas for request validation and type safety
✅ Implement repository pattern for database operations
✅ Use Prisma transactions for multi-step operations
✅ Return consistent API response formats
✅ Log errors with context (request ID, user ID, etc.)
✅ Use environment variables for configuration
✅ Implement graceful shutdown for database connections

## Common Pitfalls

❌ Not handling async/await errors (unhandled promise rejections)
❌ Mixing validation logic in route handlers instead of middleware
❌ Executing N+1 queries without Prisma includes/selects
❌ Returning sensitive data in error messages
❌ Not validating request body shape before processing
❌ Missing transaction handling for multi-step operations
❌ Hardcoding configuration values instead of using env variables

## Resources

- [Express.js Official Documentation](https://expressjs.com/)
- [Zod Type-Safe Validation](https://zod.dev/)
- [Prisma ORM Guide](https://www.prisma.io/docs/)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [TypeScript with Express](https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html)
