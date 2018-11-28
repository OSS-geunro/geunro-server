$(document).ready(function() {
  $(".btn").click(function() {
    $(location).attr('href', 'login?type='+$(this).val());
  });
});
