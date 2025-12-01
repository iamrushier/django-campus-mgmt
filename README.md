# Campus Management System

A comprehensive web-based application built with Django for managing campus activities, courses, assignments, and grades. This system facilitates interaction between students, teachers, and administrators.

## 🚀 Features

*   **User Roles & Permissions**:
    *   **Admin**: Full access to manage users, courses, and system settings.
    *   **Teacher**: Create and manage courses, assignments, and grade submissions.
    *   **Student**: Enroll in courses, view assignments, submit work, and check results.
*   **Course Management**: Teachers can create courses, and students can enroll in them.
*   **Assignment System**: Teachers can post assignments with due dates.
*   **Submission & Grading**: Students upload submissions, and teachers can grade them with feedback.
*   **Modern UI**: Clean and responsive interface styled with custom CSS.
*   **REST API**: Includes API endpoints for core functionalities using Django REST Framework.

## 🛠️ Tech Stack

*   **Backend**: Python, Django 5.2
*   **Database**: SQLite (Default)
*   **Frontend**: HTML, CSS (Vanilla)
*   **API**: Django REST Framework

## 📦 Installation & Setup

Follow these steps to get the project running on your local machine.

### Prerequisites

*   Python 3.8 or higher installed.

### Steps

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd django-campus-mgmt
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment**
    *   **Windows**:
        ```bash
        .venv\Scripts\activate
        ```
    *   **macOS/Linux**:
        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Apply database migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set a username, email, and password.

7.  **Run the development server**
    ```bash
    python manage.py runserver
    ```

## 🖥️ Usage

1.  Open your browser and navigate to `http://127.0.0.1:8000/`.
2.  **Login/Signup**:
    *   Create a new account as a Student or Teacher via the Signup page.
    *   Or log in with the superuser credentials you created to access the Admin panel at `http://127.0.0.1:8000/admin/`.
3.  **Explore**:
    *   **Teachers**: Create a course, add an assignment.
    *   **Students**: Enroll in the course, submit an assignment.
    *   **Teachers**: Grade the submission.

## 📂 Project Structure

```plaintext
django-campus-mgmt/
├── accounts/         # User authentication and role management
├── assignments/      # Assignment and submission logic
├── campus_mgmt/      # Project settings and configuration
├── core/             # Core templates and views (Home, Base)
├── courses/          # Course management and enrollment
├── static/           # Global static files (CSS, Images)
├── templates/        # Global templates
├── uploads/          # User uploaded files (Media)
├── manage.py         # Django management script
└── requirements.txt  # Project dependencies
```
