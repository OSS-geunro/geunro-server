$(document).ready(function() {
  $("#submit").click(function() {
    $(".alert").hide();
    var formData = $("#login").serialize();
    $.ajax({
      type: "POST",
      url: "/login",
      data: formData,
      dataType: "text",
      success: onSuccess,
      error: onError
    });
  });
});

function onSuccess() {
  $(location).attr('href', 'login');
}
function onError(xhr) {
  if (xhr.status == 409) $("#warning").show();
  else if (xhr.status == 401) $("#danger").show();
}
