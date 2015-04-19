(function () {
  'use strict';

  Leaflets.AddImageComponent = Ember.Component.extend({
    click: function() {
      this.sendAction('action', this.element);
    }
  });

})();