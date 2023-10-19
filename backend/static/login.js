console.log('login.js loaded');

document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault();
  
    let studentId = parseInt(document.getElementById('student_id').value);
    const password = document.getElementById('password').value;

    const data = {
        student_id: studentId,
        password: password
    };
    
    const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    };
  
    try {
        const response = await fetch('/login', options);
        console.log(response);
    
        if (response.ok) {
          // Login was successful, redirect to the /home page
          window.location.href = '/'; // Change to the correct URL
        } else {
          // Handle unsuccessful login, e.g., display an error message
          document.getElementById('error-message').innerText = 'Login failed';
          console.error('Login failed');
        }
      } catch (error) {
        console.error('An error occurred:', error);
    }
  });