const leftContainerBtn = document.querySelector(".left-container");
const rightContainerBtn = document.querySelector(".right-container");
const scrollableContainer = document.getElementById("scrollable-container");

const signinMask = document.querySelector(".signin-mask");
const signupMask = document.querySelector(".signup-mask");

const searchInput = document.querySelector(".searchKeyword");
const searchButton = document.querySelector(".input-area button");

const mrtURL = "/api/mrts";
const attractionURL = "/api/attractions";

let currentPage = 0;
let hasNextPage = true;
let isWaitingForData = false;

let isDown = false;
let startX;
let scrollLeft;

signinMask.style.display = "none";
signupMask.style.display = "none";

document.addEventListener("DOMContentLoaded", initializePage);

// 頁面載入初始化
function initializePage() {
  setupEventListeners();
  fetchGetMRTStations();
  fetchGetAttractions();
}

// 各種功能性的函數呼叫
function setupEventListeners() {
  leftContainerBtn.addEventListener("click", leftScroll);
  rightContainerBtn.addEventListener("click", rightScroll);
  searchButton.addEventListener("click", search);
  searchInput.addEventListener("keypress", enterPress);

  scrollableContainer.addEventListener("mousedown", mousedown);
  scrollableContainer.addEventListener("mouseleave", mouseleave);
  scrollableContainer.addEventListener("mouseup", mouseup);
  scrollableContainer.addEventListener("mousemove", mousemove);
}

// 頁面初始化的載入API的MRT
async function fetchGetMRTStations() {
  try {
    const response = await fetch(mrtURL);
    const data = await response.json();
    if (data && data.data) {
      if (scrollableContainer) {
        scrollableContainer.scrollLeft = 0;
      }
      data.data.forEach((mrt) => {
        const mrtBtn = document.createElement("button");
        mrtBtn.className = "list-item";
        mrtBtn.textContent = mrt;

        mrtBtn.addEventListener("click", (event) => {
          event.preventDefault();
          searchInput.value = mrt;
          searchButton.click();
        });
        scrollableContainer.appendChild(mrtBtn);
      });
    }
  } catch (error) {
    console.error("Error fetching MRT stations:", error);
  }
}

//fetch GET API頁面的景點
async function fetchGetAttractions(keyword = "", page = 0, refresh = false) {
  try {
    //開始新的資料加載前設定
    isWaitingForData = true;
    const response = await fetch(
      `${attractionURL}?keyword=${keyword}&page=${page}`
    );
    if (!response.ok) {
      throw new Error(`Server responded with status ${response.status}`);
    }

    const data = await response.json();
    if (!data || !Array.isArray(data.data)) {
      throw new Error("Invalid data structure");
    }
    displayAttractions(data.data, keyword, refresh);
    currentPage = page;
    hasNextPage = data.nextPage != null;
    isWaitingForData = false;
  } catch (error) {
    console.error("Error fetching attractions:", error);
    isWaitingForData = false;
  }
}

function displayAttractions(attractions, keyword, refresh = false) {
  lastItem = document.querySelector(".grid-item:last-child");

  const attractionsContainer = document.querySelector(".attractions-group");
  if (refresh) {
    currentPage == 0;
    attractionsContainer.innerHTML = "";
  }
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

  newItem = document.querySelector(".grid-item:last-child");

  if (lastItem) observer.unobserve(lastItem);
  if (hasNextPage) {
    if (newItem) observer.observe(newItem);
  }
}

const observer = new IntersectionObserver(
  (entries) => {
    const firstEntry = entries[0];

    if (firstEntry.isIntersecting && hasNextPage && !isWaitingForData) {
      const keywordInputValue = searchInput.value;
      //調用fetch函式的時候使用非同步加載
      fetchGetAttractions(keywordInputValue, currentPage + 1).then(() => {});
    }
  },
  { threshold: 0.5 }
);

function search(event) {
  event.preventDefault();
  if (isWaitingForData) return;

  isWaitingForData = true;
  currentPage = 0;

  const keywordInputValue = searchInput.value;

  fetchGetAttractions(keywordInputValue, currentPage, true).then(() => {});
  console.log(keywordInputValue);
}

function enterPress(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    search(event);
  }
}

function leftScroll(event) {
  event.preventDefault();
  const scrollDistance = getSrollDistance();
  scrollableContainer.scrollLeft -= scrollDistance;
  console.log("Scrolled left to:", scrollableContainer.scrollLeft);
}

function rightScroll(event) {
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

function mousedown(event) {
  isDown = true;
  startX = event.pageX - scrollableContainer.offsetLeft;
  scrollLeft = scrollableContainer.scrollLeft;
  scrollableContainer.style.cursor = "grabbing";
}

function mouseleave() {
  isDown = false;
  scrollableContainer.style.cursor = "grab";
}

function mouseup() {
  isDown = false;
  scrollableContainer.style.cursor = "grab";
}

function mousemove(event) {
  if (!isDown) return;
  event.preventDefault;
  const x = event.pageX - scrollableContainer.offsetLeft;
  const speed = (x - startX) * 1.5;
  scrollableContainer.scrollLeft = scrollLeft - speed;
}
