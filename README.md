# Luminary Blog

A modern, feature-rich blog platform built with Flask, featuring user authentication, post management, and a sleek dark/light theme interface.

## Features

- 🔐 **User Authentication** - Secure login and registration with password hashing
- 📝 **Post Management** - Create, edit, and delete blog posts
- 🖼️ **Image Uploads** - Support for profile pictures and post cover images
- 🎨 **Theme Toggle** - Beautiful dark and light mode themes
- 📱 **Responsive Design** - Mobile-friendly interface with smooth animations
- 🔒 **Security** - CSRF protection, secure file uploads, and password encryption

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: SQLite
- **Authentication**: Werkzeug password hashing, Flask-Login session management

## Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository or navigate to the project directory:
```bash
cd secondTesting
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
   - Copy `.env.example` to `.env` if provided, or ensure `.env` exists with:
     ```
     SECRET_KEY=your-secret-key-here
     DATABASE_URL=sqlite:///blog.db
     UPLOAD_FOLDER=static/uploads
     MAX_CONTENT_LENGTH=16777216
     DEBUG=True
     ```

6. Initialize the database:
```bash
python app.py
```
   The database will be created automatically on first run.

## Usage

1. Start the development server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

3. Create an account and start blogging!

## Deployment (Render)

To put your site online for free using Render:

1. **Push to GitHub**: Upload your code to a new repository on GitHub.
2. **Connect to Render**:
   - Go to [Render.com](https://render.com/) and sign up.
   - Click **"New +"** and select **"Web Service"**.
   - Connect your GitHub account and select this repository.
3. **Configure Settings**:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (This is already set in the `Procfile`)
4. **Environment Variables**:
   - Click "Advanced" and add these variables:
     - `SECRET_KEY`: A random string (e.g., `my-super-secret-123`)
     - `PYTHON_VERSION`: `3.10.0` (or your preferred version)
5. **Deploy**: Click **"Create Web Service"**. Your site will be live in a few minutes!

## Project Structure

```
secondTesting/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .gitignore            # Git ignore rules
├── static/
│   ├── styles.css        # Main stylesheet
│   ├── theme.js          # Theme toggle functionality
│   └── uploads/          # User-uploaded files
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── articles.html     # Articles listing
│   ├── article.html      # Single article view
│   ├── access.html       # Login/Register/Security
│   ├── profiles.html     # User profile
│   ├── settings.html     # User settings
│   ├── create_post.html  # Post creation/editing
│   ├── about.html        # About page
│   ├── contact.html      # Contact page
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
└── instance/
    └── blog.db           # SQLite database (created automatically)
```

## Routes

### Public Routes
- `/` - Homepage with latest posts
- `/articles` - All articles listing
- `/article/<id>` - View single article
- `/about` - About page
- `/contact` - Contact page
- `/access` - Login/Register page

### Protected Routes (Login Required)
- `/profiles` - User profile page
- `/settings` - User settings
- `/security` - Security settings
- `/create-post` - Create new post
- `/edit-post/<id>` - Edit existing post
- `/delete-post/<id>` - Delete post

## Security Notes

- Never commit the `.env` file to version control
- Change the `SECRET_KEY` in production to a strong random value
- Set `DEBUG=False` in production
- Configure proper file upload limits based on your server capacity
- Regularly update dependencies for security patches

## Future Enhancements

- [ ] Email verification
- [ ] Password reset functionality
- [ ] Two-factor authentication
- [ ] Comment system
- [ ] Search functionality
- [ ] Post categories and tags
- [ ] RSS feed
- [ ] Social media integration
- [ ] Admin dashboard

## License

This project is for educational and personal use.

## Contributing

Feel free to submit issues and enhancement requests!
