document.addEventListener("DOMContentLoaded", start)

function start() {
    const tx = document.getElementsByTagName("textarea");
    for (let i = 0; i < tx.length; i++) {
        tx[i].setAttribute("style", tx[i].style.cssText + "height:" + (tx[i].scrollHeight) + "px;overflow-y:hidden;");
        tx[i].addEventListener("input", OnInput, false);
    }
    
    function OnInput() {
        this.style.height = 0;
        this.style.height = (this.scrollHeight) + "px";
    }

    document.getElementById("newPostForm").addEventListener("submit", async (event) => {
        event.preventDefault()

        const message = document.getElementById("message").value
        const postResponse = await fetch("/api/newPost", {
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

            if (message.data == "like") {
                likeNum.innerText = parseInt(likeNum.innerText) + 1
                likeButton.innerText = "Unlike"
            }
            else if (message.data == "unlike") {
                likeNum.innerText = parseInt(likeNum.innerText) - 1
                likeButton.innerText = "Like"
            }
            else console.log("Error: Unknown message data type in like func");
        }
    })();
}

function comment(postId) {

}