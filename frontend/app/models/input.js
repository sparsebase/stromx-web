import DS from "ember-data";

export default DS.Model.extend({
  title: DS.attr('string'),
  variant: DS.attr(),
  operator: DS.belongsTo('operator', {async: true}),
  connection: DS.belongsTo('connection', {async: true}),
  observers: DS.hasMany('input-observer', {async: true})
});
