import Ember from "ember";

export default Ember.Component.extend({
  model: null,
  isEditingColor: false,
  isEditingVisualization: false,

  visualizations: [
    {label: 'Default', value: 'default'},
    {label: 'Image', value: 'image'},
    {label: 'Line segments', value: 'line_segments'},
    {label: 'Slider', value: 'slider'},
    {label: 'Points', value: 'points'},
    {label: 'Polygon', value: 'polygon'},
    {label: 'Polyline', value: 'polyline'}
  ],

  // FIXME: For some reason it is not possible to directly bind to the property
  // 'view' in templates. As a workaround the renamed property below is used.
  observerView: Ember.computed.alias('model.view'),

  // FIXME: Model rollback does not work if the color selector is bound to
  // 'properties.color'. Instead we use proxy property below and copy the value
  // 'properties.color' in saveChanges().
  color: '#000000',

  visualizationLabel: function() {
    var visualization = this.get('model.visualization');

    var array = Ember.ArrayProxy.create({content: this.visualizations});
    var record = array.findBy('value', visualization);
    return record ? record['label'] : '';
  }.property('model.visualization'),

  value: function(key, value) {
    if (value === undefined) {
      var _this = this;
      var valuePromise = this.get('model.value');
      if (! valuePromise) {
        return null;
      }

      valuePromise.then(function(value) {
        _this.set('value', value);
      });

      return null;
    } else {
      return value;
    }
  }.property('model.value'),

  actions: {
    editColor: function() {
      this.set('color', this.get('model.properties.color'));
      this.set('isEditingColor', true);
    },
    setColor: function(color) {
      this.set('color', color);
    },
    editVisualization: function() {
      this.set('color', this.get('model.properties.color'));
      this.set('isEditingVisualization', true);
    },
    saveChanges: function() {
      this.set('isEditingColor', false);
      this.set('isEditingVisualization', false);

      this.set('model.properties.color', this.get('color'));
      this.get('model').save();
    },
    discardChanges: function() {
      this.set('isEditingColor', false);
      this.set('isEditingVisualization', false);
      this.get('model').rollback();
    }
  }
});
