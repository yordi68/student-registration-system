import { Router } from "express";
import defaultController from "../controllers/studentController.js";
const {
  createStudent,
  getAllStudents,
  getStudentById,
  getStudentByEmail,
  updateStudent,
  deleteStudent,
} = defaultController;

const router = Router();

router.post("/", createStudent);
router.get("/", getAllStudents);
router.get("/:id", getStudentById);
router.get("/email/:email", getStudentByEmail);
router.put("/:id", updateStudent);
router.delete("/:id", deleteStudent);

export default router;
