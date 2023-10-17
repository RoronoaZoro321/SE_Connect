// Log in ----------

document.addEventListener("DOMContentLoaded", function() {

    var usernameInput = document.getElementById("username_login");
    var passwordInput = document.getElementById("password_login");
    var forgotPasswordLink = document.getElementById("forgot-password");

    forgotPasswordLink.addEventListener("click", function(event) {
        alert("Forgot Password link clicked!");
        event.preventDefault();
    });

    var loginForm = document.getElementById("login-form");
    loginForm.addEventListener("submit", function(event) {      
        var usernameValue = usernameInput.value;
        var passwordValue = passwordInput.value;
        if (usernameValue === "" || passwordValue === "") {
            alert("Username and password are required!");
            event.preventDefault();
        }
    });
});

// Sign up ---------

document.addEventListener("DOMContentLoaded", function() {
    var form = document.querySelector("form");
    var nameInput = document.getElementById("name");
    var idInput = document.getElementById("id");
    var passwordInput = document.getElementById("password");
    var usernameInput = document.getElementById("username");

    form.addEventListener("submit", function(event) {
        var isValid = true;

        if (nameInput.value === "") {
            isValid = false;
            alert("Please enter your name.");
        }

        if (idInput.value === "") {
            isValid = false;
            alert("Please enter your ID.");
        }

        if (passwordInput.value === "") {
            isValid = false;
            alert("Please enter your password.");
        }

        if (usernameInput.value === "") {
            isValid = false;
            alert("Please enter your username.");
        }

        if (!isValid) {
            event.preventDefault(); 
        }
    });
});

// Home Page ---------
