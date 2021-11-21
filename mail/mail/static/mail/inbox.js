document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Compose email
  document.querySelector('form').onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      if (result.error) {
        alert(result.error);
      }
      load_mailbox('sent');
    })

    // Prevent form from submitting
    return false;
  }

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails from server
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {  
    // add each email to the mailbox
    emails.forEach(add_email)
  });

  // Add email to the mailbox
  function add_email(email) {
    const element = document.createElement('div');
    element.className = 'email-item';
    if (email.read) {
      element.style.backgroundColor = 'lightgrey';
    }

    element.innerHTML = `<div class="address">${email.sender}</div>
                          <div class="subject">${email.subject}</div>
                          <div class="timestamp">${email.timestamp}</div>`;
    
    // Display email's content when clicked
    element.addEventListener('click', function() {
      fetch(`/emails/${email.id}`)
      .then(response => response.json())
      .then(email => {
        // clear out all existing contents
        document.querySelector('#email-view').innerHTML = '';

        const content = document.createElement('div');
        content.className = 'email-content';
        
        // Create archive/unarchive button for all inboxes except Sent inbox
        if (!(mailbox === 'sent')) {
          const archivebtn = document.createElement('button');
          archivebtn.className = 'btn btn-sm btn-outline-primary';
          if (!email.archived) {
            archivebtn.id = 'archive';
            archivebtn.innerHTML = 'Archive';
            // Alternatively use this simple HTML element
            // content.innerHTML += `<button id="archive" class="btn btn-sm btn-outline-primary">Archive</button>`;
          }
          else {
            archivebtn.id = 'unarchive';
            archivebtn.innerHTML = 'Unarchive';
            // Alternatively use this simple HTML element
            //content.innerHTML += `<button id="unarchive" class="btn btn-sm btn-outline-primary">Unarchive</button>`;
          }
          content.append(archivebtn);
        }

        // Create email content
        content.innerHTML += `<div><strong>From:</strong> ${email.sender}</div>
                             <div><strong>To:</strong> ${email.recipients}</div>
                             <div><strong>Subject:</strong> ${email.subject}</div>
                             <div><strong>Timestamp:</strong> ${email.timestamp}</div>
                             <button id="reply" class="btn btn-sm btn-outline-primary">Reply</button>
                             <hr>
                             <div>${email.body.replace(/\r?\n/g, '<br />')}</div>`; // format body
        
        // Add email content to view
        document.querySelector('#email-view').append(content);

        // Archive/unarchive email if button is clicked
        if (!(mailbox === 'sent')) {
          if (!email.archived) {
            document.querySelector('#archive').addEventListener('click', archive_clicked(email.id, email.archived));
          }
          else {
            document.querySelector('#unarchive').addEventListener('click', archive_clicked(email.id, email.archived));
          }
        }
        
        // Reply action
        document.querySelector('#reply').addEventListener('click', () => reply_email(email));

      });

    
      // Show email view and hide other views
      document.querySelector('#email-view').style.display = 'block';
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';

      // Mark email as read
      if (!email.read) {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
      }
    });

    // add email to inbox view
    document.querySelector('#emails-view').append(element);
  }

  // Archive email
  function archive_clicked(id, value) {
    return function() {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !value
        })
      })
      .then(() => load_mailbox('inbox'));
    }
  }

  // Reply to an email
  function reply_email(email) {

    // Pre-fill receipient
    if (mailbox === 'sent') {
      document.querySelector('#compose-recipients').value = email.recipients;
    }
    else {
      document.querySelector('#compose-recipients').value = email.sender;
    }

    // Pre-fill subject and add Re: if none
    if (email.subject.startsWith('Re:')) {
      document.querySelector('#compose-subject').value = email.subject;
    }
    else {
      document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
    }

    // Pre-fill body with text
    document.querySelector('#compose-body').value = `\nOn ${email.timestamp} ${email.sender} wrote: \n${email.body}`;

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-view').style.display = 'none';
  }

}
