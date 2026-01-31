from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-key-for-dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    if not filename or '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.login_view = 'access'
login_manager.init_app(app)

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(200), default='Creative Designer & Tech Enthusiast')
    profile_pic = db.Column(db.String(200), nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    read_time = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Note: Sample articles removed - all articles now come from database

@app.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).limit(3).all()
    return render_template('index.html', articles=posts)

@app.route('/articles')
def articles():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('articles.html', articles=posts)

@app.route('/article/<int:post_id>')
def article(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('article.html', article=post)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route('/profiles')
@login_required
def profiles():
    return render_template('profiles.html', name=current_user.name, email=current_user.email, bio=current_user.bio)

@app.route('/access')
def access():
    if current_user.is_authenticated:
        return redirect(url_for('profiles'))
    return render_template('access.html')

@app.route('/security')
@login_required
def security():
    # Show security management (same as access page but user is authenticated)
    return render_template('access.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # Validate inputs
    if not email or not name or not password:
        return {"error": "All fields are required"}, 400
    
    if len(password) < 8:
        return {"error": "Password must be at least 8 characters"}, 400
    
    user = User.query.filter_by(email=email).first()
    if user:
        return {"error": "Email already exists"}, 400

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='scrypt')
    )
    db.session.add(new_user)
    db.session.commit()

    return {"success": "Account created successfully"}, 201

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return {"error": "Please check your login details and try again."}, 401

    login_user(user)
    return {"success": "Logged in successfully"}, 200

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/update-email', methods=['POST'])
@login_required
def update_email():
    new_email = request.form.get('email')
    
    if User.query.filter_by(email=new_email).first():
        return {"error": "Email already in use."}, 400
    
    current_user.email = new_email
    db.session.commit()
    return {"success": "Email updated successfully."}, 200

@app.route('/update-password', methods=['POST'])
@login_required
def update_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    
    if not check_password_hash(current_user.password, old_password):
        return {"error": "Incorrect current password."}, 401
    
    if len(new_password) < 8:
        return {"error": "Password must be at least 8 characters"}, 400
    
    current_user.password = generate_password_hash(new_password, method='scrypt')
    db.session.commit()
    return {"success": "Password updated successfully."}, 200

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/update-info', methods=['POST'])
@login_required
def update_info():
    name = request.form.get('name')
    bio = request.form.get('bio')
    file = request.files.get('profile_pic')
    
    if file and file.filename != '':
        # Validate file type
        if not allowed_file(file.filename):
            return {"error": "Invalid file type. Only images are allowed."}, 400
        
        filename = secure_filename(f"user_{current_user.id}_{file.filename}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        current_user.profile_pic = f"/static/uploads/{filename}"
    
    current_user.name = name
    current_user.bio = bio
    db.session.commit()
    return {"success": "Information updated successfully."}, 200

@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        summary = request.form.get('summary')
        content = request.form.get('content')
        file = request.files.get('image')
        
        # Handle image upload (optional)
        image_url = "https://picsum.photos/400/250?random=999"  # Default placeholder
        
        if file and file.filename != '':
            # Validate file type
            if not allowed_file(file.filename):
                return {"error": f"Invalid file type '{file.filename}'. Only PNG, JPG, JPEG, GIF, and WEBP images are allowed."}, 400
            
            filename = secure_filename(f"post_{file.filename}")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_url = f"/static/uploads/{filename}"
        
        from datetime import datetime
        new_post = Post(
            title=title,
            category=category,
            summary=summary,
            content=content,
            image=image_url,
            date=datetime.now().strftime("%b %d, %Y"),
            read_time=f"{max(1, len(content)//500)} min read",
            author=current_user
        )
        
        db.session.add(new_post)
        db.session.commit()
        return {"success": "Post published successfully!", "id": new_post.id}, 201
        
    return render_template('create_post.html')

@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        return {"error": "Unauthorized access."}, 403
        
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.category = request.form.get('category')
        post.summary = request.form.get('summary')
        post.content = request.form.get('content')
        
        file = request.files.get('image')
        if file and file.filename != '':
            # Validate file type
            if not allowed_file(file.filename):
                return {"error": "Invalid file type. Only images are allowed."}, 400
            
            filename = secure_filename(f"post_{file.filename}")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            post.image = f"/static/uploads/{filename}"
            
        post.read_time = f"{max(1, len(post.content)//500)} min read"
        db.session.commit()
        return {"success": "Post updated successfully!", "id": post.id}, 200
        
    return render_template('create_post.html', post=post)

@app.route('/delete-post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        return {"error": "Unauthorized access."}, 403
        
    db.session.delete(post)
    db.session.commit()
    return {"success": "Post deleted successfully."}, 200

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
