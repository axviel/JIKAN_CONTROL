$(document).ready(function () {
  $('#dismiss, .overlay').on('click', function () {
      $('#sidebar').removeClass('active');
      $('.overlay').removeClass('active');
  });

  $('#sidebar-collapse').on('click', function () {
      $('#sidebar').addClass('active');
      $('.overlay').addClass('active');
  });
});