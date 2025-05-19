# New Contact Form Backend - Usage Instructions

This document provides instructions on how to set up and use the new Flask backend for your contact form.

## Overview

This backend provides a simple API endpoint that receives contact form submissions, logs them to a file, and sends email notifications. It's designed to work with your React frontend's contact form.

## Features

- **Contact Form API Endpoint**: Receives form data via POST request
- **Email Notifications**: Sends email notifications when someone submits the form
- **Local Logging**: Saves all submissions to a local log file
- **CORS Support**: Configured to allow cross-origin requests from your frontend
- **Error Handling**: Robust error handling for all operations

## Setup Instructions

### Prerequisites

- Python 3.x installed on your system
- Basic knowledge of command line operations

### Installation

1. **Extract the Files**:
   Extract the `new_contact_backend.zip` file to a location of your choice.

2. **Install Dependencies**:
   Open a terminal/command prompt, navigate to the extracted folder, and run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Email Settings**:
   You have two options for configuring email:

   **Option 1**: Set environment variables (recommended for security):
   ```bash
   # On Windows
   set EMAIL_HOST_USER=your.email@gmail.com
   set EMAIL_HOST_PASSWORD=your-app-password
   set EMAIL_RECIPIENT=recipient@example.com

   # On macOS/Linux
   export EMAIL_HOST_USER=your.email@gmail.com
   export EMAIL_HOST_PASSWORD=your-app-password
   export EMAIL_RECIPIENT=recipient@example.com
   ```

   **Option 2**: Edit the default values in `main.py` (lines 15-19):
   ```python
   EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your.email@gmail.com')
   EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-app-password')
   EMAIL_RECIPIENT = os.environ.get('EMAIL_RECIPIENT', 'recipient@example.com')
   ```

4. **Gmail-Specific Setup**:
   If using Gmail:
   - Enable 2-Step Verification in your Google Account
   - Create an App Password: Google Account → Security → App passwords
   - Use the generated 16-character password as your EMAIL_HOST_PASSWORD

### Running the Backend

1. **Start the Server**:
   ```bash
   python main.py
   ```

2. **Verify It's Running**:
   You should see output similar to:
   ```
   Starting Contact Form Backend on port 5000
   Email notifications will be sent to: recipient@example.com
   Form submissions will be logged to: /path/to/logs/contact_submissions.txt
   ```

3. **Test the Backend**:
   Open a web browser and navigate to:
   ```
   http://localhost:5000/static/test.html
   ```
   This will load a test form you can use to verify the backend is working correctly.

## Integration with React Frontend

To connect your React frontend to this backend:

1. **Update Your Contact.jsx Component**:
   Ensure your fetch call points to the correct endpoint:
   ```javascript
   const response = await fetch('http://localhost:5000/api/submit_contact_form', {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
     },
     body: JSON.stringify(formData),
   });
   ```

2. **Run Both Servers**:
   - Start this Flask backend on port 5000
   - Start your React frontend on its default port

3. **Test End-to-End**:
   Submit the contact form on your React frontend and verify:
   - The form submission is logged to the console
   - A record is added to `logs/contact_submissions.txt`
   - An email notification is sent (if configured correctly)

## Troubleshooting

### Email Issues

- **"Service not available" Error**: Your email provider might be blocking the connection. Try:
  - Using an App Password instead of your regular password
  - Checking if your email provider allows less secure apps
  - Using a different email provider

- **No Email Received**: Check:
  - Console output for specific error messages
  - Spam/junk folder in the recipient email
  - Email credentials are correct

### CORS Issues

If you see CORS errors in your browser console:
- Ensure your React app is making requests to `http://localhost:5000`
- Check that the backend is running and accessible

### Logging Issues

If submissions aren't being logged:
- Check that the `logs` directory exists and is writable
- Verify the path in the console output matches your expectations

## Production Deployment

For production deployment:

1. Set `debug=False` in the `app.run()` call
2. Use a production WSGI server like Gunicorn or uWSGI
3. Set up proper email credentials via environment variables
4. Consider using a dedicated email service like SendGrid for more reliable delivery

## Need Help?

If you encounter any issues or have questions, please let me know!
