import { checkUserState } from "./controller/auth.js";
import * as View from "./view/view.js";
import {
  AttractionsBooking,
  getAttractionIdFromPath,
} from "./view/attraction.js";
import { fetchPostBooking } from "./controller/booking.js";

// 登入
const loginSigninBtn = document.querySelector(".login-signin");
const closeSigninBtn = document.querySelector(".close-signin");
const gotoSignupBtn = document.querySelector(".go-to-signup");
const closeSignupBtn = document.querySelector(".close-signup");
const gotoSigninBtn = document.querySelector(".go-to-signin");
const signinMask = document.querySelector(".signin-mask");
const signupMask = document.querySelector(".signup-mask");

// 圖片往左往右轉換
const imagesLeftBtn = document.querySelector(".left-btn");
const imagesRightBtn = document.querySelector(".right-btn");

// 預約行程
const feeElement = document.querySelector(".fee");
const moringOption = document.getElementById("inlineRadio1");
const AfternoonOption = document.getElementById("inlineRadio2");
const bookingBtn = document.querySelector(".go-booking");

// 其餘
const attractionIdURL = "/api/attraction";
const bookingURL = "/api/booking";

let currentImageIndex = 0;
let nextImageIndex;

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
  bookingBtn.addEventListener("click", checkBooking);
}

async function checkBooking(event) {
  event.preventDefault();
  console.log("click!!");
  const isLoggedIn = await checkUserState();
  if (isLoggedIn) {
    const bookingData = await AttractionsBooking(event);
    console.log(bookingData);
    await fetchPostBooking(bookingData);
  } else {
    View.setElementDisplay(".signin-mask", "flex");
  }
}

async function fetchGetAttractionID(attractionId) {
  try {
    const response = await fetch(`${attractionIdURL}/${attractionId}`);
    if (!response.ok) {
      window.location.href = "/";
    }

    const data = await response.json();
    if (!data || !data.data || attractionId != data.data.id) {
      window.location.href = "/";
    }
    console.log(data.data);
    displayAttraction(data.data);
  } catch (error) {
    console.error("Error fetching attraction:", error);
  }
}

function displayAttraction(attraction) {
  const attractionName = document.querySelector(".attraction-name");
  const category = document.querySelector(".category");
  const mrt = document.querySelector(".attraction-mrt");
  const description = document.querySelector(".content");
  const address = document.querySelector(".address-detail");
  const transportation = document.querySelector(".transportation-detail");

  attractionName.textContent = attraction.name;
  category.textContent = attraction.category;
  mrt.textContent = attraction.mrt;
  description.textContent = attraction.description;
  address.textContent = attraction.address;
  transportation.textContent = attraction.transport;

  displayImageUI(attraction.images);
  displayCircleUI();
}

function displayImageUI(images) {
  const imgArea = document.querySelector(".location-image-area");

  const preloadedImages = images.map((imgUrl) => {
    const img = new Image();
    img.src = imgUrl;
    return img;
  });

  preloadedImages.forEach((img, index) => {
    img.alt = "景點圖片";
    img.className = "fade";

    img.style.display = index === 0 ? "block" : "none";

    imgArea.appendChild(img);
  });
}

const updateCirclesUI = (imageIndex) => {
  const circleContainer = document.querySelector(".circle-container");
  const circles = circleContainer.querySelectorAll("img");
  circles.forEach((circle, index) => {
    circle.src =
      index === imageIndex
        ? "/static/images/icon/circle-this.png"
        : "/static/images/icon/circle current.png";
  });
};

function displayCircleUI() {
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

function imagesTurnRight(event) {
  event.preventDefault();
  const images = document.querySelectorAll(".location-image-area img");

  images[currentImageIndex].style.display = "none";
  nextImageIndex = (currentImageIndex + 1 + images.length) % images.length;
  images[nextImageIndex].style.display = "block";

  currentImageIndex = nextImageIndex;
  updateCirclesUI(currentImageIndex);
}

function imagesTurnLeft(event) {
  event.preventDefault();
  const images = document.querySelectorAll(".location-image-area img");

  images[currentImageIndex].style.display = "none";
  nextImageIndex = (currentImageIndex - 1 + images.length) % images.length;
  images[nextImageIndex].style.display = "block";

  currentImageIndex = nextImageIndex;
  updateCirclesUI(currentImageIndex);
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
