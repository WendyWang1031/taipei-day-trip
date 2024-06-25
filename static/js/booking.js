import { checkUserState } from "./controller/auth.js";
import * as View from "./view/auth.js";

const reservBtn = document.querySelector(".reservation");

document.addEventListener("DOMContentLoaded", function () {
  reservBtn.addEventListener("click", async function () {
    console.log("click reservBtn!!");
    const isLoggedIn = await checkUserState();
    if (isLoggedIn) {
      window.location.href = "/booking";
    } else {
      View.setElementDisplay(".signin-mask", "flex");
    }
  });
});
