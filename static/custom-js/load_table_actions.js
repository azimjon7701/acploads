// $(document).on('click', '.research-table-row', function () {
//     id = `tr${$(this).data('id')}`
//     row_select(id)
// });


const contact_types = {
    'telegram': {
        'title': 'Telegram',
        'placeholder': '@username',
        'input-type': 'text'
    },
    'phone': {
        'title': 'Phone',
        'placeholder': 'Phone',
        'input-type': 'text'
    },
    'email': {
        'title': 'Email',
        'placeholder': 'example@mail.com',
        'input-type': 'email'
    },
}

$(document).on('click', '.result-table-row', function (e) {
    $(this).unbind('click');
    id = $(this).data('id')
    if (e.target.className === "contact-link"){
        openInNewTab(e.target.href)
    }
    row_select_expand(id)
});


function row_select_expand(id) {
    $('.selected-row-expand').toggleClass('selected-row-expand')
    $(`#${id}`).addClass('selected-row-expand')
}

function row_select(id) {
    $('.selected-row').toggleClass('selected-row')
    $(`#${id}`).addClass('selected-row')
}

$('#add-new-load').click(function () {
    var now = new Date();
    var day = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);
    var today = now.getFullYear() + "-" + (month) + "-" + (day);
    $('#input_pickup_date').val(today);
    $('option:contains("Any")').attr('selected', true)
    $('[name="age"]').val(1)
    $('[name="origin"]').val("")
    $('[name="dh_o"]').val(100)
    $('[name="destination"]').val("")
    $('[name="dh_d"]').val(100)
    $('[name="distance"]').val("")
    $('[name="length"]').val("53")
    $('[name="weight"]').val("")
    $('[name="price"]').val("")
    $('[name="name"]').val("")
    $('[name="contact"]').val("")
    $('[name="contact_type"]').val("telegram")
    $('[name="comment"]').val("")
    $('[name="form-type"]').val("post")
    $('#id02').attr('data-action', 'post')
    $('.modal-header-title').text('New Load')
    $('#id02').show()
    $('#add-new-load').prop('disabled', true)
})

$(document).on('click', '.save-new-load', function () {
    let origin = $('[name="origin"]').val();
    let contact = $('[name="contact"]').val();
    let name = $('[name="name"]').val();
    if (origin === "" || contact === "" || name === "") {
        if (origin === "") {
            $('[name="origin"]').css('border-color', '#ff0000')
        }
        if (contact === "") {
            $('[name="contact"]').css('border-color', '#ff0000')
        }
        if (name === "") {
            $('[name="name"]').css('border-color', '#ff0000')
        }
        return
    }
    let data = {
        "pickup_date": $('[name="pickup_date"]').val(),
        "type": $('[name="type"]').val(),
        "origin": $('[name="origin"]').val(),
        "destination": $('[name="destination"]').val(),
        "distance": $('[name="distance"]').val(),
        "length": $('[name="length"]').val(),
        "weight": $('[name="weight"]').val(),
        "contact_type": $('[name="contact_type"]').val(),
        "contact": $('[name="contact"]').val(),
        "name": $('[name="name"]').val(),
        "price": $('[name="price"]').val(),
        "comment": $('[name="comment"]').val(),
        "ref_number": $('[name="ref-number"]').val()
    }
    console.log(data)
    load_id = $('[name="id"]').val()
    form_type = $('[name="form-type"]').val()
    if (form_type === 'post') {
        post_data('/post-load/', data, render_load)
    } else
    if (form_type === "put"){
        if (load_id) {
            post_data(`/put-load/${load_id}/`, data, render_load_updated)
        }
    }
    $('#id02').hide()
    $('#add-new-load').prop('disabled', false)
});

$(document).on('click', '.renew', function () {
    let data = {"renew":true}
    load_id = $(this).data("id")
    post_data(`/put-load/${load_id}/`, data, render_load_updated)
});


$(document).on('click', '.load-remove', function () {
    console.log($(this).data('id'))
    get_data(`/load-delete/${$(this).data('id')}/`, function (response) {
        console.log(response.id)
        if (response.id) {
            $(`#accordion${response.id}`).toggle()
            $(`#collaps${response.id}`).toggle()
        }
    })
})

$(document).on('click', '.cancel-new-load', function () {
    $('#id02').hide()
    $('[name="id"]').val("")
    $('[name="age"]').val("")
    $('[name="origin"]').val("")
    $('[name="destination"]').val("")
    $('[name="distance"]').val("")
    $('[name="length"]').val("")
    $('[name="weight"]').val("")
    $('[name="price"]').val("")
    $('[name="name"]').val("")
    $('[name="contact"]').val("")
    $('#add-new-load').prop('disabled', false)
})

function set_default_values() {
    today = new Date() //.toLocaleString("en-US", {timeZone: "America/New_York"})
    // $('[name="pickup_date"]').datepicker({
    //     "setDate": new Date(),
    //     "autoclose": true
    // });
    // console.log()
}

$(document).on('click', '.load-edit', function () {
    const current_data = $(`#accordion${$(this).data('id')}`).data('row')
    console.log(current_data)
    var today = current_data.pickup_date_for_picker;
    $('#input_pickup_date').val(today);

    if (current_data.type_id == null)
        $('option:contains("Any")').attr('selected', true)
    else
        $(`option[value=${current_data.type_id}]`).attr('selected', true)

    $('[name="form-type"]').val("put")

    $('[name="id"]').val(current_data.id)
    $('[name="age"]').val(current_data.age)
    $('[name="origin"]').val(current_data.origin)
    $('[name="destination"]').val(current_data.destination)
    $('[name="distance"]').val(current_data.distance)
    $('[name="length"]').val(current_data.length)
    $('[name="weight"]').val(current_data.weight)
    $('[name="price"]').val(current_data.price)
    $('[name="name"]').val(current_data.name)
    $('[name="contact"]').val(current_data.contact)
    $('[name="contact_type"]').val(current_data.contact_type)
    $('[name="ref-number"]').val(current_data.ref_number)
    if (current_data.contact_type) {
        $('#contact-type-id').html(contact_types[current_data.contact_type]['title'] + `&ensp;<span class="caret"></span>`)
        $('[name="contact"]').attr('placeholder', contact_types[current_data.contact_type]['placeholder'])
        $('[name="contact"]').attr('type', contact_types[current_data.contact_type]['input-type'])

    }

    $('[name="comment"]').val(current_data.comment)
    $('#id02').attr('data-action', 'put')
    $('.modal-header-title').text('Edit Load')
    $('#id02').show()
})

$('.contact-type').click(function () {
    $('#contact-type-id').html($(this).text() + `&ensp;<span class="caret"></span>`)
    $('[name="contact"]').attr('placeholder', contact_types[$(this).data('key')]['placeholder'])
    $('[name="contact"]').attr('type', contact_types[$(this).data('key')]['input-type'])
    $('[name="contact_type"]').val($(this).data('key'))
})

$('.required-input-custom').keyup(function () {
    let origin = $('[name="origin"]').val();
    let contact = $('[name="contact"]').val();
    let name = $('[name="name"]').val();
    if (origin !== "") {
        $('[name="origin"]').css('border-color', '#d0d7de')
    }
    if (contact !== "") {
        $('[name="contact"]').css('border-color', '#d0d7de')
    }
    if (name !== "") {
        $('[name="name"]').css('border-color', '#d0d7de')
    }
    return

})


get_loads()
set_default_values()