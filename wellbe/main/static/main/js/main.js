$(function() {
    let header = $('.header'),
        pageOffset = $('.page').last().offset();
    $(window).scroll(function() {
        if($(this).scrollTop() !== 0) {
            header.addClass('header_fixed');
            $('.page').css({
               'paddingTop': pageOffset.top + 'px'
            });
        } else {
            header.removeClass('header_fixed');
            $('.page').css({
             'paddingTop': 0
            })
        }
    });
});

function copyText(element) {
    let $tmp = $("<textarea>");
    $("body").append($tmp);
    $tmp.val(element.value).select();
    document.execCommand("copy");
    $tmp.remove();
    let tooltip = document.getElementById(id);
    tooltip.textContent = 'Скопировано!';
}

function checkButton() {
    let searchField = $('#searchField').val();
    if (searchField.length > 0) {
        $('#searchButton').removeAttr('disabled');
    } else {
        $('#searchButton').attr('disabled', 'disabled');
    }
}
