function getQueryParams() {
  const params = new URLSearchParams(window.location.search);
  return {
    number: params.get("number"),
  };
}
function displayOrderDetails() {
  let { number } = getQueryParams();
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

window.onload = function () {
  displayOrderDetails();
  fetchGetOrderDetails();
};

const orderURL = "/api/orders";

async function fetchGetOrderDetails() {
  document.getElementById("loading").classList.remove("hidden");
  let { number } = getQueryParams();
  const token = localStorage.getItem("userToken");

  try {
    const response = await fetch(`${orderURL}/${number}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      console.log("Error response:");
    }

    const data = await response.json();
    console.log("data:", data);
    if (!data || !data.data || number != data.data.number) {
      window.location.href = `/thankyou?number=${data.data.number}`;
    }

    displayOrder(data.data);
  } catch (error) {
    console.error("Error fetching attraction:", error);
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
}
function displayOrder(orderDetails) {
  const container = document.getElementById("order-details-container");
  container.innerHTML = `
    <div class="order-card">      
    
      <h2>訂單狀態：${orderDetails.status === 0 ? "已完成" : "未完成"}</h2>
      <h2>訂單日期：${orderDetails.trip.date}</h2>
      <h2>訂單編號：${orderDetails.number}</h2>
      
      
      
      <div class="trip-info">
      
      <div class="trip-area">
      <div class="trip-detail">
      <h2>旅遊行程<h2>
      <p>行程：${orderDetails.trip.attraction.name}</p>
      <p>地址：${orderDetails.trip.attraction.address}</p>
      <p>時間：${orderDetails.trip.time}</p>
      <p>價格：新台幣${orderDetails.price}元</p>
      
      <br />
      <div class="contact-info">

      <h2>聯絡資訊<h2>
        <p>姓名：${orderDetails.contact.name}</p>
        <p>電子郵件：${orderDetails.contact.email}</p>
        <p>電話：${orderDetails.contact.phone}</p>
      </div>
      </div>
      <div class="trip-pic">
      <img src="${
        orderDetails.trip.attraction.images
      }" alt="景點圖片" class="attraction-image">
      </div>
      </div>
      </div>

      
      

    </div>
  `;
}
