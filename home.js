$(document).ready(function() {
    $('form').submit(function(event) {
        event.preventDefault();
        var formData = new FormData($('form')[0]);

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#result').text(response.result);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
