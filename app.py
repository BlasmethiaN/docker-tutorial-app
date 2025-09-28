import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Database connection configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'todoapp'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'port': os.environ.get('DB_PORT', '5432')
}

# def get_db_connection():
#     """Establish a connection to the PostgreSQL database."""
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)
#         return conn
#     except psycopg2.Error as e:
#         print(f"Error connecting to database: {e}")
#         return None
def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print(f"Connected to database: {DB_CONFIG['database']}")  # Debug
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database {DB_CONFIG['database']}: {e}")
        return None

@app.route('/')
def index():
    """Display all tasks on the main page."""
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed', 'error')
        return render_template('index.html', tasks=[])
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM tasks ORDER BY id DESC')
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', tasks=tasks)
    except psycopg2.Error as e:
        flash(f'Error retrieving tasks: {e}', 'error')
        return render_template('index.html', tasks=[])

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task to the database."""
    description = request.form.get('description', '').strip()
    
    if not description:
        flash('Task description cannot be empty', 'error')
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed', 'error')
        return redirect(url_for('index'))
    
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (description) VALUES (%s)', (description,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Task added successfully', 'success')
    except psycopg2.Error as e:
        print(f"Detailed database error: {e}")
        flash(f'Error adding task: {e}', 'error')
    
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    """Mark a task as completed."""
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed', 'error')
        return redirect(url_for('index'))
    
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET completed = TRUE WHERE id = %s', (task_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Task marked as completed', 'success')
    except psycopg2.Error as e:
        flash(f'Error updating task: {e}', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Delete a task from the database."""
    conn = get_db_connection()
    if not conn:
        flash('Database connection failed', 'error')
        return redirect(url_for('index'))
    
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Task deleted successfully', 'success')
    except psycopg2.Error as e:
        flash(f'Error deleting task: {e}', 'error')
    
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    conn = get_db_connection()
    if conn:
        conn.close()
        return {'status': 'healthy', 'database': 'connected'}, 200
    else:
        return {'status': 'unhealthy', 'database': 'disconnected'}, 500

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)
