import { checkUserState } from "./controller/controller_auth.js";
import * as View from "./view/view.js";
import * as ViewAttraction from "./view/view_attraction.js";
import { fetchPostBooking } from "./model/model_booking.js";

// 圖片往左往右轉換
const imagesLeftBtn = document.querySelector(".left-btn");
const imagesRightBtn = document.querySelector(".right-btn");

// 預約行程
const moringOption = document.getElementById("inlineRadio1");
const AfternoonOption = document.getElementById("inlineRadio2");
const bookingBtn = document.querySelector(".go-booking");

// 其餘
const attractionIdURL = "/api/attraction";
document.addEventListener("DOMContentLoaded", initializePage);

// 頁面載入初始化
function initializePage() {
  setupEventListeners();
  const attractionId = ViewAttraction.getAttractionIdFromPath();
  fetchGetAttractionID(attractionId);
}

// 各種功能性的函數呼叫
function setupEventListeners() {
  imagesLeftBtn.addEventListener("click", ViewAttraction.imagesTurnLeft);
  imagesRightBtn.addEventListener("click", ViewAttraction.imagesTurnRight);

  moringOption.addEventListener("change", () =>
    ViewAttraction.updateFeeOption("morning")
  );
  AfternoonOption.addEventListener("change", () =>
    ViewAttraction.updateFeeOption("afternoon")
  );

  bookingBtn.addEventListener("click", checkBooking);
  document.getElementById("start").min = new Date().toISOString().split("T")[0];
}

async function checkBooking(event) {
  event.preventDefault();
  console.log("click!!");
  const isLoggedIn = await checkUserState();
  if (isLoggedIn) {
    const bookingData = await ViewAttraction.AttractionsBooking();
    console.log(bookingData);
    await fetchPostBooking(bookingData);
  } else {
    View.setElementDisplay(".signin-mask", "flex");
  }
}

async function fetchGetAttractionID(attractionId) {
  try {
    console.log("begin:");
    const response = await fetch(`${attractionIdURL}/${attractionId}`);
    console.log("before response:");
    if (!response.ok) {
      console.log("response:");
      window.location.href = "/";
    }
    console.log("before data:");
    const data = await response.json();
    console.log("after data:");
    if (!data || !data.data || attractionId != data.data.id) {
      console.log("in data:");
      window.location.href = "/";
    }
    console.log(data.data);
    ViewAttraction.displayAttraction(data.data);
  } catch (error) {
    console.error("Error fetching attraction:", error);
  }
}
