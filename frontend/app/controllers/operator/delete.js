import Ember from "ember";

export default Ember.ObjectController.extend({
  actions: {
    remove: function () {
      var file = this.get('model');
      file.deleteRecord();
      file.save();
    },
    dismiss: function () {
      this.transitionToRoute('operator.index', this.get('model.stream'), this.get('model'));
    }
  }
});