const express = require('express');
const bodyParser = require('body-parser');
const studentRoutes = require('./routes/studentRoutes');

const app = express();

// Middleware
app.use(bodyParser.json());

// Routes
app.use('/api/students', studentRoutes);

module.exports = app;

