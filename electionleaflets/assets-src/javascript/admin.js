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



  // Leaflet image mark up tools


  // Move the panel from one side to the other
  $("#opflip").click(function() {
      $("#formpanel").hide();
      if ($("#annotspanel").css("right") == "0px")
          $("#annotspanel").css("right", "auto").css("left", "0px");
      else
          $("#annotspanel").css("left", "auto").css("right", "0px");
  });

  function removeselection() {
      $("#annotspanel li").removeClass("added");
      $("#annotspanel li").removeClass("selected");
      $("textarea#annotdesc").val("");
      annotboxselectedindex = -1;
  };

  function populateannots() {
      var jdesctext = $("div#formpanel #id_description").val().trim();
      var lannotboxlist = [ ];
      try {
          lannotboxlist = $.evalJSON(jdesctext);
      } catch(err) {
          if (jdesctext.length > 0) {
              lannotboxlist.push({ "optype":"Content", "page":1, "px":100, "px2":900, "py":100, "py2":200, "description":jdesctext });
          }
      }
      for (var i = 0; i < lannotboxlist.length; i++)
          commitbox(lannotboxlist[i], jcrop_apilist[lannotboxlist[i].page].getBounds());
  }


  var jcrop_apilist = { };
  var annotboxlist = [ ];
  var annotboxselectedindex = -1;
  var nimages = $('figure[id^="image-"]').length;
  var npagesnotcropmasked = nimages;

  $('#editor figure[id^="image-"]').each(function() {
    var crop_image = $(this);
    var image_id = crop_image.attr('id');
    crop_image.Jcrop({
            bgColor:'black',
            bgOpacity: 0.9,
            onSelect: removeselection,
            onRelease: removeselection,
            keySupport: true,
            onChange: function(e) {
                if ((annotboxselectedindex != -1) && (annotboxlist[annotboxselectedindex].page != image_id))
                    removeselection();
            },
            onKeypress: function(e) {
                if (e.keyCode == 46)  deletebox();
                if (e.keyCode == 80)  focussavebox("Party");     // p
                if (e.keyCode == 67)  focussavebox("Candidate"); // c
                if (e.keyCode == 69)  focussavebox("Election");  // e
                if (e.keyCode == 68)  focussavebox("District");  // d
                if (e.keyCode == 73)  focussavebox("Imprint");   // i
                if (e.keyCode == 13)  focussavebox("Content");   // <return>
                if (e.keyCode == 33)  $('html,body').animate({scrollTop:$(window).scrollTop() - 500}, 200);  // pageup
                if (e.keyCode == 34)  $('html,body').animate({scrollTop:$(window).scrollTop() + 500}, 200);  // pagedown
            }
        }, function() {

          jcrop_apilist[image_id] = this;
          jcrop_apilist[image_id].image_id = image_id;
          // set a class name on the cropper system so we can find it
          jcrop_apilist[image_id].setClass(image_id);

          // make the annotation holder with the non-selected boxes
          var compeleximgstyle = $($("#"+image_id+" img")[1]).attr("style");
          $("#"+image_id).append('<div id="annots'+image_id+'" style="'+image_id+'"></div>');

          npagesnotcropmasked--;
          if (npagesnotcropmasked == 0) {
                populateannots();
          }
    });
  })













})();