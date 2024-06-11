const loginSigninBtn = document.querySelector(".login-signin");
const closeSigninBtn = document.querySelector(".close-sigin");
const gotoSignupBtn = document.querySelector(".go-to-signup");
const closeSignupBtn = document.querySelector(".close-sigup");
const gotoSigninBtn = document.querySelector(".go-to-signin");
const signinMask = document.querySelector(".signin-mask");
const signupMask = document.querySelector(".signup-mask");

const images = document.querySelectorAll(".location-image-area img");
const imagesLeftBtn = document.querySelector(".left-btn");
const imagesRightBtn = document.querySelector(".right-btn");

const circleContainer = document.querySelector(".circle-container");

let currentImageIndex = 0;

signinMask.style.display = "none";
signupMask.style.display = "none";

document.addEventListener("DOMContentLoaded", initializePage);

// 頁面載入初始化
function initializePage() {
  setupEventListeners();
  //   fetchGetMRTStations();
  //   fetchGetAttractions();
  displayCircleContainer();
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
}

function displayCircleContainer() {
  images.forEach((_, index) => {
    const circle = document.createElement("img");
    circle.src =
      index === 0
        ? "./images/icon/circle-this.png"
        : "./images/icon/circle current.png";
    circleContainer.appendChild(circle);
  });
}
const updateCircles = () => {
  const circles = circleContainer.querySelectorAll("img");
  circles.forEach((circle, index) => {
    circle.src =
      index === currentImageIndex
        ? "./images/icon/circle-this.png"
        : "./images/icon/circle current.png";
  });
};

function imagesTurnLeft(event) {
  event.preventDefault();
  images[currentImageIndex].style.display = "none";
  currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
  images[currentImageIndex].style.display = "block";
  updateCircles();
}

function imagesTurnRight(event) {
  event.preventDefault();
  images[currentImageIndex].style.display = "none";
  currentImageIndex = (currentImageIndex + 1 + images.length) % images.length;
  images[currentImageIndex].style.display = "block";
  updateCircles();
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
