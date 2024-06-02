const express = require('express');
const bodyParser = require('body-parser');
const intentRoute = require('./routes/intent');
const nerRoute = require('./routes/ner');

const app = express();
const PORT = 5000;

app.use(bodyParser.json());

app.use('/api/intent', intentRoute);
app.use('/api/ner', nerRoute);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
