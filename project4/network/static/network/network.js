document.addEventListener('DOMContentLoaded', function() {
    load_follow_btn();

    load_edit_form();

    load_likes();
});


function load_follow_btn() {
    e = document.getElementById('profile_id');
    if (e != null) {
        id = e.value;
        fetch(`/follow/${id}`)
        .then(response => response.json())
        .then(data => {

            // Update number of followers
            document.getElementById('num_followers').innerHTML = data.num_followers;

            // Clear out existing contents
            document.getElementById('followbtn').innerHTML = '';

            // Dynamically create follow button
            const element = document.createElement('button');
            element.className = 'btn btn-sm btn-primary';
            if (data.is_following) {
                element.innerHTML = 'Unfollow';
            }
            else {
                element.innerHTML = 'Follow';
            }

            element.addEventListener('click', function() {
                // Update database
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const request = new Request(
                    `/follow/${id}`,
                    {headers: {'X-CSRFToken': csrftoken}}
                );

                fetch(request, {
                    method: 'PUT',
                    body: JSON.stringify({
                        follow: !data.is_following
                    })
                })
                .then(() => {
                    load_follow_btn();
                });
                
            });

            document.getElementById('followbtn').append(element);
        });
    };
}

function load_edit_form() {
    // Hide all Edit forms
    const elements = document.querySelectorAll('.edit-block');
    for (let element of elements) {
        element.style.display = 'none';
    }

    // Event for 'Edit' link for posts belonging to the current user
    document.querySelectorAll('.edit-link').forEach(function(link) {
        link.addEventListener('click', function(event) {
            // Get post's id
            const postid = link.dataset.postid;

            const content = document.getElementById(`post-content-${postid}`);
            const editblock = document.getElementById(`edit-block-${postid}`);

            // Give 'Edit' button an ability to toggle textarea
            if (content.style.display === 'none') {
                content.style.display = 'block';
                editblock.style.display = 'none';
            }
            else {
                // hide post content
                content.style.display = 'none';
                // show 'edit' textarea
                editblock.style.display = 'block';
            }

            const text = document.getElementById(`edit-text-${postid}`);
            text.focus();
            // pre-fill 'edit' textarea with post content
            text.value = content.innerHTML;
            // set cursor at the end in a textarea
            text.setSelectionRange(text.value.length, text.value.length);
            
            // When 'Save' button is clicked, save to database
            document.getElementById(`edit-form-${postid}`).onsubmit = () => {
                
                // Update database
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const request = new Request(
                    `/edit/${postid}`,
                    {headers: {'X-CSRFToken': csrftoken}}
                );

                fetch(request, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: text.value
                    })
                })
                .then(response => response.json())
                .then(result => {
                    if (result.error) {
                        alert(result.error);
                        return false;
                    }
                    // Reload the elements with new content
                    editblock.style.display = 'none';
                    content.innerHTML = text.value;
                    content.style.display = 'block';

                });

                // Prevent form from submitting
                return false;
            };


            // Prevent the link from working as an anchor tag
            event.preventDefault();
        });
    });
}


function load_likes() {
    // Event for each like button
    document.querySelectorAll('.like-icon').forEach(function(like) {

        const postid = like.dataset.postid;
        
        const num_likes = document.getElementById(`num-likes-${postid}`);
        
        // Query server to see whether the post is liked by the current user or not
        fetch(`/post/${postid}`)
        .then(response => response.json())
        .then(post => {

            // dynamically display number of likes
            num_likes.innerHTML = post.num_likes;

            // if not liked by current user, change opacity
            if (!post.liked) {
                like.style.opacity = "0.4";
            }

            // Click event for like icon
            like.addEventListener('click', function() {
                
                // Only proceed if user is logged in
                if (post.logged_in) {
                    // Update number of likes without querying database
                    if (like.style.opacity == "0.4") {
                        like.style.opacity = "1";
                        num_likes.innerHTML = parseInt(num_likes.innerHTML) + 1;
                    }
                    else {
                        like.style.opacity = "0.4";
                        num_likes.innerHTML = parseInt(num_likes.innerHTML) - 1;
                    }

                    // Update database
                    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                    const request = new Request(
                        `/post/${postid}`,
                        {headers: {'X-CSRFToken': csrftoken}}
                    );
                    fetch(request, {
                        method: "PUT",
                        body: JSON.stringify({
                            like: !post.liked
                        })
                    })
                }
            });
        })
    });
}