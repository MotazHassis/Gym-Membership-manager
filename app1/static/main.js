$(document).ready(function () {
  
  $('#search_item').keyup(function () {
      // const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      var data = $("#regForm").serialize()
      console.log('Hellllloooo')
      $.ajax({
          // headers: {'X-CSRFToken': csrftoken},
          method: "POST",
          url: '/search',
          data: data,
      })
      .done(function (res) {
        console.log('Hellllloooo_done')
          $('#results').html(res);
      })
      .fail(function () {
          console.log("Ajax request failed: ");
      });
  });
});



// popover
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl);
});

// Gender Select
if (window.location.pathname === "/") {
  const radioBtn1 = document.querySelector("#flexRadioDefault1");
  const radioBtn2 = document.querySelector("#flexRadioDefault2");
  const radioBtn3 = document.querySelector("#flexRadioDefault3");
  const genderSelect = document.querySelector("#genderSelect");

  radioBtn1.addEventListener("change", () => {
    genderSelect.classList.add("d-none");
  });
  radioBtn2.addEventListener("change", () => {
    genderSelect.classList.add("d-none");
  });
  radioBtn3.addEventListener("change", () => {
    genderSelect.classList.remove("d-none");
  });
}



