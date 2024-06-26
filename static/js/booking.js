import { checkUserState } from "./controller/auth.js";
import * as View from "./view/view.js";
import { fetchGetBooking } from "./controller/booking.js";

const reservBtn = document.querySelector(".reservation");

document.addEventListener("DOMContentLoaded", function () {
  reservBtn.addEventListener("click", checkUserTobooking);
});

async function checkUserTobooking() {
  console.log("click reservBtn!!");
  const isLoggedIn = await checkUserState();
  if (isLoggedIn) {
    window.location.href = "/booking";
    fetchGetBooking();
  } else {
    View.setElementDisplay(".signin-mask", "flex");
  }
}
