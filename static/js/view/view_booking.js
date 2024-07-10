export function updateBookingDetails(bookingDetail) {
  const image = document.querySelector(".fade");
  const attractionName = document.querySelector(".booking-attraction-name");
  const date = document.querySelector(".date-detail");
  const time = document.querySelector(".time-detail");
  const price = document.querySelector(".price-detail");
  const address = document.querySelector(".address-detail");
  const totalPrice = document.querySelector(".booking-price");

  image.src = bookingDetail.attraction.images;
  attractionName.textContent = `台北一日遊：${bookingDetail.attraction.name}`;
  date.textContent = bookingDetail.date;
  time.textContent = bookingDetail.time;
  price.textContent = bookingDetail.price;
  address.textContent = bookingDetail.attraction.address;
  totalPrice.textContent = `總價：新台幣${bookingDetail.price}`;

  time.textContent =
    bookingDetail.time === "上半天" ? "上午9點到下午4點" : "下午5點到晚上12點";
}

export function displayUserName(userName) {
  const title = document.querySelector(".no-booking-title");
  title.textContent = `您好，${userName}，待預定的行程如下：`;
}

export function removeDisplayBooking() {
  const bookingDetail = document.querySelector(".booking-location");
  const seperates = document.querySelectorAll(".seperate");
  const contactArea = document.querySelector(".contact-area");
  const cardArea = document.querySelector(".card-area");
  const totalSubmit = document.querySelector(".total-submit");

  bookingDetail.style.display = "none";
  contactArea.style.display = "none";
  cardArea.style.display = "none";
  totalSubmit.style.display = "none";
  seperates.forEach((seperate) => {
    if (seperate) seperate.style.display = "none";
  });
}
