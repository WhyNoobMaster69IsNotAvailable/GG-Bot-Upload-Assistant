
document.addEventListener('DOMContentLoaded', function() {
    const variableFilter = document.getElementById('variable-filter');
    const showRequiredOnly = document.getElementById('show-required-only');

    if (!variableFilter || !showRequiredOnly) return;

    // Filter variables based on search and filters
    function filterVariables() {
        const searchTerm = variableFilter.value.toLowerCase();
        const requiredOnly = showRequiredOnly.checked;

        document.querySelectorAll('.variable-row').forEach(row => {
            const varName = row.querySelector('.var-name').textContent.toLowerCase();
            const varDescription = row.querySelector('.var-description').textContent.toLowerCase();
            const isRequired = row.querySelector('.var-required').textContent === 'Yes';

            const matchesSearch = searchTerm === '' ||
                varName.includes(searchTerm) ||
                varDescription.includes(searchTerm);

            const matchesFilter = !requiredOnly || isRequired;

            row.style.display = (matchesSearch && matchesFilter) ? '' : 'none';
        });

        // Hide sections that have no visible variables
        document.querySelectorAll('.config-section').forEach(section => {
            const visibleRows = Array.from(section.querySelectorAll('.variable-row'))
                .filter(row => row.style.display !== 'none');

            section.style.display = visibleRows.length > 0 ? '' : 'none';
        });
    }

    // Event listeners
    variableFilter.addEventListener('input', filterVariables);
    showRequiredOnly.addEventListener('change', filterVariables);

    // Initialize smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                });
            }
        });
    });
});
