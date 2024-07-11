const bookingURL = "/api/booking";
export async function fetchPostBooking(bookingData) {
  document.getElementById("loading").classList.remove("hidden");
  try {
    const token = localStorage.getItem("userToken");
    const response = await fetch(bookingURL, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bookingData),
    });

    if (!response.ok) {
      window.location = "/";
    }

    const data = await response.json();
    if (!data || !data.data || bookingData.attractionId != data.data.id) {
      window.location = "/";
    }
    window.location.href = "/booking";
  } catch (error) {
    console.error("Error fetching post booking:", error);
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
}
