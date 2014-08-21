/* global App */

App.Connector = DS.Model.extend({
  title: DS.attr('string'),
  connectorType: DS.attr('string'),
  operator: DS.belongsTo('operator', {async: true})
});

App.Connector.FIXTURES = [
  {
    id: 1,
    title: 'Input image',
    connectorType: 'input',
    operator: 2
  },
  {
    id: 2,
    title: 'Number',
    connectorType: 'input',
    operator: 1
  },
  {
    id: 3,
    title: 'Destination image',
    connectorType: 'input',
    operator: 2
  },
  {
    id: 4,
    title: 'Output image',
    connectorType: 'output',
    operator: 2
  },
  {
    id: 5,
    title: 'Generated number',
    connectorType: 'output',
    operator: 0
  },
  {
    id: 6,
    title: 'Received image',
    connectorType: 'output',
    operator: 3
  }
];