import * as View from "../view/view.js";
import * as BookingView from "../view/booking.js";
import { checkUserState } from "./auth.js";

const bookingURL = "/api/booking";

document.addEventListener("DOMContentLoaded", async function () {
  const trashBtn = document.querySelector(".trash");
  trashBtn.addEventListener("click", fetchDeleteBooking);

  if (window.location.pathname === "/booking") {
    const isLoggedIn = await checkUserState();
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
      return;
    }

    const data = await response.json();
    if (!data || !data.data) {
      BookingView.removeDisplayBooking();
      View.setElementDisplay(".result", "flex");
      BookingView.displayUserName(userName);
      console.error("No booking data available");
      return;
    }
    console.log(data.data);
    BookingView.updateBookingDetails(data.data, userName);
    BookingView.displayUserName(userName);
  } catch (error) {
    console.error("Error fetching attraction:", error);
  }
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

    BookingView.removeDisplayBooking();
    window.location.reload();
  } catch (error) {
    console.error("Error deleting attraction:", error);
  }
}
