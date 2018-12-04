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
  let id = decodeURI(window.location.pathname.substring(1));
  if (id === '일반근로'){
    $('#general').addClass('selected');
  } else if (id === 'Helper'){
    $('#helper').addClass('selected');
  } else if (id === '국가근로'){
    $('#national').addClass('selected');
  } else {
      id=decodeURI(getUrlParams().type)
      if (id === '일반근로'){
        $('#general').addClass('selected');
      } else if (id === 'Helper'){
        $('#helper').addClass('selected');
      } else if (id === '국가근로'){
        $('#national').addClass('selected');
      }
  };
  $(".nav-link").click(function() {
    $(location).attr("href", this.text);
  });
});