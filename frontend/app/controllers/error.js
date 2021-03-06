import Ember from "ember";

export default Ember.Controller.extend({  
  time: function() {
    var model = this.get('model');
    var time = model.get('time');
    return time.toLocaleTimeString();
  }.property('model.time')
});
