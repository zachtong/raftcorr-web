# RAFTcorr Website — Project Rules

## Overview
Promotional single-page website for RAFTcorr (Deep Learning DIC software).
- **Tech stack:** Pure HTML + CSS + vanilla JS, zero dependencies
- **Hosting:** GitHub Pages (`zachtong.github.io/raftcorr-web`)
- **Style:** Dark sci-fi theme, SAM2-style hero + NeRF-style academic content

## Architecture
- Single `index.html` — all 9 sections in one page
- `style.css` — all styles, CSS variables for theming
- `script.js` — scroll animations (Intersection Observer), carousel, BibTeX copy
- `assets/` — videos, images, icons (no build step, direct references)

## Design Document
- Full design spec: `docs/plans/2026-03-12-raftcorr-website-design.md`
- Implementation plan: `docs/plans/2026-03-12-raftcorr-website-implementation.md`

## Coding Conventions
- Semantic HTML5 (`<header>`, `<section>`, `<footer>`)
- BEM-style CSS class naming (`.section__card`, `.hero__title`)
- CSS custom properties for all colors/spacing
- Mobile-first responsive design
- No frameworks, no build tools, no npm

## Permissions
- Claude has autonomous permission to use Bash, Edit, Write, Read, and MCP tools without asking for confirmation.
- Do NOT commit or push automatically — wait for explicit user approval.

## Language Policy
- Communicate with user in Chinese
- All code, comments, commit messages in English
