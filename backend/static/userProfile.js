console.log("userProfile.js loaded")

document.getElementById('userProfileForm').addEventListener('submit', async (event) => {
    event.preventDefault();
  
    const age = parseInt(document.getElementById('age').value);
    const description = document.getElementById('description').value;

    const data = {
        age: age,
        description: description,
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
        const response = await fetch('/userProfile', options);
        console.log(response);
    
        if (response.ok) {
            const data = await response.json();
            document.getElementById('done-message').innerText = data.message;
        } else {
            const data = await response.json();
            document.getElementById('error-message').innerText = data.message;
        }
      } catch (error) {
        console.error('An error occurred:', error);
    }
  });