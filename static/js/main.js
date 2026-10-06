/**
 * MPath Career Counselling - Next-Generation Dynamic Platform Engine
 * Modern scroll experience, IntersectionObserver reveals, micro-interactions,
 * live Quick Path search, ecosystem explorer, and statistics counters.
 * Zero emojis - Pure institutional polish.
 */

(function () {
    "use strict";

    // 1. Accessibility Check
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // =========================================================================
    // 2. SCROLL REVEAL SYSTEM (IntersectionObserver)
    // =========================================================================
    function initScrollReveal() {
        const revealElements = document.querySelectorAll(
            ".reveal, .reveal-up, .reveal-fade, .reveal-scale, .reveal-stagger"
        );

        if (!revealElements.length) return;

        if (prefersReducedMotion || !("IntersectionObserver" in window)) {
            revealElements.forEach((el) => el.classList.add("is-revealed"));
            return;
        }

        const revealObserver = new IntersectionObserver(
            (entries, observer) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const target = entry.target;
                        target.classList.add("is-revealed");

                        // Apply stagger delays to direct children if specified
                        if (target.classList.contains("reveal-stagger")) {
                            const children = target.querySelectorAll(".stagger-item");
                            children.forEach((child, index) => {
                                child.style.transitionDelay = `${Math.min(index * 60, 360)}ms`;
                                child.classList.add("is-revealed");
                            });
                        }

                        observer.unobserve(target);
                    }
                });
            },
            {
                threshold: 0.12,
                rootMargin: "0px 0px -40px 0px",
            }
        );

        revealElements.forEach((el) => revealObserver.observe(el));
    }

    // =========================================================================
    // 3. DYNAMIC NAVBAR SCROLL TRANSFORMATION
    // =========================================================================
    function initNavbarScroll() {
        const navbar = document.querySelector(".career-navbar");
        if (!navbar) return;

        let ticking = false;

        function updateNavbar() {
            const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
            if (currentScroll > 24) {
                navbar.classList.add("navbar-scrolled");
            } else {
                navbar.classList.remove("navbar-scrolled");
            }
            ticking = false;
        }

        window.addEventListener(
            "scroll",
            () => {
                if (!ticking) {
                    window.requestAnimationFrame(updateNavbar);
                    ticking = true;
                }
            },
            { passive: true }
        );

        updateNavbar();
    }

    // =========================================================================
    // 4. ANIMATED STATISTICS COUNTER (Eased from 0 to real DB count)
    // =========================================================================
    function initStatCounters() {
        const counters = document.querySelectorAll(".stat-count[data-target]");
        if (!counters.length) return;

        function easeOutCubic(t) {
            return 1 - Math.pow(1 - t, 3);
        }

        function animateCounter(el) {
            const rawTarget = el.getAttribute("data-target") || "0";
            const target = parseInt(rawTarget.replace(/[^0-9]/g, ""), 10);
            if (isNaN(target) || target <= 0) return;

            if (prefersReducedMotion) {
                el.textContent = target.toLocaleString("en-IN");
                return;
            }

            const duration = 1200;
            const startTime = performance.now();

            function update(now) {
                const elapsed = now - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const current = Math.floor(target * easeOutCubic(progress));
                el.textContent = current.toLocaleString("en-IN");

                if (progress < 1) {
                    requestAnimationFrame(update);
                } else {
                    el.textContent = target.toLocaleString("en-IN");
                }
            }

            requestAnimationFrame(update);
        }

        const counterObserver = new IntersectionObserver(
            (entries, observer) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.2 }
        );

        counters.forEach((c) => counterObserver.observe(c));
    }

    // =========================================================================
    // 5. QUICK PATH NAVIGATOR (Live Real-Time Suggestions on Hero)
    // =========================================================================
    function initQuickPathNavigator() {
        const input = document.getElementById("heroSearchInput");
        const dropdown = document.getElementById("heroSearchSuggestions");
        const form = document.getElementById("heroSearchForm");

        if (!input || !dropdown) return;

        let debounceTimer = null;
        let selectedIndex = -1;

        function hideDropdown() {
            dropdown.classList.remove("show");
            dropdown.innerHTML = "";
            selectedIndex = -1;
        }

        function renderResults(results, query) {
            if (!results || results.length === 0) {
                dropdown.innerHTML = `
                    <div class="p-3 text-center text-muted small">
                        <span>No records matching "<strong>${escapeHtml(query)}</strong>".</span>
                        <div class="mt-1 text-secondary" style="font-size: 0.8rem;">
                            Try searching for <em>Data Scientist, Doctor, UPSC, IIT, B.Tech,</em> or <em>Scholarships</em>.
                        </div>
                    </div>
                `;
                dropdown.classList.add("show");
                return;
            }

            const badgeStyles = {
                CAREER: "badge-cat-career",
                COURSE: "badge-cat-course",
                COLLEGE: "badge-cat-college",
                EXAM: "badge-cat-exam",
                SCHOLARSHIP: "badge-cat-scholarship",
            };

            const html = results
                .map((item, idx) => {
                    const badgeClass = badgeStyles[item.category] || "badge-cat-default";
                    return `
                    <a href="${item.url}" class="suggestion-item d-flex align-items-center justify-content-between p-2 px-3 text-decoration-none" data-index="${idx}">
                        <div class="d-flex align-items-center gap-2 overflow-hidden">
                            <span class="badge ${badgeClass} text-uppercase" style="font-size: 0.68rem; letter-spacing: 0.04em;">
                                ${item.category}
                            </span>
                            <div class="text-truncate">
                                <div class="fw-semibold text-navy text-truncate" style="font-size: 0.92rem;">
                                    ${escapeHtml(item.title)}
                                </div>
                                <div class="text-muted text-truncate" style="font-size: 0.76rem;">
                                    ${escapeHtml(item.subtitle)}
                                </div>
                            </div>
                        </div>
                        <i data-lucide="arrow-right" class="icon-xs text-muted flex-shrink-0 ms-2"></i>
                    </a>
                `;
                })
                .join("");

            const viewAllUrl = `/search?q=${encodeURIComponent(query)}`;
            dropdown.innerHTML = `
                <div class="suggestion-list py-1">
                    ${html}
                </div>
                <div class="p-2 border-top bg-light text-center">
                    <a href="${viewAllUrl}" class="small text-blue fw-semibold text-decoration-none d-inline-flex align-items-center gap-1">
                        <span>View all results for "${escapeHtml(query)}"</span>
                        <i data-lucide="arrow-right" class="icon-xs"></i>
                    </a>
                </div>
            `;

            dropdown.classList.add("show");
            if (window.lucide) window.lucide.createIcons({ root: dropdown });
        }

        input.addEventListener("input", function () {
            const query = this.value.trim();
            clearTimeout(debounceTimer);

            if (query.length < 2) {
                hideDropdown();
                return;
            }

            debounceTimer = setTimeout(() => {
                fetch(`/api/quick-search?q=${encodeURIComponent(query)}`)
                    .then((res) => res.json())
                    .then((data) => {
                        renderResults(data.results || [], query);
                    })
                    .catch(() => hideDropdown());
            }, 180);
        });

        // Keyboard navigation
        input.addEventListener("keydown", function (e) {
            const items = dropdown.querySelectorAll(".suggestion-item");
            if (!items.length) return;

            if (e.key === "ArrowDown") {
                e.preventDefault();
                selectedIndex = (selectedIndex + 1) % items.length;
                updateSelection(items);
            } else if (e.key === "ArrowUp") {
                e.preventDefault();
                selectedIndex = (selectedIndex - 1 + items.length) % items.length;
                updateSelection(items);
            } else if (e.key === "Enter") {
                if (selectedIndex >= 0 && items[selectedIndex]) {
                    e.preventDefault();
                    items[selectedIndex].click();
                }
            } else if (e.key === "Escape") {
                hideDropdown();
            }
        });

        function updateSelection(items) {
            items.forEach((item, idx) => {
                if (idx === selectedIndex) {
                    item.classList.add("active");
                    item.scrollIntoView({ block: "nearest" });
                } else {
                    item.classList.remove("active");
                }
            });
        }

        // Close on clicking outside
        document.addEventListener("click", function (e) {
            if (form && !form.contains(e.target)) {
                hideDropdown();
            }
        });
    }

    // =========================================================================
    // 6. GLOBAL SEARCH MODAL (Ctrl+K / Search Icon)
    // =========================================================================
    function initGlobalSearchModal() {
        const modalEl = document.getElementById("globalSearchModal");
        if (!modalEl) return;

        const input = document.getElementById("globalSearchInput");
        const resultsContainer = document.getElementById("globalSearchResults");
        let debounceTimer = null;

        // Keyboard Shortcut: Ctrl + K or /
        document.addEventListener("keydown", function (e) {
            if (
                (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k" ||
                (e.key === "/" && !["INPUT", "TEXTAREA"].includes(document.activeElement.tagName))
            ) {
                e.preventDefault();
                const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
                modal.show();
            }
        });

        modalEl.addEventListener("shown.bs.modal", function () {
            if (input) {
                input.focus();
                input.select();
            }
        });

        if (!input || !resultsContainer) return;

        input.addEventListener("input", function () {
            const query = this.value.trim();
            clearTimeout(debounceTimer);

            if (query.length < 2) {
                resultsContainer.innerHTML = `
                    <div class="p-4 text-center text-muted small">
                        <span>Type a career, degree, college name, or exam to search across India.</span>
                    </div>
                `;
                return;
            }

            debounceTimer = setTimeout(() => {
                fetch(`/api/quick-search?q=${encodeURIComponent(query)}`)
                    .then((r) => r.json())
                    .then((data) => {
                        const items = data.results || [];
                        if (!items.length) {
                            resultsContainer.innerHTML = `
                                <div class="p-4 text-center text-muted small">
                                    <span>No records found for "<strong>${escapeHtml(query)}</strong>".</span>
                                </div>
                            `;
                            return;
                        }

                        const badgeStyles = {
                            CAREER: "badge-cat-career",
                            COURSE: "badge-cat-course",
                            COLLEGE: "badge-cat-college",
                            EXAM: "badge-cat-exam",
                            SCHOLARSHIP: "badge-cat-scholarship",
                        };

                        resultsContainer.innerHTML = items
                            .map((it) => {
                                const badgeClass = badgeStyles[it.category] || "badge-cat-default";
                                return `
                                <a href="${it.url}" class="suggestion-item d-flex align-items-center justify-content-between p-3 text-decoration-none border-bottom">
                                    <div class="d-flex align-items-center gap-3 overflow-hidden">
                                        <span class="badge ${badgeClass} text-uppercase" style="font-size: 0.7rem;">
                                            ${it.category}
                                        </span>
                                        <div>
                                            <div class="fw-semibold text-navy" style="font-size: 0.95rem;">
                                                ${escapeHtml(it.title)}
                                            </div>
                                            <div class="text-muted" style="font-size: 0.8rem;">
                                                ${escapeHtml(it.subtitle)}
                                            </div>
                                        </div>
                                    </div>
                                    <i data-lucide="arrow-right" class="icon-xs text-muted"></i>
                                </a>
                            `;
                            })
                            .join("");

                        if (window.lucide) window.lucide.createIcons({ root: resultsContainer });
                    });
            }, 180);
        });
    }

    // =========================================================================
    // 7. INTERACTIVE ECOSYSTEM JOURNEY (Career -> Course -> College -> Skills)
    // =========================================================================
    function initEcosystemJourney() {
        const ecosystemContainer = document.getElementById("mpathEcosystem");
        if (!ecosystemContainer) return;

        const stageButtons = ecosystemContainer.querySelectorAll(".eco-step-pill");
        const stageCards = ecosystemContainer.querySelectorAll(".eco-stage-card");

        stageButtons.forEach((btn) => {
            btn.addEventListener("click", function () {
                const targetStage = this.getAttribute("data-stage");

                stageButtons.forEach((b) => b.classList.remove("active"));
                this.classList.add("active");

                stageCards.forEach((card) => {
                    if (card.getAttribute("data-stage") === targetStage) {
                        card.classList.remove("d-none");
                        card.classList.add("fade-in-active");
                    } else {
                        card.classList.add("d-none");
                        card.classList.remove("fade-in-active");
                    }
                });

                if (window.lucide) window.lucide.createIcons({ root: ecosystemContainer });
            });
        });
    }

    // =========================================================================
    // 8. INTERACTIVE AI CAREER MENTOR HOMEPAGE PREVIEW
    // =========================================================================
    function initMentorPreview() {
        const previewRoot = document.getElementById("mentorPreviewWidget");
        if (!previewRoot) return;

        const chips = previewRoot.querySelectorAll(".mentor-chip");
        const inquiryText = previewRoot.querySelector(".mentor-inquiry-text");
        const responseText = previewRoot.querySelector(".mentor-response-text");
        const actionCluster = previewRoot.querySelector(".mentor-actions-cluster");

        const sampleKnowledge = {
            "tech-math": {
                question: "What high-growth careers combine Mathematics & Computer Science?",
                answer: "Based on verified employment metrics across India, premier avenues include <strong>Data Scientist</strong>, <strong>Artificial Intelligence Engineer</strong>, and <strong>Actuarial Analyst</strong>. These paths require robust foundations in linear algebra, algorithms, and statistical modeling.",
                actions: [
                    { label: "Explore Data Science", url: "/careers/data-scientist", icon: "compass" },
                    { label: "View B.Tech AI Courses", url: "/courses/43", icon: "book-open" },
                    { label: "Find Tech Colleges", url: "/colleges/?discipline=Computer+Applications", icon: "landmark" },
                ],
            },
            psychology: {
                question: "How do I become a Clinical Psychologist in India?",
                answer: "The statutory pathway requires 10+2 (any stream with preference for Biology/Psychology) &rarr; <strong>BA / B.Sc Psychology (3–4 years)</strong> &rarr; <strong>MA / M.Sc Psychology</strong> &rarr; <strong>M.Phil in Clinical Psychology</strong> from an RCI-recognized institution.",
                actions: [
                    { label: "Psychology Degrees", url: "/courses/?discipline=Psychology", icon: "book-open" },
                    { label: "Accredited Colleges", url: "/colleges/?search=Psychology", icon: "landmark" },
                    { label: "Explore Mental Health Careers", url: "/careers/?category=Medical+%26+Healthcare", icon: "compass" },
                ],
            },
            civil: {
                question: "What are the stages and eligibility for UPSC Civil Services?",
                answer: "The UPSC CSE is an annual national examination open to graduates of any recognized university (min. age 21). It follows 3 distinct stages: <strong>Preliminary Examination</strong> (Objective), <strong>Mains Examination</strong> (Written 9 Papers), and <strong>Personality Test</strong> (Interview).",
                actions: [
                    { label: "UPSC CSE Dossier", url: "/exams/1", icon: "file-text" },
                    { label: "All Civil Services Exams", url: "/exams/?category=Civil+Services", icon: "layers" },
                    { label: "Explore IAS Officer Track", url: "/careers/?category=Government+%26+Civil+Services", icon: "briefcase" },
                ],
            },
        };

        chips.forEach((chip) => {
            chip.addEventListener("click", function () {
                const key = this.getAttribute("data-key");
                const data = sampleKnowledge[key];
                if (!data) return;

                chips.forEach((c) => c.classList.remove("active"));
                this.classList.add("active");

                if (inquiryText) inquiryText.innerHTML = `"${escapeHtml(data.question)}"`;
                if (responseText) responseText.innerHTML = data.answer;

                if (actionCluster && data.actions) {
                    actionCluster.innerHTML = data.actions
                        .map(
                            (act) => `
                        <a href="${act.url}" class="btn btn-sm btn-outline-primary d-inline-flex align-items-center gap-1 rounded-pill">
                            <i data-lucide="${act.icon}" class="icon-xs"></i>
                            <span>${act.label}</span>
                        </a>
                    `
                        )
                        .join("");
                    if (window.lucide) window.lucide.createIcons({ root: actionCluster });
                }
            });
        });
    }

    // =========================================================================
    // 9. HORIZONTAL SCROLL HELPERS
    // =========================================================================
    function initHorizontalCarousels() {
        const containers = document.querySelectorAll(".horizontal-carousel-wrapper");
        containers.forEach((wrapper) => {
            const track = wrapper.querySelector(".carousel-track");
            const prevBtn = wrapper.querySelector(".carousel-btn-prev");
            const nextBtn = wrapper.querySelector(".carousel-btn-next");

            if (!track) return;

            const scrollDistance = 340;

            if (prevBtn) {
                prevBtn.addEventListener("click", () => {
                    track.scrollBy({ left: -scrollDistance, behavior: "smooth" });
                });
            }

            if (nextBtn) {
                nextBtn.addEventListener("click", () => {
                    track.scrollBy({ left: scrollDistance, behavior: "smooth" });
                });
            }
        });
    }

    // =========================================================================
    // 10. UTILITY: ESCAPE HTML
    // =========================================================================
    function escapeHtml(str) {
        if (!str) return "";
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // =========================================================================
    // INITIALIZATION ON DOM READY
    // =========================================================================
    document.addEventListener("DOMContentLoaded", function () {
        initScrollReveal();
        initNavbarScroll();
        initStatCounters();
        initQuickPathNavigator();
        initGlobalSearchModal();
        initEcosystemJourney();
        initMentorPreview();
        initHorizontalCarousels();

        if (window.lucide) {
            window.lucide.createIcons();
        }
    });
})();
