$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading"); },
    ajaxStop: function() { $body.removeClass("loading"); },
});

achilles.onError(function(error, message, trace) {
    alert(message);
    console.log(trace);
});
