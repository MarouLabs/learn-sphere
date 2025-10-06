/**
 * Lesson Sidebar
 * Handles the toggleable sidebar for module lessons navigation
 */

class LessonSidebar {
    constructor() {
        this.sidebar = document.getElementById('lessonSidebar');
        this.toggleBtn = document.getElementById('sidebarToggle');
        this.closeBtn = document.getElementById('sidebarClose');
        this.overlay = document.getElementById('sidebarOverlay');
        this.page = document.querySelector('.ls-lesson-view-page');
        this.STORAGE_KEY = 'lessonSidebarOpen';

        if (!this.sidebar || !this.toggleBtn) {
            return;
        }

        this.init();
    }

    init() {
        // Restore sidebar state from localStorage
        this.restoreState();

        this.toggleBtn.addEventListener('click', () => this.toggle());

        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.close());
        }

        if (this.overlay) {
            this.overlay.addEventListener('click', () => this.close());
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen()) {
                this.close();
            }
        });

        // Handle window resize
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768 && this.isOpen()) {
                // Desktop: remove overlay and body scroll lock
                if (this.overlay) {
                    this.overlay.classList.remove('active');
                }
                document.body.style.overflow = '';
            }
        });
    }

    restoreState() {
        const savedState = localStorage.getItem(this.STORAGE_KEY);
        if (savedState === 'true') {
            // Open sidebar without animation on page load
            const isMobile = window.innerWidth <= 768;

            if (!isMobile) {
                // Only restore on desktop
                if (this.page) {
                    this.page.classList.add('sidebar-open');
                }
            }
        }
    }

    saveState(isOpen) {
        localStorage.setItem(this.STORAGE_KEY, isOpen.toString());
    }

    toggle() {
        if (this.isOpen()) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        const isMobile = window.innerWidth <= 768;

        if (isMobile) {
            // Mobile: overlay behavior
            this.sidebar.classList.add('open');
            if (this.overlay) {
                this.overlay.classList.add('active');
            }
            document.body.style.overflow = 'hidden';
            this.saveState(false); // Don't persist on mobile
        } else {
            // Desktop: push behavior
            if (this.page) {
                this.page.classList.add('sidebar-open');
            }
            this.saveState(true); // Persist on desktop
        }
    }

    close() {
        const isMobile = window.innerWidth <= 768;

        if (isMobile) {
            // Mobile: remove overlay
            this.sidebar.classList.remove('open');
            if (this.overlay) {
                this.overlay.classList.remove('active');
            }
            document.body.style.overflow = '';
            this.saveState(false); // Don't persist on mobile
        } else {
            // Desktop: remove push
            if (this.page) {
                this.page.classList.remove('sidebar-open');
            }
            this.saveState(false); // Persist closed state on desktop
        }
    }

    isOpen() {
        const isMobile = window.innerWidth <= 768;

        if (isMobile) {
            return this.sidebar.classList.contains('open');
        } else {
            return this.page && this.page.classList.contains('sidebar-open');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new LessonSidebar();
});
