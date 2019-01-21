$(document).ready(function() {

    var store_name = '#store-name'
    var base_url = 'http://localhost:8081'
    var logs_box = '#logs-container > ul'
    var update_list = '#update-list'

    $.get(base_url + '/init-store-list', function(data, status) {
        $(update_list).append(data)

        $('#sidebar > #search-list > #update-list > li').click(function() {

            $(store_name).text($(this).text())
    
            $.get(base_url + '/data-request:' + $(this).attr('data-id'), function(data, status) {
                $(logs_box).empty()
                $(logs_box).append(data)
            })
            
        })
    })
    
})