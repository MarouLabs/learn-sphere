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
});