$(document).ready(function() {
  $("#apply").click(function() {
    let name = window.location.pathname.substring(1);
    let tableType = "apply?type=" + name;
    $(location).attr("href", tableType);
  });
});

