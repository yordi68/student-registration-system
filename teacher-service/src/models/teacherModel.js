import { Schema, model } from 'mongoose';

const teacherSchema = new Schema({
  firstName: { type: String, required: true },
  lastName: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  subjects: [{ type: String }], // List of subjects taught by the teacher
  hireDate: { type: Date, default: Date.now },
});

export default model('Teacher', teacherSchema);
