(function () {
  
  Leaflets.AddLeafletRoute = Ember.Route.extend({
    model: function() {
      var store = this.store;
      // return this.store.find('LeafletImage');
      this.new_leaflet = store.createRecord('Leaflet', {id: 'new'});
      return this.new_leaflet
    },
    setupController: function(controller, leaflet) {
      controller.set('model', this.new_leaflet.get('LeafletImage'));
    }
  });
  
  Leaflets.Router.map(function() {
    this.route("add_leaflet", { 
      path: "/",
    });
  });
  
  Leaflets.Router.reopen({
    rootURL: '/leaflets/add/',
    location: 'history'
  });


})();