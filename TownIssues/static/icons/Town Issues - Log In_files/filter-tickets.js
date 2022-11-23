$(document).ready(function() {
    $('.table-filter').on("input", function () {
        $('.table-filter').each(function (){
            let filterDate;
            let currentFilter = this.id;
            let filter = $(this).val().toLowerCase();
            $('#tickets > tbody > tr').each(function(){
                let date = new Date($(this).children('td').eq(2).text().split(" ")[0]);
                switch (currentFilter) {
                    case 'namefilter':
                        if ($(this).children('td').eq(0).text().toLowerCase().indexOf(filter) >= 0 && $(this).hasClass('nameFilterHidden')){
                            $(this).removeClass('nameFilterHidden');
                        } else if ($(this).children('td').eq(0).text().toLowerCase().indexOf(filter) < 0) {
                            $(this).hide();
                            $(this).addClass('nameFilterHidden');
                        }
                        break;
                    case 'authorfilter':
                        if ($(this).children('td').eq(1).text().toLowerCase().indexOf(filter) >= 0 && $(this).hasClass('authorFilterHidden')){
                            $(this).removeClass('authorFilterHidden');
                        } else if ($(this).children('td').eq(1).text().toLowerCase().indexOf(filter) < 0) {
                            $(this).hide();
                            $(this).addClass('authorFilterHidden');
                        }
                        break;
                    case 'datefilterfrom':
                        filterDate = new Date(filter);
                        if ((date >= filterDate && $(this).hasClass('dateFromFilterHidden')) || filter === '') {
                            $(this).removeClass('dateFromFilterHidden');
                        }
                        else if (date < filterDate) {
                            $(this).hide();
                            $(this).addClass('dateFromFilterHidden');
                        }
                        break;
                    case 'datefilterto':
                        filterDate = new Date(filter);
                        if ((date <= filterDate && $(this).hasClass('dateToFilterHidden')) || filter === ''){
                            $(this).removeClass('dateToFilterHidden');
                        }
                        else if (date > filterDate) {
                            $(this).hide();
                            $(this).addClass('dateToFilterHidden');
                        }
                        break;
                    case 'statefilter':
                        filter = $('#statefilter option:selected').text().toLowerCase();
                        if (($(this).children('td').eq(3).text().toLowerCase().indexOf(filter) >= 0
                                && $(this).hasClass('stateFilterHidden')) || filter === 'select one'){
                            $(this).removeClass('stateFilterHidden');
                        } else if ($(this).children('td').eq(3).text().toLowerCase().indexOf(filter) < 0) {
                            $(this).hide();
                            $(this).addClass('stateFilterHidden');
                        }
                        break;
                }
                if ($(this)[0].classList.length === 0){
                    $(this).show();
                }
            })
        })
    });
});