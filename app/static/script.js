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

    // Refresh the list of charities when the user clicks search
    document.getElementById('searchBtn').addEventListener('click', function() {
        const province = document.getElementById('provinceList').value;
        const city = document.getElementById('city').value;
        const nation = document.getElementById('NationList').value;
        const language = document.getElementById('language').value;
        const has_service = document.getElementById('service').checked ? 1 : 0;

        filterCharities(province, city, nation, language, has_service);
    });
    
});


function filterCharities(province, city, nation, language, has_service) {
    fetch('/filter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            province: province,
            city: city,
            nation: nation,
            language: language,
            has_service: has_service
        })
    })
    .then(response => response.json())
    .then(data => {
        // Update the displayed results
        const scrollableList = document.getElementById('scrollableList');
        scrollableList.innerHTML = ''; // Clear the existing results

        data.forEach(charity => {
            const listSection = document.createElement('div');
            listSection.className = 'listSection';

            listSection.innerHTML = `
                <div class="charityName">${charity.organization_name}</div>
                <div class="location">
                    ${charity.address}, ${charity.city_name}, ${charity.province_name}
                </div>
                <br>
                <div>
                    Has church service: ${charity.has_service ? 'Yes' : 'No'}
                </div>
                <div>${charity.description || ''}</div>
                <br>
                <div>Languages: ${charity.languages || ''}</div>
                <div>Nations: ${charity.nations || ''}</div>
                <br>
                <div>${charity.phone || ''} | ${charity.website_name || ''} | ${charity.email || ''}</div>
            `;

            scrollableList.appendChild(listSection);
        });
    });
}