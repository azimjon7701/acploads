$(document.body).on("mouseenter",'.rating-review .star-rate',function (e) {
    $(e.target).parent().children('.star-rate').addClass('fa-star');
    $(e.target).parent().children('.star-rate').css('color', '#ffbd00');
    $(e.target).parent().children('.star-rate').removeClass('fa-star-o');
    $(e.target).addClass('fa-star');
    $(e.target).css('color', '#ffbd00');
    $(e.target).prevAll().each(function () {
        $(this).addClass('fa-star');
    })
    $(e.target).nextAll().each(function () {
        $(this).addClass('fa-star-o');
        $(this).removeClass('fa-star');
    })
    $(e.target).parent().attr("data-selected-rate", $(e.target).attr('data-value'))
});

// Unselect rating
$(document.body).on("mouseleave",'.rating-review',function (e) {
    var rateStars = $(e.currentTarget).children('.star-rate');
    var defaultRate = parseInt($(e.currentTarget).attr('data-user-rate'));
    for (let i = defaultRate; i < rateStars.length; i++) {
        $(rateStars[i]).removeClass('fa-star');
        $(rateStars[i]).addClass('fa-star-o');
        $(rateStars[i]).removeAttr('style');
    }
    for (let j = 0; j < defaultRate; j++) {
        $(rateStars[j]).removeClass('fa-star-o');
        $(rateStars[j]).addClass('fa-star');
    }
});

// Set rating
$(document.body).on('click','.rating-review .star-rate',function (e) {
    ratingSelected = true;
    $(e.target).addClass('fa-star');
    $(e.target).parent().addClass('rated');
    var selectedRating = parseInt($(e.target).parent().attr('data-selected-rate'));
    $(e.target).parent().attr('data-user-rate', selectedRating);
    var profile_id = $(e.target).parent().attr('data-profile');
    var company_id = $(e.target).parent().attr('data-company');
    var data_field = $(e.target).parent().attr('data-field');
    var data = {
        "profile_id":$('#current-owner').val()
    };
    data[data_field] = selectedRating;
    console.log(selectedRating, data);
    post_data('/rate/',data,rate_response);
});

function rate_response(response) {
    console.log(response);
    get_ratings();
}
function block_response(response) {
    console.log(response);
    get_blocks_count();
}

function get_ratings() {
    cid = $('#current-owner').val();
    get_data(`/get-rate/${cid}/`,render_ratings);
}

function get_blocks_count() {
    cid = $('#current-owner').val();
    get_data(`/get-blocks-count/${cid}/`,render_blocks_count);
}

function render_ratings(response) {
    console.log(response);
    $('.field-loc').html(response.rate_loc_html);
    $('.field-los').html(response.rate_los_html);
    $('.field-ri').html(response.rate_ri_html);
    $('.field-lofc').html(response.rate_lofc_html);
    $('.field-sop').html(response.rate_sop_html);
    $('.rated-loc').html(response.loc_starred);
    $('.rated-los').html(response.los_starred);
    $('.rated-ri').html(response.ri_starred);
    $('.rated-lofc').html(response.lofc_starred);
    $('.rated-sop').html(response.sop_starred);
    $('.rated-avg').html(response.avg_starred);
}

function render_blocks_count(response) {
    console.log(response);
    $('.nc_count').html(response.nc_count);
    $('.ds_count').html(response.ds_count);
    $('.ui_count').html(response.ui_count);
    $('.ff_count').html(response.ff_count);
    $('.np_count').html(response.np_count);
    $('.field-block-nc').html(response.nc_modal);
    $('.field-block-ds').html(response.ds_modal);
    $('.field-block-ui').html(response.ui_modal);
    $('.field-block-ff').html(response.ff_modal);
    $('.field-block-np').html(response.np_modal);
}

//Blocking
$(document.body).on('click','.block-user-btn', function (e) {
    let field = $(e.target).data('field');
    var data = {
        "profile_id":$('#current-owner').val(),
        "field": field
    };
    console.log(field);
    post_data('/block/',data,block_response);
    get_blocks_count()
})