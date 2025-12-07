# Project Requirements: MyPortal

## 1. Introduction
MyPortal is a web-based Learning Management System (LMS) designed to bridge the gap between students and teachers. It provides a centralized platform for managing academic activities, including subject enrollment, content delivery (lectures, videos, PDFs), assessment (quizzes, grades), and communication (chat). The system aims to streamline the educational process by offering an intuitive and modern interface for both instructors and learners.

## 2. Objectives
*   **Centralized Learning Hub:** To provide a single location for students to access all their course materials and for teachers to manage their subjects.
*   **Streamlined Communication:** To facilitate easy communication between students and teachers through integrated chat features.
*   **Efficient Content Delivery:** To allow teachers to easily upload and organize lecture notes, videos, and supplementary materials.
*   **Automated Assessment:** To simplify the grading process through online quizzes and a digital gradebook.
*   **User-Friendly Experience:** To offer a modern, responsive, and accessible interface that works across different devices.

## 3. Functional Requirements

### 3.1. Authentication & Authorization
*   **Registration:** The system shall allow users to register as either a Student or a Teacher.
*   **Login:** The system shall allow users to log in using their email and password.
*   **Role-Based Access:** The system shall restrict access to certain features based on the user's role (e.g., only teachers can create subjects).
*   **Profile Management:** Users shall be able to update their profile information, including their avatar and password.

### 3.2. Subject Management
*   **Create Subject:** Teachers shall be able to create new subjects, which will generate a unique access code.
*   **Join Subject:** Students shall be able to join subjects using the unique access code provided by the teacher.
*   **Add Secondary Teachers:** Primary teachers shall be able to add other teachers to a subject.
*   **View Subjects:** Users shall be able to view a dashboard of all subjects they are enrolled in or teaching.

### 3.3. Content Management
*   **Manage Lectures:** Teachers shall be able to create, update, and delete lectures within a subject.
*   **Upload Materials:** Teachers shall be able to upload and link various materials to lectures, including:
    *   PDF documents
    *   Video links (e.g., YouTube, Drive)
    *   Google Drive book links
*   **View Content:** Students shall be able to view and download all materials uploaded by the teacher.

### 3.4. Assessment & Grading
*   **Create Quizzes:** Teachers shall be able to create timed quizzes with descriptions and links.
*   **Take Quizzes:** Students shall be able to access and take quizzes within the specified time window.
*   **Gradebook:** Teachers shall be able to view a list of all students in a subject and manage their grades.
*   **View Grades:** Students shall be able to view their own grades for each subject.

### 3.5. Communication
*   **Subject Chat:** The system shall provide a real-time chat interface for each subject where students and teachers can exchange messages.
*   **Announcements:** Teachers shall be able to post announcements visible to all students in the subject.

## 4. Non-Functional Requirements

### 4.1. Usability
*   **Responsive Design:** The application shall be responsive and function correctly on desktop, tablet, and mobile devices.
*   **Intuitive Interface:** The UI shall be clean, modern, and easy to navigate, minimizing the learning curve for new users.
*   **Dark Mode:** The system shall support a dark mode theme for better visual comfort in low-light environments.

### 4.2. Performance
*   **Response Time:** The system shall respond to user interactions (e.g., page loads, form submissions) within a reasonable time frame (ideally under 2 seconds).
*   **Scalability:** The database and backend structure shall be designed to handle multiple concurrent users and subjects.

### 4.3. Security
*   **Password Hashing:** User passwords shall be hashed (e.g., using Bcrypt) before being stored in the database.
*   **Session Management:** The system shall use secure server-side sessions to manage user login states.
*   **Input Validation:** All user inputs shall be validated to prevent common vulnerabilities like SQL injection and XSS.

### 4.4. Reliability & Availability
*   **Data Integrity:** The system shall ensure data consistency, particularly for critical operations like grading and enrollment.
*   **Error Handling:** The system shall handle errors gracefully and provide informative feedback to the user (e.g., custom 404 pages, flash messages).
