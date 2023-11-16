console.log('startUpAdd.js loaded');
let count = 1;

function addMoreRows() {
    let formInput = document.getElementById("form-input");
    count+=1;
    let ret = 
    `
        <div id="form-group${count}" class="second">
            <div class="c">
                <label for="sktitle${count}">
                Skill Title:</label>
                <input type="text" id="sktitle${count}" name="sktitle" value="" required>
            </div>
            <div class="d">
                <label for="skdescription${count}">
                Skill Description:</label>
                <textarea name="skdescription${count}" id="skdescription${count}" cols="30" rows="4"></textarea>    
            </div>
            <button type="button" onclick="removeRow(${count})" >Remove</button>
        </div>
    `
    formInput.insertAdjacentHTML("beforeend", ret);
}

function removeRow(countToRemove) {
    let formGroup = document.getElementById(`form-group${countToRemove}`);
    formGroup.remove();

    // Update the count and renumber the remaining rows
    count -= 1;
    for (let i = countToRemove + 1; i <= count + 1; i++) {
        let currentFormGroup = document.getElementById(`form-group${i}`);
        currentFormGroup.id = `form-group${i - 1}`;
        currentFormGroup.querySelector(`[for="sktitle${i}"]`).htmlFor = `sktitle${i - 1}`;
        currentFormGroup.querySelector(`#sktitle${i}`).id = `sktitle${i - 1}`;
        currentFormGroup.querySelector(`[for="skdescription${i}"]`).htmlFor = `skdescription${i - 1}`;
        currentFormGroup.querySelector(`#skdescription${i}`).id = `skdescription${i - 1}`;
        currentFormGroup.querySelector(`button`).setAttribute("onclick", `removeRow(${i - 1})`);
    }
}

document.getElementById("form").addEventListener("submit", async (event) => {
    event.preventDefault();
  
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    
    // Extract all skills dynamically
    const skills = [];
    for (let i = 1; i <= count; i++) {
        const skillTitle = document.getElementById(`sktitle${i}`).value;
        const skillDescription = document.getElementById(`skdescription${i}`).value;

        skills.push({
            title: skillTitle,
            description: skillDescription
        });
    }

    const data = {
        title: title,
        description: description,
        skills: skills
    };
    
    const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    };
  
    try {
        const response = await fetch('/startupAdd', options);
        console.log(response);
    
        if (response.ok) {
          // Login was successful, redirect to the /home page
          window.location.href = '/startup'; // Change to the correct URL
        } else {
          document.getElementById('error-message').innerText = 'Create Post failed';
        }
      } catch (error) {
        console.error('An error occurred:', error);
    }
  });

// function scrollToBottom() {
//     window.scrollTo(0, document.body.scrollHeight);
// }

// window.onload = scrollToBottom;