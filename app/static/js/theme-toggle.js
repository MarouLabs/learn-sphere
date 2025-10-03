// Theme toggle functionality using user preferences API
class ThemeToggle {
    constructor() {
        this.init();
    }

    init() {
        // Load saved theme on page load
        this.loadSavedTheme();

        // Set up event listener for theme toggle button
        this.setupToggleButton();
    }

    setupToggleButton() {
        const toggleButton = document.getElementById('theme-toggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', () => this.toggleTheme());
        }
    }

    async toggleTheme() {
        // Toggle the UI immediately for responsiveness
        document.body.classList.toggle('light-theme');

        // Determine new theme
        const isLight = document.body.classList.contains('light-theme');
        const newTheme = isLight ? 'light' : 'dark';

        try {
            // Save theme preference via API
            const response = await fetch('/api/user-preferences/theme', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    theme: newTheme
                })
            });

            const result = await response.json();

            if (!result.success) {
                console.error('Failed to save theme preference:', result.error);
                // Revert UI change if API call failed
                document.body.classList.toggle('light-theme');
            }
        } catch (error) {
            console.error('Error saving theme preference:', error);
            // Revert UI change if API call failed
            document.body.classList.toggle('light-theme');
        }
    }

    async loadSavedTheme() {
        try {
            const response = await fetch('/api/user-preferences/theme');
            const result = await response.json();

            if (result.success && result.theme === 'light') {
                document.body.classList.add('light-theme');
            }
        } catch (error) {
            console.error('Error loading theme preference:', error);
            // Fallback to default dark theme
        }
    }
}

// Initialize theme toggle when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ThemeToggle();
});