import * as IndexView from "./view/view_index.js";

const leftContainerBtn = document.querySelector(".left-container");
const rightContainerBtn = document.querySelector(".right-container");
const scrollableContainer = document.getElementById("scrollable-container");

const searchInput = document.querySelector(".searchKeyword");
const searchButton = document.querySelector(".input-area button");

const mrtURL = "/api/mrts";
const attractionURL = "/api/attractions";

let currentPage = 0;
let hasNextPage = true;
let isWaitingForData = false;

document.addEventListener("DOMContentLoaded", initializePage);

// 頁面載入初始化
function initializePage() {
  setupEventListeners();
  fetchGetMRTStations();
  fetchGetAttractions();
}

// 各種功能性的函數呼叫
function setupEventListeners() {
  leftContainerBtn.addEventListener("click", IndexView.leftScroll);
  rightContainerBtn.addEventListener("click", IndexView.rightScroll);
  searchButton.addEventListener("click", searchEvent);
  searchInput.addEventListener("keypress", enterPress);

  scrollableContainer.addEventListener("mousedown", IndexView.mousedown);
  scrollableContainer.addEventListener("mouseleave", IndexView.mouseleave);
  scrollableContainer.addEventListener("mouseup", IndexView.mouseup);
  scrollableContainer.addEventListener("mousemove", IndexView.mousemove);
}

function enterPress(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    searchEvent(event);
  }
}

function searchEvent(event) {
  event.preventDefault();

  if (isWaitingForData) return;

  refresh();

  const searchInput = document.querySelector(".searchKeyword");
  const keywordInputValue = searchInput.value;

  fetchGetAttractions(keywordInputValue, currentPage, true).then(() => {});
  console.log(keywordInputValue);
}

function refresh() {
  currentPage = 0;
  IndexView.refreshContent();
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

//fetch GET API頁面的景點
async function fetchGetAttractions(keyword = "") {
  try {
    //開始新的資料加載前設定
    isWaitingForData = true;

    const response = await fetch(
      `${attractionURL}?keyword=${keyword}&page=${currentPage}`
    );
    if (!response.ok) {
      throw new Error(`Server responded with status ${response.status}`);
    }

    const data = await response.json();
    if (!data || !Array.isArray(data.data)) {
      throw new Error("Invalid data structure");
    }

    currentPage++;
    hasNextPage = data.nextPage != null;
    console.log("currentPage :", currentPage);

    let lastItem = document.querySelector(".grid-item:last-child");

    IndexView.displayAttractions(data.data, keyword);

    let newItem = document.querySelector(".grid-item:last-child");

    if (lastItem) observer.unobserve(lastItem);
    if (hasNextPage) {
      if (newItem) observer.observe(newItem);
    }

    isWaitingForData = false;
  } catch (error) {
    console.error("Error fetching attractions:", error);
    isWaitingForData = false;
  }
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
