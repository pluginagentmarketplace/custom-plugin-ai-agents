---
name: system-design
description: Design scalable systems using CAP theorem, load balancing, caching, and distributed system patterns. Use when architecting large-scale applications and solving distributed systems challenges.
---

# System Design

Master large-scale system design with focus on scalability, availability, and consistency in distributed environments.

## Quick Start

### System Design Process

```
1. Understand Requirements
   ├─ Functional (what system does)
   └─ Non-Functional (performance, scalability, availability)

2. Estimate Scale
   ├─ DAU (Daily Active Users)
   ├─ QPS (Queries Per Second)
   └─ Data Volume

3. Design High-Level Architecture
   ├─ Load Balancers
   ├─ API Servers
   ├─ Databases
   └─ Caching Layer

4. Deep Dive & Refinement
   ├─ Data Partitioning
   ├─ Replication Strategy
   ├─ Failure Handling
   └─ Monitoring
```

## CAP Theorem

Every distributed system can only guarantee two of three properties:

```
        ┌────────────────┐
        │  Consistency   │
        │   (C)          │
        └────────────────┘
               / \
              /   \
             /     \
            /       \
    ┌─────────┐   ┌──────────┐
    │Partition│───│Availability│
    │ Tolerance│   │    (A)     │
    │   (P)   │   │            │
    └─────────┘   └──────────┘

CA: ACID Databases (no partition tolerance)
CP: HBase, BigTable (sacrifice availability)
AP: DynamoDB, Cassandra (eventual consistency)
```

### Consistency Models

```typescript
// Strong Consistency
// All nodes see the same data at same time
// Example: Bank transactions

// Weak Consistency
// No guarantee of immediate consistency
// Eventually becomes consistent
// Example: Social media likes

// Eventual Consistency
// System will converge to consistent state
// Example: DNS, Email systems
```

## Load Balancing

Distributes incoming traffic across multiple servers.

```
                    ┌──────────────┐
                    │   Clients    │
                    └──────┬───────┘
                           │
                    ┌──────▼──────┐
                    │ Load Balancer│
                    │ (Round Robin)│
                    └──────┬───────┘
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────▼────┐        ┌────▼────┐       ┌────▼────┐
    │Server 1 │        │Server 2 │       │Server 3 │
    │ (8GB)   │        │ (8GB)   │       │ (8GB)   │
    └────┬────┘        └────┬────┘       └────┬────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                       ┌────▼───────┐
                       │ Database    │
                       │ (Primary)   │
                       └─────────────┘
```

### Load Balancing Strategies

```typescript
// Round Robin
// Distributes requests in order
servers: [S1, S2, S3, S4]
request 1 -> S1
request 2 -> S2
request 3 -> S3
request 4 -> S4
request 5 -> S1 (cycles)

// Least Connections
// Routes to server with fewest active connections
S1: 5 connections
S2: 2 connections ← Route here
S3: 8 connections

// Weighted Round Robin
S1 (capacity 10): 40%
S2 (capacity 20): 60%

// IP Hash
hash(client_ip) % num_servers = server_index
Same client always goes to same server (sticky sessions)
```

## Caching Strategies

Caching reduces latency and database load.

```
┌────────┐
│Request │
└────┬───┘
     │
     ▼
  ┌──────┐      Cache Hit
  │Cache │◄─────────────┐
  └──┬───┘              │
     │                  │
  Cache Miss         (Serve)
     │
     ▼
 ┌────────┐
 │Database│
 └────┬───┘
      │
   (Get Data)
      │
      ▼
   ┌──────┐       (Store)
   │Cache │──────────────┐
   └──────┘              │
      │                  │
  (Return)           (Update)
```

### Caching Patterns

```typescript
// Cache Aside / Lazy Loading
get(key) {
  data = cache.get(key);
  if (data == null) {
    data = db.get(key);
    cache.put(key, data);
  }
  return data;
}

// Write-Through
put(key, data) {
  cache.put(key, data);
  db.put(key, data);
}

// Write-Behind / Write-Back
put(key, data) {
  cache.put(key, data);
  queue.add({key, data});
  // Async write to DB
}
```

### Cache Eviction Policies

```
LRU (Least Recently Used)
├─ Removes least recently accessed item
├─ Common in web caching
└─ Example: Redis, Memcached

LFU (Least Frequently Used)
├─ Removes least frequently used item
├─ Good for hot data workloads
└─ Example: Caffeine cache

FIFO (First In First Out)
├─ Removes oldest item
└─ Simple but less effective

TTL (Time To Live)
├─ Expires data after time period
└─ Used with other policies
```

## Database Replication

Increases availability and read throughput.

```
                  ┌─────────────────┐
                  │ Master Database │
     Write ──────►│  (Primary)      │
                  └────────┬────────┘
                           │ Replication
          ┌────────────────┼────────────────┐
          │                │                │
       ┌──▼──┐          ┌──▼──┐         ┌──▼──┐
       │Slave│          │Slave│         │Slave│
       │  1  │          │  2  │         │  3  │
       └──┬──┘          └─────┘         └─────┘
     Read ◄─
     (Distribute across slaves)
```

### Replication Strategies

```typescript
// Synchronous Replication
Master writes -> Waits for all slaves
Pros: Consistent data
Cons: High latency

// Asynchronous Replication
Master writes -> Returns immediately
Slaves catch up
Pros: Low latency
Cons: Data loss possible

// Semi-Synchronous
Master waits for at least one slave
Middle ground between sync/async
```

## Data Partitioning (Sharding)

```
┌──────────────┐
│   Requests   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Shard Key   │
│  (user_id)   │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────┐
│  Hash Function / Range Query    │
└──┬───────────┬──────────┬──────┬┘
   │           │          │      │
┌──▼──┐    ┌──▼──┐   ┌──▼──┐ ┌──▼──┐
│Shard│    │Shard│   │Shard│ │Shard│
│  1  │    │  2  │   │  3  │ │  4  │
│ DB  │    │ DB  │   │ DB  │ │ DB  │
└─────┘    └─────┘   └─────┘ └─────┘
```

### Partitioning Strategies

```typescript
// Range-Based Sharding
Shard 1: user_id 0-1000
Shard 2: user_id 1001-2000
Shard 3: user_id 2001-3000

// Hash-Based Sharding
Shard = hash(user_id) % num_shards
Distributes evenly but harder to rebalance

// Directory-Based Sharding
Lookup table: user_id -> Shard_id
Most flexible but adds lookup overhead

// Geo-Sharding
Shard 1: US East users
Shard 2: EU users
Shard 3: Asia users
Reduces latency for regional users
```

## High Availability Patterns

### Multi-Datacenter Replication

```
┌──────────────────┐              ┌──────────────────┐
│   Datacenter 1   │              │   Datacenter 2   │
│  (Primary)       │   Replicate  │  (Secondary)     │
│ ┌──────────────┐ │◄────────────►│ ┌──────────────┐ │
│ │  Database    │ │              │ │  Database    │ │
│ │  Cluster     │ │              │ │  Cluster     │ │
│ └──────────────┘ │              │ └──────────────┘ │
└──────────────────┘              └──────────────────┘
     (Active)                         (Active/Standby)
```

### Circuit Breaker Pattern

```
┌────────────────────────────────────┐
│       Closed State                 │
│  (Normal operation)                │
│  Requests flow normally            │
└──────────────┬─────────────────────┘
               │
         (Error rate > threshold)
               │
               ▼
┌────────────────────────────────────┐
│       Open State                   │
│  (Service failing)                 │
│  Requests fail immediately         │
│  (Don't call failing service)      │
└──────────────┬─────────────────────┘
               │
        (After timeout)
               │
               ▼
┌────────────────────────────────────┐
│    Half-Open State                 │
│  (Testing recovery)                │
│  Limited requests allowed          │
└──────────────┬─────────────────────┘
               │
      (Success/Failure)
               │
      ┌────────┴─────────┐
      │                  │
      ▼                  ▼
    Closed            Open
   (Success)        (Failure)
```

### Bulkhead Pattern

Isolate components to prevent cascade failures.

```
┌──────────────────────────────────────┐
│         Service Layer                │
├──────────────┬───────────┬──────────┤
│  Bulkhead 1  │Bulkhead 2 │Bulkhead 3│
│  (Critical)  │(Standard) │(Batch)   │
│  Thread Pool │Thread Pool│Thread Pool│
│   Size: 10   │ Size: 20  │ Size: 50 │
├──────────────┼───────────┼──────────┤
│  Request A   │ Request B │ Request C│
│  Request D   │ Request E │ Request F│
│  Request G   │ Request H │          │
└──────────────┴───────────┴──────────┘
```

## Example: Designing Instagram Scale

Requirements:
- 100M DAU
- 10K QPS reads, 1K QPS writes
- 500PB+ photo storage

Architecture:

```
┌──────────────────────────────────┐
│      CDN (CloudFlare)            │  Fast photo delivery
└──────────┬───────────────────────┘
           │
┌──────────▼───────────────────────┐
│      API Gateway / LB             │  Route to servers
└──────────┬───────────────────────┘
           │
┌──────────▼───────────────────────┐
│  Web Servers (1000+ instances)    │  Process requests
└──────────┬───────────────────────┘
           │
    ┌──────┼──────┬──────────┐
    │      │      │          │
┌───▼─┐ ┌──▼──┐ ┌──▼──┐ ┌───▼──┐
│Cache│ │Graph│ │Search│ │Object│
│Redis│ │ DB  │ │Engine│ │Store │
│     │ │     │ │      │ │(S3)  │
└─────┘ └─────┘ └──────┘ └──────┘
```

## Best Practices

✅ **Design for failure** - Assume components will fail
✅ **Use caching** - Reduces database load and latency
✅ **Implement monitoring** - Know system behavior
✅ **Horizontal scaling** - Add more servers not bigger servers
✅ **Async processing** - Use queues for long operations
✅ **Database optimization** - Indexes, partitioning, replication
✅ **Load testing** - Verify scalability assumptions

## Common Pitfalls

❌ Single point of failure - No redundancy
❌ Synchronous everywhere - Blocks and creates bottlenecks
❌ No monitoring - Can't diagnose problems
❌ Over-caching - Stale data issues
❌ Premature optimization - Complexity without need
❌ Ignoring failure scenarios - Cascade failures
❌ Too fine-grained sharding - Too many databases

## Resources

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Designing Data-Intensive Applications by Martin Kleppmann](https://dataintensive.net/)
- [The Twelve-Factor App](https://12factor.net/)
- [CAP Theorem Explained](https://en.wikipedia.org/wiki/CAP_theorem)
- [AWS Architecture Patterns](https://aws.amazon.com/blogs/architecture/)
