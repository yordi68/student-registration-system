import { createStudent, getStudents } from "../controllers/studentController";
import { Router } from "express";

const router = Router();

router.post('/', createStudent);
router.get('/', getStudents);

export default router;
