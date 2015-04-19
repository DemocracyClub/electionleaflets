/*global App, DS */
(function () {
  'use strict';
  var attr = DS.attr;
  Leaflets.Leaflet = DS.Model.extend({
    postcode: attr(),
    images: DS.hasMany('LeafletImage')
  });
  
  Leaflets.LeafletImage = DS.Model.extend({
    leaflet: DS.belongsTo('Leaflet'),
    name: attr(),
    image: attr()
  });
  
  
})();