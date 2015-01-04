import Ember from "ember";

export default Ember.ObjectController.extend({
  actions: {
    remove: function () {
      var file = this.get('model');
      file.deleteRecord();
      file.save();
    },
    dismiss: function () {
      this.transitionToRoute('stream.index', this.get('model.stream'));
    }
  }
});
