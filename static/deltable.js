$("#del").click(function() {
  let id = decodeURI(window.location.pathname.substring(1));
  $.ajax({
    url: "api/work/delete",
    type: "post",
    data: {
      worktable: id
    },
    success: function(xhr) {
      
      $(location).attr("href", id);
    },
    error: function(xhr) {
      $(location).attr("href", id);
    }
  });
});