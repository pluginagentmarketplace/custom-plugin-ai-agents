---
name: database-architecture
description: Design efficient PostgreSQL schemas with proper indexing and normalization. Use when building scalable database architectures.
---

# Database Architecture

Master PostgreSQL schema design with normalization principles, strategic indexing, query optimization, and migration strategies for scalable systems.

## Quick Start

```sql
-- Create optimized schema with proper constraints
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Strategic indexes for query performance
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_published_created_at ON posts(published, created_at DESC);
CREATE INDEX idx_users_email ON users(email);
```

## Key Concepts

### Schema Normalization (3NF)
```sql
-- Users table (First Normal Form - atomic values)
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL
);

-- Tags table (separate entity, not embedded)
CREATE TABLE tags (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Post-Tags junction table (many-to-many relationship)
CREATE TABLE post_tags (
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

-- Comments table with proper normalization
CREATE TABLE comments (
    id UUID PRIMARY KEY,
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE SET NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Strategic Indexing for Query Performance
```sql
-- B-tree indexes for equality and range queries
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX idx_comments_post_id_created_at ON comments(post_id, created_at DESC);

-- Partial indexes for common filtered queries
CREATE INDEX idx_posts_published ON posts(created_at DESC)
    WHERE published = true;

-- Multi-column index for frequent combined filters
CREATE INDEX idx_posts_user_published ON posts(user_id, published, created_at DESC);

-- GiST index for full-text search
CREATE INDEX idx_posts_content_fts ON posts
    USING GiST(to_tsvector('english', content));

-- Check index usage
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM posts WHERE published = true ORDER BY created_at DESC LIMIT 10;
```

### Query Optimization Patterns
```sql
-- N+1 Problem: Inefficient (multiple queries)
-- DON'T: Loop in application to fetch posts, then for each post fetch user
SELECT * FROM posts LIMIT 100; -- Query 1
-- Then loop: SELECT * FROM users WHERE id = $1; (100 queries)

-- Optimized: Single JOIN query
SELECT
    p.id, p.title, p.content,
    u.id, u.email, u.name,
    COUNT(c.id) as comment_count
FROM posts p
    JOIN users u ON p.user_id = u.id
    LEFT JOIN comments c ON p.id = c.post_id
WHERE p.published = true
GROUP BY p.id, u.id
ORDER BY p.created_at DESC
LIMIT 50;

-- Use EXPLAIN to analyze query plans
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM posts
WHERE user_id = $1 AND published = true
ORDER BY created_at DESC
LIMIT 20;
```

## Common Patterns

### Migration Strategy with Prisma
```typescript
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  password  String
  posts     Post[]
  comments  Comment[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
  @@map("users")
}

model Post {
  id        String   @id @default(cuid())
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  title     String
  content   String
  published Boolean  @default(false)
  tags      Tag[]
  comments  Comment[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([userId])
  @@index([published, createdAt])
  @@map("posts")
}

model Tag {
  id    String  @id @default(cuid())
  name  String  @unique
  posts Post[]

  @@map("tags")
}

model Comment {
  id        String   @id @default(cuid())
  postId    String
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)
  userId    String?
  user      User?    @relation(fields: [userId], references: [id], onDelete: SetNull)
  content   String
  createdAt DateTime @default(now())

  @@index([postId])
  @@index([userId])
  @@map("comments")
}
```

### Materialized Views for Reporting
```sql
-- Create materialized view for analytics
CREATE MATERIALIZED VIEW user_stats AS
SELECT
    u.id,
    u.email,
    COUNT(DISTINCT p.id) as total_posts,
    COUNT(DISTINCT c.id) as total_comments,
    MAX(p.created_at) as last_post_date
FROM users u
    LEFT JOIN posts p ON u.id = p.user_id
    LEFT JOIN comments c ON u.id = c.user_id
GROUP BY u.id, u.email;

-- Create index on materialized view
CREATE INDEX idx_user_stats_total_posts ON user_stats(total_posts DESC);

-- Refresh materialized view (can be scheduled)
REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats;
```

### Connection Pooling Configuration
```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL
    }
  },
  // Connection pool settings
  transactionOptions: {
    maxWait: 5000,
    timeout: 30000
  }
});

// Graceful shutdown
process.on('SIGINT', async () => {
  await prisma.$disconnect();
  process.exit(0);
});

// Monitor connection pool
setInterval(async () => {
  const connection = await prisma.$queryRaw`SELECT count(*) as count FROM pg_stat_activity;`;
  console.log('Active connections:', connection);
}, 60000);
```

## Best Practices

✅ Normalize schemas to 3NF to reduce redundancy and maintain data integrity
✅ Use strategic indexes on foreign keys and frequently queried columns
✅ Implement soft deletes with timestamp-based filtering for audit trails
✅ Use EXPLAIN ANALYZE to verify index usage in queries
✅ Denormalize only when performance analysis proves necessity
✅ Implement connection pooling for efficient resource utilization
✅ Use constraints (NOT NULL, UNIQUE, FOREIGN KEY) for data validation
✅ Schedule regular ANALYZE and VACUUM for query optimizer accuracy

## Common Pitfalls

❌ Creating indexes on every column without analyzing actual query patterns
❌ Using SELECT * instead of selecting only needed columns
❌ Missing indexes on foreign key columns causing slow joins
❌ Not using JOIN and instead fetching data in application loops
❌ Storing duplicate data instead of properly normalizing
❌ Using VARCHAR without length constraints
❌ Missing ON DELETE CASCADE/SET NULL for referential integrity
❌ Ignoring connection pool exhaustion in production

## Resources

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
- [Database Normalization Guide](https://en.wikipedia.org/wiki/Database_normalization)
- [Query Optimization Tutorial](https://www.postgresql.org/docs/current/sql-explain.html)
- [Prisma Database Migrations](https://www.prisma.io/docs/concepts/components/prisma-migrate)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
