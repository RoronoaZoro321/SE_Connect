console.log("friends.js loaded");

document.getElementById('friends-form').addEventListener('submit', async (event) => {
    event.preventDefault();
  
    const friend_id = parseInt(document.getElementById('friend_id').value);

    const data = {
        friend_id: friend_id,
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
        const response = await fetch('/add_friend', options);
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