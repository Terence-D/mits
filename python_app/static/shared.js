var filtered = [];
var foundTagToHide = false;
var movieData;
var seriesData = [];
var filterString = "";
var tagsToHide = [];
var listOfFilters = [];
var collectionSize = 0;
var filterSize = 0;
var displayMovies = true;
var displaySeries = true;

export var sortBy = 10;
export var sortAsc = true;

export const sortByTitle = 10;
export const sortByYear = 20;

function buildUiFunction() {};

async function fetchCount() {
    try {
        const response = await fetch('/api/count');
        const data = await response.json();
        collectionSize = data;
        filterSize = collectionSize;
        buildCountsView();
    } catch (err) {
        console.error('Error fetching data count:', err);
    }
}

async function fetchFilters() {
    try {
        const response = await fetch('/api/filters')
        listOfFilters = await response.json();

        if (listOfFilters.length > 0) {
            buildFilterList();
        }
    } catch (err) {
        console.error(err);
    }
}

async function fetchData() {
    try {
        const responseMovies = await fetch('/api/movies');
        movieData = await responseMovies.json();
        const responseSeries = await fetch('/api/series');
        seriesData = await responseSeries.json();
        viewFilter();
    } catch (err) {
        console.error(err);
    }
}

function viewFilter() {
    filtered = [];
    filterString = filterString.toLowerCase();
    filterSize = 0;

    if (displayMovies) {
        filtered = getFilteredData(movieData);
    }
    if (displaySeries) {
        filtered = filtered.concat(getFilteredData(seriesData, true));
    }
    buildUiFunction(filtered);
    buildCountsView();
}

function getFilteredData(data, checkSeasons = false) {
    filtered = [];
    for (var key in data) {
        const item = JSON.parse(data[key]);
        item.key = key;
        if (item.title.toLowerCase().includes(filterString)) {
            //the title matches, now match the filters
            foundTagToHide = false;
            if (checkSeasons && item.seasons.length > 0) {
                for (var tag in tagsToHide) {
                    for (var season in item.seasons) {
                        if (item.seasons[season].hasOwnProperty('tags')) {
                            if (item.seasons[season].tags.includes(tagsToHide[tag]))
                                foundTagToHide = true;
                        }
                    }
                }
            } else {
                for (var tag in tagsToHide) {
                    if (item.hasOwnProperty('tags')) {
                        if (item.tags.includes(tagsToHide[tag]))
                            foundTagToHide = true;
                    }
                }
            }
            if (!foundTagToHide) {
                filtered.push(item);
                filterSize++;
            }
        }
    }
    return filtered;
}

function buildCountsView() {
    const parentElement = document.getElementById('media-count');
    var displayText = `Size: ${collectionSize} `;
    if (collectionSize != filterSize)
        displayText += `(Displayed: ${filterSize})`;
    parentElement.textContent = displayText;
}

function buildFilterElement(parentElement, id, text) {
    const formElement = document.createElement('li');
    formElement.classList.add('ps-3');

    const checkboxId = "checkbox" + id;
    const inputElement = document.createElement('input');
    inputElement.classList.add('form-check-input');
    inputElement.type = "checkbox";
    inputElement.name = "checkboxGroup";
    inputElement.id = checkboxId;
    inputElement.value = id;
    inputElement.checked = true;
    inputElement.addEventListener('change', function () {
        if (this.checked)
            tagsToHide = tagsToHide.filter(item => item !== this.value);
        else
            tagsToHide.push(this.value);
        viewFilter();
    });
    formElement.appendChild(inputElement);
    const labelElement = document.createElement('label');
    labelElement.classList.add('form-check-inputlabel');
    labelElement.for = checkboxId;
    labelElement.textContent = text;
    formElement.appendChild(labelElement);

    parentElement.appendChild(formElement);
}

function buildFilterList() {
    const parentElement = document.getElementById('filter-list');
    for (var filterItem in listOfFilters) {
        buildFilterElement(parentElement, listOfFilters[filterItem], listOfFilters[filterItem]);
    }
}

function removeArticles(str) {
    var words = str.split(" ");
    if (words.length <= 1) return str;
    if (words[0] == 'a' || words[0] == 'the' || words[0] == 'an')
        return words.splice(1).join(" ");
    return str;
}

function buildControls() {
    const searchInput = document.querySelector('.search-input');

    searchInput.addEventListener('keyup', (event) => {
        const searchTerm = event.target.value; // Get the search term in lowercase
        // Perform your search logic here using searchTerm
        filterString = searchTerm
        viewFilter();
    });

    let clicked = false; // Flag to track clicks

    const refreshFullLink = document.getElementById('refreshFullLink');
    refreshFullLink.addEventListener('click', function (event) {
        new bootstrap.Modal(document.querySelector("#waitModal")).show();
        window.location.href = "/api/refresh/full";
    });
    const refreshPartialLink = document.getElementById('refreshPartialLink');
    refreshPartialLink.addEventListener('click', function (event) {
        new bootstrap.Modal(document.querySelector("#waitModal")).show();
        window.location.href = "/api/refresh/partial";
    });

    const chkMovies = document.getElementById('showMovies');
    const chkSeries = document.getElementById('showSeries');
    chkMovies.addEventListener('click', function (event) {
        displayMovies = chkMovies.checked;
        viewFilter();
    });
    chkSeries.addEventListener('click', function (event) {
        displaySeries = chkSeries.checked;
        viewFilter();
    });
}

document.querySelector('.clear-button').addEventListener('click', () => {
  const searchInput = document.querySelector('.search-input');
  searchInput.value = '';
  filterString = searchInput.value;
  viewFilter();
});

export var compare = function (a, b) {
    var aYear = a.year;
    var bYear = b.year;
    var aTitle = a.title.toLowerCase(),
        bTitle = b.title.toLowerCase();

    var rv = 0;

    if (sortBy == sortByTitle) {
        aTitle = removeArticles(aTitle);
        bTitle = removeArticles(bTitle);
    
        if (aTitle > bTitle) rv = 1;
        if (aTitle < bTitle) rv = -1;
    } else {
        if (aYear > bYear) rv =  1;
        if (aYear < bYear) rv = -1;
    }
    if (!sortAsc)
        rv *= -1;
    return rv;
};

export function initialLoad(uiFunction) {
    buildUiFunction = uiFunction;
    fetchFilters();
    fetchData();
    fetchCount();
    buildControls();
}

export function showSeasonModal(item) {
    const modalTitle = document.getElementById('seasonModalLabel');
    modalTitle.innerText = item.title;
    const modal = document.getElementById('modalBody');
    modal.innerHTML = "";
    for (const season of item.seasons) {
      modal.innerHTML += season.seasonTitle + "&nbsp;&nbsp;&nbsp;";
      if (season.hasOwnProperty('tags') && season.tags.length > 0) {
        for (const tag of season.tags) {
          modal.innerHTML += `<img src=/static/images/icons/${tag}.png alt="${tag}" class="tag-icon"><br/>`;
        }
      }
    }
    new bootstrap.Modal(document.querySelector("#seasonModal")).show();
}

export function changeSort(newSort) {
    //if the sort already is set, just reverse it
    if (newSort == sortBy)
        sortAsc = !sortAsc;
    else if (newSort == sortByTitle || newSort == sortByYear) {
        sortAsc = true;
        sortBy = newSort;
    }
}