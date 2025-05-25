# Student Query System

A full-stack web application built with Python Flask and PostgreSQL that enables seamless communication between students and teachers through a query management system.

## 🌟 Features

### For Students
- **Cross-Department Queries**: Submit queries to any teacher across all departments
- **Subject Management**: Register for subjects from any department  
- **Real-time Tracking**: Monitor query status and responses
- **Personal Dashboard**: View all submitted queries and responses
- **Profile Management**: Update personal information and academic details

### For Teachers
- **Query Management**: View and respond to student queries efficiently
- **Subject Assignment**: Manage subjects you teach
- **Student Information**: Access student details for better context
- **Response Tracking**: Monitor answered and pending queries
- **Analytics Dashboard**: View query statistics and trends

### System Features
- **Role-based Authentication**: Secure login for students and teachers
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Modern UI**: Beautiful gradient-based design with smooth animations
- **Secure Database**: PostgreSQL with proper data relationships
- **Session Management**: Secure user sessions with password hashing

## 🚀 Quick Start

### Demo Credentials

**Student Account:**
- Email: `alice.student@demo.edu`
- Password: `student123`

**Teacher Account:**  
- Email: `robert.teacher@demo.edu`
- Password: `teacher123`

### Installation

1. **Install Dependencies**
```bash
pip install flask flask-sqlalchemy werkzeug gunicorn psycopg2-binary
```

2. **Set Environment Variables**
```bash
export DATABASE_URL="postgresql://username:password@localhost/dbname"
export SESSION_SECRET="your-secret-key-here"
```

3. **Run the Application**
```bash
python main.py
```

4. **Access the Application**
- Open your browser to `http://localhost:5000`
- Register new accounts or use demo credentials
- Start exploring the features!

## 📱 Usage Guide

### For Students:
1. **Register/Login** with student role
2. **Register for Subjects** you're interested in
3. **Submit Queries** to any teacher across departments
4. **Track Responses** in your dashboard
5. **Manage Profile** and update information

### For Teachers:
1. **Register/Login** with teacher role  
2. **Assign Subjects** you teach
3. **View Incoming Queries** from students
4. **Respond to Queries** with detailed answers
5. **Monitor Query History** and student interactions

## 🏗️ Architecture

### Backend (Python Flask)
- **app.py**: Application configuration and database setup
- **models.py**: Database models and relationships
- **routes.py**: URL routing and business logic
- **main.py**: Application entry point

### Frontend (HTML/CSS/Jinja2)
- **templates/**: Jinja2 templates for all pages
- **static/style.css**: Modern gradient-based styling
- **Responsive Design**: Mobile-first approach

### Database (PostgreSQL)
- **Users**: Student and teacher accounts with role-based access
- **Subjects**: Academic subjects with department organization
- **Queries**: Student-teacher communication with status tracking
- **Relationships**: Proper foreign keys and constraints

## 🎨 Design Features

- **Gradient UI**: Beautiful pink-to-blue gradient theme
- **Inter Font**: Modern typography throughout
- **Responsive Grid**: Flexible layouts for all screen sizes
- **Smooth Animations**: CSS transitions and hover effects
- **Accessibility**: Proper form labels and semantic HTML

## 🔒 Security

- **Password Hashing**: Werkzeug security for password protection
- **Session Management**: Secure Flask sessions
- **Role-based Access**: Proper authorization for different user types
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **Input Validation**: Form validation and sanitization

## 🌐 Cross-Department Feature

The system's standout feature allows students to submit queries to teachers from ANY department, promoting:
- **Interdisciplinary Learning**: Students can explore topics across fields
- **Knowledge Sharing**: Teachers can share expertise beyond their department
- **Academic Collaboration**: Breaks down departmental silos
- **Comprehensive Support**: Students get help from the best available experts

## 📊 Database Schema

```sql
Users (id, role, name, email, password_hash, department, roll_no, created_at)
Subjects (id, name, department)
StudentSubjects (id, student_id, subject_id, registered_at)
TeacherSubjects (id, teacher_id, subject_id, assigned_at)
Queries (id, student_id, teacher_id, subject_id, message, reply, status, created_at, updated_at)
```

## 🛠️ Tech Stack

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Database**: PostgreSQL with psycopg2
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Server**: Gunicorn WSGI server
- **Styling**: Custom CSS with CSS Grid and Flexbox
- **Security**: Werkzeug password hashing

## 📈 Future Enhancements

- Email notifications for new queries/responses
- File attachment support for queries
- Advanced search and filtering
- Query categorization and tagging
- Mobile app development
- Integration with learning management systems

## 🤝 Contributing

This is a complete, production-ready application that demonstrates best practices in:
- Modern web development with Flask
- Database design and relationships
- User authentication and authorization
- Responsive UI/UX design
- Security implementation

## 📄 License

This project is a demonstration of full-stack web development capabilities, showcasing modern technologies and best practices for educational applications.

---

**Built with ❤️ using Python Flask and PostgreSQL**