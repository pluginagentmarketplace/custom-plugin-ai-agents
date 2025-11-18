---
name: css-modern
description: Modern CSS layouts with Flexbox, Grid, animations, responsive design, custom properties for scalable styling.
---

# Modern CSS

Master modern CSS techniques for building responsive, performant, and maintainable layouts. Learn Flexbox, Grid, animations, custom properties, and responsive design patterns.

## Quick Start

```css
/* CSS Custom Properties (Variables) */
:root {
  --primary-color: #3498db;
  --spacing-unit: 8px;
  --transition-duration: 0.3s;
}

/* Flexbox Layout */
.flex-container {
  display: flex;
  gap: var(--spacing-unit);
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

/* CSS Grid Layout */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-unit);
  grid-auto-rows: auto;
}

/* Animation with transitions */
.button {
  background-color: var(--primary-color);
  transition: background-color var(--transition-duration) ease;
}

.button:hover {
  background-color: darken(var(--primary-color), 10%);
}

/* Responsive Design */
@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: 1fr;
  }
}
```

## Key Concepts

### Flexbox for Component Layouts

Flexbox is ideal for one-dimensional layouts and aligning components:

```css
/* Navigation bar with flex */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.navbar__logo {
  font-weight: bold;
  font-size: 1.5rem;
}

.navbar__menu {
  display: flex;
  gap: calc(var(--spacing-unit) * 2);
  list-style: none;
  margin: 0;
  padding: 0;
}

.navbar__item {
  flex: 0 1 auto;
}

/* Card layout with flex direction column */
.card {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card__image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card__content {
  flex: 1;
  padding: calc(var(--spacing-unit) * 2);
  display: flex;
  flex-direction: column;
}

.card__footer {
  display: flex;
  gap: var(--spacing-unit);
  margin-top: auto;
}
```

### CSS Grid for Page Layouts

Grid excels at two-dimensional layouts:

```css
/* Dashboard layout with grid */
.dashboard {
  display: grid;
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  gap: calc(var(--spacing-unit) * 2);
}

.dashboard__header {
  grid-column: 1 / -1;
  padding: calc(var(--spacing-unit) * 2);
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.dashboard__sidebar {
  grid-row: 2;
  padding: calc(var(--spacing-unit) * 2);
  background-color: #fafafa;
  overflow-y: auto;
}

.dashboard__main {
  grid-column: 2;
  grid-row: 2;
  padding: calc(var(--spacing-unit) * 2);
  overflow-y: auto;
}

.dashboard__footer {
  grid-column: 1 / -1;
  padding: calc(var(--spacing-unit) * 2);
  background-color: #f5f5f5;
  border-top: 1px solid #ddd;
}

/* Responsive grid with auto-fit */
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: calc(var(--spacing-unit) * 2);
  padding: calc(var(--spacing-unit) * 2);
}
```

### Animations and Transitions

Create smooth, performant animations:

```css
/* Simple transition */
.button {
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all var(--transition-duration) ease-in-out;
}

.button:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Keyframe animation */
@keyframes slideInFromLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.slide-in {
  animation: slideInFromLeft 0.5s ease-out;
}

/* Loading spinner */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Smooth page transitions */
.fade-enter {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
```

## Common Patterns

### 1. Responsive Navigation

```css
/* Mobile-first responsive navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-unit);
}

.navbar__menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  flex-direction: column;
  background-color: white;
  border-top: 1px solid #ddd;
}

.navbar__toggle {
  display: block;
  background: none;
  border: none;
  cursor: pointer;
}

/* Show menu on desktop */
@media (min-width: 768px) {
  .navbar__menu {
    display: flex;
    position: static;
    flex-direction: row;
    border: none;
  }

  .navbar__toggle {
    display: none;
  }
}
```

### 2. Responsive Grid with Fallbacks

```css
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: calc(var(--spacing-unit) * 2);
  padding: calc(var(--spacing-unit) * 2);
}

@supports (display: grid) {
  .product-grid {
    display: grid;
  }
}

/* Fallback for older browsers */
@supports not (display: grid) {
  .product-grid {
    display: flex;
    flex-wrap: wrap;
    margin: calc(var(--spacing-unit) * -1);
  }

  .product-grid > * {
    margin: var(--spacing-unit);
    flex: 0 0 calc(33.333% - calc(var(--spacing-unit) * 2));
  }
}
```

### 3. Sticky Header with Flex

```css
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  position: sticky;
  top: 0;
  flex-shrink: 0;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.content {
  flex: 1;
  overflow-y: auto;
}

.footer {
  flex-shrink: 0;
  background-color: #f5f5f5;
  border-top: 1px solid #ddd;
}
```

### 4. Aspect Ratio Container

```css
.video-container {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
}

.video-container > * {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* Modern CSS aspect-ratio property */
.modern-video-container {
  aspect-ratio: 16 / 9;
  width: 100%;
}
```

## Best Practices

✅ Use CSS custom properties for consistent theming and responsive values
✅ Prefer Flexbox for one-dimensional layouts and Grid for two-dimensional layouts
✅ Design mobile-first with media queries progressively enhancing for larger screens
✅ Use `gap` property instead of margin hacks for cleaner code
✅ Leverage `grid-auto-fit` and `minmax()` for truly responsive grids
✅ Test animations with `prefers-reduced-motion` for accessibility

## Common Pitfalls

❌ Using absolute positioning when Flexbox or Grid would be simpler
❌ Creating animations that trigger expensive layout thrashing
❌ Forgetting to test media queries on actual devices
❌ Setting fixed widths that break responsive layouts
❌ Animating properties like `width` and `left` instead of `transform` and `opacity`

## Resources

- [MDN: CSS Flexbox](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Flexbox)
- [MDN: CSS Grid](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Grids)
- [CSS Tricks: Complete Guide to Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Web.dev: Learn CSS](https://web.dev/learn/css/)
- [Can I use CSS Grid/Flexbox](https://caniuse.com/)
