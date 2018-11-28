function getUrlParams() {
  var params = {};
  window.location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(
    str, key, value
  ) {
    params[key] = value;
  });
  return params;
}

$(document).ready(function() {
  $("#submit").click(function() {
    $(".alert").hide();
    param = getUrlParams();
    var formData = $("#login").serialize();
    userType = "&type=" + param.type;
    fullData = formData.concat(userType);
    $.ajax({
      type: "POST",
      url: "/login",
      data: fullData,
      dataType: "text",
      success: onSuccess,
      error: onError
    });
  });
});

function onSuccess() {
  $(location).attr("href", "login");
}
function onError(xhr) {
  if (xhr.status == 409) $("#warning").show();
  else if (xhr.status == 401) $("#danger").show();
}
