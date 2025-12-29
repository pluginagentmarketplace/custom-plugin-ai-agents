---
name: assess
description: Knowledge Assessment
allowed-tools: Read
---

# Knowledge Assessment

Test your understanding and track your progress in any technology roadmap.

## Usage

```
/assess [technology] [level]
```

**Parameters:**
- `technology`: The roadmap to assess (e.g., react, python, kubernetes)
- `level`: Optional - `beginner`, `intermediate`, `advanced`, or `expert`

## Examples

```
/assess react
/assess python beginner
/assess kubernetes advanced
/assess system-design expert
```

---

## Assessment Types

### 1. Quick Check (5-10 questions)
Fast assessment to identify knowledge gaps.

```
/assess react quick
```

### 2. Comprehensive Evaluation (20-30 questions)
In-depth assessment covering all aspects.

```
/assess backend comprehensive
```

### 3. Interview Prep
Real interview questions with detailed solutions.

```
/assess python interview
```

### 4. Hands-On Challenge
Practical coding challenges.

```
/assess javascript challenge
```

---

## Sample Assessment: React (Intermediate)

When you run `/assess react intermediate`, you'll get:

### Knowledge Check Questions

**1. Hooks & State Management**
```typescript
// What's wrong with this code?
function Component() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    setCount(count + 1);
  }, []);

  return <div>{count}</div>;
}
```

<details>
<summary>Show Answer</summary>

**Issue:** The dependency array is empty, but `count` is used inside useEffect. This will only run once with the initial value of `count` (0).

**Fix:** Either add `count` to dependencies (causes infinite loop), or use functional update:
```typescript
useEffect(() => {
  setCount(prev => prev + 1);
}, []);
```
</details>

**2. Performance Optimization**
```
When should you use useMemo vs useCallback?
```

<details>
<summary>Show Answer</summary>

- **useMemo**: Memoize the *result* of expensive computations
  ```typescript
  const expensiveValue = useMemo(() => computeHeavy(a, b), [a, b]);
  ```

- **useCallback**: Memoize the *function itself* to prevent re-creation
  ```typescript
  const handleClick = useCallback(() => doSomething(a), [a]);
  ```

Use `useCallback` when passing callbacks to optimized child components that use `React.memo`.
</details>

**3. State Management**
```
Compare Context API vs Redux Toolkit. When would you choose each?
```

<details>
<summary>Show Answer</summary>

**Context API:**
- ✅ Simple global state
- ✅ Avoiding prop drilling
- ✅ Theme, auth, user preferences
- ❌ Frequent updates cause re-renders

**Redux Toolkit:**
- ✅ Complex state logic
- ✅ Many state updates
- ✅ Time-travel debugging
- ✅ Middleware (API calls, logging)
- ❌ More boilerplate

**Rule of thumb:** Start with Context API, migrate to Redux when state becomes complex.
</details>

---

## Assessment Results

After completing an assessment, you'll receive:

### 1. Score & Level
```
📊 Assessment Results: React Intermediate

Score: 24/30 (80%)
Level: ✅ Intermediate Confirmed

Strengths:
✅ Hooks (useState, useEffect, useRef)
✅ Component composition
✅ Performance optimization basics

Areas to improve:
⚠️ Advanced hooks (useReducer, useImperativeHandle)
⚠️ Server-side rendering (Next.js)
⚠️ Testing (React Testing Library)
```

### 2. Personalized Learning Path
```
📚 Recommended Next Steps:

1. Study useReducer for complex state
   Resource: /roadmap react (Advanced Section)
   Skill: react-development

2. Learn Next.js App Router
   Resource: /roadmap nextjs
   Skill: nextjs-fullstack

3. Practice component testing
   Project: /project react advanced (Testing-focused)

4. Review Server Components
   Ask: "Explain React Server Components vs Client Components"
```

### 3. Skill Gaps
```
🎯 Skill Development Plan:

Week 1-2: Advanced Hooks
- useReducer for form state
- useImperativeHandle for ref forwarding
- Custom hooks library

Week 3-4: Next.js
- App Router navigation
- Server Components
- Data fetching patterns

Week 5-6: Testing
- React Testing Library
- Mock API calls
- E2E with Playwright
```

### 4. Project Recommendations
```
💡 Build These Projects:

1. Advanced Todo App
   - useReducer for state
   - Custom hooks for localStorage
   - Unit tests with Vitest

2. Blog with Next.js
   - App Router
   - Server Components
   - MDX support

3. Testing Workshop
   - Set up testing environment
   - Write 20+ component tests
   - E2E test critical flows
```

---

## Assessment Categories

### Frontend
- `frontend`, `react`, `vue`, `angular`
- `typescript`, `javascript`, `html`, `css`
- `nextjs`, `ux-design`

### Backend
- `backend`, `nodejs`, `spring-boot`
- `api-design`, `graphql`, `databases`

### Mobile
- `android`, `ios`, `react-native`, `flutter`

### DevOps
- `devops`, `docker`, `kubernetes`
- `aws`, `terraform`, `linux`

### AI & Data
- `machine-learning`, `data-science`, `ai-agents`
- `python`, `sql`, `mlops`

### Architecture
- `system-design`, `software-architecture`
- `cyber-security`, `blockchain`

---

## Interview Preparation Mode

```
/assess [technology] interview
```

**Example: Backend Interview**
```
/assess backend interview
```

You'll get:
- System design questions
- Coding challenges
- Database design problems
- API design scenarios
- Behavioral questions
- Mock interview format

**Sample Questions:**
1. "Design a rate limiter" (System Design)
2. "Implement a REST API for a blog" (Coding)
3. "Optimize this slow query" (Database)
4. "How would you secure an API?" (Security)
5. "Tell me about a challenging project" (Behavioral)

---

## Hands-On Challenges

```
/assess [technology] challenge
```

**Example: React Challenge**
```
/assess react challenge
```

You'll get a coding challenge like:

```typescript
/**
 * Challenge: Build a Searchable Product List
 *
 * Requirements:
 * 1. Fetch products from /api/products
 * 2. Implement search/filter functionality
 * 3. Add pagination (10 items per page)
 * 4. Optimize performance (useMemo, useCallback)
 * 5. Add loading and error states
 * 6. Write tests
 *
 * Time: 60 minutes
 * Difficulty: Intermediate
 */

interface Product {
  id: number;
  name: string;
  price: number;
  category: string;
}

function ProductList() {
  // Your implementation here
}
```

---

## Track Your Progress

Assessments are saved to help you track improvement:

```
📈 Your Progress: React

Assessment History:
- Dec 15, 2024: Beginner (65%) → Study hooks
- Jan 10, 2025: Intermediate (80%) → Learn Next.js
- Feb 5, 2025: Advanced (72%) → Master performance

Next Milestone: Advanced (85%+)
Estimated Time: 4-6 weeks
```

---

**Start your assessment now:** `/assess [technology]` 📝

Track your learning journey and identify exactly what to study next!
