import * as Model from "../model/auth.js";
import * as View from "../view/view.js";

const userRegisterUrl = "/api/user";
const userSignInUrl = "/api/user/auth";

export function setupEventListeners() {
  document
    .querySelector(".login-signin")
    .addEventListener("click", () =>
      View.setElementDisplay(".signin-mask", "flex")
    );

  document.querySelector(".go-to-signup").addEventListener("click", () => {
    View.setElementDisplay(".signin-mask", "none");
    View.setElementDisplay(".signup-mask", "flex");
    View.setElementDisplay(".hint-signin-message", "none");
    View.clearInputs("signin-email", "signin-password");
  });

  document.querySelector(".go-to-signin").addEventListener("click", () => {
    View.setElementDisplay(".signup-mask", "none");
    View.setElementDisplay(".signin-mask", "flex");
    View.setElementDisplay(".hint-signup-message", "none");
    View.clearInputs("signup-name", "signup-email", "signup-password");
  });

  document.querySelector(".close-signin").addEventListener("click", () => {
    View.setElementDisplay(".signin-mask", "none"),
      View.setElementDisplay(".hint-signin-message", "none");
    View.clearInputs("signin-email", "signin-password");
  });

  document.querySelector(".close-signup").addEventListener("click", () => {
    View.setElementDisplay(".signup-mask", "none"),
      View.setElementDisplay(".hint-signup-message", "none"),
      View.clearInputs("signup-name", "signup-email", "signup-password");
  });

  document
    .querySelector(".signin")
    .addEventListener("submit", async (event) => {
      event.preventDefault();
      console.log("Form submitted");

      const formData = new FormData(event.target);

      const result = await Model.fetchApi(userSignInUrl, "PUT", formData);
      if (result.ok) {
        localStorage.setItem("userToken", result.data.token);
        View.updateMessage(".hint-signin-message", "登入成功", true);
        View.clearInputs("signin-email", "signin-password");
        window.location.reload();
        View.displayUserInterface(true);
      } else {
        View.updateMessage(".hint-signin-message", result.message, false);
        View.clearInputs("signin-email", "signin-password");
      }
    });

  document
    .querySelector(".signup")
    .addEventListener("submit", async (event) => {
      event.preventDefault();
      const formData = new FormData(event.target);

      //   for (let [key, value] of formData.entries()) {
      //     console.log(`${key}: ${value}`);
      //   }

      const result = await Model.fetchApi(userRegisterUrl, "POST", formData);
      if (result.ok) {
        View.updateMessage(
          ".hint-signup-message",
          "註冊成功，請登入會員",
          true
        );
        View.clearInputs("signup-name", "signup-email", "signup-password");
      } else {
        View.updateMessage(".hint-signup-message", result.message, false);
        View.clearInputs("signup-name", "signup-email", "signup-password");
      }
    });
}

export async function checkUserState() {
  const token = localStorage.getItem("userToken");

  if (!token) {
    View.displayUserInterface(false);
    return false;
  }

  const result = await Model.fetchUserState(token);

  if (result.ok && result.data.data) {
    View.displayUserInterface(true);
    localStorage.setItem("userName", result.data.data.name);
    return true;
  } else {
    console.error("驗證用戶狀態失敗：", result.data.data);
    View.displayUserInterface(false);
    window.location.href = "/";
    return false;
  }
}

// export async function fetchGetUserName() {
//   const token = localStorage.getItem("userToken");
//   try {
//     const response = await fetch(userSignInUrl, {
//       headers: {
//         Authorization: `Bearer ${token}`,
//       },
//     });

//     if (!response.ok) {
//       console.error("Failed to fetch booking details:", response.status);
//       return;
//     }

//     const data = await response.json();

//     if (!data || !data.data) {
//       console.error("No booking data available");
//       return;
//     }
//     console.log(data.data.name);
//     localStorage.setItem("userName", data.data.name);
//     return data.data.name;
//   } catch (error) {
//     console.error("Error fetching attraction:", error);
//   }
// }

export function setupLogoutListener() {
  const logout = document.querySelector(".logout");
  logout.addEventListener("click", logOut);
}

function logOut() {
  Model.clearUserSession();

  window.location.reload();
  window.location.href = "/";
}

export function initialize() {
  setupEventListeners();
  setupLogoutListener();
  // fetchGetUserName();
}
