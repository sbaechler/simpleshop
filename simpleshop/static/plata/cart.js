$('.order-button').click(function(evt){
    var btn = $(this);
    // log ('adding:' + btn.data('action'));
    $.post(btn.data('action'),
            {'csrfmiddlewaretoken': btn.data('token'),
            'quantity': 1 },
            function(response){
                if (response == 'ok') {
                    window.location = btn.data('href');
                }
            }
    );
    return false;
});
$('#product-list').on('show hide', function(evt) {
    var icon = $(evt.target).prev('div').find('i.arrow');
    icon.toggleClass('icon-circle-arrow-down icon-circle-arrow-right');
});