$(document).ready(function() {
    $('.user-filter').on("input", function () {
        $('.user-filter').each(function (){
            let filter = $(this).val().toLowerCase();
            let currentFilter = this.id;
            $('#users > tbody > tr').each(function(){
                if (currentFilter === 'userfilter') {
                    if ($(this).children('td').eq(0).text().toLowerCase().indexOf(filter) >= 0 && $(this).hasClass('userFilterHidden')) {
                        $(this).removeClass('userFilterHidden');
                    } else if ($(this).children('td').eq(0).text().toLowerCase().indexOf(filter) < 0) {
                        $(this).hide();
                        $(this).addClass('userFilterHidden');
                    }
                } else{
                    filter = $('#rolefilter option:selected').text().toLowerCase();
                    if (($(this).children('td').eq(1).text().toLowerCase().indexOf(filter) >= 0
                        && $(this).hasClass('roleFilterHidden')) || filter === 'select one'){
                        $(this).removeClass('roleFilterHidden');
                    } else if ($(this).children('td').eq(1).text().toLowerCase().indexOf(filter) < 0) {
                        $(this).hide();
                        $(this).addClass('roleFilterHidden');
                    }
                }
                if ($(this)[0].classList.length === 0){
                    $(this).show();
                }
            })
        })
    });
});