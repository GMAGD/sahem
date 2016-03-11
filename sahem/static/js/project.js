/* Project specific Javascript goes here. */

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('#remove-event-modal').on('shown.bs.modal', function () {
    $('#remove-event-button').focus()
});

// Create Event
$(document).ready(function () {

    $('#create-event-btn').click(createEvent)

});

function createEvent() {


    $name = $('#id_name').val();
    $category = $('#id_category').val();
    $description = $('#id_description').val();
    $start = $("#id_start").val();
    $end = $("#id_end").val();
    $lattitude = $("#id_position_0").val();
    $longitude = $("#id_position_1").val();

    $.post('/events/create/',
        {
            name: $name,
            category: $category,
            description: $description,
            start: $start,
            end: $end,
            position_0: $lattitude,
            position_1: $longitude
        },
        function (data, status) {
            console.log(data);
            console.log(status);

            $("#create-form").html(data);

        });
}


$(document).ready(function () {
    $('.collapsible').collapsible({
        accordion: false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
    });
});

$(document).ready(function () {
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    $('.modal-trigger').leanModal();
});
