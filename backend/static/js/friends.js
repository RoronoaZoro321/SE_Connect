console.log("friends.js loaded");

// Disable scrolling on number input
document.addEventListener("wheel", function(event){
    if(document.activeElement.type === "number"){
        document.activeElement.blur();
    }
});

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
    
        if (response.status === 200) {
            console.log("Friend added");
            const data = await response.json();
            document.getElementById('error-message').innerText = "";
            document.getElementById('done-message').innerText = data.message;
            window.location.href = '/friends';
        } else {
            const data = await response.json();
            document.getElementById('done-message').innerText = "";
            document.getElementById('error-message').innerText = data.message;
        }
      } catch (error) {
        console.error('An error occurred:', error);
    }
  });