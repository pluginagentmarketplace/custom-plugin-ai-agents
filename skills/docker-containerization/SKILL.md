---
name: docker-containerization
description: Master containerization with Docker multi-stage builds, Compose, and registry management.
---

# Docker Containerization

Docker containerization enables consistent deployment across environments by packaging applications with all dependencies. Master Dockerfile optimization, multi-stage builds, Docker Compose orchestration, and container registry management for production-ready deployments.

## Quick Start

**Basic Dockerfile with multi-stage build:**

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Runtime
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

**Docker Compose setup:**

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

## Key Concepts

### Multi-Stage Builds
Reduce image size by using multiple FROM statements to separate build and runtime environments:

```dockerfile
FROM golang:1.21 AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /app .

FROM alpine:3.18
COPY --from=build /app /app
ENTRYPOINT ["/app"]
```

### Image Optimization
- Use `.dockerignore` to exclude unnecessary files
- Layer caching: place frequently-changing commands later in Dockerfile
- Use specific base image tags (avoid `latest`)
- Minimize layers by combining RUN commands

```dockerfile
# Bad: 3 layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# Good: 1 layer
RUN apt-get update && apt-get install -y curl && apt-get clean
```

### Registry Management
Push/pull images from Docker Hub or private registries:

```bash
docker build -t myregistry.azurecr.io/app:v1.0 .
docker push myregistry.azurecr.io/app:v1.0
docker pull myregistry.azurecr.io/app:v1.0
```

## Common Patterns

**Health checks:**

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD curl -f http://localhost:3000/health || exit 1
```

**Environment-based configuration:**

```dockerfile
FROM node:18-alpine
ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV
COPY . .
RUN npm ci --only=${NODE_ENV}
```

**Docker Compose with networks:**

```yaml
services:
  api:
    build: ./api
    networks:
      - app-network
  worker:
    build: ./worker
    networks:
      - app-network
networks:
  app-network:
    driver: bridge
```

## Best Practices

✅ Use specific base image versions (e.g., `node:18.17-alpine`)
✅ Run containers as non-root users
✅ Use .dockerignore to exclude unnecessary files
✅ Implement health checks for monitoring
✅ Tag images with semantic versioning
✅ Use multi-stage builds to minimize image size
✅ Scan images for vulnerabilities with `docker scan`
✅ Keep layers small and cacheable

## Common Pitfalls

❌ Using `latest` tags in production
❌ Running containers as root user
❌ Creating oversized images by not using multi-stage builds
❌ Including secrets in image layers
❌ Not using .dockerignore (includes all files)
❌ Assuming containers are isolated from host (security)
❌ Not specifying resource limits in Compose

## Resources

- [Docker Official Documentation](https://docs.docker.com/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Compose Specification](https://github.com/compose-spec/compose-spec)
- [Container Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
