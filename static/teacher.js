$(document).ready(function() {
  $("#create").click(function() {
    let name = window.location.pathname.substring(1);
    let tableType = "create?type=" + name;
    $(location).attr("href", tableType);
  });
});

