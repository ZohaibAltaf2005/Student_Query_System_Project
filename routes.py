from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from models import User, Subject, StudentSubject, TeacherSubject, Query
from sqlalchemy import or_

# Helper function to check if user is logged in
def is_logged_in():
    return 'user_id' in session

def get_current_user():
    if is_logged_in():
        return User.query.get(session['user_id'])
    return None

def login_required(f):
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def student_required(f):
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or not user.is_student():
            flash('Access denied. Student account required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def teacher_required(f):
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or not user.is_teacher():
            flash('Access denied. Teacher account required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', '')
        department = request.form.get('department', '').strip()
        roll_no = request.form.get('roll_no', '').strip() if role == 'student' else None
        
        # Validation
        if not all([name, email, password, role, department]):
            flash('All fields are required.', 'error')
            return render_template('register.html')
        
        if role == 'student' and not roll_no:
            flash('Roll number is required for students.', 'error')
            return render_template('register.html')
        
        if role not in ['student', 'teacher']:
            flash('Invalid role selected.', 'error')
            return render_template('register.html')
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            name=name,
            email=email,
            role=role,
            department=department,
            roll_no=roll_no
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            app.logger.error(f"Registration error: {e}")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash(f'Welcome back, {user.name}!', 'success')
            
            if user.is_student():
                return redirect(url_for('student_dashboard'))
            else:
                return redirect(url_for('teacher_dashboard'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Make helper functions available to all templates
@app.context_processor
def inject_user():
    return dict(
        is_logged_in=is_logged_in(),
        current_user=get_current_user()
    )

@app.route('/student/dashboard')
@login_required
@student_required
def student_dashboard():
    user = get_current_user()
    
    # Get student's subjects
    student_subjects = db.session.query(Subject).join(StudentSubject).filter(
        StudentSubject.student_id == user.id
    ).all()
    
    # Get recent queries
    recent_queries = Query.query.filter_by(student_id=user.id).order_by(
        Query.created_at.desc()
    ).limit(5).all()
    
    return render_template('student_dashboard.html', 
                         user=user, 
                         subjects=student_subjects, 
                         recent_queries=recent_queries)

@app.route('/teacher/dashboard')
@login_required
@teacher_required
def teacher_dashboard():
    user = get_current_user()
    
    # Get teacher's subjects
    teacher_subjects = db.session.query(Subject).join(TeacherSubject).filter(
        TeacherSubject.teacher_id == user.id
    ).all()
    
    # Get pending queries
    pending_queries = Query.query.filter_by(
        teacher_id=user.id, 
        status='pending'
    ).order_by(Query.created_at.desc()).limit(5).all()
    
    return render_template('teacher_dashboard.html', 
                         user=user, 
                         subjects=teacher_subjects, 
                         pending_queries=pending_queries)

@app.route('/student/profile', methods=['GET', 'POST'])
@login_required
@student_required
def student_profile():
    user = get_current_user()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        department = request.form.get('department', '').strip()
        roll_no = request.form.get('roll_no', '').strip()
        
        if not all([name, email, department, roll_no]):
            flash('All fields are required.', 'error')
            return render_template('student_profile.html', user=user)
        
        # Check if email is taken by another user
        existing_user = User.query.filter(User.email == email, User.id != user.id).first()
        if existing_user:
            flash('Email already taken by another user.', 'error')
            return render_template('student_profile.html', user=user)
        
        try:
            user.name = name
            user.email = email
            user.department = department
            user.roll_no = roll_no
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Failed to update profile.', 'error')
            app.logger.error(f"Profile update error: {e}")
    
    return render_template('student_profile.html', user=user)

@app.route('/teacher/profile', methods=['GET', 'POST'])
@login_required
@teacher_required
def teacher_profile():
    user = get_current_user()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        department = request.form.get('department', '').strip()
        
        if not all([name, email, department]):
            flash('All fields are required.', 'error')
            return render_template('teacher_profile.html', user=user)
        
        # Check if email is taken by another user
        existing_user = User.query.filter(User.email == email, User.id != user.id).first()
        if existing_user:
            flash('Email already taken by another user.', 'error')
            return render_template('teacher_profile.html', user=user)
        
        try:
            user.name = name
            user.email = email
            user.department = department
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Failed to update profile.', 'error')
            app.logger.error(f"Profile update error: {e}")
    
    return render_template('teacher_profile.html', user=user)

@app.route('/student/subjects', methods=['GET', 'POST'])
@login_required
@student_required
def student_subjects():
    user = get_current_user()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'register':
            subject_name = request.form.get('subject_name', '').strip()
            subject_department = request.form.get('subject_department', '').strip()
            
            if not all([subject_name, subject_department]):
                flash('Subject name and department are required.', 'error')
            else:
                # Check if subject exists, if not create it
                subject = Subject.query.filter_by(
                    name=subject_name, 
                    department=subject_department
                ).first()
                
                if not subject:
                    subject = Subject(name=subject_name, department=subject_department)
                    db.session.add(subject)
                    db.session.flush()
                
                # Check if student is already registered
                existing = StudentSubject.query.filter_by(
                    student_id=user.id,
                    subject_id=subject.id
                ).first()
                
                if existing:
                    flash('You are already registered for this subject.', 'warning')
                else:
                    try:
                        student_subject = StudentSubject(
                            student_id=user.id,
                            subject_id=subject.id
                        )
                        db.session.add(student_subject)
                        db.session.commit()
                        flash('Successfully registered for subject!', 'success')
                    except Exception as e:
                        db.session.rollback()
                        flash('Failed to register for subject.', 'error')
                        app.logger.error(f"Subject registration error: {e}")
        
        elif action == 'withdraw':
            subject_id = request.form.get('subject_id')
            if subject_id:
                try:
                    student_subject = StudentSubject.query.filter_by(
                        student_id=user.id,
                        subject_id=subject_id
                    ).first()
                    
                    if student_subject:
                        db.session.delete(student_subject)
                        db.session.commit()
                        flash('Successfully withdrawn from subject!', 'success')
                    else:
                        flash('Subject registration not found.', 'error')
                except Exception as e:
                    db.session.rollback()
                    flash('Failed to withdraw from subject.', 'error')
                    app.logger.error(f"Subject withdrawal error: {e}")
    
    # Get student's registered subjects
    registered_subjects = db.session.query(Subject).join(StudentSubject).filter(
        StudentSubject.student_id == user.id
    ).all()
    
    return render_template('student_subjects.html', 
                         user=user, 
                         registered_subjects=registered_subjects)

@app.route('/teacher/subjects', methods=['GET', 'POST'])
@login_required
@teacher_required
def teacher_subjects():
    user = get_current_user()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'assign':
            subject_name = request.form.get('subject_name', '').strip()
            subject_department = request.form.get('subject_department', '').strip()
            
            if not all([subject_name, subject_department]):
                flash('Subject name and department are required.', 'error')
            else:
                # Check if subject exists, if not create it
                subject = Subject.query.filter_by(
                    name=subject_name, 
                    department=subject_department
                ).first()
                
                if not subject:
                    subject = Subject(name=subject_name, department=subject_department)
                    db.session.add(subject)
                    db.session.flush()
                
                # Check if teacher is already assigned
                existing = TeacherSubject.query.filter_by(
                    teacher_id=user.id,
                    subject_id=subject.id
                ).first()
                
                if existing:
                    flash('You are already assigned to this subject.', 'warning')
                else:
                    try:
                        teacher_subject = TeacherSubject(
                            teacher_id=user.id,
                            subject_id=subject.id
                        )
                        db.session.add(teacher_subject)
                        db.session.commit()
                        flash('Successfully assigned to subject!', 'success')
                    except Exception as e:
                        db.session.rollback()
                        flash('Failed to assign subject.', 'error')
                        app.logger.error(f"Subject assignment error: {e}")
        
        elif action == 'unassign':
            subject_id = request.form.get('subject_id')
            if subject_id:
                try:
                    teacher_subject = TeacherSubject.query.filter_by(
                        teacher_id=user.id,
                        subject_id=subject_id
                    ).first()
                    
                    if teacher_subject:
                        db.session.delete(teacher_subject)
                        db.session.commit()
                        flash('Successfully unassigned from subject!', 'success')
                    else:
                        flash('Subject assignment not found.', 'error')
                except Exception as e:
                    db.session.rollback()
                    flash('Failed to unassign from subject.', 'error')
                    app.logger.error(f"Subject unassignment error: {e}")
    
    # Get teacher's assigned subjects
    assigned_subjects = db.session.query(Subject).join(TeacherSubject).filter(
        TeacherSubject.teacher_id == user.id
    ).all()
    
    return render_template('teacher_subjects.html', 
                         user=user, 
                         assigned_subjects=assigned_subjects)

@app.route('/student/submit-query', methods=['GET', 'POST'])
@login_required
@student_required
def submit_query():
    user = get_current_user()
    
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        teacher_id = request.form.get('teacher_id')
        message = request.form.get('message', '').strip()
        
        if not all([subject_id, teacher_id, message]):
            flash('All fields are required.', 'error')
        else:
            try:
                query = Query(
                    student_id=user.id,
                    teacher_id=teacher_id,
                    subject_id=subject_id,
                    message=message
                )
                db.session.add(query)
                db.session.commit()
                flash('Query submitted successfully!', 'success')
                return redirect(url_for('view_queries'))
            except Exception as e:
                db.session.rollback()
                flash('Failed to submit query.', 'error')
                app.logger.error(f"Query submission error: {e}")
    
    # Get all subjects
    subjects = Subject.query.all()
    
    # Get all teachers
    teachers = User.query.filter_by(role='teacher').all()
    
    return render_template('submit_query.html', 
                         user=user, 
                         subjects=subjects, 
                         teachers=teachers)

@app.route('/student/queries')
@login_required
@student_required
def view_queries():
    user = get_current_user()
    
    # Get all queries submitted by this student
    queries = Query.query.filter_by(student_id=user.id).order_by(
        Query.created_at.desc()
    ).all()
    
    return render_template('view_queries.html', user=user, queries=queries)

@app.route('/teacher/queries')
@login_required
@teacher_required
def teacher_queries():
    user = get_current_user()
    
    # Get all queries sent to this teacher
    queries = Query.query.filter_by(teacher_id=user.id).order_by(
        Query.created_at.desc()
    ).all()
    
    return render_template('teacher_queries.html', user=user, queries=queries)

@app.route('/teacher/respond-query/<int:query_id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def respond_query(query_id):
    user = get_current_user()
    
    # Get the query and ensure it belongs to this teacher
    query = Query.query.filter_by(id=query_id, teacher_id=user.id).first()
    
    if not query:
        flash('Query not found or access denied.', 'error')
        return redirect(url_for('teacher_queries'))
    
    if request.method == 'POST':
        reply = request.form.get('reply', '').strip()
        
        if not reply:
            flash('Reply cannot be empty.', 'error')
        else:
            try:
                query.reply = reply
                query.status = 'answered'
                db.session.commit()
                flash('Reply sent successfully!', 'success')
                return redirect(url_for('teacher_queries'))
            except Exception as e:
                db.session.rollback()
                flash('Failed to send reply.', 'error')
                app.logger.error(f"Reply error: {e}")
    
    return render_template('respond_query.html', user=user, query=query)

# Context processors to make functions available in templates
@app.context_processor
def inject_user():
    return dict(current_user=get_current_user(), is_logged_in=is_logged_in())
