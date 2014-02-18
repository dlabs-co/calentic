function get_calendar() {
    $('#calendar_1').calendar({
        events_url:'/events/all',
        'tmpl_path':'/static/bootstrap-calendar/tmpls/',
        'onAfterEventsLoad' : function(){
        window.setTimeout(function(){
            jQuery('a[href^="/event/"]').each(function(){
                do_hack_links(this);
            });
            }, 1000);
        }
    });
}

function do_hack_links(that){
    if ($(this).attr('data-href') != "#") { $(that).attr('data-href', $(that).attr('href')); $(that).attr('href', '#'); }
    $(that).click(function(){ var href=$(that).attr('data-href'); $('.modal-body').load(href, function(result){ $('#event').modal({show:true});}); return false; } );
}

function get_soon_calendar() {
    a = new Date();
    $.get(
        '/events/'+ "start_date="+ new Date().getTime() + "/end_date=" + new Date(a.getFullYear(), a.getMonth() +1, 1).getTime(),
        function(data){
            data=JSON.parse(data);
            $(data.events).each(function(){
                console.log(this);
                $('#events_top').append(
                    "<div class=col-md-3>"+
                    "<span class=date>" + new Date(this.start).toString("dd/MM/yy HH:mm") +  "</span>" +
                    "<h4>" + this.title + "</h4>" +
                    "</div>" );
            });
            $('#events_top').append("<div class=col-md-3><h3 class=addnew><a href='/create_event'>Añadir un evento </a></h3></div>");
        }
    );
}

function get_monthly_calendar() {
    a = new Date();
    $.get(
        '/events/'+ "start_date="+ new Date(a.getFullYear(), a.getMonth(), 1).getTime() + "/end_date=" + new Date(a.getFullYear(), a.getMonth() +1, 1).getTime(),
        function(data){
            data=JSON.parse(data);
            $(data.events).each(function(){
                $('#events_monthly').append("<li>" + this.title + "</li>" );
            });
        }
    );
}

function main() {
    get_monthly_calendar();
    get_soon_calendar();
    get_calendar();
}

var _gaq=[['_setAccount','UA-XXXXX-X'],['_trackPageview']];
(function(d,t){var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
g.src=('https:'==location.protocol?'//ssl':'//www')+'.google-analytics.com/ga.js';
s.parentNode.insertBefore(g,s)}(document,'script'));
