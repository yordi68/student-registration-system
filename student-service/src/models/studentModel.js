import { Schema, model } from 'mongoose';

const studentSchema = new Schema({
  name: { type: String, required: true },
  age: { type: Number, required: true },
  email: { type: String, required: true, unique: true },
});

export default model('Student', studentSchema);
