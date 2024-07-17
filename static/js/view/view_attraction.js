let currentImageIndex = 0;
let nextImageIndex;

export function getAttractionIdFromPath() {
  const path = window.location.pathname;

  const pathSegments = path.split("/");

  return pathSegments[pathSegments.length - 1];
}

export async function AttractionsBooking() {
  const attractionId = getAttractionIdFromPath();
  const form = document.querySelector(".booking");
  const date = form.querySelector("#start").value;
  const timeOption = form.querySelector(
    'input[name="inlineRadioOptions"]:checked'
  ).value;
  const timeMapping = { option1: "morning", option2: "afternoon" };
  const time = timeMapping[timeOption] || "morning";
  const price = form.querySelector(".fee").textContent;
  const priceNumber = price.replace(/\D/g, "");

  const bookingData = {
    attraction_id: parseInt(attractionId),
    date: date,
    time: time,
    price: parseInt(priceNumber),
  };
  return bookingData;
}

export function displayAttraction(attraction) {
  const attractionName = document.querySelector(".attraction-name");
  const category = document.querySelector(".category");
  const mrt = document.querySelector(".attraction-mrt");
  const description = document.querySelector(".content");
  const address = document.querySelector(".address-detail");
  const transportation = document.querySelector(".transportation-detail");

  attractionName.textContent = attraction.name;
  category.textContent = attraction.category;
  mrt.textContent = attraction.mrt;
  description.textContent = attraction.description;
  address.textContent = attraction.address;
  transportation.textContent = attraction.transport;

  displayImageUI(attraction.images);
  displayCircleUI();
}

function displayImageUI(images) {
  const imgArea = document.querySelector(".location-image-area");

  const preloadedImages = images.map((imgUrl) => {
    const img = new Image();
    img.src = imgUrl;
    return img;
  });

  preloadedImages.forEach((img, index) => {
    img.alt = "景點圖片";
    img.className = "fade";

    img.style.display = index === 0 ? "block" : "none";

    imgArea.appendChild(img);
  });
}

function displayCircleUI() {
  const circleContainer = document.querySelector(".circle-container");
  const images = document.querySelectorAll(".location-image-area img");
  images.forEach((_, index) => {
    const circle = document.createElement("img");

    circle.src =
      index === 0
        ? "/static/images/icon/circle-this.png"
        : "/static/images/icon/circle current.png";

    circleContainer.appendChild(circle);
  });
}

const updateCirclesUI = (imageIndex) => {
  const circleContainer = document.querySelector(".circle-container");
  const circles = circleContainer.querySelectorAll("img");
  circles.forEach((circle, index) => {
    circle.src =
      index === imageIndex
        ? "/static/images/icon/circle-this.png"
        : "/static/images/icon/circle current.png";
  });
};

export function imagesTurnRight(event) {
  event.preventDefault();
  const images = document.querySelectorAll(".location-image-area img");

  images[currentImageIndex].style.display = "none";
  nextImageIndex = (currentImageIndex + 1 + images.length) % images.length;
  images[nextImageIndex].style.display = "block";

  currentImageIndex = nextImageIndex;
  updateCirclesUI(currentImageIndex);
}

export function imagesTurnLeft(event) {
  event.preventDefault();
  const images = document.querySelectorAll(".location-image-area img");

  images[currentImageIndex].style.display = "none";
  nextImageIndex = (currentImageIndex - 1 + images.length) % images.length;
  images[nextImageIndex].style.display = "block";

  currentImageIndex = nextImageIndex;
  updateCirclesUI(currentImageIndex);
}

export function updateFeeOption(timeOption) {
  const feeElement = document.querySelector(".fee");
  const feeMapping = {
    morning: "新台幣 2000 元",
    afternoon: "新台幣 2500 元",
  };

  feeElement.textContent = feeMapping[timeOption] || feeMapping["morning"];
}
