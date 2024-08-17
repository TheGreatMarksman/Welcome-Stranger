document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('searchForm');
    const searchBar = document.getElementById('searchBar');
    const scrollableList = document.getElementById('scrollableList');
    const listSections = scrollableList.getElementsByClassName('listSection');

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting
        const query = searchBar.value.toLowerCase();
        Array.from(listSections).forEach(section => {
            const text = section.textContent.toLowerCase();
            if (text.includes(query)) {
                section.style.display = '';
            } else {
                section.style.display = 'none';
            }
        });
    });
});
