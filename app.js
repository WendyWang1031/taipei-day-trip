const loginSigninBtn = document.querySelector(".login-signin");
const closeSigninBtn = document.querySelector(".close-sigin");
const gotoSignupBtn = document.querySelector(".go-to-signup");
const closeSignupBtn = document.querySelector(".close-sigup");
const gotoSigninBtn = document.querySelector(".go-to-signin");
const signinMask = document.querySelector(".signin-mask");
const signupMask = document.querySelector(".signup-mask");

const leftContainerBtn = document.querySelector(".left-container");
const rightContainerBtn = document.querySelector(".right-container");

signinMask.style.display = "none";
signupMask.style.display = "none";
document.addEventListener("DOMContentLoaded", () => {
  const scrollableContainer = document.getElementById("scrollable-container");
  if (scrollableContainer) {
    scrollableContainer.scrollLeft = 0;
  }
});

loginSigninBtn.addEventListener("click", loginSignin);
function loginSignin(event) {
  event.preventDefault();
  signinMask.style.display = "flex";
}

closeSigninBtn.addEventListener("click", closeSignin);
function closeSignin(event) {
  event.preventDefault();
  signinMask.style.display = "none";
}

gotoSignupBtn.addEventListener("click", gotoSignup);
function gotoSignup(event) {
  event.preventDefault();
  signinMask.style.display = "none";
  signupMask.style.display = "flex";
}

closeSignupBtn.addEventListener("click", closeSignup);
function closeSignup(event) {
  event.preventDefault();
  signupMask.style.display = "none";
}

gotoSigninBtn.addEventListener("click", gotoSignin);
function gotoSignin(event) {
  event.preventDefault();
  signupMask.style.display = "none";
  signinMask.style.display = "flex";
}

leftContainerBtn.addEventListener("click", leftScroll);
function leftScroll(event) {
  event.preventDefault();

  const container = document.getElementById("scrollable-container");
  container.scrollLeft -= 300;
  console.log("Scrolled left to:", container.scrollLeft);
}

rightContainerBtn.addEventListener("click", rightScroll);
function rightScroll(event) {
  event.preventDefault();

  const container = document.getElementById("scrollable-container");
  container.scrollLeft += 300;
  console.log("Scrolled right to:", container.scrollLeft);
}
