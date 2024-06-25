import { checkUserState } from "./controller/auth.js";
import * as View from "./view/auth.js";

const reservBtn = document.querySelector(".reservation");

const bookingURL = "/api/booking";

document.addEventListener("DOMContentLoaded", function () {
  reservBtn.addEventListener("click", checkUserTobooking);
  fetchGetBooking();
});

async function checkUserTobooking() {
  console.log("click reservBtn!!");
  const isLoggedIn = await checkUserState();
  if (isLoggedIn) {
    window.location.href = "/booking";
  } else {
    View.setElementDisplay(".signin-mask", "flex");
  }
}

async function fetchGetBooking() {
  const token = localStorage.getItem("userToken");
  try {
    const response = await fetch(bookingURL, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log(response);
    if (!response.ok) {
      console.error("Failed to fetch booking details:", response.status);
      return;
    }

    const data = await response.json();
    if (!data || !data.data) {
      console.error("No booking data available");
      return;
    }
    console.log(data.data);
    displayBooking(data.data);
  } catch (error) {
    console.error("Error fetching attraction:", error);
  }
}

function displayBooking(attraction) {
  const image = document.querySelector(".fade");
  const attractionName = document.querySelector(".attraction-name");
  const date = document.querySelector(".date-detail");
  const time = document.querySelector(".time-detail");
  const price = document.querySelector(".price-detail");
  const address = document.querySelector(".address-detail");
  const totalPrice = document.querySelector(".booking-price");

  image.src = attraction.attraction.image;
  attractionName.textContent = `台北一日遊：${attraction.attraction.name}`;
  date.textContent = attraction.date;
  time.textContent = attraction.time;
  price.textContent = attraction.price;
  address.textContent = attraction.attraction.address;
  totalPrice.textContent = `總價：新台幣${attraction.price}`;

  time.textContent =
    attraction.time === "上半天" ? "上午9點到下午4點" : "下午5點到晚上12點";
}
