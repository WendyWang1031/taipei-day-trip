const loginSigninBtn = document.querySelector(".login-signin");
const closeSigninBtn = document.querySelector(".close-sigin");
const gotoSignupBtn = document.querySelector(".go-to-signup");
const closeSignupBtn = document.querySelector(".close-sigup");
const gotoSigninBtn = document.querySelector(".go-to-signin");
const signinMask = document.querySelector(".signin-mask");
const signupMask = document.querySelector(".signup-mask");

const imagesLeftBtn = document.querySelector(".left-btn");
const imagesRightBtn = document.querySelector(".right-btn");

const feeElement = document.querySelector(".fee");
const moringOption = document.getElementById("inlineRadio1");
const AfternoonOption = document.getElementById("inlineRadio2");

const attractionIdURL = "/api/attraction";

let currentImageIndex = 0;

signinMask.style.display = "none";
signupMask.style.display = "none";

document.addEventListener("DOMContentLoaded", initializePage);

// 頁面載入初始化
function initializePage() {
  setupEventListeners();

  const attractionId = getAttractionIdFromPath();
  fetchGetAttractionID(attractionId);
}

// 各種功能性的函數呼叫
function setupEventListeners() {
  loginSigninBtn.addEventListener("click", loginSignin);
  closeSigninBtn.addEventListener("click", closeSignin);
  gotoSignupBtn.addEventListener("click", gotoSignup);
  closeSignupBtn.addEventListener("click", closeSignup);
  gotoSigninBtn.addEventListener("click", gotoSignin);

  imagesLeftBtn.addEventListener("click", imagesTurnLeft);
  imagesRightBtn.addEventListener("click", imagesTurnRight);

  moringOption.addEventListener("change", moringFeeOption);
  AfternoonOption.addEventListener("change", AfternoonFeeOption);
}

function getAttractionIdFromPath() {
  const path = window.location.pathname;
  console.log(path);
  const pathSegments = path.split("/");
  console.log(pathSegments);
  return pathSegments[pathSegments.length - 1];
}

async function fetchGetAttractionID(attractionId) {
  try {
    const response = await fetch(`${attractionIdURL}/${attractionId}`);
    if (!response.ok) {
      window.location = "/";
    }

    const data = await response.json();
    if (!data || !data.data || attractionId != data.data.id) {
      window.location = "/";
    }
    console.log(data.data);
    displayAttractionID(data.data);
  } catch (error) {
    console.error("Error fetching attraction:", error);
  }
}

function displayAttractionID(attraction) {
  const attractionName = document.querySelector(".attraction-name");
  const category = document.querySelector(".category");
  const mrt = document.querySelector(".attraction-mrt");
  const description = document.querySelector(".content");
  const address = document.querySelector(".address-detail");
  const transportation = document.querySelector(".transportation-detail");
  const imgArea = document.querySelector(".location-image-area");

  attractionName.textContent = attraction.name;
  category.textContent = attraction.category;
  mrt.textContent = attraction.mrt;
  description.textContent = attraction.description;
  address.textContent = attraction.address;
  transportation.textContent = attraction.transport;

  attraction.images.forEach((imgUrl, index) => {
    const img = document.createElement("img");
    img.src = imgUrl;
    img.alt = "景點圖片";
    img.className = "fade";

    if (index === 0) {
      img.style.display = "block";
    } else {
      img.style.display = "none";
    }
    imgArea.appendChild(img);
  });
  displayCircleContainer();
}

function displayCircleContainer() {
  const circleContainer = document.querySelector(".circle-container");
  const images = document.querySelectorAll(".location-image-area img");
  images.forEach((_, index) => {
    const circle = document.createElement("img");
    circle.src =
      index === 0
        ? "/static/images/icon/circle-this.png"
        : "/static/images/icon/circle current.png";
    circleContainer.appendChild(circle);
  });
}
const updateCircles = () => {
  const circleContainer = document.querySelector(".circle-container");
  const circles = circleContainer.querySelectorAll("img");
  circles.forEach((circle, index) => {
    circle.src =
      index === currentImageIndex
        ? "/static/images/icon/circle-this.png"
        : "/static/images/icon/circle current.png";
  });
};

function imagesTurnLeft(event) {
  event.preventDefault();
  const images = document.querySelectorAll(".location-image-area img");

  images[currentImageIndex].style.display = "none";
  currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
  images[currentImageIndex].style.display = "block";
  updateCircles();
}

function imagesTurnRight(event) {
  event.preventDefault();
  const images = document.querySelectorAll(".location-image-area img");
  images[currentImageIndex].style.display = "none";
  currentImageIndex = (currentImageIndex + 1 + images.length) % images.length;
  images[currentImageIndex].style.display = "block";
  updateCircles();
}

function moringFeeOption(event) {
  event.preventDefault();
  if (this.checked) {
    feeElement.textContent = "新台幣 2000 元";
  }
}

function AfternoonFeeOption(event) {
  event.preventDefault();
  if (this.checked) {
    feeElement.textContent = "新台幣 2500 元";
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
