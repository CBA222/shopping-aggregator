$(document).ready(function() {

    var cheaper_button = '#buy-box #cheaper button'
    var cheaper_options = '#cheaper-options-wrapper'

    $(cheaper_button).click(function() {
        if ($(cheaper_options).is(':visible')) {
            $(this).text('Show Cheaper Options')
            $(cheaper_options).animate({
                height: '0'
            }, 250, function() {
                $(this).hide()
                $('#other-stores #two-p').show(150)
                $('#other-stores #one-p').show(150)
                $('#other-stores tr:nth-child(n+3)').show()
            })
            
        } else {
            $(this).text('Hide Cheaper Options')
            $(cheaper_options).css('height','0').show()
            $(cheaper_options).animate({
                height: '170px'
            }, 250)
            $(cheaper_options).animate({
                height: '150px'
            }, 150)
            
            $('#other-stores p').hide(150)
            $('#other-stores tr:nth-child(n+3)').hide()
        }
        
    })
});