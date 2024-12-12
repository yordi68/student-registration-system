import { Schema, model } from 'mongoose';

const StudentSchema = new Schema({
    name: { type: String, required: true },
    email: { type: String, required: true },
    dob: { type: Date, required: true },
    grade: { type: String, required: true },
});

export default model('Student', StudentSchema);
