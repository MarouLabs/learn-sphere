// Module toggle functionality for collapsible modules
function toggleModule(moduleId) {
    const moduleContent = document.getElementById(moduleId);
    const moduleHeader = moduleContent.previousElementSibling;
    const toggleIcon = moduleHeader.querySelector('.ls-module-toggle-icon');
    const moduleCell = moduleContent.closest('.ls-module-cell');
    const moduleNumberColumn = moduleCell.querySelector('.ls-module-number-column');

    if (moduleContent.classList.contains('ls-module-expanded')) {
        // Collapse
        moduleContent.classList.remove('ls-module-expanded');
        moduleHeader.classList.remove('ls-module-header-expanded');
        moduleNumberColumn.classList.remove('ls-module-number-expanded');
        toggleIcon.textContent = '▼';
    } else {
        // Expand
        moduleContent.classList.add('ls-module-expanded');
        moduleHeader.classList.add('ls-module-header-expanded');
        moduleNumberColumn.classList.add('ls-module-number-expanded');
        toggleIcon.textContent = '▲';
    }
}

// Initialize all modules as collapsed on page load
document.addEventListener('DOMContentLoaded', function() {
    const moduleContents = document.querySelectorAll('.ls-module-content');
    moduleContents.forEach(content => {
        content.classList.remove('ls-module-expanded');
    });

    const moduleHeaders = document.querySelectorAll('.ls-module-header');
    moduleHeaders.forEach(header => {
        header.classList.remove('ls-module-header-expanded');
    });

    const toggleIcons = document.querySelectorAll('.ls-module-toggle-icon');
    toggleIcons.forEach(icon => {
        icon.textContent = '▼';
    });

    // Check if URL has a module anchor (e.g., #module-introduction)
    if (window.location.hash) {
        const hash = window.location.hash.substring(1);

        if (hash.startsWith('module-')) {
            const targetModule = document.getElementById(hash);

            if (targetModule) {
                // Find the module content element within this module cell
                const moduleContent = targetModule.querySelector('.ls-module-lessons');

                if (moduleContent) {
                    // Get the module ID for toggling
                    const moduleId = moduleContent.id;

                    // Expand the module
                    const moduleHeader = moduleContent.previousElementSibling;
                    const toggleIcon = moduleHeader.querySelector('.ls-module-toggle-icon');
                    const moduleNumberColumn = targetModule.querySelector('.ls-module-number-column');

                    moduleContent.classList.add('ls-module-expanded');
                    moduleHeader.classList.add('ls-module-header-expanded');
                    moduleNumberColumn.classList.add('ls-module-number-expanded');
                    toggleIcon.textContent = '▲';

                    // Scroll to the module instantly with offset for header
                    setTimeout(() => {
                        const headerOffset = 80;
                        const elementPosition = targetModule.getBoundingClientRect().top;
                        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                        window.scrollTo({
                            top: offsetPosition,
                            behavior: 'auto'
                        });
                    }, 100);
                }
            }
        }
    }
});