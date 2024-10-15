import * as Shared from './shared.js';

function buildListView(data) {
  const parentElement = document.getElementById('movie-grid');

  parentElement.innerHTML = '';
  data = data.sort(Shared.compare);
  for (var key in data) {
    const item = data[key];

    //outer card
    const cardElement = document.createElement('div');
    cardElement.classList.add('col-sm-3', 'card', 'card-body', 'card-dark', 'py-0');
    //will add this at the end

    //title div 
    const titleDivElement = document.createElement('div');
    cardElement.appendChild(titleDivElement);

    //title div
    const titleElement = document.createElement('h5');
    titleElement.classList.add('card-title', 'title');
    titleElement.textContent = item.title;
    titleDivElement.appendChild(titleElement);

    //card row
    const rowElement = document.createElement('div');
    rowElement.classList.add('row', 'no-gutters');
    cardElement.appendChild(rowElement);

    //image div 
    const imageDivElement = document.createElement('div');
    imageDivElement.classList.add('col-6');
    rowElement.appendChild(imageDivElement);

    //image itself
    const imageElement = document.createElement('img');
    imageElement.src = `/static/images/media/${item.key}.jpg`;
    imageElement.alt = item.title;
    imageElement.classList.add('movie-poster', 'img-fluid');
    imageDivElement.appendChild(imageElement);

    //details div 
    const detailsDivElement = document.createElement('div');
    detailsDivElement.classList.add('col-6');
    rowElement.appendChild(detailsDivElement);

    //title div
    const detailsElement = document.createElement('p');
    detailsElement.textContent = `Year: ${item.year}`;
    detailsDivElement.appendChild(detailsElement);

    //imdb div
    if (item.imdb != '-') {
      const imdbElement = document.createElement('a');
      imdbElement.href = item.imdb;
      detailsDivElement.appendChild(imdbElement);
      const imdbIconElement = document.createElement('img');
      imdbIconElement.src = '/static/images/icons/imdb.png';
      imdbIconElement.alt = 'IMDb';
      imdbIconElement.classList.add('imdb-icon');
      imdbElement.appendChild(imdbIconElement);
    }

    //tmdb div
    if (item.tmdb != '-') {
      const tagDiv = document.createElement('br');
      detailsDivElement.appendChild(tagDiv);
      const tmdbElement = document.createElement('a');
      tmdbElement.href = item.tmdb;
      detailsDivElement.appendChild(tmdbElement);
      const tmdbIconElement = document.createElement('img');
      tmdbIconElement.alt = "TMDB";
      tmdbIconElement.src = '/static/images/icons/tmdb.png';
      tmdbIconElement.classList.add('tmdb-icon');
      tmdbElement.appendChild(tmdbIconElement);
    }

    //seasons div
    if (item.hasOwnProperty('seasons') && item.seasons.length > 0) {
      const tagDiv = document.createElement('p');
      detailsDivElement.appendChild(tagDiv);
      const buttonDiv = document.createElement('button');
      buttonDiv.type = 'button';
      buttonDiv.innerText = "Season Details";
      buttonDiv.classList.add('btn', 'btn-primary');
      buttonDiv.addEventListener('click', function (event) {
        Shared.showSeasonModal(item);
      });
      detailsDivElement.appendChild(buttonDiv);
    } else {
      //tags div
      if (item.hasOwnProperty('tags') && item.tags.length > 0) {
        for (const tag of item.tags) {
          const tagDiv = document.createElement('p');
          detailsDivElement.appendChild(tagDiv);
          const tagElement = document.createElement('img');
          tagElement.src = `/static/images/icons/${tag}.png`;
          tagElement.alt = `${tag}`;
          tagElement.classList.add('tag-icon');
          detailsDivElement.appendChild(tagElement);
        }
      } else {
        const tagDiv = document.createElement('p');
        detailsDivElement.appendChild(tagDiv);
        const tagElement = document.createElement('img');
        tagElement.src = `/static/images/icons/default.png`;
        tagElement.alt = `Default`;
        tagElement.classList.add('tag-icon');
        detailsDivElement.appendChild(tagElement);
      }
    }

    //add built card to parent
    parentElement.appendChild(cardElement);
  }

  var length = data.length;
  while (length % 3 != 0) {
    length++;
    const emptyElement = document.createElement('div');
    emptyElement.innerText = "asdf";
    emptyElement.classList.add('col-sm-3', 'card', 'card-body', 'card-dark', 'py-0');
    emptyElement.style = "visibility:hidden";
    parentElement.appendChild(emptyElement);
  }
}

Shared.initialLoad(buildListView);