document.addEventListener('DOMContentLoaded', function() {

    e = document.getElementById('id')
    if (e != null) {
        id = e.value;
        fetch(`/follow/${id}`)
        .then(response => response.json())
        .then(follow => {
            console.log(follow.is_following);
            console.log(id);

            const element = document.createElement('button');
            element.className = "btn btn-sm btn-primary";
            if (follow.is_following) {
                element.innerHTML = "Unfollow";
            }
            else {
                element.innerHTML = "Follow";
            }

            element.addEventListener('click', function() {
                console.log('Oohooo clicked');

                fetch(`/follow/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        follow: !follow.is_following
                    })
                  })
                  .then(() => {
                      console.log('Okay, flicked!');
                  })
            });

            document.querySelector("#follow").append(element);
        })
    }
});