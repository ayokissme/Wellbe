$(function () {
    let header = $('.header'),
        pageOffset = $('.page').last().offset();
    $(window).scroll(function () {
        if ($(this).scrollTop() !== 0) {
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

    const $categoryCards = $("[data-category]");
    const $inputCategory = $(".cardCheckBox");
    $inputCategory.on("change", function () {
        const checkedArr = $inputCategory.filter(":checked").get().map(el => el.value);
        if (!checkedArr.length) return $categoryCards.removeClass("hidden");
        $categoryCards.each(function () {
            const cardCategory = $(this).data("category");
            let categorySplit = cardCategory.split('|')
            $(this).toggleClass("hidden", !categorySplit.some(r => checkedArr.includes(r)));
        });

    });

    const $brandCards = $("[data-brand]");
    const $inputBrand = $(".cardCheckBox2");
    $inputBrand.on("change", function () {
        const checkedArrBrand = $inputBrand.filter(":checked").get().map(el => el.value);
        if (!checkedArrBrand.length) return $brandCards.removeClass("hidden");

        $(this).toggleClass("hidden", !$inputBrand.includes(checkedArrBrand));

        // $brandCards.each(function () {
        //     const cardCategory = $(this).data("category");
        //     let brandSplit = cardCategory.split('|')
        // });

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