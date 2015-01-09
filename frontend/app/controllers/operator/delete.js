import OperatorController from 'stromx-web/controllers/operator';

export default OperatorController.extend({
  actions: {
    dismiss: function () {
      this.transitionToRoute('stream.index', this.get('model.stream'));
    },
    remove: function() {
      var _this = this;
      this.removeConnections().then(function() {
        var model = _this.get('model');
        model.deleteRecord();
        model.save();
      });
    }
  }
});
