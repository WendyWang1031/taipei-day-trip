import * as View from "./view/view.js";

document.addEventListener("DOMContentLoaded", async function () {
  const token = localStorage.getItem("userToken");
  if (!token) {
    window.location.href = "/";
    View.setElementDisplay(".signin-mask", "flex");
  } else {
    View.setElementDisplay(".member-setting", "flex");
    const memberBtn = document.querySelector(".member-setting");
    memberBtn.addEventListener("click", function () {
      window.location.href = "/member";
    });
  }
});
