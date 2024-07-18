import * as View from "./view/view.js";

document.addEventListener("DOMContentLoaded", async function () {
  const token = localStorage.getItem("userToken");
  const pathname = window.location.pathname;

  if (!token) {
    if (pathname !== "/" && !pathname.startsWith("/attraction/")) {
      window.location.href = "/";
    }
  } else {
    View.setElementDisplay(".member-setting", "flex");
    const memberBtn = document.querySelector(".member-setting");
    memberBtn.addEventListener("click", function () {
      window.location.href = "/member";
    });
  }
});
