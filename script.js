/**
 * RAFTcorr Website — Interactions
 *
 * Features:
 *   1. Scroll-triggered animations (Intersection Observer)
 *   2. Navbar scroll state + mobile hamburger menu
 *   3. Results gallery carousel (arrows, dots, touch/swipe, auto-rotate)
 *   4. BibTeX one-click copy
 *   5. Smooth scroll for nav links (mobile menu auto-close)
 */

document.addEventListener("DOMContentLoaded", () => {
  initScrollAnimations();
  initNavbar();
  initCarousel();
  initBibTeXCopy();
  initNewsletterConfirmation();
});


/* ===========================================
   1. SCROLL-TRIGGERED ANIMATIONS
   =========================================== */

function initScrollAnimations() {
  const animatedElements = document.querySelectorAll("[data-animate]");
  if (animatedElements.length === 0) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const delay = parseInt(el.dataset.delay || "0", 10);
        setTimeout(() => {
          el.classList.add("is-visible");
        }, delay);
        observer.unobserve(el);
      });
    },
    {
      threshold: 0.12,
      rootMargin: "0px 0px -40px 0px",
    }
  );

  animatedElements.forEach((el) => observer.observe(el));
}


/* ===========================================
   2. NAVBAR
   =========================================== */

function initNavbar() {
  const navbar = document.getElementById("navbar");
  const hamburger = document.getElementById("hamburger");
  const navLinks = document.getElementById("nav-links");

  if (!navbar || !hamburger || !navLinks) return;

  // --- Scroll state ---
  let lastScrollY = 0;
  const SCROLL_THRESHOLD = 60;

  function handleNavScroll() {
    const currentY = window.scrollY;
    if (currentY > SCROLL_THRESHOLD) {
      navbar.classList.add("navbar--scrolled");
    } else {
      navbar.classList.remove("navbar--scrolled");
    }
    lastScrollY = currentY;
  }

  window.addEventListener("scroll", handleNavScroll, { passive: true });
  handleNavScroll();

  // --- Hamburger toggle ---
  hamburger.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("navbar__links--open");
    hamburger.classList.toggle("navbar__hamburger--open", isOpen);
    hamburger.setAttribute("aria-expanded", String(isOpen));
  });

  // --- Close menu on link click ---
  navLinks.querySelectorAll(".navbar__link").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("navbar__links--open");
      hamburger.classList.remove("navbar__hamburger--open");
      hamburger.setAttribute("aria-expanded", "false");
    });
  });

  // --- Close menu on outside click ---
  document.addEventListener("click", (e) => {
    if (
      navLinks.classList.contains("navbar__links--open") &&
      !navLinks.contains(e.target) &&
      !hamburger.contains(e.target)
    ) {
      navLinks.classList.remove("navbar__links--open");
      hamburger.classList.remove("navbar__hamburger--open");
      hamburger.setAttribute("aria-expanded", "false");
    }
  });

  // --- Active link highlighting based on scroll position ---
  const sections = document.querySelectorAll("section[id]");
  const navAnchors = navLinks.querySelectorAll(".navbar__link[href^='#']");

  function highlightActiveLink() {
    const scrollY = window.scrollY + 120;
    let currentSection = "";

    sections.forEach((section) => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      if (scrollY >= top && scrollY < top + height) {
        currentSection = section.id;
      }
    });

    navAnchors.forEach((anchor) => {
      const href = anchor.getAttribute("href");
      if (href === "#" + currentSection) {
        anchor.classList.add("navbar__link--active");
      } else {
        anchor.classList.remove("navbar__link--active");
      }
    });
  }

  window.addEventListener("scroll", highlightActiveLink, { passive: true });
  highlightActiveLink();
}


/* ===========================================
   3. RESULTS GALLERY CAROUSEL
   =========================================== */

function initCarousel() {
  const track = document.getElementById("carousel-track");
  const prevBtn = document.getElementById("carousel-prev");
  const nextBtn = document.getElementById("carousel-next");
  const dotsContainer = document.getElementById("carousel-dots");

  if (!track || !prevBtn || !nextBtn || !dotsContainer) return;

  const slides = track.querySelectorAll(".results__slide");
  const slideCount = slides.length;
  if (slideCount === 0) return;

  let currentIndex = 0;
  let autoRotateTimer = null;
  const AUTO_ROTATE_INTERVAL = 5000;

  // --- Build dot navigation ---
  for (let i = 0; i < slideCount; i++) {
    const dot = document.createElement("button");
    dot.classList.add("results__carousel-dot");
    if (i === 0) dot.classList.add("results__carousel-dot--active");
    dot.setAttribute("aria-label", `Go to slide ${i + 1}`);
    dot.addEventListener("click", () => goToSlide(i));
    dotsContainer.appendChild(dot);
  }

  const dots = dotsContainer.querySelectorAll(".results__carousel-dot");

  function goToSlide(index) {
    currentIndex = ((index % slideCount) + slideCount) % slideCount;
    track.style.transform = `translateX(-${currentIndex * 100}%)`;

    dots.forEach((d, i) => {
      d.classList.toggle("results__carousel-dot--active", i === currentIndex);
    });
  }

  prevBtn.addEventListener("click", () => {
    goToSlide(currentIndex - 1);
    resetAutoRotate();
  });

  nextBtn.addEventListener("click", () => {
    goToSlide(currentIndex + 1);
    resetAutoRotate();
  });

  // --- Touch / Swipe support ---
  let touchStartX = 0;
  let touchEndX = 0;
  const SWIPE_THRESHOLD = 50;

  track.addEventListener("touchstart", (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  track.addEventListener("touchend", (e) => {
    touchEndX = e.changedTouches[0].screenX;
    const diff = touchStartX - touchEndX;
    if (Math.abs(diff) > SWIPE_THRESHOLD) {
      if (diff > 0) {
        goToSlide(currentIndex + 1);
      } else {
        goToSlide(currentIndex - 1);
      }
      resetAutoRotate();
    }
  }, { passive: true });

  // --- Auto-rotate ---
  function startAutoRotate() {
    autoRotateTimer = setInterval(() => {
      goToSlide(currentIndex + 1);
    }, AUTO_ROTATE_INTERVAL);
  }

  function resetAutoRotate() {
    clearInterval(autoRotateTimer);
    startAutoRotate();
  }

  // Pause on hover
  const carouselRoot = track.closest(".results__carousel");
  if (carouselRoot) {
    carouselRoot.addEventListener("mouseenter", () => {
      clearInterval(autoRotateTimer);
    });
    carouselRoot.addEventListener("mouseleave", () => {
      startAutoRotate();
    });
  }

  startAutoRotate();
}


/* ===========================================
   4. BIBTEX COPY
   =========================================== */

function initBibTeXCopy() {
  const copyBtn = document.getElementById("copy-bibtex");
  const codeBlock = document.getElementById("bibtex-code");

  if (!copyBtn || !codeBlock) return;

  copyBtn.addEventListener("click", async () => {
    const text = codeBlock.textContent.trim();
    try {
      await navigator.clipboard.writeText(text);
      showCopyFeedback(copyBtn, true);
    } catch {
      // Fallback for older browsers
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand("copy");
        showCopyFeedback(copyBtn, true);
      } catch {
        showCopyFeedback(copyBtn, false);
      }
      document.body.removeChild(textarea);
    }
  });
}

/* ===========================================
   5. NEWSLETTER SUBSCRIPTION CONFIRMATION
   =========================================== */

function initNewsletterConfirmation() {
  const params = new URLSearchParams(window.location.search);
  if (params.get("subscribed") !== "1") return;

  const form = document.querySelector(".newsletter__form");
  if (!form) return;

  // Replace form with confirmation message
  const confirmation = document.createElement("p");
  confirmation.className = "newsletter__confirmed newsletter__confirmed--visible";
  confirmation.textContent = "Thanks for subscribing! We\u2019ll keep you posted.";
  form.replaceWith(confirmation);

  // Clean URL without reload
  window.history.replaceState({}, "", window.location.pathname);
}


function showCopyFeedback(btn, success) {
  const textEl = btn.querySelector(".citation__copy-text");
  if (!textEl) return;

  const original = textEl.textContent;
  textEl.textContent = success ? "Copied!" : "Failed";
  btn.classList.add("citation__copy-btn--copied");

  setTimeout(() => {
    textEl.textContent = original;
    btn.classList.remove("citation__copy-btn--copied");
  }, 2000);
}
