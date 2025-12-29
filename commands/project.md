---
name: project
description: Project Ideas by Skill Level
allowed-tools: Read
---

# Project Ideas by Skill Level

Find hands-on projects to build and strengthen your skills in any technology.

## Usage

```
/project [technology] [level]
```

**Parameters:**
- `technology`: Any roadmap (react, python, kubernetes, etc.)
- `level`: `beginner`, `intermediate`, `advanced`, or `expert`

## Examples

```
/project react beginner
/project python intermediate
/project kubernetes advanced
/project system-design expert
```

---

## Project Ideas

### Frontend Development

#### Beginner (0-4 months)
```
/project react beginner
```

**1. Todo List with Local Storage**
- Technologies: React, TypeScript, CSS
- Features:
  - Add, edit, delete, complete todos
  - Filter by status (all, active, completed)
  - Persist data in localStorage
  - Responsive design
- Skills learned: useState, useEffect, event handling, localStorage API
- Time: 8-12 hours
- GitHub template: Search "react-todo-typescript"

**2. Weather Dashboard**
- Technologies: React, TypeScript, Weather API
- Features:
  - Search city weather
  - Display current conditions
  - 5-day forecast
  - Geolocation support
- Skills learned: API fetching, useEffect, error handling, conditional rendering
- Time: 12-16 hours
- API: OpenWeatherMap API (free tier)

**3. Portfolio Website**
- Technologies: React, Next.js, Tailwind CSS
- Features:
  - About, projects, contact sections
  - Responsive navigation
  - Dark/light mode toggle
  - Contact form
- Skills learned: Routing, Tailwind, theming, forms
- Time: 16-20 hours

#### Intermediate (4-8 months)
```
/project react intermediate
```

**1. E-commerce Product Catalog**
- Technologies: React, TypeScript, Redux Toolkit, React Router
- Features:
  - Product listing with filtering
  - Shopping cart functionality
  - Product search and sort
  - Checkout flow (UI only)
- Skills learned: Redux, routing, complex state, performance optimization
- Time: 30-40 hours
- API: FakeStore API or create mock data

**2. Real-time Chat Application**
- Technologies: React, Socket.io, Node.js, Express
- Features:
  - User authentication (JWT)
  - Real-time messaging
  - Typing indicators
  - Online user list
- Skills learned: WebSocket, authentication, real-time updates
- Time: 40-50 hours

**3. Task Management Dashboard**
- Technologies: React, TypeScript, Drag-and-Drop library, Firebase
- Features:
  - Kanban board (like Trello)
  - Drag-and-drop tasks
  - User authentication
  - Cloud persistence
- Skills learned: DnD, Firebase, authentication, complex interactions
- Time: 50-60 hours

#### Advanced (8-12 months)
```
/project react advanced
```

**1. Full-Stack Blog Platform**
- Technologies: Next.js 14, PostgreSQL, Prisma, NextAuth.js
- Features:
  - Server Components and Server Actions
  - Markdown editor with preview
  - Comments and reactions
  - User profiles and authentication
  - SEO optimization
- Skills learned: SSR, Server Actions, database design, SEO
- Time: 60-80 hours

**2. Analytics Dashboard**
- Technologies: React, TypeScript, D3.js, WebSocket, Node.js
- Features:
  - Real-time data visualization
  - Multiple chart types
  - Data filtering and aggregation
  - Export to CSV/PDF
- Skills learned: Data visualization, performance with large datasets, real-time updates
- Time: 80-100 hours

**3. Video Streaming Platform (UI)**
- Technologies: React, Video.js, HLS.js, AWS S3
- Features:
  - Video player with controls
  - Playlist management
  - Comments and likes
  - Recommendations
- Skills learned: Video streaming, media optimization, complex UI
- Time: 100+ hours

---

### Backend Development

#### Beginner
```
/project nodejs beginner
```

**1. RESTful Todo API**
- Technologies: Node.js, Express, JSON file storage
- Features:
  - CRUD operations for todos
  - Input validation
  - Error handling
  - API documentation
- Skills learned: Express, routing, middleware, file system
- Time: 8-12 hours

**2. User Authentication API**
- Technologies: Node.js, Express, PostgreSQL, bcrypt, JWT
- Features:
  - User registration and login
  - Password hashing
  - JWT token generation
  - Protected routes
- Skills learned: Authentication, security, database, JWT
- Time: 16-20 hours

#### Intermediate
```
/project backend intermediate
```

**1. Blog API with Comments**
- Technologies: Node.js, Express, PostgreSQL, Prisma
- Features:
  - User authentication
  - Post CRUD operations
  - Comments system
  - Like/unlike functionality
  - Pagination
- Skills learned: Complex database relations, ORM, authorization
- Time: 30-40 hours

**2. E-commerce Backend**
- Technologies: Node.js, Express, MongoDB, Stripe
- Features:
  - Product management
  - Shopping cart
  - Order processing
  - Payment integration
  - Inventory management
- Skills learned: Transactions, payment processing, complex business logic
- Time: 60-80 hours

#### Advanced
```
/project backend advanced
```

**1. Microservices Architecture**
- Technologies: Node.js, Docker, Kubernetes, RabbitMQ, PostgreSQL
- Features:
  - User service, product service, order service
  - API gateway
  - Message queue communication
  - Service discovery
- Skills learned: Microservices, messaging, orchestration
- Time: 100+ hours

**2. Real-time Collaboration Platform API**
- Technologies: Node.js, Socket.io, Redis, PostgreSQL, WebRTC
- Features:
  - Real-time document editing
  - Operational transformation
  - Presence awareness
  - Video/audio calls
- Skills learned: Real-time systems, conflict resolution, WebRTC
- Time: 150+ hours

---

### Mobile Development

#### Beginner
```
/project android beginner
```

**1. Calculator App**
- Technologies: Kotlin, Jetpack Compose
- Features:
  - Basic arithmetic operations
  - History of calculations
  - Material Design 3
- Skills learned: Compose UI, state management, basic logic
- Time: 10-15 hours

**2. Weather App**
- Technologies: Kotlin, Jetpack Compose, Retrofit, Weather API
- Features:
  - City search
  - Current weather display
  - 7-day forecast
  - Save favorite cities
- Skills learned: API integration, Room database, MVVM
- Time: 20-25 hours

#### Intermediate
```
/project flutter intermediate
```

**1. Expense Tracker**
- Technologies: Flutter, Dart, SQLite, Provider
- Features:
  - Add/edit/delete expenses
  - Categories and tags
  - Charts and analytics
  - Export to CSV
- Skills learned: Local database, state management, charts
- Time: 30-40 hours

**2. Social Media Clone**
- Technologies: Flutter, Firebase, Riverpod
- Features:
  - User profiles
  - Post creation with images
  - Likes and comments
  - Follow system
- Skills learned: Firebase integration, image upload, complex state
- Time: 60-80 hours

#### Advanced
```
/project ios advanced
```

**1. Fitness Tracking App**
- Technologies: Swift, SwiftUI, HealthKit, CoreML
- Features:
  - Workout tracking
  - Health data integration
  - ML-powered exercise detection
  - Custom charts
- Skills learned: HealthKit, CoreML, advanced SwiftUI
- Time: 80-100 hours

---

### DevOps & Infrastructure

#### Beginner
```
/project docker beginner
```

**1. Containerize a Web Application**
- Technologies: Docker, Node.js
- Tasks:
  - Create Dockerfile
  - Multi-stage build
  - Docker Compose with database
  - Environment variables
- Skills learned: Containerization basics
- Time: 6-8 hours

#### Intermediate
```
/project kubernetes intermediate
```

**1. Deploy Microservices to Kubernetes**
- Technologies: Kubernetes, Docker, Helm
- Tasks:
  - Create deployments and services
  - ConfigMaps and Secrets
  - Ingress controller
  - Horizontal Pod Autoscaling
- Skills learned: K8s orchestration, Helm charts
- Time: 30-40 hours

#### Advanced
```
/project terraform advanced
```

**1. Multi-Environment AWS Infrastructure**
- Technologies: Terraform, AWS, GitHub Actions
- Tasks:
  - VPC with public/private subnets
  - ECS Fargate cluster
  - RDS with backups
  - CloudFront CDN
  - CI/CD pipeline
- Skills learned: IaC, cloud architecture, automation
- Time: 60-80 hours

---

### AI & Data Science

#### Beginner
```
/project python beginner
```

**1. Data Analysis of CSV Dataset**
- Technologies: Python, Pandas, Matplotlib
- Tasks:
  - Load and clean data
  - Exploratory data analysis
  - Create visualizations
  - Statistical summary
- Skills learned: Data manipulation, visualization
- Time: 8-12 hours
- Dataset: Kaggle beginner datasets

#### Intermediate
```
/project machine-learning intermediate
```

**1. Customer Churn Prediction**
- Technologies: Python, Scikit-learn, Pandas
- Tasks:
  - Feature engineering
  - Train multiple models
  - Model evaluation and comparison
  - Deploy with FastAPI
- Skills learned: ML pipeline, model deployment
- Time: 30-40 hours

**2. Sentiment Analysis on Tweets**
- Technologies: Python, NLTK, Transformers
- Tasks:
  - Data collection (Twitter API)
  - Text preprocessing
  - Train sentiment classifier
  - Create dashboard
- Skills learned: NLP, transformers, deployment
- Time: 40-50 hours

#### Advanced
```
/project ai-agents advanced
```

**1. RAG-based Q&A System**
- Technologies: LangChain, OpenAI, Pinecone, FastAPI
- Tasks:
  - Document ingestion and chunking
  - Vector embedding and storage
  - Retrieval-augmented generation
  - Web interface
- Skills learned: RAG, vector databases, LLMs
- Time: 50-70 hours

**2. Multi-Agent Research Assistant**
- Technologies: LangChain, AutoGPT, multiple APIs
- Tasks:
  - Research agent, summarizer agent, writer agent
  - Tool use (web search, calculator)
  - Agent coordination
  - Results compilation
- Skills learned: Multi-agent systems, autonomous agents
- Time: 80-100 hours

---

## Project Selection Tips

### Choose Based On:

1. **Current Skill Level**
   - Start slightly below your level to build confidence
   - Then challenge yourself with next level

2. **Career Goals**
   - Building portfolio? Choose diverse projects
   - Interview prep? Focus on common interview projects

3. **Time Available**
   - Weekend project: Beginner (8-12 hours)
   - Monthly project: Intermediate (30-50 hours)
   - Long-term: Advanced (80+ hours)

4. **Learning Objectives**
   - Want to learn React? Choose a React project
   - Want full-stack experience? Choose projects with frontend + backend

---

## Project Success Checklist

✅ **Before Starting:**
- [ ] Understand the requirements
- [ ] Set up development environment
- [ ] Create GitHub repository
- [ ] Plan the architecture

✅ **During Development:**
- [ ] Commit regularly with meaningful messages
- [ ] Write clean, documented code
- [ ] Implement error handling
- [ ] Add unit tests (for intermediate+)

✅ **After Completion:**
- [ ] Deploy to production (Vercel, Heroku, etc.)
- [ ] Write comprehensive README
- [ ] Add screenshots/demo
- [ ] Share on LinkedIn/Twitter
- [ ] Ask for code review

---

**Start building:** `/project [technology] [level]` 🛠️

The best way to learn is by building real projects!
