document.addEventListener("DOMContentLoaded", function () {
  fetchUserProfile();
});

const memberURL = "/api/member";

async function updateProfile() {
  document.getElementById("loading").classList.remove("hidden");
  const token = localStorage.getItem("userToken");
  const form = document.getElementById("updateProfileForm");
  const formData = new FormData(form);

  try {
    const response = await fetch(memberURL, {
      method: "POST",
      body: formData,
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      let errorMessage = "重複的信箱，請重新輸入";
      console.log(
        "Failed to post member details:",
        response.status,
        errorMessage
      );
      const errorMessageDiv = document.getElementById("errorMessage");
      errorMessageDiv.textContent = errorMessage;
      errorMessageDiv.style.display = "block";
      throw new Error(errorMessage);
    } else {
      let errorMessage = "會員資料更新成功";
      const errorMessageDiv = document.getElementById("errorMessage");
      errorMessageDiv.textContent = errorMessage;
      errorMessageDiv.style.display = "block";
      window.location.reload();
    }
  } catch (error) {
    console.error("Error updating profile");
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
}

async function fetchUserProfile() {
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
