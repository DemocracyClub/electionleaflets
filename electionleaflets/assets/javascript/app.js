(function () {

  $('.file_input_button').change(function() {
    var el = $(this);
    var file = el.find('input')[0].files[0];
    var fr = new FileReader();
    fr.onload = receivedImage;
    fr.readAsDataURL(file);
    function receivedImage() {
      $('.upload-prompt').hide();
      $('.replace').show();
      $('.file_input_preview *').remove();
      el.find('.action').text('change')
      var img = $('<img class="uploaded_image">');
      img.attr('src', this.result);
      $('.file_input_preview').append(img);
    }
  })

  //alerts
  $('.alert-box').delay(4000).slideUp();
})();
