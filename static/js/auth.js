import { initialize, checkUserState } from "./controller/controller_auth.js";

const signinMask = document.querySelector(".signin-mask");
const signupMask = document.querySelector(".signup-mask");

signinMask.style.display = "none";
signupMask.style.display = "none";

document.addEventListener("DOMContentLoaded", function () {
  initialize();
  checkUserState();
});
