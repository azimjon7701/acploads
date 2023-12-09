$('.aye-button').click(function (e) {
    $('.aye-icon').toggleClass('glyphicon-eye-close')
    $('.aye-icon').toggleClass('glyphicon-eye-open')
    console.log($('.aye-icon').attr('class').split(' '))
    if ($('.aye-icon').attr('class').split(' ')[3] === "glyphicon-eye-open") {
        $('[name="password"]').attr('type', 'text')
        $('[name="new-password"]').attr('type', 'text')
    } else if ($('.aye-icon').attr('class').split(' ')[3] === "glyphicon-eye-close") {
        $('[name="password"]').attr('type', 'password')
        $('[name="new-password"]').attr('type', 'password')
    }
})
$('.aye-button1').click(function (e) {
    $('.aye-icon1').toggleClass('glyphicon-eye-close')
    $('.aye-icon1').toggleClass('glyphicon-eye-open')
    console.log($('.aye-icon1').attr('class').split(' '))
    if ($('.aye-icon1').attr('class').split(' ')[3] === "glyphicon-eye-open") {
        $('[name="password1"]').attr('type', 'text')
        $('[name="confirm-password"]').attr('type', 'text')
    } else if ($('.aye-icon1').attr('class').split(' ')[3] === "glyphicon-eye-close") {
        $('[name="password1"]').attr('type', 'password')
        $('[name="confirm-password"]').attr('type', 'password')
    }
})
$('.aye-button0').click(function (e) {
    $('.aye-icon0').toggleClass('glyphicon-eye-close');
    $('.aye-icon0').toggleClass('glyphicon-eye-open');
    console.log($('.aye-icon0').attr('class').split(' '));
    if ($('.aye-icon0').attr('class').split(' ')[3] === "glyphicon-eye-open") {
        $('[name="password0"]').attr('type', 'text');
        $('[name="current-password"]').attr('type', 'text');
    } else if ($('.aye-icon0').attr('class').split(' ')[3] === "glyphicon-eye-close") {
        $('[name="password0"]').attr('type', 'password');
        $('[name="current-password"]').attr('type', 'password');
    }
})


const rmCheck = document.getElementById("login-rememberme"),
    emailInput = document.getElementById("email");

if (localStorage.checkbox && localStorage.checkbox !== "") {
    rmCheck.setAttribute("checked", "checked");
    emailInput.value = localStorage.username;
} else {
    rmCheck.removeAttribute("checked");
    if (emailInput) {
        emailInput.value = "";
    }
}

function lsRememberMe() {
    if (rmCheck.checked && emailInput.value !== "") {
        localStorage.username = emailInput.value;
        localStorage.checkbox = rmCheck.value;
    } else {
        localStorage.username = "";
        localStorage.checkbox = "";
    }
}

$('#company-id').on('keyup', function () {
    let id_check_res = $('.id-check-res');
    let inpval = $(this).val().toUpperCase();
    console.log($('#is-new-company').val());
    if (inpval.length === 4) {
        id_check_res.css('color', 'slategrey');
        id_check_res.html('&nbsp;&nbsp;Only characters A-Z');
        $.get(`/check-company-id/?company=${inpval}`, function (data, status) {
            if ($('#is-new-company').val()==='true') {
                if (data.avialable) {
                    id_check_res.css('display', 'block');
                    id_check_res.css('color', 'red');
                    id_check_res.html('&nbsp;&nbsp;Company ID taken');
                    $('.company-signup-btn').prop('disabled',true);
                } else {
                    id_check_res.css('display', 'block');
                    id_check_res.css('color', 'green');
                    id_check_res.html('&nbsp;&nbsp;Company ID available');
                    $('.company-signup-btn').prop('disabled',false);
                }
            } else {
                if (data.avialable) {
                    id_check_res.css('display', 'block');
                    id_check_res.css('color', 'green');
                    id_check_res.html('&nbsp;&nbsp;Company ID is avialable');
                    $('.company-signup-btn').prop('disabled',false);
                } else {
                    id_check_res.css('display', 'block');
                    id_check_res.css('color', 'red');
                    id_check_res.html('&nbsp;&nbsp;Company ID not found');
                    $('.company-signup-btn').prop('disabled',true);
                }
            }

        });
    } else {
        id_check_res.css('color', 'slategrey');
        id_check_res.html('&nbsp;&nbsp;Only characters A-Z');
    }

})

function allLetter(inputtxt) {

}