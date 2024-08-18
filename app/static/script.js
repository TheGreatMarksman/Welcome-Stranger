document.addEventListener('DOMContentLoaded', function () {
    // Refresh the list of charities when the user clicks search
    document.getElementById('searchBtn').addEventListener('click', function() {
        const province = document.getElementById('provinceList').value;
        const city = document.getElementById('city').value;
        const nation = document.getElementById('NationList').value;
        const language = document.getElementById('language').value;
        const has_service = document.getElementById('service').checked ? 1 : 0;

        filterCharities(province, city, nation, language, has_service);
    });
    
    filterCharities();

    const searchForm = document.getElementById('searchForm');
    const searchBar = document.getElementById('searchBar');
    let scrollableList = document.getElementById('scrollableList');
    const listSections = scrollableList.getElementsByClassName('listSection');
    
    console.log("list sections: " + listSections[0]);

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
    
    filterCharities();

    for (const dropdown of document.getElementsByClassName('dropdown-input')) {
        menu =  document.getElementById('dropdown-menu');
        dropdown.addEventListener('focus', function() {
            menu.style.display = 'block';
        });

        function filterOptions() {
            let filter = dropdown.value.toLowerCase();
            let dropdownMenu = dropdown.parentElement.querySelector('.dropdown-menu');
            let items = dropdownMenu.getElementsByClassName('dropdown-item');
        
            for (let i = 0; i < items.length; i++) {
                let itemText = items[i].textContent.toLowerCase();
                if (itemText.indexOf(filter) > -1) {
                    items[i].style.display = "";
                } else {
                    items[i].style.display = "none";
                }
            }
        }

        dropdown.addEventListener('input', () => {
            filterOptions();
            menu.style.display = 'block';
        })

        dropdown.parentElement.querySelector('.clear-button').addEventListener('click', function() {
            dropdown.value = ''; // Clear the input field
            document.getElementById('dropdown-menu').style.display = 'none'; // Hide dropdown after clearing input
            filterOptions();
        });
    }
    
    document.getElementById('dropdown-menu').addEventListener('click', function(e) {
        if (e.target.classList.contains('dropdown-item')) {
            e.target.parentElement.parentElement.querySelector('.dropdown-input').value = e.target.textContent;
            e.target.parentElement.style.display = 'none';
        }
    });
    
    document.addEventListener('click', function(e) {
        for (const dropdownMenu of document.getElementsByClassName('dropdown-menu')) {
            let dropdown = dropdownMenu.parentElement.querySelector('.dropdown-input');
            if (!dropdown.contains(e.target)) {
                if (dropdownMenu.style.display == 'none') {
                    continue;
                }

                dropdownMenu.style.display = 'none';

                let value = dropdown.value.toLowerCase();

                if (value.trim() == "") {
                    dropdown.value = "";
                    continue;
                }

                let items = dropdownMenu.getElementsByClassName('dropdown-item');
            
                let hasMatch = false;
                for (let i = 0; i < items.length; i++) {
                    let itemText = items[i].textContent.toLowerCase();
                    if (itemText.indexOf(value) > -1) {
                        hasMatch = true;
                        dropdown.value = items[i].textContent;
                        break;
                    }
                }

                if (!hasMatch) dropdown.value = "";

                filterFromUI();
            }
        }
    });
    
    document.getElementById('provinceList').addEventListener('change', () => {
        updateCityList(document.getElementById('provinceList').value);
    });

    document.getElementById('provinceList').addEventListener('change', () => {
        filterFromUI();
    });
    
    document.getElementById('NationList').addEventListener('change', () => {
        filterFromUI();
    });
});

function updateCityList(province) {
    console.log(province);
    for (const city of document.getElementsByClassName("city-option")) {
        city.classList.remove('hidden');
        if (province != "" && city.attributes.province.value != province) {
            city.classList.add('hidden');
        }
    }
}

function filterFromUI() {
    const province = document.getElementById('provinceList').value;
    const city = document.getElementById('city').value;
    const nation = document.getElementById('NationList').value;

    filterCharities(province, city, nation, null, null);
}

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
                <a class="charityName" href="https://${charity.website_name}">${charity.organization_name}</a>
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
                <div>
                    ${charity.phone || ''} | 
                    <a href="https://${charity.website_name || ''}">${charity.website_name || ''} </a> | 
                    ${charity.email || ''}
                </div>
                <button class="mapButton">Show on Map</button>
            `;
            scrollableList.appendChild(listSection);
        });

        const mapIframe = document.getElementById('map');
        let mapButtons = scrollableList.getElementsByClassName('mapButton');

        // Adds listener for every map button
        Array.from(mapButtons).forEach(btn => {
            btn.addEventListener('click', function(){
                const section = btn.closest('.listSection');
                const location = section.getElementsByClassName('location')[0];
                const address = location.textContent.split(',')[0];
                let mapUrl = `https://www.google.com/maps?q=${encodeURIComponent(address)}&z=15&output=embed`;
                mapIframe.src = mapUrl;
            });
        });
    });
}