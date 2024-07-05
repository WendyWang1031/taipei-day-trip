let isDown = false;
let startX;
let scrollLeft;

const scrollableContainer = document.getElementById("scrollable-container");

export function leftScroll(event) {
  event.preventDefault();
  const scrollDistance = getSrollDistance();
  scrollableContainer.scrollLeft -= scrollDistance;
  console.log("Scrolled left to:", scrollableContainer.scrollLeft);
}

export function rightScroll(event) {
  event.preventDefault();
  const scrollDistance = getSrollDistance();
  scrollableContainer.scrollLeft += scrollDistance;
  console.log("Scrolled right to:", scrollableContainer.scrollLeft);
}

function getSrollDistance() {
  const width = window.innerWidth;
  if (width >= 601 && width <= 1200) {
    return 200;
  } else if (width >= 360 && width <= 600) {
    return 100;
  } else {
    return 400;
  }
}

export function mousedown(event) {
  isDown = true;
  startX = event.pageX - scrollableContainer.offsetLeft;
  scrollLeft = scrollableContainer.scrollLeft;
  scrollableContainer.style.cursor = "grabbing";
}

export function mouseleave() {
  isDown = false;
  scrollableContainer.style.cursor = "grab";
}

export function mouseup() {
  isDown = false;
  scrollableContainer.style.cursor = "grab";
}

export function mousemove(event) {
  if (!isDown) return;
  event.preventDefault;
  const x = event.pageX - scrollableContainer.offsetLeft;
  const speed = (x - startX) * 1.5;
  scrollableContainer.scrollLeft = scrollLeft - speed;
}

export function refreshContent() {
  const attractionsContainer = document.querySelector(".attractions-group");
  attractionsContainer.innerHTML = "";
}

export function displayAttractions(attractions, keyword) {
  const attractionsContainer = document.querySelector(".attractions-group");

  if (attractions.length === 0) {
    attractionsContainer.innerHTML = "";
    const noDataMessage = document.createElement("div");
    noDataMessage.textContent = `查無此"${keyword}"相關景點`;
    noDataMessage.style.color = "red";
    attractionsContainer.appendChild(noDataMessage);
  } else {
    attractions.forEach((attraction) => {
      const gridItem = document.createElement("div");
      gridItem.className = "grid-item";
      gridItem.innerHTML = `
      <div class="img">
          <img src="${attraction.image[0]}" alt="${attraction.description}" />
          <div class="location-name">
              <p>${attraction.name}</p>
          </div>
      </div>
      <div class="mrt-category">
          <p>${attraction.mrt}</p>
          <p>${attraction.category}</p>
      </div>
  `;
      gridItem.addEventListener("click", () => {
        window.location.href = `/attraction/${attraction.id}`;
      });
      attractionsContainer.appendChild(gridItem);
    });
  }
}
