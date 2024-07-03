function getQueryParams() {
  const params = new URLSearchParams(window.location.search);
  return {
    number: params.get("number"),
  };
}
function displayOrderDetails() {
  const { number } = getQueryParams();
  const userName = localStorage.getItem("userName");

  const orderDetailDiv = document.getElementById("order-details");
  orderDetailDiv.innerHTML = `
    <h1>嗨！ ${userName} ，付款成功，預約行程資訊如下：</h1>
   
    <p>訂單編號： ${number}</p>
    `;
}
window.onload = displayOrderDetails;
