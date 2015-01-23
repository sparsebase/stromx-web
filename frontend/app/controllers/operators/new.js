import Ember from "ember";

export default Ember.Controller.extend({
  selectedOperator: null,
  selectedPackage: null,
  packages: function(key, value) {
    if (value !== undefined) {
      return value;
    }
    
    var _this = this;
    this.store.find('operatorTemplate').then(function(templates) {
      var packageNames = new Set(templates.mapBy('package'));
      var packages = [];
      for (var p of packageNames.values()){
        var operators = templates.filterBy('package', p);
        packages.push({
          name: p,
          operators: operators.sortBy('type')
        });
      }
      packages = packages.sortBy('package');
      _this.set('packages', packages);
    });
    
    return [];
  }.property(),
  saveIsDisabled: Ember.computed.equal('selectedOperator', null),
  name: '',
  actions: {
    save: function () {
      var stream = this.get('model');
      var op = this.store.createRecord('operator', {
        name: this.get('name'),
        package: this.get('selectedOperator.package'),
        type: this.get('selectedOperator.type'),
        stream: stream,
        status: 'none',
        position: {
          x: 0,
          y: 0
        }
      });
      
      var _this = this;
      op.save().then(function(op) {
        _this.transitionToRoute('operator', op);
      });
    }
  }
});
