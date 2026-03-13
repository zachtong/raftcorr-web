# RAFTcorr Website Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a polished promotional single-page website for RAFTcorr with dark sci-fi aesthetic, scroll animations, and academic content sections.

**Architecture:** Pure HTML/CSS/JS single-page site. CSS custom properties for theming, Intersection Observer for scroll animations, vanilla JS carousel. Zero build tools, zero dependencies. GitHub Pages deployment.

**Tech Stack:** HTML5, CSS3 (custom properties, grid, flexbox, backdrop-filter), vanilla JavaScript (ES6+)

**Design Spec:** `docs/plans/2026-03-12-raftcorr-website-design.md`

---

## Phase 1: Foundation & Hero (Tasks 1-5)

### Task 1: HTML skeleton + CSS reset + theme variables

**Files:**
- Create: `index.html`
- Create: `style.css`

**Step 1: Create HTML skeleton with all 9 section placeholders**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RAFTcorr — Deep Learning Digital Image Correlation</title>
  <meta name="description" content="Zero-parameter, GPU-accelerated full-field deformation analysis in seconds.">
  <link rel="stylesheet" href="style.css">
  <!-- Fonts loaded here -->
</head>
<body>
  <nav class="navbar">...</nav>
  <section id="hero" class="hero">...</section>
  <section id="highlights" class="highlights">...</section>
  <section id="demo" class="demo">...</section>
  <section id="method" class="method">...</section>
  <section id="results" class="results">...</section>
  <section id="comparison" class="comparison">...</section>
  <section id="team" class="team">...</section>
  <section id="citation" class="citation">...</section>
  <footer class="footer">...</footer>
  <script src="script.js"></script>
</body>
</html>
```

**Step 2: Create CSS with reset + custom properties + base styles**

All colors, spacing, typography defined as CSS variables. Dark theme base.

**Step 3: Verify in browser**

Open `index.html`, verify dark background renders, fonts load.

**Step 4: Commit**

```bash
git add index.html style.css
git commit -m "feat: HTML skeleton and CSS foundation with dark theme"
```

---

### Task 2: Navbar (sticky, semi-transparent)

**Files:**
- Modify: `index.html` (nav section)
- Modify: `style.css` (navbar styles)

**Step 1: Implement navbar HTML**

Logo text "RAFTcorr" on left, section links on right (Method, Results, Compare, GitHub).
Mobile: hamburger menu.

**Step 2: Style navbar**

- `position: fixed`, `backdrop-filter: blur(10px)`
- Semi-transparent background `rgba(10, 15, 28, 0.8)`
- Smooth scroll via `scroll-behavior: smooth` on `html`
- Active link highlighting based on scroll position

**Step 3: Verify**

Scroll page, navbar stays fixed, links work, mobile hamburger toggles.

**Step 4: Commit**

```bash
git commit -m "feat: sticky navbar with blur backdrop and mobile menu"
```

---

### Task 3: Hero section — layout and typography

**Files:**
- Modify: `index.html` (hero section)
- Modify: `style.css` (hero styles)

**Step 1: Implement Hero HTML**

Centered layout: video placeholder (top) + title + tagline + 2 buttons.
Full viewport height.

**Step 2: Style Hero**

- `min-height: 100vh`, centered flex column
- Radial gradient background: `#0a0f1c` → `#162a4a`
- Faint grid texture overlay (CSS `background-image` repeating pattern)
- Title: `clamp(2.5rem, 5vw, 4rem)` responsive font size
- Buttons: solid blue primary, outlined secondary
- Scroll-down arrow: CSS keyframe bounce animation

**Step 3: Add placeholder for video area**

Rounded card with dashed border where video will go. Aspect ratio 16:9.

**Step 4: Verify and commit**

```bash
git commit -m "feat: hero section layout with gradient background and typography"
```

---

### Task 4: Hero section — video integration

**Files:**
- Modify: `index.html` (video element)
- Modify: `style.css` (video card styles)
- Add: `assets/videos/` (placeholder or real video)

**Step 1: Add `<video>` element**

```html
<div class="hero__video-card">
  <video autoplay muted loop playsinline>
    <source src="assets/videos/hero-demo.mp4" type="video/mp4">
    <source src="assets/videos/hero-demo.webm" type="video/webm">
  </video>
</div>
```

**Step 2: Style video card**

- Rounded corners (`border-radius: 16px`)
- Blue glow: `box-shadow: 0 0 60px rgba(74, 158, 255, 0.15)`
- `overflow: hidden` to clip video to rounded corners
- Max-width: ~70% viewport width
- Fallback: show a static image poster if video not loaded

**Step 3: Create a placeholder video or static image**

If real video not ready, use a gradient placeholder or screenshot.

**Step 4: Verify and commit**

```bash
git commit -m "feat: hero video card with glow effect and autoplay"
```

---

### Task 5: Scroll animation system

**Files:**
- Create: `script.js`

**Step 1: Implement Intersection Observer**

```javascript
// Observe all elements with [data-animate] attribute
// Add .is-visible class when element enters viewport
// Supports: fade-in, slide-up, slide-left, stagger
```

**Step 2: Add CSS animation classes**

```css
[data-animate] { opacity: 0; transform: translateY(30px); transition: ... }
[data-animate].is-visible { opacity: 1; transform: none; }
```

**Step 3: Add `data-animate` attributes to Hero elements**

**Step 4: Verify scroll triggers work and commit**

```bash
git commit -m "feat: scroll-triggered animation system with Intersection Observer"
```

---

## Phase 2: Content Sections (Tasks 6-10)

### Task 6: Highlights section (4 feature cards)

**Files:**
- Modify: `index.html`
- Modify: `style.css`

**Content:**
- Card 1: "0" / Zero Parameters
- Card 2: "<1s" / Per-Frame Speed
- Card 3: "200+ px" / Displacement Range
- Card 4: "$0" / Free & Open Source

**Visual:** Glass-morphism cards, CSS Grid 4-col → 2-col on mobile, hover glow, stagger animation.

**Commit:** `feat: highlights section with 4 glass-morphism feature cards`

---

### Task 7: Demo Video section (YouTube embed)

**Files:**
- Modify: `index.html`
- Modify: `style.css`

**Implementation:**
- YouTube `<iframe>` with `loading="lazy"`
- Custom thumbnail overlay (click to load iframe — performance optimization)
- "Load Images → Set ROI → Process → Visualize" flow text below
- Glow card wrapper matching Hero style

**Commit:** `feat: demo video section with lazy-loaded YouTube embed`

---

### Task 8: Method section (pipeline diagram)

**Files:**
- Modify: `index.html`
- Modify: `style.css`

**Implementation:**
- 4-node horizontal pipeline with CSS Grid
- Gradient connecting lines (SVG or CSS `::after` pseudo-elements)
- Each node: image placeholder + label
- Summary text below
- Vertical layout on mobile

**Commit:** `feat: method pipeline section with connected node diagram`

---

### Task 9: Results Gallery (carousel)

**Files:**
- Modify: `index.html`
- Modify: `style.css`
- Modify: `script.js`

**Implementation:**
- Vanilla JS carousel (~60 lines)
- Slide structure: left image + right image + caption
- Dot navigation + arrow buttons
- Touch/swipe support (`touchstart`/`touchmove`)
- Auto-rotate 5s, pause on hover
- 4-6 placeholder slides

**Commit:** `feat: results gallery carousel with touch support`

---

### Task 10: Comparison table

**Files:**
- Modify: `index.html`
- Modify: `style.css`

**Implementation:**
- HTML `<table>` with custom dark styling
- RAFTcorr column highlighted with blue accent
- Alternating row backgrounds
- Advantage cells in bright text
- Footnote for accuracy trade-off
- Mobile: horizontal scroll or card transform

**Commit:** `feat: comparison table with highlighted RAFTcorr column`

---

## Phase 3: Academic & Polish (Tasks 11-15)

### Task 11: Team section (authors)

**Files:**
- Modify: `index.html`
- Modify: `style.css`

**Implementation:**
- 5 circular avatar placeholders (initials or photos)
- Name + institution below each
- Clickable links to personal pages
- Flex row, centered

**Commit:** `feat: team section with author cards`

---

### Task 12: Citation section (BibTeX)

**Files:**
- Modify: `index.html`
- Modify: `style.css`
- Modify: `script.js`

**Implementation:**
- Dark code block with monospace font
- Placeholder BibTeX entry
- "Copy" button: `navigator.clipboard.writeText()`
- Visual feedback on copy (button text changes briefly)

**Commit:** `feat: citation section with one-click BibTeX copy`

---

### Task 13: Footer

**Files:**
- Modify: `index.html`
- Modify: `style.css`

**Implementation:**
- Minimal: "RAFTcorr · The University of Texas at Austin"
- Links: GitHub · Paper · Contact
- Darker background `#060a14`

**Commit:** `feat: minimal footer with links`

---

### Task 14: Responsive polish

**Files:**
- Modify: `style.css`

**Implementation:**
- Test all sections at 1440px, 1024px, 768px, 480px, 375px
- Fix any layout breaks
- Hamburger menu interaction
- Touch-friendly tap targets (min 44px)
- Carousel swipe on mobile

**Commit:** `fix: responsive layout polish across all breakpoints`

---

### Task 15: Performance & SEO

**Files:**
- Modify: `index.html`
- Modify: `style.css`

**Implementation:**
- Open Graph meta tags (for social sharing preview)
- `<link rel="icon">` favicon
- Image lazy loading (`loading="lazy"`)
- Preload hero video/fonts
- Minify CSS/JS (optional, can use online tool)
- `<meta>` description, keywords
- Structured data (optional)

**Commit:** `chore: add meta tags, favicon, lazy loading, and preload hints`

---

## Phase 4: Deployment (Task 16)

### Task 16: GitHub Pages deployment

**Steps:**
1. Create GitHub repo `raftcorr` (public)
2. Push all code to `main`
3. Enable GitHub Pages: Settings → Pages → Source: main branch, root
4. Verify at `zachtong.github.io/raftcorr`
5. Test on mobile device

**Commit:** `chore: configure GitHub Pages deployment`

---

## Phase 5: Content Population (Ongoing)

### Task 17: Replace placeholders with real assets

- [ ] Hero animation video (MP4, <5MB)
- [ ] YouTube demo video URL
- [ ] 4-6 result image pairs (original + colormap)
- [ ] Method diagram images
- [ ] Author photos
- [ ] Comparison screenshots (optional)
- [ ] Final BibTeX entry (when paper ready)
- [ ] License decision

This phase is ongoing as assets become available.

---

## Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| 1 | 1-5 | Foundation: skeleton, navbar, hero, video, animations |
| 2 | 6-10 | Content: highlights, demo, method, results, comparison |
| 3 | 11-15 | Academic: team, citation, footer, responsive, SEO |
| 4 | 16 | Deployment to GitHub Pages |
| 5 | 17 | Asset population (ongoing) |

**Total estimated tasks:** 17 (Phase 1-4: 16 implementation tasks + 1 ongoing content task)
