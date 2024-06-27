export async function AttractionsBooking(event) {
  event.preventDefault();

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
