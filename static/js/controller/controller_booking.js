import * as View from "../view/view.js";
import * as BookingView from "../view/view_booking.js";
import { checkUserState, initialize } from "./controller_auth.js";
import { tappayGetPrime } from "./taypay_fields.js";

const bookingURL = "/api/booking";

document.addEventListener("DOMContentLoaded", async function () {
  View.signUpSignInDisplayNone();
  tappayGetPrime();

  const trashBtn = document.querySelector(".trash");
  if (trashBtn) {
    trashBtn.addEventListener("click", fetchDeleteBooking);
  } else {
    console.log("Trash button not found");
  }

  document
    .querySelector("#contact-phone")
    .addEventListener("input", BookingView.mobileTextValidate);

  if (window.location.pathname === "/booking") {
    initialize();
    const isLoggedIn = await checkUserState(BookingView.handleUserDataDisplay);

    if (isLoggedIn) {
      await fetchGetBooking();
    } else {
      window.location.href = "/";
      View.setElementDisplay(".signin-mask", "flex");
    }
  }
});

export async function fetchGetBooking() {
  const token = localStorage.getItem("userToken");
  const userName = localStorage.getItem("userName");
  try {
    const response = await fetch(bookingURL, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      BookingView.removeDisplayBooking();
      View.setElementDisplay(".result", "flex");
      BookingView.displayUserName(userName);
      console.log("Failed to fetch booking details:", response.status);
      return null;
    }

    const data = await response.json();
    if (!data || !data.data) {
      BookingView.removeDisplayBooking();
      View.setElementDisplay(".result", "flex");
      BookingView.displayUserName(userName);
      console.error("No booking data available");
      return null;
    }
    console.log(data.data);
    BookingView.updateBookingDetails(data.data);
    BookingView.displayUserName(userName);
    return data.data;
  } catch (error) {
    console.error("Error fetching attraction:", error);
  }
}

export async function fetchDeleteBooking() {
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

    BookingView.removeDisplayBooking();
    window.location.reload();
  } catch (error) {
    console.error("Error deleting attraction:", error);
  }
}

// export async function fetchPostBooking(bookingData) {
//   try {
//     const token = localStorage.getItem("userToken");
//     const response = await fetch(bookingURL, {
//       method: "POST",
//       headers: {
//         Authorization: `Bearer ${token}`,
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(bookingData),
//     });

//     if (!response.ok) {
//       window.location = "/";
//     }

//     const data = await response.json();
//     if (!data || !data.data || bookingData.attractionId != data.data.id) {
//       window.location = "/";
//     }
//     window.location.href = "/booking";
//   } catch (error) {
//     console.error("Error fetching post booking:", error);
//   }
// }
