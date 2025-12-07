# System Design Documentation - MyPortal

This document outlines the structural and behavioral design of the **MyPortal** application, a web-based learning management system connecting Students and Teachers.

---

## 1. Use Case Diagram

**Actors:**
*   **Student:** A user who joins subjects, views lectures, takes quizzes, and checks grades.
*   **Teacher:** A user who creates subjects, uploads lectures/materials, creates quizzes, and manages grades.
*   **System:** The backend Flask application and Database.

**Use Cases:**
*   **Authentication:**
    *   Register (Student/Teacher)
    *   Login
    *   Logout
    *   Reset Password
*   **Profile Management:**
    *   Edit Profile (Avatar, Name, Password)
*   **Subject Management:**
    *   Create Subject (Teacher)
    *   Add Secondary Teacher (Teacher)
    *   Join Subject via Code (Student)
    *   View Enrolled Subjects
*   **Content Management:**
    *   Add Lecture (Teacher)
    *   Upload Materials (PDFs, Videos, Books) (Teacher)
    *   View/Download Materials (Student)
*   **Assessment:**
    *   Create Quiz (Teacher)
    *   Take Quiz (Student)
    *   View Grades (Student)
    *   Edit Grades (Teacher)
*   **Communication:**
    *   Post Announcements (Teacher)
    *   Send Chat Messages (Student/Teacher)

---

## 2. Class Diagram

Based on the database schema (`init_db.py`) and application logic.

*   **User (Abstract/Logical)**
    *   Attributes: `id`, `first_name`, `last_name`, `email`, `password`, `profile_avatar`, `email_verified`.
*   **Student (Extends User)**
    *   Relationships:
        *   Many-to-Many with **Subject** (via `student_sub`).
        *   One-to-Many with **Grade**.
*   **Teacher (Extends User)**
    *   Relationships:
        *   Many-to-Many with **Subject** (via `teacher_sub`).
        *   One-to-Many with **SubjectAnnChat**.
*   **Subject**
    *   Attributes: `id`, `name`, `code`, `created_date`.
    *   Relationships:
        *   One-to-Many with **Lecture**.
        *   One-to-Many with **Book**.
        *   One-to-Many with **Quiz**.
        *   One-to-Many with **ChatMessage**.
*   **Lecture**
    *   Attributes: `id`, `title`, `notes`.
    *   Relationships:
        *   One-to-Many with **Video**, **PDFs**, **Sheets**.
*   **Material (Video/PDFs/Sheets/Book)**
    *   Attributes: `id`, `link`.
*   **Quiz**
    *   Attributes: `id`, `description`, `start_time`, `duration`, `link`.
*   **ChatMessage**
    *   Attributes: `id`, `message`, `timestamp`, `role`.

---

## 3. Data Flow Diagrams (DFD)

### Level 0 (Context Diagram)
*   **Central Process:** MyPortal System.
*   **External Entities:** Student, Teacher.
*   **Flows:**
    *   *Student -> System:* Login Credentials, Subject Code, Quiz Answers, Chat Messages.
    *   *System -> Student:* Course Content, Grades, Notifications, Chat History.
    *   *Teacher -> System:* Login Credentials, Course Materials, Quiz Data, Grades.
    *   *System -> Teacher:* Student Lists, Submitted Assignments, System Status.

### Level 1 (High-Level Processes)
1.  **Authentication Process:** Handles login/register requests, verifies credentials against the **User DB**, and manages sessions.
2.  **Subject Management:** Handles creating subjects (generating codes) and enrolling students. Interacts with **Subject DB** and **Enrollment DB**.
3.  **Content Delivery:** Manages upload and retrieval of lectures, PDFs, and videos. Interacts with **Content DB**.
4.  **Assessment System:** Handles quiz creation, submission, and grading. Interacts with **Grade DB** and **Quiz DB**.
5.  **Communication System:** Handles real-time chat and announcements. Interacts with **Chat DB**.

---

## 4. Activity Diagrams

### 4.1. User Registration (Student)
1.  **Start**
2.  User fills Registration Form (Name, Email, Password).
3.  System validates input (checks if email exists).
4.  **Decision:**
    *   *If Email Exists:* Show error -> Go back to step 2.
    *   *If Valid:* Hash Password -> Insert into DB -> Set `email_verified=1`.
5.  Redirect to Login Page.
6.  **End**

### 4.2. Adding a Subject (Student)
1.  **Start** (on Home Page)
2.  Student clicks "Add Subject".
3.  Student enters **Subject Code**.
4.  System queries Database for Code.
5.  **Decision:**
    *   *If Code not found:* Display "Subject not found" error.
    *   *If Code found:* Check if already enrolled.
        *   *If Enrolled:* Display "Already Exists" error.
        *   *If Not Enrolled:* Link Student to Subject -> Initialize Grade to 0.
6.  Refresh Home Page with new Subject Card.
7.  **End**

### 4.3. Creating a Subject (Teacher)
1.  **Start** (on Home Page)
2.  Teacher clicks "Add Subject".
3.  Teacher enters **Subject Name**.
4.  (Optional) Teacher adds Secondary Teacher emails or Book links.
5.  System generates unique UUID **Subject Code**.
6.  System saves Subject to DB.
7.  System links Teacher to Subject (as Primary).
8.  Refresh Home Page with new Subject Card.
9.  **End**

### 4.4. Sending a Chat Message
1.  **Start** (Inside Subject Chat)
2.  User types message and clicks Send.
3.  JS captures input -> Sends POST request to `/subject/<code>/chat/api/send`.
4.  Server validates Session.
5.  Server inserts message into `chat_messages` table with Timestamp and Role.
6.  Server returns JSON Success.
7.  Client JS clears input field.
8.  (Async) Client polls API -> Updates Chat Window.
9.  **End**

### 4.5. Uploading a Lecture PDF (Teacher)
1.  **Start** (On Subject Page)
2.  Teacher clicks "Add Lecture" or selects existing Lecture.
3.  Teacher selects "Upload PDF".
4.  Teacher provides Drive Link or File URL.
5.  System processes link (converts `/view` to `/preview` for embedding).
6.  System inserts link into `pdfs` table linked to `lecture_id`.
7.  Page Reloads showing the new PDF icon.
8.  **End**

---

## 5. Sequence Diagrams

### 5.1. Login Sequence
1.  **User** enters Email/Password on `login.html`.
2.  **Browser** sends POST request to `/login`.
3.  **Server (Flask)** queries `student` and `teacher` tables.
4.  **Database** returns user record (hash, id, role).
5.  **Server** compares password hash (`bcrypt`).
6.  **Server** sets `session['id']`, `session['role']`.
7.  **Server** redirects to `/home`.
8.  **Browser** requests `/home`.
9.  **Server** renders `home.html`.

### 5.2. Student Joining Subject
1.  **Student** clicks "Add Subject" modal.
2.  **Student** submits form with `Subject Code`.
3.  **Browser** sends POST to `/home`.
4.  **Server** calls `subject_add_from_type()`.
5.  **Server** queries `subject` table by Code.
6.  **Database** returns `sub_id`.
7.  **Server** inserts into `student_sub` (Student ID, Subject ID).
8.  **Server** inserts into `grade` (Student ID, Subject ID, 0).
9.  **Server** redirects to `/home`.

### 5.3. Viewing Subject Details
1.  **User** clicks Subject Card.
2.  **Browser** requests `/subject/<code`.
3.  **Server** validates User enrollment in Subject.
4.  **Server** queries `lecture` table for the subject.
5.  **Server** queries `video`, `pdfs`, `sheets` for each lecture.
6.  **Server** renders `subject.html` with nested content.
7.  **Browser** displays Accordion view of lectures.

### 5.4. Chat System (Polling)
1.  **User** opens Chat Page.
2.  **Browser** renders `chat.html`.
3.  **Browser (JS)** sends GET to `/subject/<code>/chat/api`.
4.  **Server** queries `chat_messages` joined with User table (for avatars).
5.  **Server** renders `chat_messages.html` fragment.
6.  **Browser** injects HTML into `#chat-container`.
7.  **User** sends message via POST.
8.  **Server** saves to DB.
9.  **Browser** re-fetches API (Step 3) to show new message.

### 5.5. Teacher Editing Grades
1.  **Teacher** navigates to `/subject/<code>/grades`.
2.  **Server** queries all students in subject and their grades.
3.  **Server** renders `edit_grades.html`.
4.  **Teacher** modifies a grade input field.
5.  **Teacher** clicks "Update".
6.  **Browser** sends POST to `/subject/<code>/grades`.
7.  **Server** iterates through form data.
8.  **Server** executes `UPDATE grade SET grade = ... WHERE id = ...`.
9.  **Server** redirects back to Grade page with Success Flash.
