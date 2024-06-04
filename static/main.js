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
  const scrollableContainer = document.getElementById("scrollable-container");
  if (scrollableContainer) {
    scrollableContainer.scrollLeft = -100000;
  }

  fetch("/api/mrts")
    .then((response) => response.json())
    .then((data) => {
      if (data && data.data) {
        data.data.forEach((mrt) => {
          console.log(data.data);
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

function fetchAttractions(keyword = "") {
  const url = `/api/attractions?page=0&keyword=${encodeURIComponent(keyword)}`;
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      displayAttractions(data.data);
    })
    .catch((error) => console.error("Error fetching attractions:", error));
}
fetchAttractions();

function displayAttractions(attractions) {
  const attractionsContainer = document.querySelector(".attractions-group");
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

loginSigninBtn.addEventListener("click", loginSignin);
function loginSignin(event) {
  event.preventDefault();
  signinMask.style.display = "flex";
}

closeSigninBtn.addEventListener("click", closeSignin);
function closeSignin(event) {
  event.preventDefault();
  signinMask.style.display = "none";
}

gotoSignupBtn.addEventListener("click", gotoSignup);
function gotoSignup(event) {
  event.preventDefault();
  signinMask.style.display = "none";
  signupMask.style.display = "flex";
}

closeSignupBtn.addEventListener("click", closeSignup);
function closeSignup(event) {
  event.preventDefault();
  signupMask.style.display = "none";
}

gotoSigninBtn.addEventListener("click", gotoSignin);
function gotoSignin(event) {
  event.preventDefault();
  signupMask.style.display = "none";
  signinMask.style.display = "flex";
}

leftContainerBtn.addEventListener("click", leftScroll);
function leftScroll(event) {
  event.preventDefault();

  const container = document.getElementById("scrollable-container");
  container.scrollLeft -= 300;
  console.log("Scrolled left to:", container.scrollLeft);
}

rightContainerBtn.addEventListener("click", rightScroll);
function rightScroll(event) {
  event.preventDefault();

  const container = document.getElementById("scrollable-container");
  container.scrollLeft += 300;
  console.log("Scrolled right to:", container.scrollLeft);
}
