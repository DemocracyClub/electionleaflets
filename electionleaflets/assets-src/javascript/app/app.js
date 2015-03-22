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

  // Maps
  window.create_leaflet_map = function(point, constituency_id) {
    var map = L.map('leaflet_map', {zoomControl:false});
    map.dragging.disable();
    map.touchZoom.disable();
    map.doubleClickZoom.disable();
    map.scrollWheelZoom.disable();

    var Stamen_TonerLite = L.tileLayer('http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png', {
    	attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    	subdomains: 'abcd',
    }).addTo(map);


    var ConstituencyStyles = {
        "color": "#99CCFF",
        "fillColor": "#99CCFF",
        "weight": 1,
        "fillOpacity": 0.7
    };

    window.map = map;
    window.ConstituencyStyles = ConstituencyStyles;


    var constituency = new L.geoJson();
    constituency.addTo(map);
    L.marker(point, {
        'icon': L.divIcon({className: 'leaflet_location_icon'}),
        'clickable': false,

    }).addTo(map);

    $.ajax({
    dataType: "jsonp",
    url: "https://mapit.mysociety.org/area/"+constituency_id+".geojson",
    success: function(data) {
        constituency.addData(data,{style: ConstituencyStyles});
        constituency.setStyle(function() {return ConstituencyStyles});
        map.fitBounds(constituency.getBounds());
        map.zoomOut();
    }
    }).error(function() {});


    //add div over the top so scrolling works on a touch device
    cover = $('<div></div>');
    cover.css({"position":"absolute", "top": 0, "bottom": 0, "left": 0, "right":0})
    $('#leaflet_map').parent().css({"position": "relative"})
    $('#leaflet_map').parent().append(cover)


  }



})();