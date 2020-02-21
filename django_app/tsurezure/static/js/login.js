$(function() {
    $('#login-buttton').click(login);
});

function login() {
    let $loginForm = $('#login-form');

    let next = getNext();

    if (next != null) {
        let $input = $('<input>').attr({
            type: 'hidden',
            name: 'next',
            value: getNext(),
            id: 'id_next',
        });
        $input.appendTo($loginForm);
    }

    $loginForm.submit();
}

function getNext() {
    let argument  = new Object;
    splitUrlList = location.search.substring(1).split('&');

    for(let splitUrl of splitUrlList) {
        let value = splitUrl.split('=');
        argument[value[0]] = value[1];
    }

    return argument.next;
}