// Get the select_modal
var select_modal = document.getElementById("myModal");
var btn_open_select_modal = document.getElementById("btn-open-select-modal")

if (btn_open_select_modal) {
    document.getElementById("btn-open-select-modal").onclick = function () {
        select_modal.style.display = "block";
    }
}


window.onclick = function (event) {
    // console.log(event.target)
    // if (event.target == select_modal) {
    //     select_modal.style.display = "none";
    //     window.location.url('/')
    // }
}
$(".close-btn-modal").click(function () {
    select_modal.style.display = "none";
    window.location.url('/')
})

// $('body').addClass('c-header-cart-shown')