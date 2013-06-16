Date.prototype.addDays = function(days){
    var dat = new Date(this.valueOf())
    dat.setDate(dat.getDate() + days);
    return dat;
}

Date.prototype.getMonthName = function(lang) {
    lang = lang && (lang in Date.locale) ? lang : 'en';
    return Date.locale[lang].month_names[this.getMonth()];
};

Date.locale = {
     en: { month_names: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']},
     es: { month_names: ['Enero', 'Febero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septimbre', 'Octubre', 'Noviembre', 'Diciembre']}
};
    
(function($) {  
    $.fn.simpleHtml5Calendar = function(options) {  
           var params = $.extend({}, $.fn.simpleHtml5Calendar.defaults, options);
           function create_month(date_start, date_end, day_contents, month){ 
                result = "<div style='display:none' class='month' id='month_" + date_start.getMonth() + "'>"
                result += "<h1>"+ date_start.getMonthName(params['lang']) +"</h1>";
                while (date_start.getTime() < date_end.getTime()) { 
                    date_start = date_start.addDays(1); content=date_start.getDate(); 
                    if (day_contents && day_contents[0]){
                        if (day_contents[0][date_start.getDate()]){ 
                            content=day_contents[0][date_start.getDate()];
                        } else { 
                            content=date_start.getDate(); 
                        }
                    }

                    result += "<time datetime='" + date_start.toJSON() + "'>" + content + "</time>"; 
                }
                return result;
           }

           this.each(function() {
                $(this).data('month', params['show_month']); 
                for (number=0;number<=11;number++){ 
                        var date_start = new Date(); date_start.setYear(params['year']); date_start.setMonth(number); date_start.setDate(0); 
                        var date_end = new Date(); date_end.setYear(params['year']); date_end.setMonth(number + 1); date_end.setDate(0); 
                        if (params['day_contents'][0]){ month_contents=params['day_contents'][0][number]} else { month_contents=Array(); }
                       $(this).append( create_month( date_start, date_end, month_contents, params['show_month']) ); 
                 }
                $(this).children('#month_' + params['show_month']).css('display', 'block');
            });  
            return this;  
    };  
    $.fn.simpleHtml5Calendar.defaults = {day_contents: new Array(), lang: "en", show_month: 0, year: 2012 }
})(jQuery);  
    
(function($) {  
    $.fn.updateCalendar = function(increase) {  
            function update_month(elem, increase){
                var elem = $(elem).parent().parent().parent(); 
                if (increase){
                    if (elem.data('month') > 0){ 
                        var new_month = elem.data('month') - 1;
                    }
                } else {
                    if (elem.data('month') < 11){ 
                        var new_month = elem.data('month') + 1;
                    }
                }
                elem.children('#month_' + elem.data('month')).hide(); 
                elem.data('month', new_month);
                elem.children('#month_' + elem.data('month')).show(); 
            }
           return update_month(this, increase);  
    };  
})(jQuery);
