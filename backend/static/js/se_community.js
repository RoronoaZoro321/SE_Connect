document.addEventListener("DOMContentLoaded", start)

function start() {
    // Scroll to correct section on page reload if has hash
    const hasHash = Boolean(window.location.hash)
    if (hasHash) scrollToPost()

    // Scroll to correct section on hash change (no reload)
    addEventListener("hashchange", (_) => { scrollToPost() })

    function scrollToPost() {
        const hashElement = document.getElementById(window.location.hash.split("#")[1])
        const overlay = document.getElementById("overlay")

        // Scroll to view
        // hashElement.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" })
        hashElement.scrollIntoView(true)

        // Scroll more
        overlay.scrollBy(0, -100)
        // setTimeout(() => { overlay.scrollBy({ behavior: "smooth", top: "-100" }) }, 100)
        // overlay.scrollBy({behavior: "smooth", top: "-100"})

        // Highlight post
        hashElement.style.cssText = "box-shadow: 0px 0px 10px blue; border: 1px solid blue; transition: 1s"
        setTimeout(() => { hashElement.style.cssText = "transition: 1s" }, 1000)
        setTimeout(() => { hashElement.style.cssText = "" }, 2000)
    }

    // Auto adjust new-post form text area height
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
        const imageFiles = document.getElementById('imageUpload').files;
        const formData = new FormData()
        formData.append("text", message)
        if (imageFiles.length !== 0) formData.append("image", imageFiles[0])


        const postResponse = await fetch("/api/newPost", {
            method: "POST",
            headers: {
                'Accept': 'application/json'
            },
            body: formData
        })

        if (postResponse.status == 200) {
            location.reload()
        } else {
            console.error("Error: " + await postResponse.text())
            console.error("status code" + postResponse.status);
        }
    })

    // Show image preview
    const inputFile = document.getElementById('imageUpload');

    inputFile.addEventListener('change', async function () {
        const file = document.querySelector('#imageUpload').files;
        const img = await convert_to_base64(file[0]);
        toggleImagePreview(img)
    })

    const convert_to_base64 = file => new Promise((response) => {
        const file_reader = new FileReader();
        file_reader.readAsDataURL(file);
        file_reader.onload = () => response(file_reader.result);
    });

}

function toggleImagePreview(img) {
    const imgPreviewDiv = document.getElementById("imageUploadPreview")
    const removeImgButton = document.getElementById("removeImageUploadPreviewButton")
    if (img) {
        imgPreviewDiv.style.cssText = ""
        removeImgButton.style.cssText = ""
        imgPreviewDiv.style.backgroundImage = `url(${img})`
    } else {
        imgPreviewDiv.style.cssText = "display: none;"
        removeImgButton.style.cssText = "display: none;"
        document.querySelector('#imageUpload').value = "";
    }
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
            const staticImagesPath = document.location.origin + "/static/images" 

            if (message.data == "like") {
                const imagePath = staticImagesPath + "/liked.png"
                likeNum.innerText = parseInt(likeNum.innerText) + 1

                const unlikeImage = document.createElement("img")
                unlikeImage.width = 15
                unlikeImage.alt = "Post Image"
                unlikeImage.src = imagePath
                likeButton.replaceChildren(unlikeImage)
            }
            else if (message.data == "unlike") {
                const imagePath = staticImagesPath + "/like.png"
                likeNum.innerText = parseInt(likeNum.innerText) - 1

                const likeImage = document.createElement("img")
                likeImage.width = 15
                likeImage.alt = "Post Image"
                likeImage.src = imagePath
                likeButton.replaceChildren(likeImage)
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

function share(postId) {
    navigator.clipboard.writeText(document.location.host + document.location.pathname + `#post${postId}`);

    const tooltip = document.getElementById(`toolTipText${postId}`);
    tooltip.style.visibility = "visible"
    tooltip.style.opacity = 1

    setTimeout(() => { tooltip.style.visibility = "hidden"; tooltip.style.opacity = 0 }, 2000)
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