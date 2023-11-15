document.addEventListener("DOMContentLoaded", start)

function start() {
    const tx = document.getElementsByTagName("textarea");
    for (let i = 0; i < tx.length; i++) {
        tx[i].setAttribute("style", tx[i].style.cssText + "height:" + (tx[i].scrollHeight) + "px");
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

function comment(postId, username) {
    const comment = document.getElementById(`commentForm${postId}`).value
    if (!comment) {
        // Does comment promp already exist
        if (document.getElementById(`commentPrompt${postId}`)) return

        const col1 = document.getElementById(`col1${postId}`)
        const p = document.createElement("p")
        p.style = "text-align: center; color: red;"
        p.innerText = "Please Type Something"
        p.id = `commentPrompt${postId}`
        col1.appendChild(p);
        return
    }

    // Remove comment prompt after successfully commenting
    const commentPrompt = document.getElementById(`commentPrompt${postId}`)
    if (commentPrompt) commentPrompt.remove();

    (async () => {
        const res = await fetch(`/api/comment/${postId}`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: comment }),
            credentials: "include"
        });

        const message = await res.json();
        if (res.status == 200) {
            console.log(message);

            // Update DOM
            document.getElementById(`commentForm${postId}`).value = ""
            toggleCommentForm(postId)
            let commentsCount = document.getElementById(`commentsCount${postId}`)
            let showCommentsButton = document.getElementById(`showCommentsButton${postId}`)

            if (!commentsCount && !showCommentsButton) {
                showCommentsButton = document.createElement("button")
                commentsCount = document.createElement("span")
                const p = document.createElement("p")
                const commentFormDiv = document.getElementById(`commentFormDiv${postId}`)

                showCommentsButton.id = `showCommentsButton${postId}`
                showCommentsButton.onclick = () => { toggleShowComments(postId) }
                showCommentsButton.innerText = "Show Comments"
                commentsCount.id = `commentsCount${postId}`
                commentsCount.innerText = "1"

                p.append(commentsCount, " comment")
                commentFormDiv.insertAdjacentElement("afterend", p)
                commentFormDiv.insertAdjacentElement("afterend", showCommentsButton)
            } else {
                commentsCount.innerText = parseInt(commentsCount.innerText) + 1
                commentsCount.parentElement.lastChild.data = " comments"
            }

            // New comment
            const li = document.createElement("li")
            const timeSpan = document.createElement("span")
            const userDataP = document.createElement("p")
            const commentTextP = document.createElement("p")

            timeSpan.className = "time"
            timeSpan.innerText = "Just now"
            userDataP.appendChild(timeSpan)
            userDataP.insertAdjacentText("afterbegin", username + " ")
            userDataP.insertAdjacentText("beforeend", " :")
            commentTextP.innerText = comment
            li.append(userDataP, commentTextP)

            // Show new comment
            const commentsList = document.getElementById(`commentsList${postId}`)
            commentsList.prepend(li)
        }
        else console.error(message)
    })();
}

function toggleCommentForm(postId) {
    const commentFormDiv = document.getElementById(`commentFormDiv${postId}`)
    commentFormDiv.style = commentFormDiv.style.cssText ? "" : "display: none;"
}

function toggleShowComments(postId) {
    const commentsList = document.getElementById(`commentsList${postId}`)
    const showCommentsButton = document.getElementById(`showCommentsButton${postId}`)
    const areCommentsHidden = Boolean(commentsList.style.cssText)

    // toggle visibility
    commentsList.style.cssText = areCommentsHidden ? "" : "display: none;"
    // visibility is now toggled
    showCommentsButton.innerText = areCommentsHidden ? "Hide Comments" : "Show Comments"
}