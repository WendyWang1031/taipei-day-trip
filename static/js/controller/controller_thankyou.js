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
    <h1>嗨！ ${userName} ，行程預定成功</h1>
    <h1>您的訂單編號如下</h1>
    <p> ${number}</p>
    <div>請記住此編號，請到會員中心查詢歷史訂單</div>
    <a href="/">
    <h2>回首頁</h2>
    </a>
    `;
}
window.onload = displayOrderDetails;
