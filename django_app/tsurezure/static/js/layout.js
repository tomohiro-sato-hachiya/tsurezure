$(function() {
    let $messages =  $('#message-area').children();
    $messages.each(function() {
        setClass($(this));
    });
});

function setClass(message) {
    if (message.hasClass('success')) {
        message.addClass('alert-success');
    }
    if (message.hasClass('error')) {
        message.addClass('alert-danger');
    }
}