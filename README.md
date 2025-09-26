# Django Assignment: Campus Management System

## 🎯 Objective
Build a web-based **Campus Management System** where students, teachers, and administrators interact.  
This project should use a wide range of Django features to simulate a real-world application.

---

## 🔧 Functional Requirements

### 1. User Management (Authentication & Authorization)
- Three user roles: **Student**, **Teacher**, and **Admin**  
- User registration, login, logout  
- Permissions:  
  - **Admin**: Full access  
  - **Teacher**: Can manage courses, see enrolled students  
  - **Student**: Can enroll in courses, view results  

---

### 2. Models
- **User** (extend `AbstractUser` for roles)  
- **Course**  
- **Enrollment** (link between Student and Course)  
- **Assignment**  
- **Submission**  
- **Result**  

---

### 3. Admin Panel Customization
- Customize the Django admin for managing users, courses, and grades  
- Inline models for enrollments and submissions  
- Use `list_display`, `search_fields`, `list_filter`  

---

### 4. Views and Templates (CBVs + FBVs)
- Use a mix of **Function-Based Views (FBVs)** and **Class-Based Views (CBVs)**  
- Example Pages:  
  - Course list & detail  
  - Enrollment dashboard (Student)  
  - Assignment upload form (Student)  
  - Submission review & grading form (Teacher)  
  - Result view (Student)  

---

### 5. Forms
- Use both **Django Forms** and **ModelForms**  
- Validate file uploads, date formats, etc.  
- Create custom widgets where appropriate (e.g., DatePicker)  

---

### 6. Middleware
- Create a custom middleware to log user actions (login/logout, course enrolled, submission made)  

---

### 7. Signals
- When a user is created, assign a default role  
- When a submission is graded, notify the student via email (mock or console backend)  

---

### 8. Email Integration
- Use Django’s console email backend to simulate sending:  
  - Enrollment confirmation  
  - Grade notification  

---

### 9. Static and Media Files
- Use **STATICFILES** for styles/scripts  
- Allow media upload for assignments/submissions using **MEDIA_ROOT**  

---

### 10. REST API (Django REST Framework)
- Create API endpoints for:  
  - Course listing  
  - Assignment upload  
  - Enrollment  
- Add token-based authentication using DRF  

---

### 11. Unit Testing
- Write unit tests for:  
  - Models  
  - Views  
  - Forms  
  - APIs  

---

### 12. Bonus Features (Optional)
- Pagination in course listing  
- Search and filter courses  
- AJAX for dynamic form updates (e.g., loading assignments via JS)  

---

## 🗃️ Project Structure (Example)

```plaintext
campus_mgmt/
│
├── accounts/         # User handling
├── courses/          # Course, Enrollment, Assignments
├── submissions/      # Upload and grading
├── api/              # DRF-based APIs
├── templates/        # HTML templates
├── static/           # Static files
├── media/            # Uploaded files
├── middleware/       # Custom middleware
├── campus_mgmt/      # Main settings & URL conf
