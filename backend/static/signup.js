console.log('signUp.js loaded');

document.getElementById('signup-form_').addEventListener('submit', async (event) => {
    event.preventDefault();
  
    let studentId = parseInt(document.getElementById('id').value);
    const username = document.getElementById('username').value;
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const password = document.getElementById('password').value;

    const data = {
        student_id: studentId,
        username: username,
        firstName: firstName,
        lastName: lastName,
        password: password,
    };

    console.log(data);
    
    const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    };
  
    try {
        const response = await fetch('/signup', options);
        console.log(response);
    
        if (response.ok) {
          // Login was successful, redirect to the /home page
          window.location.href = '/'; // Change to the correct URL
        } else {
          document.getElementById('error-message').innerText = 'Signup failed';
        }
      } catch (error) {
        console.error('An error occurred:', error);
    }
  });