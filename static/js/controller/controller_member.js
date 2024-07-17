import * as MemberView from "../view/view_member.js";

document.addEventListener("DOMContentLoaded", function () {
  fetchGetUserProfile();

  const updateButton = document.querySelector('button[type="button"]');
  updateButton.addEventListener("click", updateProfile);
});

const memberURL = "/api/member";

async function updateProfile() {
  document.getElementById("loading").classList.remove("hidden");

  const token = localStorage.getItem("userToken");
  const form = document.getElementById("updateProfileForm");
  const formData = new FormData(form);

  if (!checkFormValue()) {
    document.getElementById("loading").classList.add("hidden");
    return;
  }

  try {
    const response = await fetch(memberURL, {
      method: "POST",
      body: formData,
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      console.log("Failed to post member details:", response.status);
      if (response.status === 400) {
        MemberView.updateMessage(
          "errorMessage",
          "該電子郵件已被註冊，請使用其他郵件地址。"
        );
      } else {
        MemberView.updateMessage(
          "errorMessage",
          "提交表單回應有誤，請聯繫客服人員。"
        );
      }

      throw new Error(response.status);
    } else {
      MemberView.updateMessage("errorMessage", "會員資料更新成功");
      window.location.reload();
    }
  } catch (error) {
    console.error("Error updating profile");
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
}

async function fetchGetUserProfile() {
  const token = localStorage.getItem("userToken");
  try {
    const response = await fetch(memberURL, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const result = await response.json();

    if (result.ok && result.data) {
      document.getElementById("userName").textContent = result.data.name;
      document.getElementById("userEmail").textContent = result.data.email;
      document.getElementById("userPhone").textContent =
        result.data.phone_number || "未提供手機號碼";
      const defaultAvatar =
        "../static/images/image/blank-profile-picture-973460_960_720_2583405935a02dfab699c6.jpeg";
      document.getElementById("userAvatar").src =
        result.data.avatar || defaultAvatar;
      document.getElementById("userAvatar").alt = result.data.avatar
        ? "User Avatar"
        : "Default Avatar";
    } else {
      console.error("Failed to retrieve user profile.");
    }
  } catch (error) {
    console.error("Error fetching user profile:", error);
  }
}

function checkFormValue() {
  const form = document.getElementById("updateProfileForm");
  const email = form.querySelector('[name="email"]').value;
  const name = form.querySelector('[name="name"]').value;
  const phone = form.querySelector('[name="phone"]').value;
  const avatar = form.querySelector('[name="avatar"]');

  const hasAvatar = avatar.files.length > 0;

  // 驗證電子郵件
  if (email && !email.includes("@")) {
    MemberView.updateMessage("errorMessage", "電子郵件地址必須包含 '@'。");
    return false;
  }

  // 驗證手機號碼
  if (phone && !(phone.startsWith("09") && phone.length === 10)) {
    MemberView.updateMessage(
      "errorMessage",
      "手機號碼必須以 '09' 開頭且為 10 位數字。"
    );
    return false;
  }

  // 驗證是否所有欄位都為空
  if (!email.trim() && !name.trim() && !phone.trim() && !hasAvatar) {
    MemberView.updateMessage(
      "errorMessage",
      "請至少更新一項資料（姓名、電子郵件、電話或頭像）。"
    );
    document.getElementById("loading").classList.add("hidden");
    return false;
  }

  return true;
}
