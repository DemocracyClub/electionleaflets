(function () {
  
  if(jQuery().Jcrop) {
    $('body.cropper figure img').Jcrop({
      boxWidth: 800,
      boxHeight: 600,
      bgColor:'black',
      bgOpacity: 0.8,
      onSelect: function(e) {
        $('input[name=x]').val(parseInt(e.x));
        $('input[name=y]').val(parseInt(e.y));
        $('input[name=x2]').val(parseInt(e.x2));
        $('input[name=y2]').val(parseInt(e.y2));
      }
    })
  }
  
})();