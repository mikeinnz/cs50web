document.addEventListener('DOMContentLoaded', function() {
    load_follow_btn();
});

function load_follow_btn() {
    e = document.getElementById('profile_id');
    if (e != null) {
        id = e.value;
        fetch(`/follow/${id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data.is_following);
            console.log(id);

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
                })
                
            });

            document.getElementById('followbtn').append(element);
        })
    }
}