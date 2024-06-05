const loginSigninBtn = document.querySelector(".login-signin");
const closeSigninBtn = document.querySelector(".close-sigin");
const gotoSignupBtn = document.querySelector(".go-to-signup");
const closeSignupBtn = document.querySelector(".close-sigup");
const gotoSigninBtn = document.querySelector(".go-to-signin");
const signinMask = document.querySelector(".signin-mask");
const signupMask = document.querySelector(".signup-mask");

const leftContainerBtn = document.querySelector(".left-container");
const rightContainerBtn = document.querySelector(".right-container");

const searchInput = document.querySelector(".searchKeyword");
const searchButton = document.querySelector(".input-area button");
let currentPage = 0;
let hasNextPage = true;

signinMask.style.display = "none";
signupMask.style.display = "none";
document.addEventListener("DOMContentLoaded", () => {
  loginSigninBtn.addEventListener("click", loginSignin);
  closeSigninBtn.addEventListener("click", closeSignin);
  gotoSignupBtn.addEventListener("click", gotoSignup);
  closeSignupBtn.addEventListener("click", closeSignup);
  gotoSigninBtn.addEventListener("click", gotoSignin);

  const scrollableContainer = document.getElementById("scrollable-container");
  if (scrollableContainer) {
    scrollableContainer.scrollLeft = 0;
  }

  leftContainerBtn.addEventListener("click", leftScroll);
  rightContainerBtn.addEventListener("click", rightScroll);
  searchButton.addEventListener("click", search);

  fetch("/api/mrts")
    .then((response) => response.json())
    .then((data) => {
      if (data && data.data) {
        data.data.forEach((mrt) => {
          const mrtBtn = document.createElement("button");
          mrtBtn.className = "list-item";
          mrtBtn.textContent = mrt;
          scrollableContainer.appendChild(mrtBtn);
          mrtBtn.addEventListener("click", mrtToSearch);
          function mrtToSearch(event) {
            event.preventDefault();
            searchInput.value = mrt;
            searchButton.click();
          }
        });
      }
    })
    .catch((error) => console.error("Error fetching MRT stations:", error));
});

function fetchAttractions(keyword = "", page = 0, isKeywordSearch = false) {
  const url = `/api/attractions?page=${page}&keyword=${encodeURIComponent(
    keyword
  )}`;
  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Server responded with status ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (!data || !Array.isArray(data.data)) {
        throw new Error("Invalid data structure");
      }
      displayAttractions(data.data, keyword, isKeywordSearch);

      currentPage = page;
      hasNextPage = data.nextPage != null;
    })
    .catch((error) => console.error("Error fetching attractions:", error));
}
fetchAttractions();

const observer = new IntersectionObserver(
  (entries) => {
    const firstEntry = entries[0];
    if (firstEntry.isIntersecting && hasNextPage) {
      fetchAttractions("", currentPage + 1);
    }
  },
  { threshold: 0.5 }
);

const lastItem = document.querySelector(".grid-item:last-child");
observer.observe(lastItem);

function updateObserver() {
  const lastItem = document.querySelector(".grid-item:last-child");
  observer.unobserve(lastItem);
  if (hasNextPage) {
    observer.observe(lastItem);
  }
}

function displayAttractions(attractions, keyword, isKeywordSearch = false) {
  const attractionsContainer = document.querySelector(".attractions-group");
  if (isKeywordSearch) {
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
      attractionsContainer.appendChild(gridItem);
    });
  }
  if (!isKeywordSearch) {
    updateObserver();
  }
}

function loginSignin(event) {
  event.preventDefault();
  signinMask.style.display = "flex";
}

function closeSignin(event) {
  event.preventDefault();
  signinMask.style.display = "none";
}

function gotoSignup(event) {
  event.preventDefault();
  signinMask.style.display = "none";
  signupMask.style.display = "flex";
}

function closeSignup(event) {
  event.preventDefault();
  signupMask.style.display = "none";
}

function gotoSignin(event) {
  event.preventDefault();
  signupMask.style.display = "none";
  signinMask.style.display = "flex";
}

function leftScroll(event) {
  event.preventDefault();

  const scrollableContainer = document.getElementById("scrollable-container");
  scrollableContainer.scrollLeft -= 300;
  console.log("Scrolled left to:", scrollableContainer.scrollLeft);
}

function rightScroll(event) {
  event.preventDefault();

  const scrollableContainer = document.getElementById("scrollable-container");
  scrollableContainer.scrollLeft += 300;
  console.log("Scrolled right to:", scrollableContainer.scrollLeft);
}

function search(event) {
  event.preventDefault();
  const keyword = searchInput.value;
  fetchAttractions(keyword, currentPage, true);
  console.log(keyword);
}
