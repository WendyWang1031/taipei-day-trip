import { checkUserState } from "../auth.js";
import * as View from "../view/view.js";

const reservBtn = document.querySelector(".reservation");
const trashBtn = document.querySelector(".trash");

const bookingURL = "/api/booking";
const userSignInUrl = "/api/user/auth";

document.addEventListener("DOMContentLoaded", function () {
  reservBtn.addEventListener("click", checkUserTobooking);
  trashBtn.addEventListener("click", fetchDeleteBooking);
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

async function fetchGetUserName() {
  const token = localStorage.getItem("userToken");
  try {
    const response = await fetch(userSignInUrl, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      console.error("Failed to fetch booking details:", response.status);
      return;
    }

    const data = await response.json();

    if (!data || !data.data) {
      console.error("No booking data available");
      return;
    }
    return data.data.name;
  } catch (error) {
    console.error("Error fetching attraction:", error);
  }
}

async function fetchGetBooking() {
  const token = localStorage.getItem("userToken");
  const userName = await fetchGetUserName();
  try {
    const response = await fetch(bookingURL, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      removeDisplayBooking();
      noBooking();
      displayName(userName);
      console.log("Failed to fetch booking details:", response.status);
      return;
    }

    const data = await response.json();
    if (!data || !data.data) {
      removeDisplayBooking();
      noBooking();
      displayName(userName);
      console.error("No booking data available");
      return;
    }
    console.log(data.data);
    displayBooking(data.data, userName);
    displayName(userName);
  } catch (error) {
    console.error("Error fetching attraction:", error);
  }
}
function displayName(userName) {
  const title = document.querySelector(".no-booking-title");
  title.textContent = `您好，${userName}，待預定的行程如下：`;
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

async function fetchDeleteBooking() {
  const token = localStorage.getItem("userToken");
  try {
    const response = await fetch(bookingURL, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log(response);
    if (!response.ok) {
      console.error("Failed to delete details:", response.status);
      return;
    }

    removeDisplayBooking();
    window.location.reload();
  } catch (error) {
    console.error("Error deleting attraction:", error);
  }
}

function removeDisplayBooking() {
  const bookingDetail = document.querySelector(".booking-location");
  const seperates = document.querySelectorAll(".seperate");
  const contactArea = document.querySelector(".contact-area");
  const cardArea = document.querySelector(".card-area");
  const totalSubmit = document.querySelector(".total-submit");

  bookingDetail.remove();
  contactArea.remove();
  cardArea.remove();
  totalSubmit.remove();
  seperates.forEach((seperate) => {
    if (seperate) seperate.remove();
  });
}

function noBooking() {
  const result = document.querySelector(".result");
  result.style.display = "flex";
}
