like_button = document.getElementById("like").addEventListener("click", () => {
    (async () => {
        const rawResponse = await fetch('/api/like', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ student_id, username, post_id })
    //  student_id: int
    // username: str
    // post_id: int
        });
        const content = await rawResponse.json();

        console.log(content);
    })();
})
comment_button = document.getElementById("comment")

like_button.addEve