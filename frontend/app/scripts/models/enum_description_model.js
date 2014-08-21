/* global App */

App.EnumDescription = DS.Model.extend({
  value: DS.attr('number'),
  title: DS.attr('string')
});

App.EnumDescription.FIXTURES = [
  {
    id: 0,
    value: 0,
    title: 'Manual'
  },
  {
    id: 1,
    value: 1,
    title: 'Allocate'
  },
  {
    id: 2,
    value: 2,
    title: 'In place'
  },
  {
    id: 3,
    value: 2,
    title: 'Square'
  },
  {
    id: 4,
    value: 3,
    title: 'Circle'
  },
  {
    id: 5,
    value: 7,
    title: 'Gaussian'
  }
];