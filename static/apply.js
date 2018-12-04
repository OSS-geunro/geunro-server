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
    var formData = $("#apply").serialize();
    userType = "&type=" + param.type;
    fullData = formData.concat(userType);
    console.log(fullData)
    $.ajax({
      type: "POST",
      url: "/apply",
      data: fullData,
      dataType: "text",
      success: onSuccess,
      error: onError
    });
  });
});

function onSuccess() {
  // $(location).attr('href', 'student');
}
function onError(xhr) {
  if (xhr.status == 409) $("#warning").show();
  else if (xhr.status == 401) $("#danger").show();
}
