import * as Shared from './shared.js';

var localData;
var headerTitle;
var headerYear;

function removeRowsExceptHeader(table) {
  if (!table) return; // Check if table exists

  const rows = table.rows; // Get all table rows
  for (let i = rows.length - 1; i > 0; i--) { // Loop from 1 to skip the header row
    rows[i].remove(); // Remove each row except the first one (index 0)
  }
}

function buildListView(data) {
  localData = data;
  const table = document.getElementById('movie-table');
  removeRowsExceptHeader(table);

  headerTitle.querySelector('.sort-arrow').classList.remove('sort-asc', 'sort-desc');
  headerYear.querySelector('.sort-arrow').classList.remove('sort-asc', 'sort-desc');

  if (Shared.sortBy == Shared.sortByTitle) 
    if (Shared.sortAsc)
      headerTitle.querySelector('.sort-arrow').classList.add('sort-asc');
    else
      headerTitle.querySelector('.sort-arrow').classList.add('sort-desc');
  else 
    if (Shared.sortAsc)
      headerYear.querySelector('.sort-arrow').classList.add('sort-asc');
    else
      headerYear.querySelector('.sort-arrow').classList.add('sort-desc');

  data = data.sort(Shared.compare);
  for (var key in data) {
    const item = data[key];

    //row
    const tableRow = document.createElement('tr');
    //will add this at the end

    //title div 
    const title = document.createElement('td');
    title.textContent = item.title;
    title.style = "text-align: left;";
    tableRow.appendChild(title);

    //year 
    const year = document.createElement('td');
    year.textContent = item.year;
    tableRow.appendChild(year);

    //seasons div
    const seasonTags = document.createElement('td');
    if (item.hasOwnProperty('seasons') && item.seasons.length > 0) {
      const buttonDiv = document.createElement('button');
      buttonDiv.type = 'button';
      buttonDiv.innerText = "Season Details";
      buttonDiv.classList.add('btn', 'btn-primary');
      buttonDiv.addEventListener('click', function (event) {
        Shared.showSeasonModal(item);
      });
      seasonTags.appendChild(buttonDiv);
    } else {
      //tags div
      if (item.hasOwnProperty('tags') && item.tags.length > 0) {
        for (const tag of item.tags) {
          const tagElement = document.createElement('img');
          tagElement.src = `/static/images/icons/${tag}.png`;
          tagElement.alt = `${tag}`;
          tagElement.classList.add('tag-icon');
          seasonTags.appendChild(tagElement);
        }
      }
    }
    tableRow.appendChild(seasonTags);

    //imdb 
    const imdb = document.createElement('td');
    if (item.imdb != '-') {
      const imdbLink = document.createElement('a');
      imdbLink.href = item.imdb;
      imdb.appendChild(imdbLink);
      const imdbIcon = document.createElement('img');
      imdbIcon.src = '/static/images/icons/imdb.png';
      imdbIcon.classList.add('imdb-icon');
      imdbLink.appendChild(imdbIcon);
    }
    tableRow.appendChild(imdb);

    //tmdb 
    const tmdb = document.createElement('td');
    if (item.tmdb != '-') {
      const tmdbLink = document.createElement('a');
      tmdbLink.href = item.tmdb;
      tmdb.appendChild(tmdbLink);
      const tmdbIcon = document.createElement('img');
      tmdbIcon.src = '/static/images/icons/tmdb.png';
      tmdbIcon.classList.add('tmdb-icon');
      tmdbLink.appendChild(tmdbIcon);
    }
    tableRow.appendChild(tmdb);

    //add built card to parent
    table.append(tableRow);
  }
}

headerYear = document.getElementById('headerYear');
headerTitle = document.getElementById('headerTitle');

headerYear.addEventListener('click', (event) => {
  Shared.changeSort(Shared.sortByYear);
  buildListView(localData);
});

headerTitle.addEventListener('click', (event) => {
  Shared.changeSort(Shared.sortByTitle);
  buildListView(localData);
});

Shared.initialLoad(buildListView);

