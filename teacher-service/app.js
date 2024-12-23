import express from 'express';
import teacherRoutes from './src/routes/teacherRoutes.js';
import pkg from 'body-parser';


const app = express();
const { json } = pkg;


app.use(json());
app.use('/api/teachers', teacherRoutes);

export default app;
