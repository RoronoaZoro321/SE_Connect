// document.addEventListener("DOMContentLoaded", function() {

//     var usernameInput = document.getElementById("username_login");
//     var passwordInput = document.getElementById("password_login");
//     var forgotPasswordLink = document.getElementById("forgot-password");

//     forgotPasswordLink.addEventListener("click", function(event) {
//         alert("Forgot Password link clicked!");
//         event.preventDefault();
//     });

//     var loginForm = document.getElementById("login-form");
//     loginForm.addEventListener("submit", function(event) {      
//         var usernameValue = usernameInput.value;
//         var passwordValue = passwordInput.value;
//         if (usernameValue === "" || passwordValue === "") {
//             alert("Username and password are required!");
//             event.preventDefault();
//         }
//     });
// });

console.log('login.js loaded');

document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault();
  
    let studentId = document.getElementById('student_id').value;
    studentId = parseInt(studentId);
    const password = document.getElementById('password').value;
    console.log(studentId);
    console.log(password);


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
          window.location.href = '/home'; // Change to the correct URL
        } else {
          // Handle unsuccessful login, e.g., display an error message
          document.getElementById('error-message').innerText = 'Login failed';
          console.error('Login failed');
        }
      } catch (error) {
        console.error('An error occurred:', error);
    }
  });