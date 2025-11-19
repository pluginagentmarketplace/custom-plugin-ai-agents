---
name: api-security
description: Secure APIs with JWT, rate limiting, input validation, and CORS. Use when implementing authentication, authorization, and protection mechanisms.
---

# API Security

Implement comprehensive security measures including JWT authentication, rate limiting, input validation, CORS, security headers, and OAuth 2.0 integration.

## Quick Start

```typescript
import express, { Express, Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import rateLimit from 'express-rate-limit';
import helmet from 'helmet';

const app: Express = express();

// Security headers
app.use(helmet());

// CORS configuration
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', process.env.ALLOWED_ORIGIN);
  res.header('Access-Control-Allow-Credentials', 'true');
  res.header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type,Authorization');
  next();
});

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: 'Too many requests from this IP'
});
app.use(limiter);

app.post('/login', async (req: Request, res: Response) => {
  try {
    const token = jwt.sign(
      { userId: user.id, email: user.email },
      process.env.JWT_SECRET!,
      { expiresIn: '24h' }
    );
    res.json({ token });
  } catch (error) {
    res.status(500).json({ error: 'Authentication failed' });
  }
});

app.listen(3000);
```

## Key Concepts

### JWT Authentication with Refresh Tokens
```typescript
interface TokenPayload {
  userId: string;
  email: string;
}

class AuthService {
  private readonly accessTokenSecret = process.env.ACCESS_TOKEN_SECRET!;
  private readonly refreshTokenSecret = process.env.REFRESH_TOKEN_SECRET!;

  generateTokens(payload: TokenPayload) {
    const accessToken = jwt.sign(payload, this.accessTokenSecret, {
      expiresIn: '15m',
      algorithm: 'HS256'
    });

    const refreshToken = jwt.sign(payload, this.refreshTokenSecret, {
      expiresIn: '7d',
      algorithm: 'HS256'
    });

    return { accessToken, refreshToken };
  }

  verifyAccessToken(token: string): TokenPayload {
    try {
      return jwt.verify(token, this.accessTokenSecret) as TokenPayload;
    } catch (error) {
      throw new UnauthorizedError('Invalid or expired token');
    }
  }

  refreshAccessToken(refreshToken: string): string {
    try {
      const payload = jwt.verify(refreshToken, this.refreshTokenSecret) as TokenPayload;
      const newAccessToken = jwt.sign(payload, this.accessTokenSecret, {
        expiresIn: '15m'
      });
      return newAccessToken;
    } catch (error) {
      throw new UnauthorizedError('Invalid refresh token');
    }
  }
}

// Middleware for protected routes
const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const payload = authService.verifyAccessToken(token);
    (req as any).user = payload;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};
```

### Input Validation and Sanitization
```typescript
import { z } from 'zod';
import mongoSanitize from 'express-mongo-sanitize';
import xss from 'xss-clean';

// Sanitization middleware
app.use(mongoSanitize()); // Prevent NoSQL injection
app.use(xss()); // Prevent XSS attacks

// Strict validation schemas
const createUserSchema = z.object({
  email: z.string().email().max(255),
  password: z.string().min(12).regex(
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/,
    'Password must contain uppercase, lowercase, number, and special character'
  ),
  name: z.string().min(2).max(100).regex(
    /^[a-zA-Z\s'-]+$/,
    'Name contains invalid characters'
  )
});

const validateRequest = (schema: z.ZodSchema) =>
  (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({
        error: 'Validation failed',
        issues: result.error.issues
      });
    }
    req.body = result.data;
    next();
  };

app.post('/register',
  validateRequest(createUserSchema),
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = await prisma.user.create({
        data: {
          email: req.body.email,
          name: req.body.name,
          password: await bcrypt.hash(req.body.password, 12)
        }
      });
      res.status(201).json({ userId: user.id });
    } catch (error) {
      next(error);
    }
  }
);
```

### Rate Limiting Strategies
```typescript
import RedisStore from 'rate-limit-redis';
import redis from 'redis';

const redisClient = redis.createClient();

// Global rate limiting
const globalLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:global:'
  }),
  windowMs: 15 * 60 * 1000,
  max: 100
});

// Per-user rate limiting
const userLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:user:'
  }),
  keyGenerator: (req: Request) => (req as any).user?.userId || req.ip,
  windowMs: 60 * 1000,
  max: 30
});

// Strict limits on sensitive endpoints
const authLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:auth:'
  }),
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true
});

app.post('/login', globalLimiter, authLimiter, loginHandler);
app.post('/api/data', globalLimiter, userLimiter, authMiddleware, dataHandler);
```

### OAuth 2.0 Implementation
```typescript
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';

passport.use(new GoogleStrategy({
  clientID: process.env.GOOGLE_CLIENT_ID!,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  callbackURL: '/auth/google/callback'
}, async (accessToken, refreshToken, profile, done) => {
  try {
    let user = await prisma.user.findUnique({
      where: { email: profile.emails![0].value }
    });

    if (!user) {
      user = await prisma.user.create({
        data: {
          email: profile.emails![0].value,
          name: profile.displayName,
          googleId: profile.id,
          emailVerified: true
        }
      });
    }

    return done(null, user);
  } catch (error) {
    return done(error);
  }
}));

app.get('/auth/google',
  passport.authenticate('google', { scope: ['profile', 'email'] })
);

app.get('/auth/google/callback',
  passport.authenticate('google', { failureRedirect: '/login' }),
  (req: Request, res: Response) => {
    const { accessToken, refreshToken } = authService.generateTokens({
      userId: (req.user as any).id,
      email: (req.user as any).email
    });
    res.json({ accessToken, refreshToken });
  }
);
```

## Common Patterns

### CORS Security Configuration
```typescript
import cors from 'cors';

const corsOptions = {
  origin: (origin: string | undefined, callback: Function) => {
    const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(',') || [];

    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  maxAge: 600
};

app.use(cors(corsOptions));
```

### Security Headers Configuration
```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'", process.env.API_URL]
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },
  frameguard: { action: 'deny' },
  noSniff: true,
  xssFilter: true
}));
```

### Secure Password Handling
```typescript
import bcrypt from 'bcrypt';

class PasswordService {
  async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, 12);
  }

  async verifyPassword(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
  }

  async validatePasswordStrength(password: string): Promise<{
    isValid: boolean;
    issues: string[];
  }> {
    const issues: string[] = [];

    if (password.length < 12) issues.push('Password must be at least 12 characters');
    if (!/[A-Z]/.test(password)) issues.push('Must include uppercase letter');
    if (!/[a-z]/.test(password)) issues.push('Must include lowercase letter');
    if (!/\d/.test(password)) issues.push('Must include number');
    if (!/[@$!%*?&]/.test(password)) issues.push('Must include special character');

    return {
      isValid: issues.length === 0,
      issues
    };
  }
}
```

## Best Practices

✅ Always use HTTPS in production for all communications
✅ Store JWT secrets in environment variables, never hardcode
✅ Use short-lived access tokens (15 minutes) with refresh tokens
✅ Implement rate limiting on authentication endpoints
✅ Validate and sanitize all user inputs before processing
✅ Use CORS properly with specific allowed origins
✅ Implement security headers with helmet
✅ Hash passwords with bcrypt (12+ rounds)
✅ Log security events for audit trails
✅ Regular security audits and dependency updates

## Common Pitfalls

❌ Storing passwords in plaintext or with weak hashing
❌ Long-lived access tokens without refresh token rotation
❌ Missing rate limiting on login endpoints
❌ Exposing sensitive data in error messages
❌ Using wildcard CORS origins (*) in production
❌ Not validating input, allowing SQL injection or XSS
❌ Hardcoding API keys and secrets in code
❌ Missing HTTPS enforcement or security headers
❌ Not rotating refresh tokens after use
❌ Ignoring security dependencies updates

## Resources

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8949)
- [Helmet Security Middleware](https://helmetjs.github.io/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/nodejs-security/)
- [OAuth 2.0 Specification](https://tools.ietf.org/html/rfc6749)
