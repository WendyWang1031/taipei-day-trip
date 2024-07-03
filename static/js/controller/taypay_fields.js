import { fetchGetBooking, fetchDeleteBooking } from "./controller_booking.js";

const orderURL = "/api/orders";
let prime;

export function tappayGetPrime() {
  TPDirect.setupSDK(
    151739,
    "app_GRDJY8GRSFthRldTXuilOl2ecy2VR6F9VmixnWK1XOCBf6BYatOgmf2vFAo1",
    "sandbox"
  );
  TPDirect.card.setup({
    fields: {
      number: {
        // css selector
        element: document.getElementById("card-number"),
        placeholder: "**** **** **** ****",
      },
      expirationDate: {
        // DOM object
        element: document.getElementById("card-expiration-date"),
        placeholder: "MM / YY",
      },
      ccv: {
        element: document.getElementById("card-cvc"),
        placeholder: "CVC",
      },
    },
    styles: {
      input: {
        color: "gray",
        border: "1px solid #e8e8e8 ",
        height: "38px",
        "border-radius": "5px",
        padding: "8px",
      },
      "input.cvc": {
        "font-size": "16px",
      },
      ":focus": {
        color: "black",
      },
      ".valid": {
        color: "green",
      },
      ".invalid": {
        color: "red",
      },
      "@media screen and (max-width: 400px)": {
        input: {
          color: "orange",
        },
      },
    },
    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
      beginIndex: 6,
      endIndex: 11,
    },
  });
  TPDirect.card.onUpdate(function (update) {
    /* Disable / enable submit button depend on update.canGetPrime  */
    /* ============================================================ */

    // update.canGetPrime === true
    //     --> you can call TPDirect.card.getPrime()
    // const submitButton = document.querySelector('button[type="submit"]')
    if (update.canGetPrime) {
      // submitButton.removeAttribute('disabled')
      $('button[type="submit"]').removeAttr("disabled");
    } else {
      // submitButton.setAttribute('disabled', true)
      $('button[type="submit"]').attr("disabled", true);
    }

    /* Change card type display when card type change */
    /* ============================================== */

    // cardTypes = ['visa', 'mastercard', ...]
    var newType = update.cardType === "unknown" ? "" : update.cardType;
    $("#cardtype").text(newType);

    /* Change form-group style when tappay field status change */
    /* ======================================================= */

    // number 欄位是錯誤的
    if (update.status.number === 2) {
      setNumberFormGroupToError(".card-number-group");
    } else if (update.status.number === 0) {
      setNumberFormGroupToSuccess(".card-number-group");
    } else {
      setNumberFormGroupToNormal(".card-number-group");
    }

    if (update.status.expiry === 2) {
      setNumberFormGroupToError(".expiration-date-group");
    } else if (update.status.expiry === 0) {
      setNumberFormGroupToSuccess(".expiration-date-group");
    } else {
      setNumberFormGroupToNormal(".expiration-date-group");
    }

    if (update.status.ccv === 2) {
      setNumberFormGroupToError(".ccv-group");
    } else if (update.status.ccv === 0) {
      setNumberFormGroupToSuccess(".ccv-group");
    } else {
      setNumberFormGroupToNormal(".ccv-group");
    }
  });

  $("form").on("submit", function (event) {
    event.preventDefault();

    // fix keyboard issue in iOS device
    forceBlurIos();

    const tappayStatus = TPDirect.card.getTappayFieldsStatus();
    console.log(tappayStatus);

    // Check TPDirect.card.getTappayFieldsStatus().canGetPrime before TPDirect.card.getPrime
    if (tappayStatus.canGetPrime === false) {
      alert("can not get prime");
      return;
    }

    // Get prime
    TPDirect.card.getPrime(function (result) {
      if (result.status !== 0) {
        alert("get prime error " + result.msg);
        return;
      }
      alert("get prime 成功，prime: " + result.card.prime);

      return new Promise((resolve, reject) => {
        TPDirect.card.getPrime(function (result) {
          if (result.status !== 0) {
            console.error("Error getting prime:", result.msg);
            reject("Error getting prime: " + result.msg);
          } else {
            console.log("Successfully obtained prime:", result.card.prime);
            resolve(fetchPostOrder(result.card.prime));
          }
        });
      });

      var command = `
          Use following command to send to server \n\n
          curl -X POST https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime \\
          -H 'content-type: application/json' \\
          -H 'x-api-key: partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM' \\
          -d '{
              "partner_key": "partner_6ID1DoDlaPrfHw6HBZsULfTYtDmWs0q0ZZGKMBpp4YICWBxgK97eK3RM",
              "prime": "${result.card.prime}",
              "amount": "1",
              "merchant_id": "GlobalTesting_CTBC",
              "details": "Some item",
              "cardholder": {
                  "phone_number": "+886923456789",
                  "name": "王小明",
                  "email": "LittleMing@Wang.com",
                  "zip_code": "100",
                  "address": "台北市天龍區芝麻街1號1樓",
                  "national_id": "A123456789"
              }
          }'`.replace(/                /g, "");
      // document.querySelector("#curl").innerHTML = command;
      console.log(command);
      prime = result.card.prime;
      return result.card.prime;
    });
  });

  function setNumberFormGroupToError(selector) {
    $(selector).addClass("has-error");
    $(selector).removeClass("has-success");
  }

  function setNumberFormGroupToSuccess(selector) {
    $(selector).removeClass("has-error");
    $(selector).addClass("has-success");
  }

  function setNumberFormGroupToNormal(selector) {
    $(selector).removeClass("has-error");
    $(selector).removeClass("has-success");
  }

  function forceBlurIos() {
    if (!isIos()) {
      return;
    }
    var input = document.createElement("input");
    input.setAttribute("type", "text");
    // Insert to active element to ensure scroll lands somewhere relevant
    document.activeElement.prepend(input);
    input.focus();
    input.parentNode.removeChild(input);
  }

  function isIos() {
    return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  }
  return prime;
}

export async function fetchPostOrder(prime) {
  try {
    console.log("test1");
    const token = localStorage.getItem("userToken");

    const bookingData = await fetchGetBooking();
    console.log("fetchGet:", bookingData);

    const orderData = BookingToOrderData(prime, bookingData);
    console.log("orderData:", orderData);

    const response = await fetch(orderURL, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(orderData),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }

    const data = await response.json();
    if (data && data.data) {
      await fetchDeleteBooking();
      window.location.href = `/thankyou?number=${data.data.number}`;
    } else {
      throw new Error("Payment data is missing.");
    }
  } catch (error) {
    console.error("Error fetching post booking:", error);
  }
}

function BookingToOrderData(prime, bookingData) {
  const contactName = document.querySelector("#contact-name").value;
  const contactEmail = document.querySelector("#contact-email").value;
  const contactPhone = document.querySelector("#contact-phone").value;

  const orderData = {
    prime: prime,
    order: {
      price: parseInt(bookingData.price),
      trip: {
        attraction: {
          id: parseInt(bookingData.attraction.id),
          name: bookingData.attraction.name,
          address: bookingData.attraction.address,
          images: bookingData.attraction.images,
        },
        date: bookingData.date,
        time: bookingData.time,
      },
      contact: {
        name: contactName,
        email: contactEmail,
        phone: contactPhone,
      },
    },
  };
  return orderData;
}
