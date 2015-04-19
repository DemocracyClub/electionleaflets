(function () {
  'use strict';

    Leaflets.AddLeafletController = Ember.ArrayController.extend({
      actions: {
        AddImage: function(element) {
          var store = this.store;
          var leaflet = store.find('leaflet', 'new');
          var f = $(element).find('#image_front')[0].files[0];
          var fr = new FileReader();
          fr.onload = receivedText;
          fr.readAsDataURL(f);
          function receivedText() {
            var image = new Image();
            image.src = this.result;
            store.createRecord('LeafletImage', {
              'leaflet': leaflet,
              'image': this.result
            });
          }
        }
      }


    });
    
})();