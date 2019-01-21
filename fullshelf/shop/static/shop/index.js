$(document).ready(function() {

    //var show_watchlist = false;

    //$("#watchlist" ).not( ":visible" )

    $("#bottom-nav div").hover(
        function() {
            $(this).find('#submenu').show()
            $(this).find('#submenu').css('visibility', 'visible')
            $(this).find("#nav-header").addClass("hovered");
        }, function() {
            $(this).find('#submenu').hide()
            $(this).find('#submenu').css('visibility', 'hidden')
            $(this).find("#nav-header").removeClass("hovered");
        }
    )

    $("#tools").hover(
        function() {
            $(this).find('#watchlist').css('height','0').show()
            $(this).find('#watchlist').animate({
                height: '80%'
            }, 300)

            $('#screen').css('z-index','1')
            $('#screen').animate({
                opacity: '0.3',
            }, 300)

        }, function() {
            $(this).find('#watchlist').animate({
                height: '0%'
            }, 300, function() {
                $(this).hide()
            })
            
            $('#screen').animate({
                opacity: '0.0',
            }, 300, function() {
                $('#screen').css('z-index','-10')
            })
            
        }
    )


 });