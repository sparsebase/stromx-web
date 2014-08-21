/* global App */

App.ViewController = Ember.ObjectController.extend({
  parameterObservers: Ember.computed.alias('observers'),

  connectorObservers: Ember.computed.filter('observers', function(observer) {
    return observer instanceof App.ConnectorObserver;
  }),

  observerSorting: ['zvalue:desc'],

  sortedObservers: Ember.computed.sort('observers', 'observerSorting'),

  isEditingName: false,

  actions: {
    saveName: function() {
      var model = this.get('model');
      model.save();
      this.set('isEditingName', false);
    },

    rename: function() {
      this.set('isEditingName', true);
    },

    remove: function () {
        var view = this.get('model');
        view.deleteRecord();
        view.save();
    }
  }
});