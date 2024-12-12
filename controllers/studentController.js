import Student from '../models/student';

export async function createStudent(req, res) {
    try {
        const student = new Student(req.body);
        await student.save();
        res.status(201).json({ message: 'Student created successfully', studentId: student._id });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
}

export async function getStudents(req, res) {
    // try {
    //     const students = await find();
    //     res.status(200).json(students);
    // } catch (err) {
    //     res.status(500).json({ error: err.message });
    // }
}
