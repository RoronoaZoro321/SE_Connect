document.addEventListener("DOMContentLoaded", start)

function start() {
    document.getElementById("newPostForm").addEventListener("submit", async (event) => {
        event.preventDefault()

        const message = document.getElementById("message").value
        const postResponse = await fetch("/newPost", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: message })
        })

        if (postResponse.status == 200) {
            location.reload()
        } else {
            console.log("status code" + postResponse.status);
        }
    })

    // document.getElementById("like").addEventListener("click", () => {
    //     (async () => {
    //         const rawResponse = await fetch('/api/like', {
    //             method: 'POST',
    //             headers: {
    //                 'Accept': 'application/json',
    //                 'Content-Type': 'application/json'
    //             },
    //             body: JSON.stringify({ student_id, username, post_id })
    //             //  student_id: int
    //             // username: str
    //             // post_id: int
    //         });
    //         const content = await rawResponse.json();

    //         console.log(content);
    //     })();
    // })

    // document.getElementById("comment")
}

function like(postId) {
    (async () => {
        const res = await fetch(`/api/like/${postId}`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json'
            },
            credentials: "include"
        });

        if (res.status == 200) {
            const message = await res.json();
            const likeNum = document.getElementById(`likeNum${postId}`)
            const likeButton = document.getElementById(`likeButton${postId}`)

            if (message.data == "like") 
            {
                likeNum.innerText = parseInt(likeNum.innerText) + 1
                likeButton.innerText = "Unlike"
            }
            else if (message.data == "unlike") 
            {
                likeNum.innerText = parseInt(likeNum.innerText) - 1
                likeButton.innerText = "Like"
            }
            else console.log("Error: Unknown message data type in like func");
        }
    })();
}

function comment(postId) {

}