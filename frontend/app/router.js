import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function () {
  this.resource('files', { path: '/'}, function() {
    this.route('upload');
    this.route('new');
    this.resource('file', { path: 'files/:file_id' }, function() {
      this.route('delete');
    });
  });
  this.resource('streams', function() {
    this.resource('stream', { path: '/:stream_id' }, function() {
      this.route('newThread');
      this.route('newView');
      this.resource('operators', function() {
        this.resource('operator', { path: '/:operator_id' }, function() {
          this.route('delete');
        });
        this.route('new');
      });
      this.resource('threads', function() {
        this.resource('thread', { path: '/:thread_id' }, function() {
          this.route('delete');
        });
        this.route('new');
      });
    });
  });
  this.resource('views', function() {
    this.resource('view', { path: '/:view_id' }, function() {
      this.route('newObserver');
    });
  });
});


export default Router;
