const loginSigninBtn = document.querySelector(".login-signin");
const closeSigninBtn = document.querySelector(".close-sigin");
const gotoSignupBtn = document.querySelector(".go-to-signup");
const closeSignupBtn = document.querySelector(".close-sigup");
const gotoSigninBtn = document.querySelector(".go-to-signin");
const signinMask = document.querySelector(".signin-mask");
const signupMask = document.querySelector(".signup-mask");

const registerForm = document.querySelector(".signup");
const signInForm = document.querySelector(".signin");

signinMask.style.display = "none";
signupMask.style.display = "none";

const userRegisterUrl = "/api/user";
const userSignInUrl = "/api/user/auth";

document.addEventListener("DOMContentLoaded", initializePage);

// 各種功能性的函數呼叫
function initializePage() {
  loginSigninBtn.addEventListener("click", loginSignin);
  closeSigninBtn.addEventListener("click", closeSignin);
  gotoSignupBtn.addEventListener("click", gotoSignup);
  closeSignupBtn.addEventListener("click", closeSignup);
  gotoSigninBtn.addEventListener("click", gotoSignin);

  registerForm.addEventListener("submit", fetchUserRegister);
  signInForm.addEventListener("submit", fetchUserSignIn);
}

async function fetchUserRegister(event) {
  event.preventDefault();
  const formData = new FormData();
  formData.append("name", document.getElementById("signup-name").value.trim());
  formData.append(
    "email",
    document.getElementById("signup-email").value.trim()
  );
  formData.append(
    "password",
    document.getElementById("signup-password").value.trim()
  );

  try {
    const response = await fetch(userRegisterUrl, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    const hintSignupMessage = document.querySelector(".hint-signup-message");

    if (response.ok) {
      console.log("註冊成功");
      hintSignupMessage.textContent = "註冊成功";

      clearSignupValue();
    } else {
      hintSignupMessage.textContent = data.message;
      hintSignupMessage.style.display = "block";
    }
  } catch (error) {
    console.error("Error Registering user:", error);
  }
}
async function fetchUserSignIn(event) {
  event.preventDefault();
  const formData = new FormData();
  formData.append(
    "email",
    document.getElementById("signin-email").value.trim()
  );
  formData.append(
    "password",
    document.getElementById("signin-password").value.trim()
  );

  try {
    const response = await fetch(userSignInUrl, {
      method: "PUT",
      body: formData,
    });

    const data = await response.json();

    const hintSigninMessage = document.querySelector(".hint-signin-message");

    if (response.ok) {
      console.log("登入成功");
      hintSigninMessage.textContent = "登入成功";
    } else {
      hintSigninMessage.textContent = data.message;
      hintSigninMessage.style.display = "block";
    }
  } catch (error) {
    console.error("Error Registering user:", error);
  }
}

function loginSignin(event) {
  event.preventDefault();
  signinMask.style.display = "flex";
}

function closeSignin(event) {
  event.preventDefault();
  signinMask.style.display = "none";
  clearSignupValue();
  clearSigninValue();
}

function gotoSignup(event) {
  event.preventDefault();
  signinMask.style.display = "none";
  signupMask.style.display = "flex";
  clearSignupValue();
  clearSigninValue();
}

function closeSignup(event) {
  event.preventDefault();
  signupMask.style.display = "none";
  clearSignupValue();
  clearSigninValue();
}

function gotoSignin(event) {
  event.preventDefault();
  signupMask.style.display = "none";
  signinMask.style.display = "flex";
  clearSignupValue();
  clearSigninValue();
}

function clearSignupValue() {
  const hintSignupMessage = document.querySelector(".hint-signup-message");
  hintSignupMessage.style.display = "none";

  document.getElementById("signup-name").value = "";
  document.getElementById("signup-email").value = "";
  document.getElementById("signup-password").value = "";
}
function clearSigninValue() {
  const hintSigninMessage = document.querySelector(".hint-signin-message");
  hintSigninMessage.style.display = "none";

  document.getElementById("signin-email").value = "";
  document.getElementById("signin-password").value = "";
}
