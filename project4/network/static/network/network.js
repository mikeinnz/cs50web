document.addEventListener('DOMContentLoaded', function() {
    load_follow_btn();

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
            text.value = content.innerHTML; // TODO: save  & load content when Edit is toggled
            // set cursor at the end in a textarea
            text.setSelectionRange(text.value.length, text.value.length);


            // When 'Save' button is clicked, save to database
            document.getElementById(`edit-form-${postid}`).onsubmit = () => {

                // Update database
                fetch(`/edit/${postid}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: text.value
                    })
                })
                .then(response => response.json())
                .then(result => {
                    if (result.error) {
                        alert(result.error);
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
                fetch(`/follow/${id}`, {
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