---
name: database-optimization
description: Optimize database performance through indexing, query optimization, partitioning, and replication. Use when improving database query performance and managing large datasets.
---

# Database Optimization

Master database performance tuning, query optimization, and scaling strategies for large datasets.

## Quick Start

### Database Performance Hierarchy

```
┌──────────────────────────────────────┐
│  1. Good Schema Design               │ Most impact
│     (Normalization, proper types)    │
├──────────────────────────────────────┤
│  2. Proper Indexing Strategy         │
│     (Indexed columns, index types)   │
├──────────────────────────────────────┤
│  3. Query Optimization               │
│     (Execution plans, rewrites)      │
├──────────────────────────────────────┤
│  4. Connection Pooling               │
│     (Resource management)            │
├──────────────────────────────────────┤
│  5. Caching                          │
│     (Application-level caching)      │
├──────────────────────────────────────┤
│  6. Hardware & Infrastructure        │ Least impact
│     (Server resources)               │
└──────────────────────────────────────┘
```

## Indexing Strategies

Indexes dramatically improve query performance by organizing data.

```
Without Index (Full Table Scan):
┌──────────────────────────────┐
│ Table: users (1M rows)       │
│                              │
│ id | name   | email | ...    │
│ 1  | Alice  | ...   │        │
│ 2  | Bob    | ...   │        │
│ 3  | Carol  | ...   │        │
│ ... (1M rows to scan)        │
│ 1M | Zoe    | ...   │        │
└──────────────────────────────┘
Time: O(n) - Slow

With Index on email:
┌──────────────────────┐
│ B-Tree Index         │
│ (email column)       │
│                      │
│ alice@... → row 1    │
│ bob@...   → row 2    │
│ carol@... → row 3    │
│ zoe@...   → row 1M   │
└──────────────────────┘
Time: O(log n) - Fast
```

### Index Types

```typescript
// 1. Single Column Index (Most Common)
CREATE INDEX idx_email ON users(email);

// Query Plan
EXPLAIN SELECT * FROM users WHERE email = 'john@example.com';
// Uses index efficiently

// 2. Composite Index (Multiple Columns)
CREATE INDEX idx_user_date ON orders(user_id, created_date);

// Efficient for:
WHERE user_id = 123 AND created_date > '2024-01-01'
WHERE user_id = 123  // Leftmost column rule

// Not efficient for:
WHERE created_date > '2024-01-01'  // Skips user_id

// 3. Full Text Index (Text Search)
CREATE FULLTEXT INDEX idx_title ON articles(title, content);

SELECT * FROM articles
WHERE MATCH(title, content) AGAINST('database optimization' IN BOOLEAN MODE);

// 4. Unique Index (Constraint + Performance)
CREATE UNIQUE INDEX idx_unique_email ON users(email);
// Ensures no duplicates + faster lookups

// 5. Partial/Conditional Index
CREATE INDEX idx_active_users ON users(id) WHERE status = 'active';
// Smaller index, only active users

// 6. Expression-based Index
CREATE INDEX idx_lower_email ON users(LOWER(email));
// Optimizes case-insensitive searches
```

### When to Index

```typescript
✅ Frequently queried columns
✅ Columns in WHERE clauses
✅ Columns in JOIN conditions
✅ Columns in ORDER BY
✅ Columns with low cardinality (if filtered)

❌ Low cardinality columns (many NULLs)
❌ Columns rarely queried
❌ Frequently updated columns
❌ Small tables (< 1000 rows)
```

## Query Optimization

### EXPLAIN Plans

Analyze query execution to find bottlenecks.

```typescript
// MySQL/PostgreSQL
EXPLAIN SELECT * FROM orders
WHERE user_id = 123 AND status = 'completed'
ORDER BY created_date DESC;

Output:
┌─────────────────────────────────────────┐
│ id | type  | key           | rows | ...│
├─────────────────────────────────────────┤
│ 1  | range | idx_user_stat | 45   |    │ Uses index
│                                         │ ~45 rows examined
└─────────────────────────────────────────┘

// Detailed analysis with EXPLAIN FORMAT=JSON
EXPLAIN FORMAT=JSON SELECT ...;

// Identify issues:
// - type: ALL = full table scan (bad)
// - type: index, range, ref = uses index (good)
// - rows: High number = many rows scanned
// - Extra: Using where, Using filesort, Using temporary
```

### Common Query Problems

```typescript
// Problem 1: Unnecessary Columns (SELECT *)
// Bad
SELECT * FROM users WHERE id = 1;  // Loads all columns

// Good
SELECT id, name, email FROM users WHERE id = 1;  // Only needed columns

// Problem 2: Missing Index
// Bad (No index on email)
SELECT * FROM users WHERE email = 'john@example.com';
// Results in full table scan

// Good (Index on email)
CREATE INDEX idx_email ON users(email);

// Problem 3: Using Functions in WHERE (Breaks Index)
// Bad
SELECT * FROM users WHERE LOWER(email) = 'john@example.com';
// Index on email not used!

// Good - Multiple approaches
// Option 1: Function-based index
CREATE INDEX idx_lower_email ON users(LOWER(email));

// Option 2: Normalize data at insert
const email = userInput.toLowerCase();

// Problem 4: OR Conditions (Complex Indexing)
// Less efficient
SELECT * FROM products
WHERE category = 'electronics' OR status = 'featured';

// Often better with UNION for separate indexes
SELECT * FROM products WHERE category = 'electronics'
UNION
SELECT * FROM products WHERE status = 'featured';

// Problem 5: JOIN with Unindexed Columns
// Bad
CREATE TABLE users (id, name);
CREATE TABLE orders (id, user_id, amount);
// Missing index on orders.user_id

// Good
CREATE INDEX idx_orders_user_id ON orders(user_id);
SELECT o.* FROM orders o
JOIN users u ON o.user_id = u.id;

// Problem 6: Subqueries Instead of JOINs
// Slower
SELECT * FROM users WHERE id IN (
  SELECT user_id FROM orders WHERE total > 100
);

// Faster
SELECT DISTINCT u.* FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.total > 100;

// Problem 7: Inefficient Pagination
// Bad - Offset scans all rows
SELECT * FROM posts LIMIT 1000000, 20;

// Good - Use keyset pagination
SELECT * FROM posts WHERE id > 999999 LIMIT 20;

// Problem 8: Missing JOIN Conditions
// Bad - Cartesian product!
SELECT * FROM users, orders WHERE users.name = 'John';

// Good
SELECT * FROM users
JOIN orders ON users.id = orders.user_id
WHERE users.name = 'John';
```

### Query Optimization Techniques

```typescript
// 1. Use EXISTS instead of IN for subqueries
// Slower
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders);

// Faster
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);

// 2. Avoid NOT IN with NULLs
// Problematic
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM orders);
// Returns nothing if any order.user_id IS NULL!

// Safe
SELECT * FROM users u
WHERE NOT EXISTS (SELECT 1 FROM orders WHERE user_id = u.id);

// 3. Batch Operations
// Slower - Multiple queries
for (const id of userIds) {
  await db.query('DELETE FROM orders WHERE user_id = ?', [id]);
}

// Faster - Single query
await db.query('DELETE FROM orders WHERE user_id IN (?)', [userIds]);

// 4. Use LIMIT for existence checks
// Slower
const count = await db.query('SELECT COUNT(*) FROM large_table WHERE condition');

// Faster
const exists = await db.query('SELECT 1 FROM large_table WHERE condition LIMIT 1');

// 5. Denormalization for Performance
// Normalized - Multiple JOINs
SELECT COUNT(o.id) FROM users u
JOIN orders o ON u.id = o.user_id;

// Denormalized - Cache count
ALTER TABLE users ADD COLUMN order_count INT;
// Update on ORDER INSERT/DELETE
```

## Partitioning (Sharding)

Divide data across multiple tables or databases.

```
Without Partitioning:
┌──────────────────────────┐
│ orders (1B rows)         │
│ Slow queries             │
│ High memory usage        │
│ Lock contention          │
└──────────────────────────┘

With Partitioning:
┌────────────────┬────────────────┬────────────────┐
│ orders_2024_q1 │ orders_2024_q2 │ orders_2024_q3 │
│ (250M rows)    │ (250M rows)    │ (250M rows)    │
└────────────────┴────────────────┴────────────────┘
Faster queries, lower memory, better concurrency
```

### Partitioning Strategies

```typescript
// 1. Range Partitioning (Time-based)
CREATE TABLE orders (
  id INT,
  user_id INT,
  created_date DATE,
  amount DECIMAL(10,2)
) PARTITION BY RANGE (YEAR(created_date)) (
  PARTITION p2022 VALUES LESS THAN (2023),
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p2024 VALUES LESS THAN (2025)
);

// 2. List Partitioning (Categories)
CREATE TABLE products (
  id INT,
  category VARCHAR(50),
  name VARCHAR(255)
) PARTITION BY LIST (category) (
  PARTITION p_electronics VALUES IN ('laptop', 'phone'),
  PARTITION p_books VALUES IN ('fiction', 'nonfiction'),
  PARTITION p_other VALUES IN (DEFAULT)
);

// 3. Hash Partitioning (Distribution)
CREATE TABLE users (
  id INT,
  name VARCHAR(255)
) PARTITION BY HASH(id) PARTITIONS 4;
// Distributes evenly across 4 partitions

// 4. Composite Partitioning
CREATE TABLE large_table (
  id INT,
  user_id INT,
  created_date DATE
) PARTITION BY RANGE (YEAR(created_date))
  SUBPARTITION BY HASH(user_id) SUBPARTITIONS 4;
```

## Replication

Maintain copies of data across servers.

```
┌──────────────┐
│ Primary DB   │  Write
│ (Master)     ├─────┐
└──────────────┘     │
                     │ Replication
                     ▼
        ┌────────────────────────┐
        │ Replica DB (Slave)     │
        │                        │
        │ Read-only copy         │
        │                        │
        └────────────────────────┘
```

### Replication Types

```typescript
// 1. Statement-Based Replication (SBR)
Primary: INSERT INTO users (name) VALUES ('John');
Replica: Executes same SQL statement

Pros: Less data transfer
Cons: Non-deterministic functions problematic

// 2. Row-Based Replication (RBR)
Primary: INSERT affects row 123
Replica: Updates row 123 with exact data

Pros: Works with all queries
Cons: More data transfer

// 3. Mixed-Mode Replication
Uses SBR when safe, RBR when needed

// Connection Pooling for Replication
const pool = createPool({
  master: 'master-db:3306',
  slaves: ['slave1:3306', 'slave2:3306']
});

// Writes go to master
await pool.execute('INSERT INTO users...', 'master');

// Reads distributed across slaves
await pool.execute('SELECT * FROM users...', 'slave');
```

## Connection Pooling

Manage database connections efficiently.

```
Without Pooling:
Request 1 → Create connection → Query → Close connection
Request 2 → Create connection → Query → Close connection
Request 3 → Create connection → Query → Close connection
...
Overhead: Creating/destroying connections is expensive

With Pooling:
┌──────────────────────────────┐
│ Connection Pool              │
│ ┌────────┬────────┬────────┐ │
│ │ Conn 1 │ Conn 2 │ Conn 3 │ │
│ └────────┴────────┴────────┘ │
└──────────────────────────────┘
Request 1 → Get from pool → Query → Return to pool
Request 2 → Get from pool → Query → Return to pool
...
Much faster!
```

### Connection Pool Configuration

```typescript
// PostgreSQL Pool Example
const { Pool } = require('pg');

const pool = new Pool({
  user: 'postgres',
  password: 'password',
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  max: 20,           // Max connections
  idleTimeoutMillis: 30000,  // Idle timeout
  connectionTimeoutMillis: 2000  // Connection timeout
});

// Get connection from pool
const client = await pool.connect();
try {
  await client.query('SELECT * FROM users');
} finally {
  client.release();  // Return to pool
}

// MySQL Connection Pool
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'mydb',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

const connection = await pool.getConnection();
try {
  const [rows] = await connection.query('SELECT * FROM users');
} finally {
  connection.release();
}
```

## Caching Strategies

```
Query → Cache Hit → Return (Fast!)
Query → Cache Miss → DB → Cache → Return (Slow first time)
```

### Cache Invalidation Strategies

```typescript
// 1. Time-to-Live (TTL)
cache.set('user:123', userData, 3600);  // 1 hour TTL

// 2. Event-Based Invalidation
db.update('users', userData);
cache.del('user:123');  // Invalidate on change

// 3. Dependency-Based
cache.set('user:123', userData, {
  depends_on: ['user-list']
});
// Invalidate user-list → invalidates dependent caches

// 4. Smart Caching Layer
class CachedRepository {
  async getUser(id) {
    const cached = await cache.get(`user:${id}`);
    if (cached) return cached;

    const user = await db.getUser(id);
    await cache.set(`user:${id}`, user, 3600);
    return user;
  }

  async updateUser(id, data) {
    const user = await db.updateUser(id, data);
    await cache.del(`user:${id}`);  // Invalidate
    return user;
  }
}

// 5. Cache Warming
async function warmCache() {
  const topUsers = await db.query('SELECT * FROM users ORDER BY created_date DESC LIMIT 1000');
  for (const user of topUsers) {
    await cache.set(`user:${user.id}`, user, 86400);  // 24 hours
  }
}
```

## Monitoring & Profiling

```typescript
// Slow Query Log (MySQL)
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;
// Logs queries taking > 2 seconds

// Query Analysis Tools
// - EXPLAIN ANALYZE (PostgreSQL)
// - Percona Monitoring and Management (PMM)
// - New Relic Database Performance
// - DataGrip Profiler

// Application-Level Monitoring
const startTime = Date.now();
const result = await db.query('SELECT ...');
const duration = Date.now() - startTime;

if (duration > 1000) {
  logger.warn(`Slow query: ${duration}ms`);
}

// Index Usage Statistics
// MySQL
SELECT * FROM sys.schema_unused_indexes;

// PostgreSQL
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

## Best Practices

✅ **Normalize schema** - Reduce redundancy
✅ **Strategic indexing** - Index WHERE, JOIN, ORDER BY columns
✅ **Use EXPLAIN** - Understand query plans
✅ **Connection pooling** - Manage resources efficiently
✅ **Partition large tables** - Improve query performance
✅ **Replication** - High availability and read scaling
✅ **Cache strategically** - Reduce database load
✅ **Monitor continuously** - Identify bottlenecks early

## Common Pitfalls

❌ Over-indexing - Slows writes, wastes storage
❌ Indexing low-cardinality columns
❌ SELECT * - Loads unnecessary columns
❌ Using functions in WHERE - Breaks indexes
❌ N+1 queries - Fetch in loops instead of JOINs
❌ Ignoring NULL handling - Can break queries
❌ No monitoring - Problems appear suddenly
❌ Premature optimization - Without measurement

## Resources

- [Use The Index, Luke](https://use-the-index-luke.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [MongoDB Query Performance](https://docs.mongodb.com/manual/core/query-performance/)
- [Designing Data-Intensive Applications by Martin Kleppmann](https://dataintensive.net/)
