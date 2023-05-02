document.addEventListener("DOMContentLoaded", function() {
  document.addEventListener("scroll", function() {
    document.cookie = "scroll_position=" + window.pageYOffset + "; path=/";
  });

  var scroll_position = parseInt(getCookie("scroll_position"));
  if (!isNaN(scroll_position)) {
    window.scrollTo(0, scroll_position);
  }

  function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
  }
});