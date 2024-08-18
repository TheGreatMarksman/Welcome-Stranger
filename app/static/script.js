document.addEventListener('DOMContentLoaded', function () {
    const mapSection = document.querySelector('.mapSection');
    mapSection.addEventListener('click', function () {
        mapSection.classList.toggle('fullscreen');
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const mapSection = document.querySelector('.mapSection');
    const minimizeButton = document.createElement('div');

    // Create the minimize button
    minimizeButton.textContent = 'Minimize';
    minimizeButton.classList.add('minimize-button');
    mapSection.appendChild(minimizeButton);

    // Toggle fullscreen mode when the map or arrow is clicked
    mapSection.addEventListener('click', function (e) {
        // Check if the map is already fullscreen
        if (!mapSection.classList.contains('fullscreen')) {
            // Expand to fullscreen
            mapSection.classList.add('fullscreen');
            minimizeButton.style.display = 'block';
        } else if (!e.target.classList.contains('minimize-button')) {
            // If clicking on the map and it's already fullscreen, do nothing
            return;
        }
    });

    // Handle minimize button click
    minimizeButton.addEventListener('click', function (e) {
        e.stopPropagation(); // Prevent the map from toggling fullscreen again
        mapSection.classList.remove('fullscreen');
        minimizeButton.style.display = 'none';
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const filterButton = document.getElementById('filter-button');
    const selector = document.querySelector('.selector');
    const searchForm = document.getElementById('searchForm');
    const charityList = document.querySelector('.charitylist');

    // Show the filter section when the filter button is clicked
    filterButton.addEventListener('click', function () {
        selector.classList.add('active');
        charityList.classList.add('blurred');
    });

    // Hide the filter section when search is submitted
    searchForm.addEventListener('submit', function () {
        selector.classList.remove('active');
        charityList.classList.remove('blurred');
    });

    // Optional: allow users to minimize the filter manually
    selector.addEventListener('click', function () {
        selector.classList.remove('active');
        charityList.classList.remove('blurred');
    });
});