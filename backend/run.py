import os
from app import create_app
from app.models import db

# Get environment
env = os.getenv('FLASK_ENV', 'development')

# Create application
app = create_app(env)

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=(env == 'development')
    )
