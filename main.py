import os
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add parent directory to path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
# Enable CORS for all routes to allow requests from frontend
CORS(app)
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Email configuration - can be overridden with environment variables
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 465))
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'princenyarkoedwin@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'ocon gldj taoa eqpc')
EMAIL_RECIPIENT = os.environ.get('EMAIL_RECIPIENT', 'francisdugbe967@gmail.com')

# Create logs directory for storing submissions
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "contact_submissions.txt")

def send_email(name, email, comment):
    """Send an email with the contact form data"""
    if EMAIL_HOST_USER == 'your.email@gmail.com' or EMAIL_HOST_PASSWORD == 'your-app-password':
        print("Email settings not configured. Update environment variables or defaults in the code.")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = f"New Contact Form Submission from {name}"
        
        # Email body
        body = f"""
        You have received a new contact form submission:
        
        Name: {name}
        Email: {email}
        Message:
        {comment}
        
        This is an automated message from your portfolio website.
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to server and send
        if EMAIL_USE_SSL:
            server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        else:
            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            if os.environ.get('EMAIL_USE_TLS', 'False').lower() == 'true':
                server.starttls()
                
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_HOST_USER, EMAIL_RECIPIENT, text)
        server.quit()
        
        print(f"Email sent successfully to {EMAIL_RECIPIENT}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@app.route('/', methods=['GET'])
def index():
    """Serve the index page or API information"""
    return jsonify({
        'status': 'success',
        'message': 'Contact Form Backend API is running',
        'endpoints': {
            '/api/submit_contact_form': 'POST - Submit contact form data'
        }
    })

@app.route('/api/submit_contact_form', methods=['POST'])
def submit_contact_form():
    """Handle contact form submission"""
    if request.method == 'POST':
        try:
            # Get JSON data from request
            data = request.get_json()
            
            # Extract form fields
            name = data.get('name')
            email = data.get('email')
            comment = data.get('comment')
            
            # Validate required fields
            if not name or not email:
                return jsonify({
                    'status': 'error',
                    'message': 'Name and Email are required fields'
                }), 400
                
            # Log submission to console
            print(f"Received contact form submission:")
            print(f"Name: {name}")
            print(f"Email: {email}")
            print(f"Comment: {comment}")
            
            # Save submission to log file
            with open(log_file, "a") as f:
                f.write(f"Name: {name}, Email: {email}, Comment: {comment}\n")
            
            # Send email notification
            email_sent = send_email(name, email, comment)
            
            # Return appropriate response
            if email_sent:
                return jsonify({
                    'status': 'success',
                    'message': 'Form submitted successfully and email notification sent!'
                }), 200
            else:
                return jsonify({
                    'status': 'partial_success',
                    'message': 'Form submitted successfully, but email notification could not be sent.'
                }), 200
                
        except Exception as e:
            print(f"Error processing form: {e}")
            return jsonify({
                'status': 'error',
                'message': f'Error processing request: {str(e)}'
            }), 500
    else:
        return jsonify({
            'status': 'error',
            'message': 'Method not allowed'
        }), 405

# Serve static files (if any)
@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from the static folder"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if os.path.exists(os.path.join(static_folder_path, path)):
        from flask import send_from_directory
        return send_from_directory(static_folder_path, path)
    else:
        return jsonify({
            'status': 'error',
            'message': 'File not found'
        }), 404

if __name__ == '__main__':
    print(f"Starting Contact Form Backend on port 5000")
    print(f"Email notifications will be sent to: {EMAIL_RECIPIENT}")
    print(f"Form submissions will be logged to: {log_file}")
    app.run(host='0.0.0.0', port=5000, debug=True)
