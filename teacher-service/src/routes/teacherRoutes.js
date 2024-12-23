import { Router } from 'express';
import defaultController from '../controllers/teacherController.js';

const router = Router();
const { createTeacher, getAllTeachers, getTeacherById } = defaultController;

router.post('/', createTeacher); // Create a new teacher
router.get('/', getAllTeachers); // Get all teachers
router.get('/:id', getTeacherById); // Get teacher by ID

export default router;
