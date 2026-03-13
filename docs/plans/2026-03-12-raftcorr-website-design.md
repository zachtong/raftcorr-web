# RAFTcorr Promotional Website — Design Document

**Date:** 2026-03-12
**Status:** Approved

## Overview

A promotional single-page website for RAFTcorr, combining product-style visual impact (SAM2 aesthetic) with academic content (NeRF-style). Dark sci-fi theme with colorful DIC result visualizations.

## Decisions

| Decision | Choice |
|----------|--------|
| Style | Hybrid: product hero + academic content |
| Paper status | In preparation (placeholder BibTeX) |
| Assets available | Results, comparisons, GUI recordings, experiment photos, method diagrams |
| Hosting | GitHub Pages (`username.github.io/raftcorr`) |
| Tech stack | Pure HTML + CSS + vanilla JS, zero dependencies |
| Color scheme | Dark sci-fi (deep blue-black + blue/teal accents) |
| Hero visual | Deformation animation (auto-loop video), centered, minimal text |
| Video hosting | YouTube embed |
| Sections | All 9 (Hero, Highlights, Demo, Method, Results, Comparison, Authors, Citation, Footer) |

## Tech Stack

- **Structure:** Single `index.html` + `style.css` + `script.js`
- **Animations:** CSS transitions + `Intersection Observer` for scroll-triggered fade-in/slide-up
- **Video:** `<video>` autoplay for Hero, YouTube `<iframe>` for Demo
- **Glass effect:** CSS `backdrop-filter: blur()` on cards
- **Responsive:** Mobile-first media queries
- **Deployment:** GitHub Pages, `main` branch, push-to-deploy

## Color System

```css
:root {
  --bg-primary: #0a0f1c;
  --bg-secondary: #1a2332;
  --bg-card: rgba(255, 255, 255, 0.03);
  --accent-blue: #4a9eff;
  --accent-teal: #00d4aa;
  --text-primary: #ffffff;
  --text-secondary: #94a3b8;
  --glow-blue: rgba(74, 158, 255, 0.15);
  --footer-bg: #060a14;
}
```

## Project Structure

```
raftcorr-website/
├── index.html
├── style.css
├── script.js
├── assets/
│   ├── videos/          # Hero animation (MP4/WebM), compressed <5MB
│   ├── images/          # Result figures, comparison images, author photos
│   ├── icons/           # Paper/Code/Data SVG icons
│   └── fonts/           # Optional self-hosted fonts
├── CNAME                # Optional custom domain
└── README.md
```

## Section Designs

### 1. Hero (Full Viewport)

**Layout:** Centered, video-dominant, Apple-style minimal.

- Deformation animation occupies 60-70% of visual area, centered
- Below video: project name (2 words) + one-line tagline
- Two small buttons: "Get Started" (solid blue) + "GitHub" (outlined)
- Background: radial gradient `#0a0f1c` → `#162a4a` with faint grid texture
- Video card: rounded corners + subtle blue glow border
- Faint scroll-down arrow animation at bottom
- **Principle: First screen does ONE thing — visually captivate. No clutter.**

### 2. Highlights (4 Cards)

**Layout:** 4 equal-width cards in a row, stagger fade-in on scroll.

| Card | Big Text | Title | Description |
|------|----------|-------|-------------|
| 1 | **0** | Zero Parameters | No subset size, step size, or strain window to tune |
| 2 | **<1s** | Per-Frame Speed | GPU-accelerated dense field in under a second |
| 3 | **200+ px** | Displacement Range | Native large deformation without initial guess |
| 4 | **$0** | Free & Open Source | Fully open source, runs on any NVIDIA GPU |

- Glass-morphism cards (`rgba(255,255,255,0.03)` + blur)
- Hover: card border glows blue
- Stagger animation: 100ms delay between cards
- Mobile: 2×2 grid

### 3. Demo Video

**Layout:** Centered YouTube embed, ~70% page width.

- Rounded card with blue glow border (matches Hero card style)
- Custom thumbnail: GUI screenshot showing strain field visualization
- Click-to-play (not autoplay — differentiate from Hero)
- Below video: minimal 4-step flow text
  `Load Images → Set ROI → Process → Visualize`
- Fade-in on scroll

### 4. Method (How It Works)

**Layout:** Horizontal pipeline, 4 nodes connected by gradient lines.

```
[Speckle Images] →  [RAFT Network]  →  [Displacement Field]  →  [Strain Field]
   (photo)        (architecture)         (u,v colormap)       (εxx,εyy colormap)
```

- Each node: small card with real image/figure on top, label below
- Connecting lines: gradient blue→teal with arrowheads
- Labels on lines: "Feature Extraction", "Iterative Update", "Strain Computation"
- 2-3 sentence summary below (~50 words):
  > "RAFTcorr feeds speckle image pairs into a deep optical flow network (RAFT) to produce dense displacement fields. Strain fields are then computed via a virtual strain gauge method — no iterative optimization, no parameter tuning."
- Scroll animation: nodes appear left-to-right sequentially
- Mobile: vertical layout

### 5. Results Gallery

**Layout:** Large carousel with left-right image pairs.

- Each slide: original speckle image (left) + colormap result (right)
- Caption below: experiment name and type
- Glass card + glow border
- Dot navigation + arrow buttons, swipe/drag support
- Auto-rotate every 5s, pause on hover
- Fade-in on scroll

**Suggested cases (4-6):**

| # | Experiment Type | Showcase Focus |
|---|----------------|----------------|
| 1 | Tensile test | Basic displacement + strain concentration |
| 2 | Bending/compression | Complex deformation patterns |
| 3 | Large deformation | 200+ px capability |
| 4 | Low-texture surface | Robustness advantage |
| 5 | High-speed/dynamic | Time-series animation |
| 6 | Side-by-side comparison | RAFTcorr vs traditional DIC |

### 6. Comparison Table

**Layout:** 3-column dark table with RAFTcorr column highlighted.

| Metric | RAFTcorr ✦ | Ncorr | Commercial (VIC-2D) |
|--------|-----------|-------|---------------------|
| Speed | <1s/frame | ~minutes | ~minutes |
| Range | 200+ px | ~15 px | ~20 px |
| Parameters | 0 | 5-8 | 5-8 |
| Accuracy | ~0.03 px | ~0.01 px | ~0.01 px |
| Cost | Free | Free | $$$ |
| GPU Accel. | ✓ CUDA | ✗ | ✗ |
| Interface | Web GUI | MATLAB | Desktop |

- Dark semi-transparent rows with alternating shades
- RAFTcorr column: blue highlight
- Advantages in bright text, trade-offs (accuracy) in normal gray — honest presentation
- Footnote: accuracy trade-off disclaimer
- Scroll animation: rows slide in from left
- Mobile: card-based comparison (one card per tool)

### 7. Team (Authors)

- Circular avatar photos (or initials placeholder if no photo)
- Names clickable → personal homepage / Google Scholar
- Institution: UT Austin for all
- PI (Jin Yang) in final position or with special marker

**Authors:** Zixiang (Zach) Tong, Lehu Bu, Qihang Shi, Runtian Du, Jin Yang

### 8. Citation

- Dark code block, monospace font
- BibTeX entry (placeholder until paper published)
- "Copy" button in bottom-right corner (one-click clipboard copy)
- Pre-publication format:

```bibtex
@article{tong2026raftcorr,
  title={RAFTcorr: Deep Learning Digital Image Correlation},
  author={Tong, Zixiang and Bu, Lehu and Shi, Qihang and Du, Runtian and Yang, Jin},
  year={2026},
  note={In preparation}
}
```

### 9. Footer

- Minimal single line: `RAFTcorr · UT Austin`
- Links: GitHub · Paper · Contact
- Optional: UT Austin or lab logo
- Background: `#060a14` (darker than main)

## Asset Preparation Checklist

- [ ] Hero animation: 5-10s loop, MP4, compressed <5MB
- [ ] Demo video: 1-2 min GUI walkthrough, upload to YouTube
- [ ] Result images: 4-6 cases, original + colormap pairs, high-res PNG
- [ ] Comparison images: RAFTcorr vs traditional DIC side-by-side
- [ ] Method diagram: RAFT architecture simplified figure
- [ ] Author photos: square crop, consistent style
- [ ] GUI screenshots: for video thumbnail and fallback

## Implementation Notes

- Font: `Inter` or `Space Grotesk` (Google Fonts) for headings, system font stack for body
- All animations via CSS `@keyframes` + `Intersection Observer` in JS
- Carousel: vanilla JS implementation (~50 lines), no library needed
- BibTeX copy: `navigator.clipboard.writeText()` API
- Responsive breakpoints: 768px (tablet), 480px (mobile)
- Lazy load images below the fold for fast initial paint
- Video: `<video muted autoplay loop playsinline>` for Hero
