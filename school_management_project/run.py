from app import create_app, db

# Create the app instance
app = create_app()

if __name__ == '__main__':
    
    app.run(debug=True)














"""
post: http://127.0.0.1:5000/classes/class
{
   "class_name": "6th",
   "section": "A",
   "teacher_id": 1
}

delete: http://127.0.0.1:5000/classes/class?id=409
"""