$(document).ready(function() {
  $("#submit").click(function() {
   var formData = $("#login").serialize();
   $.ajax({
    type : "POST",
    url : '/login',
    data : formData,
    success : onSuccess,
    error : onError
   });
  });
 });
 
 function onSuccess(json, status){
  // alert($.trim(json));
 }
 function onError(data, status){
  // alert("error");
 }