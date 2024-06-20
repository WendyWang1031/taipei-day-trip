import { initialize, checkUserState } from "./controller/auth.js";

const signinMask = document.querySelector(".signin-mask");
const signupMask = document.querySelector(".signup-mask");

signinMask.style.display = "none";
signupMask.style.display = "none";

document.addEventListener("DOMContentLoaded", function () {
  initialize();
  checkUserState();
});

//-----------------------old Backup Version----------------------------
// const loginSigninBtn = document.querySelector(".login-signin");
// const closeSigninBtn = document.querySelector(".close-sigin");
// const gotoSignupBtn = document.querySelector(".go-to-signup");
// const closeSignupBtn = document.querySelector(".close-sigup");
// const gotoSigninBtn = document.querySelector(".go-to-signin");
// const signinMask = document.querySelector(".signin-mask");
// const signupMask = document.querySelector(".signup-mask");

// const registerForm = document.querySelector(".signup");
// const signInForm = document.querySelector(".signin");

// const loginAndSignin = document.querySelector(".login-signin");
// const logout = document.querySelector(".logout");

// signinMask.style.display = "none";
// signupMask.style.display = "none";

// const userRegisterUrl = "/api/user";
// const userSignInUrl = "/api/user/auth";

// document.addEventListener("DOMContentLoaded", function () {
//   initialize();
//   checkUserState();
// });

// 各種功能性的函數呼叫
// function initializePage() {
//   loginSigninBtn.addEventListener("click", loginSignin);
//   closeSigninBtn.addEventListener("click", closeSignin);
//   gotoSignupBtn.addEventListener("click", gotoSignup);
//   closeSignupBtn.addEventListener("click", closeSignup);
//   gotoSigninBtn.addEventListener("click", gotoSignin);

//   registerForm.addEventListener("submit", fetchUserRegister);
//   signInForm.addEventListener("submit", fetchUserSignIn);

//   logout.addEventListener("click", logOut);

//   fetchCheckUserState();
// }

// async function fetchUserRegister(event) {
//   event.preventDefault();
//   const formData = new FormData();
//   formData.append("name", document.getElementById("signup-name").value.trim());
//   formData.append(
//     "email",
//     document.getElementById("signup-email").value.trim()
//   );
//   formData.append(
//     "password",
//     document.getElementById("signup-password").value.trim()
//   );

//   try {
//     const response = await fetch(userRegisterUrl, {
//       method: "POST",
//       body: formData,
//     });

//     const data = await response.json();

//     const hintSignupMessage = document.querySelector(".hint-signup-message");

//     if (response.ok) {
//       console.log("註冊成功");
//       hintSignupMessage.style.display = "block";
//       hintSignupMessage.textContent = "註冊成功，請登入會員";
//       hintSignupMessage.style.color = "#367688";

//       clearSignupValue();
//     } else {
//       hintSignupMessage.textContent = data.message;
//       hintSignupMessage.style.display = "block";
//       hintSignupMessage.style.color = "red";
//     }
//   } catch (error) {
//     console.error("Error Registering user:", error);
//   }
// }
// async function fetchUserSignIn(event) {
//   event.preventDefault();
//   const formData = new FormData();
//   formData.append(
//     "email",
//     document.getElementById("signin-email").value.trim()
//   );
//   formData.append(
//     "password",
//     document.getElementById("signin-password").value.trim()
//   );

//   try {
//     const response = await fetch(userSignInUrl, {
//       method: "PUT",
//       body: formData,
//     });

//     const data = await response.json();

//     const hintSigninMessage = document.querySelector(".hint-signin-message");

//     if (response.ok) {
//       console.log("登入成功");
//       hintSigninMessage.textContent = "登入成功！";
//       hintSigninMessage.style.color = "#367688";
//       hintSigninMessage.style.display = "block";

//       localStorage.setItem("userToken", data.token);

//       window.location.reload();
//     } else {
//       hintSigninMessage.textContent = data.message;
//       hintSigninMessage.style.display = "block";
//       hintSigninMessage.style.color = "red";
//     }
//   } catch (error) {
//     console.error("Error Signin in:", error);
//     hintSigninMessage.textContent = "網路錯誤，無法完成登入。";
//     hintSigninMessage.style.display = "block";
//   }
// }

// async function fetchCheckUserState() {
//   try {
//     const response = await fetch(userSignInUrl, {
//       method: "GET",
//       headers: {
//         Authorization: `Bearer ${localStorage.getItem("userToken")}`,
//         "Content-Type": "application/json",
//       },
//     });

//     const data = await response.json();

//     if (response.ok) {
//       if (data.data) {
//         loginAndSignin.style.display = "none";
//         logout.style.display = "flex";
//       } else {
//         loginAndSignin.style.display = "flex";
//         logout.style.display = "none";
//       }
//     } else {
//       console.error("驗證用戶狀態失敗：", data.message);
//     }
//   } catch (error) {
//     console.error("Error Checking User's State:", error);
//   }
// }

// function logOut() {
//   localStorage.removeItem("userToken");
//   loginAndSignin.style.display = "flex";
//   logout.style.display = "none";

//   window.location.href = "/";
// }

// function loginSignin(event) {
//   event.preventDefault();
//   signinMask.style.display = "flex";
// }

// function closeSignin(event) {
//   event.preventDefault();
//   const hintSignupMessage = document.querySelector(".hint-signup-message");
//   signinMask.style.display = "none";

//   hintSignupMessage.style.display = "none";
//   clearSignupValue();
//   clearSigninValue();
// }

// function gotoSignup(event) {
//   event.preventDefault();
//   const hintSignupMessage = document.querySelector(".hint-signup-message");
//   signinMask.style.display = "none";
//   signupMask.style.display = "flex";

//   hintSignupMessage.style.display = "none";
//   clearSignupValue();
//   clearSigninValue();
// }

// function closeSignup(event) {
//   event.preventDefault();
//   const hintSignupMessage = document.querySelector(".hint-signup-message");
//   signupMask.style.display = "none";

//   hintSignupMessage.style.display = "none";
//   clearSignupValue();
//   clearSigninValue();
// }

// function gotoSignin(event) {
//   event.preventDefault();
//   const hintSignupMessage = document.querySelector(".hint-signup-message");
//   signupMask.style.display = "none";
//   signinMask.style.display = "flex";

//   hintSignupMessage.style.display = "none";
//   clearSignupValue();
//   clearSigninValue();
// }

// function clearSignupValue() {
//   document.getElementById("signup-name").value = "";
//   document.getElementById("signup-email").value = "";
//   document.getElementById("signup-password").value = "";
// }
// function clearSigninValue() {
//   const hintSigninMessage = document.querySelector(".hint-signin-message");
//   hintSigninMessage.style.display = "none";

//   document.getElementById("signin-email").value = "";
//   document.getElementById("signin-password").value = "";
// }
