/**
 * Breadcrumb builder utility
 * Builds breadcrumb navigation from breadcrumb data passed from backend
 */

class BreadcrumbBuilder {
    /**
     * Build breadcrumb HTML from breadcrumb data
     * @param {Array} breadcrumbData - Array of breadcrumb items with {title, url} structure
     * @param {string} containerSelector - CSS selector for breadcrumb container
     */
    static build(breadcrumbData, containerSelector = '.ls-breadcrumb') {
        const container = document.querySelector(containerSelector);
        if (!container) return;

        // Clear existing breadcrumbs
        container.innerHTML = '';

        // Build breadcrumb elements
        breadcrumbData.forEach((item, index) => {
            const isLast = index === breadcrumbData.length - 1;

            // Create link or span based on whether it has a URL
            if (isLast || !item.url) {
                const current = document.createElement('span');
                current.className = 'ls-breadcrumb-current';
                current.textContent = item.title;
                container.appendChild(current);
            } else {
                const link = document.createElement('a');
                link.href = item.url;
                link.className = 'ls-breadcrumb-link';
                link.textContent = item.title;
                container.appendChild(link);

                // Add separator
                const separator = document.createElement('span');
                separator.className = 'ls-breadcrumb-separator';
                separator.textContent = '/';
                container.appendChild(separator);
            }
        });
    }
}
