function clearEditView(postId) {
    // Remove text area, save button and cancel button
    document.getElementById(`textarea_${postId}`).remove()
    document.getElementById(`save_${postId}`).remove()
    document.getElementById(`cancel_${postId}`).remove()

    // Show content, edit button and no. of likes
    document.getElementById(`post_body_${postId}`).style.display = 'block';
    document.getElementById(`edit_${postId}`).style.display = 'inline-block';
    document.getElementById(`post_likes_${postId}`).style.display = 'block';
}

// Adds validation message within parentDiv
function addValidationMsg(message, parentDiv) {
    
    // Adds validation message
    const warningMsg = document.createElement('p');
    warningMsg.innerHTML = message;
    warningMsg.className = `text-danger`;

    // Adds validation message to DOM
    document.getElementById(parentDiv).append(warningMsg);
}

// Updates number of likes for a given ID
function updateLikes(id, likes) {
    let likeCount = document.getElementById(`post_likecount_${id}`);

    if (likes === 1) {
        likeCount.innerHTML = `${likes} like`;
    }
    else {
        likeCount.innerHTML = `${likes} likes`;
    }
}

document.addEventListener('DOMContentLoaded', function() {

    // Add event listener that listens for any clicks on the page
    document.addEventListener('click', event => {
        
        // Save the element the user clicked on
        const element = event.target;

        // If the user clicked on a like icon
        if (element.id.startsWith('post_like_icon_')) {
        
            // Save post ID from data in element
            let id = element.dataset.id;
            
            // Make fetch request to update page without full reload
            fetch(`/updatelike/${id}`, {
                method: "POST"
            })
            .then(function(response) {
                if (response.ok) {
                    return response.json()
                }
                // If response receives an error, rejects the promise and returns an error to the console.
                else {
                    return Promise.reject('There has been an error.')
                }
            }).then(function(data) {
                
                // Saving data from response
                const likes = data.likesCount;
                const likesPost = data.likesPost;

                // Like icon on page
                let likeIcon = document.getElementById(`post_like_icon_${id}`);
                
                // Update no of likes on page
                updateLikes(id, likes)

                // Updates like icon correctly according to whether user likes post or not
                if (likesPost) {
                    likeIcon.className = 'like_icon fa fa-heart fas';
                } else {
                    likeIcon.className = 'like_icon fa fa-heart-o';
                }
                
            }).catch(function(ex) {
                console.log("parsing failed", ex);
            });
        }

        // If the thing the user clicked is the edit button
        if (element.id.startsWith('edit_')) {
            
            // Save necessary variables
            const editButton = element;
            const postId = editButton.dataset.id;
            const postText = document.getElementById(`post_body_${postId}`);

            // Adding prepopulated text area element
            let textArea = document.createElement('textarea');
            textArea.innerHTML = postText.innerHTML;
            textArea.id = `textarea_${postId}`;
            textArea.className = 'form-control';
            document.getElementById(`post_bodygroup${postId}`).append(textArea);

            // Hiding text containing original content
            postText.style.display = 'none';

            // Hiding likes
            document.getElementById(`post_likes_${postId}`).style.display = 'none';

            // Remove edit button
            editButton.style.display = 'none';

            // Adding 'Cancel' button
            const cancelButton = document.createElement('button');
            cancelButton.innerHTML = '<i class="fa fa-times-circle" aria-hidden="true"></i> Cancel';
            cancelButton.className = 'btn btn-outline-danger cancel-badge badge ml-1 text-right btn-sm';
            cancelButton.id = `cancel_${postId}`

            // Adding 'Save' button
            const saveButton = document.createElement('button');
            saveButton.innerHTML = 'Save';
            saveButton.className = 'btn btn-success mt-2 px-2';
            saveButton.id = `save_${postId}`

            // Add save button to DOM
            document.getElementById(`save_buttons_${postId}`).append(saveButton);

            // Event listener for when user clicks new 'Cancel' button
            cancelButton.addEventListener('click', function() {
                clearEditView(postId)
            })
            
            // Add cancel button to DOM
            document.getElementById(`post_header_${postId}`).append(cancelButton)
            

            // Fetch request when the user clicks 'save' button
            saveButton.addEventListener('click', function() {
                
                textArea = document.getElementById(`textarea_${postId}`);
                
                // Make fetch request to update page without full reload
                fetch(`/editpost/${postId}`, {
                    method: 'POST',
                    body: JSON.stringify({
                        // Pass through the new content typed in the text area
                        content: textArea.value,
                    })
                })
                
                .then(response => {
                    if (response.ok || response.status == 400) {
                        return response.json()
                    // Throws error for users who don't have permission (ie users not logged in)
                    } else if(response.status === 404) {
                        clearEditView(postId)
                        
                        // Hide edit button to prevent happening again
                        editButton.style.display = 'none';

                        // Creates validation message
                        addValidationMsg("You are not authorised to do this", `post_contentgroup_${postId}`)

                        // Rejects promise and throws error
                        return Promise.reject('Error 404')

                    } else {
                        return Promise.reject('There has been an error: ' + response.status)
                    } 
                })

                .then(result => {
                    
                    // If successful, load user's sent inbox
                    if (!result.error) {
                    
                        // Sets on screen text to what the user edited
                        postText.innerHTML = result.content;
                        
                        // Removes all edit fields and restores to normal view
                        clearEditView(postId)
                    } 
                    else {
                        clearEditView(postId)

                        // Hide edit button to prevent happening again
                        editButton.style.display = 'none';
                        
                        addValidationMsg(result.error, `post_contentgroup_${postId}`)
                        // Add validation message
                        /* const warningMsg = document.createElement('p');
                        warningMsg.innerHTML = result.error;
                        warningMsg.className = 'text-danger';
                        
                        // add validation message to DOM
                        document.getElementById(`post_contentgroup_${postId}`).append(warningMessage); */
                        
                    }
                })
                .catch(error => {
                    console.error(error);
                })
            })

        }
        



    })

    
    

    
})