$(document).ready(function() {
  $(".nav-link").click(function() {
    $(location).attr("href", this.text);
  });
});