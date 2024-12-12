import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import connectDB from './config/db.js';
import students from './routes/students.js'

const app = express();
const { json } = bodyParser;
connectDB();

app.use(json());
app.use(cors());

app.use('/students', students);
// app.use('/courses', require('./routes/courses'));
// app.use('/enrollments', require('./routes/enrollments'));

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
