import express from 'express';
// import { json } from 'body-parser';
import studentRoutes from './src/routes/studentRoutes.js';
import pkg from 'body-parser';
const app = express();

const { json } = pkg;
// Middleware
app.use(json());

// Routes
app.use('/api/students', studentRoutes);

export default app;

