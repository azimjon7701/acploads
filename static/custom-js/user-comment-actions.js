var current_chat_owner = null;

function open_comment_modal(owner_id) {
    $('#user-model').css('display', 'block');
    $('#current-owner').val(owner_id);
    get_data(`/get-current-customer-info/${owner_id}/`, render_current_owner);
    update_comment_chat();
    $('.chat-body').animate({scrollTop: 10000000000000}, 500);

    get_ratings();
    get_blocks_count()

}

$('.close-user-modal').click(function () {
    $('#user-model').css('display', 'none');
})

$('#submit-comment-button').click(function (event) {
    event.preventDefault();
    let new_message = $('#message-textbox').val();
    let current_owner = $('#current-owner').val();
    if (new_message == '' || !current_owner) {
        return;
    }
    post_data('/comment-post/', data = {
        'new_message': new_message,
        'current_owner': current_owner
    }, render_new_message);
    $('.chat-body').animate({scrollTop: 10000000000000}, 500);
})

function render_new_message(data) {
    let messages = $('.chat-body').html();
    messages += data.new_message;
    $('.chat-body').html(messages);
    $('#message-textbox').val("");
}

function render_messages(data) {
    $('.chat-body').html(data.comments);
}

function update_comment_chat() {
    let current_owner = $('#current-owner').val();
    if (current_owner) {
        get_data(`/comment-get/${current_owner}`, render_messages);
    }
}

function render_current_owner(data) {
    console.log(data.customer_info);
    $('#user-info-div').html(data.customer_info);
}

window.setInterval(() => {
    update_comment_chat();
}, 10000);
