const cassandra = require('cassandra-driver');

const client = new cassandra.Client({
  contactPoints: ['localhost:9042'],
  localDataCenter: 'Mars',
  keyspace: 'ramayana'
});

const query = 'select * from characters';

client.execute(query)
  .then(result => {
    // Access the columns based on their names in the result.rows array
    console.log('Character with id %s, name %s, and description %s', 
      result.rows[0].id, result.rows[0].name, result.rows[0].description);
  })
  .catch(error => console.error('Error executing query:', error))
  .finally(() => client.shutdown());