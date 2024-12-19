import { Schema, model } from 'mongoose';

const studentSchema = new Schema({
  name: { type: String, required: true },
  age: { type: Number, required: true },
  email: { type: String, required: true, unique: true },
  enrolledCourses: [{ type: String }], // Array of course IDs
});

export default model('Student', studentSchema);
