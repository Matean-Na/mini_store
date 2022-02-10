const postForm = document.querySelector("#PostCreateForm");


function handleSubmit(postForm) {
    postForm.addEventListener("submit", e => {
        e.preventDefault();
        formData = new FormData(postForm);
        fetch('/account/profile/', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                postForm.reset();
                // document.querySelector("#notify").innerHTML = `<div class="alert alert-info alert-dismissible fade show" role="alert">
                //                                                   <strong>Успех!</strong> ${data.username} <strong>сохранен</strong>.
                //                                                   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                //                                                 </div> `
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        
        let my_form = document.forms.my;
        let form_username = my_form.elements.username;
        let form_email = my_form.elements.email;
        let form_first_name = my_form.elements.first_name;
        let form_last_name = my_form.elements.last_name;

        let login = document.querySelector('#login');
        let email = document.querySelector('#email');
        let first_name = document.querySelector('#first_name');
        let last_name = document.querySelector('#last_name');

        login.textContent = form_username.value;
        email.textContent = form_email.value;
        first_name.textContent = form_first_name.value;
        last_name.textContent = form_last_name.value;

    })

}

handleSubmit(postForm)