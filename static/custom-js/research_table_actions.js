var input_row = document.getElementById('#new-search-row');

$(document).on('click', '.research-table-row', function () {
    id = `tr${$(this).data('id')}`
    row_select(id)
});

function row_select(id) {
    $('.selected-row').toggleClass('selected-row')
    $(`#${id}`).addClass('selected-row')
}

$('#add-new-search').click(function () {
    var now = new Date();
    var day = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);
    var today = now.getFullYear() + "-" + (month) + "-" + (day);
    $('#input_pickup_date').val(today);
    $('option:contains("Any")').attr('selected', true)
    $('[name="age"]').val(4)
    $('[name="origin"]').val("")
    $('[name="dh_o"]').val(100)
    $('[name="destination"]').val("")
    $('[name="dh_d"]').val("")
    $('[name="dh_d"]').attr("readonly",true)
    $('[name="distance"]').val("")
    $('[name="length"]').val("53")
    $('[name="weight"]').val("")
    $('[name="form-type"]').val("post")
    $('#id01').attr('data-action', 'post')
    $('.modal-header-title').text('New Search')
    $('#id01').show()
    $('#add-new-search').prop('disabled', true)
})

$(document).on('click', '.search-edit', function () {
    console.log($(this).data('id'))
    $('#id01').attr('data-action', 'put')
    $('.modal-header-title').text('Edit Search')
    const current_data = $(`#tr${$(this).data('id')}`).data('row')
    $('[name="form-type"]').val('put')
    $('[name="id"]').val(current_data.id)
    $('[name="age"]').val(current_data.age)
    var today = current_data.pickup_date_for_picker;

    $('#input_pickup_date').val(today);
    if (current_data.type_id == null)
        $('option:contains("Any")').attr('selected', true)
    else
        $(`option[value=${current_data.type_id}]`).attr('selected', true)
    $('[name="origin"]').val(current_data.origin)
    $('[name="dh_o"]').val(current_data.dh_o)
    $('[name="destination"]').val(current_data.destination)
    if(current_data.destination === ""){
        $('[name="dh_d"]').attr("readonly",true)
        $('[name="dh_d"]').val("")
    }else{
    $('[name="distance"]').val(current_data.distance)
    }
    $('[name="length"]').val(current_data.length)
    $('[name="weight"]').val(current_data.weight)

    if ($('[name="destination"]').val() !== ""){
        $('[for="input-dh-d"]').html(`DH-D<span style="color: red">*</span>`)
    }
    $('#id01').show()
    $('#add-new-search').prop('disabled', true)
})

$(document).on('click', '.save-new-search', function () {
    let origin = $('[name="origin"]').val();
    if (origin === "") {
        $('[name="origin"]').css('border-color', '#ff0000')
        return
    }
    let dh_o = $('[name="dh_o"]').val();
    if (dh_o === "") {
        $('[name="dh_o"]').css('border-color', '#ff0000')
        return
    }
    if ($('[name="destination"]').val() !== "") {
        let dh_d = $('[name="dh_d"]').val();
        if (dh_d === "") {
            $('[name="dh_d"]').css('border-color', '#ff0000')
            return
        }
    }
    $('[for="input-dh-d"]').html(`DH-D`)
    let data = {
        "age": $('[name="age"]').val(),
        "type": $('[name="type"]').val(),
        "pickup_date": $('[name="pickup_date"]').val(),
        "origin": $('[name="origin"]').val(),
        "dh_o": $('[name="dh_o"]').val(),
        "destination": $('[name="destination"]').val(),
        "dh_d": $('[name="dh_d"]').val(),
        "distance": $('[name="distance"]').val(),
        "length": $('[name="length"]').val(),
        "weight": $('[name="weight"]').val()
    }
    console.log(data)
    search_id = $('[name="id"]').val()
    form_type = $('[name="form-type"]').val()
    if (form_type === 'post') {
        post_data('/post-research/', data, render_research)
    } else
    if (form_type === 'put'){
        if (search_id) {
            post_data(`/put-research/${search_id}/`, data, render_research_updated)
            $(`#tr${search_id}`).click()
        }
    }
    $('#id01').hide()
    $('#add-new-search').prop('disabled', false)
});

$(document).on('click', '.search-remove', function () {
    let current_row = $(this).parents('td').parents('tr').prev('tr').attr('id')
    console.log(current_row)
    get_data(`/search-delete/${$(this).data('id')}/`, function (response) {
        if (response.id) {
            $(`#tr${response.id}`).toggle()
        }
    })
        all_loads()
})

$(document).on('click', '.cancel-new-search', function () {
    $('[for="input-dh-d"]').html(`DH-D`)
    $('#id01').hide()
    $('#add-new-search').prop('disabled', false)
})


$(document).on('click', '.research-table-row', function () {
    $('#load-result-table-body').html(`<div >
        <div class="loader">
          <div class="inner one"></div>
          <div class="inner two"></div>
          <div class="inner three"></div>
        </div>
        </div>`)
    $('#results-count').html(`${0} results`)
    selected_search = $(this).data('id')
    get_data(`/search/${selected_search}/`, render_result_loads)
})

$(document).on('click', '#view-all-loads', function () {
    $('#load-result-table-body').html(`
    <div >
        <div class="loader">
          <div class="inner one"></div>
          <div class="inner two"></div>
          <div class="inner three"></div>
        </div>
        </div>`)
    $('.selected-row').toggleClass('selected-row')
    get_data(`/search/0/`, render_result_loads)
});

function all_loads() {
    $('#load-result-table-body').html(`<div >
        <div class="loader">
          <div class="inner one"></div>
          <div class="inner two"></div>
          <div class="inner three"></div>
        </div>
        </div>`)
    $('#load-table-body').html('')
    $('.selected-row').toggleClass('selected-row')
    get_data(`/search/0/`, render_result_loads)
}



$('.required-input-custom').keyup(function () {
    let origin = $('[name="origin"]').val();
    let dh_o = $('[name="dh_o"]').val();
    let dh_d = $('[name="dh_d"]').val();
    if (origin !== "") {
        $('[name="origin"]').css('border-color', '#d0d7de')
    }
    if (dh_o !== "") {
        $('[name="dh_o"]').css('border-color', '#d0d7de')
    }
    if (dh_d !== "") {
        $('[name="dh_d"]').css('border-color', '#d0d7de')
    }
    return
})

$('.input-addresses').keyup(function () {
    let origin = $('[name="origin"]').val();
    let destination = $('[name="destination"]').val();
    if (origin !== "" || destination !== "") {
        $('[name="distance"]').val("")
    }
    return
})


$('[name="length"]').keyup(function () {
    if ($(this).val()>65) {
        $(this).val("65")
    }
    if ($(this).val()<1) {
        $(this).val("")
    }
    return
})


$('[name="length"]').change(function () {
    if ($(this).val()>65) {
        $(this).val("65")
    }
    if ($(this).val()<1) {
        $(this).val("")
    }
    return
})

$('[name="age"]').keyup(function () {
    if ($(this).val()>24) {
        $(this).val("24")
    }else if($(this).val()<1){
        $(this).val("1")
    }
    return
})

$('[name="age"]').change(function () {
    if ($(this).val()>24) {
        $(this).val("24")
    }else if($(this).val()<1){
        $(this).val("1")
    }
    return
})

$('[name="weight"]').keyup(function () {
    if ($(this).val()>80000) {
        $(this).val("80000")
    }else if ($(this).val()<1) {
        $(this).val("")
    }
    return
})

$('[name="weight"]').change(function () {
    if ($(this).val()>80000) {
        $(this).val("80000")
    }else if ($(this).val()<1) {
        $(this).val("")
    }
    return
})

$('[name="dh_o"]').keyup(function () {
    console.log($(this).val())
    if ($(this).val()>500) {
        $(this).val("500")
    }else if ($(this).val()<1) {
        $(this).val("1")
    }
    return
})

$('[name="dh_o"]').change(function () {
    if ($(this).val()>500) {
        $(this).val("500")
    }else if ($(this).val()<1) {
        $(this).val("1")
    }
    return
})

$('[name="dh_d"]').keyup(function () {
    if ($(this).val()>500) {
        $(this).val("500")
    }else if ($(this).val()<1) {
        $(this).val("1")
    }
    return
})

$('[name="dh_d"]').change(function () {
    if ($(this).val()>500) {
        $(this).val("500")
    }else if ($(this).val()<1) {
        $(this).val("1")
    }
    return
})

$('[name="destination"]').keyup(function () {
    if ($(this).val() !== ""){
        $('[for="input-dh-d"]').html(`DH-D<span style="color: red">*</span>`)
        $('[name="dh_d"]').val("100")
        $('[name="dh_d"]').attr("readonly",false)
    }else{
        $('[for="input-dh-d"]').html(`DH-D`)
        $('[name="dh_d"]').val("")
        $('[name="dh_d"]').attr("readonly",true)
    }
})


function openInNewTab(url) {
  window.open(url, '_blank').focus();
}

get_my_research()
// all_loads()

