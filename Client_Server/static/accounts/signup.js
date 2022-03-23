const performOnLoad = () => {
    document.querySelectorAll(".info-symbol").forEach(ele => {
        ele.addEventListener("mouseenter", displayInfo);
        ele.addEventListener("mouseleave", hideInfo);
    })
    document.querySelectorAll(".input-field").forEach(ele => {
        ele.value = '';
        ele.addEventListener("input", validateInput);
    })
    document.querySelector("#confirmPasswordField").addEventListener("click", validateInput);
    document.querySelector("#signup-btn").addEventListener("click", registerUser);
};

const displayInfo = (event) => {
    let infos = {
        "userNameFieldInfo": "User Name: <br>- Should contain only english alphabet letters and numbers.<br>- Should start with a capital letter of english alphabet.<br>- Should atleast be 8 characters long.<br>- Should not contain any spaces.<br>- Should not contain any special characters other than _ (underscore).",
        "passwordFieldInfo": "Password: <br>- Should contain only english alphabet letters and numbers.<br>- Should contain atleast one uppercase english alphabet letter.<br>- Should atleast be 8 characters long.<br>- Should not contain any special characters and white spaces."
    }
    let infodialog = document.querySelector("#info-dialog");
    infodialog.innerHTML = infos[event.target.id];
    infodialog.style.left = event.clientX + "px", infodialog.style.top = event.clientY + "px";
    infodialog.classList.remove('invisible');
}

const hideInfo = (event) => {
    let infodialog = document.querySelector("#info-dialog");
    infodialog.classList.add('invisible');
    infodialog.innerHTML = '';
}

const validateInput = (event) => {
    if (validateFields(event.target.id)){
        event.target.classList.remove("red-border");
        if (validateFields("all")){
            document.querySelector("#signup-btn").disabled = false;
        }
    }else{
        event.target.classList.add("red-border");
        document.querySelector("#signup-btn").disabled = true;
    }
}

const validateFields = (fieldname) => {
    var count = 0;
    if (fieldname == "userNameField" || fieldname == "all"){
        let inputName = "#userNameField";
        if (/^[A-Z]([a-zA-Z]|_|[0-9])*$/.test(document.querySelector(inputName).value) && document.querySelector(inputName).value.length >= 8){
            if (fieldname == "all"){
                count += 1;
            }else{
                return true;
            }
        }else{
            if (fieldname != "all"){
                return false;
            }
        }
    } 
    if (fieldname == "emailField" || fieldname == "all"){
        let inputName = "#emailField";
        if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(document.querySelector(inputName).value)){
            if (fieldname == "all"){
                count += 1;
            }else{
                return true;
            }
        }else{
            if (fieldname != "all"){
                return false;
            }
        }
    }
    if (fieldname == "passwordField" || fieldname == "all"){
        let inputName = "#passwordField";
        if (/([A-Za-z]|[0-9])*[A-Z]([A-Za-z]|[0-9])*$/.test(document.querySelector(inputName).value) && document.querySelector(inputName).value.length >= 8){
            if (fieldname == "all"){
                count += 1;
            }else{
                return true;
            }
        }else{
            if (fieldname != "all"){
                return false;
            }
        }
    }
    if (fieldname == "confirmPasswordField" || fieldname == "all"){
        let inputName = "#confirmPasswordField";
        if ((/([A-Za-z]|[0-9])*[A-Z]([A-Za-z]|[0-9])*$/.test(document.querySelector(inputName).value)) && ((document.querySelector(inputName).value === document.querySelector("#passwordField").value) && document.querySelector(inputName).value.length >= 8)){
            if (fieldname == "all"){
                count += 1;
            }else{
                return true;
            }
        }else{
            if (fieldname != "all"){
                return false;
            }
        }
    }
    return (count == 4);
}

const registerUser = (event) => {
    event.preventDefault();
    if (validateFields("all")){
        let registrationdata = {
            "username": document.querySelector("#userNameField").value,
            "email": document.querySelector("#emailField").value,
            "password": document.querySelector("#passwordField").value 
        }
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'post',
            url: registrationurl,
            dataType: 'json',
            data: JSON.stringify(registrationdata),
            headers: { "X-CSRFToken": csrftoken},
            beforeSend: function() {
                document.querySelector("#error-message").classList.add("invisible")
            },
            success: function (response){
                if (response['message'] == 'Error'){
                    document.querySelector("#error-message").classList.remove("invisible");
                    document.querySelector("#emailField").focus();
                }else{
                    window.location.href = accounts_home;
                }
            },
            error: function(){
                alert("Something went wrong! Try again later!");
            }
        })
    }else{
        document.querySelector("#signup-btn").disabled = true;
    }
}

const getCookie = (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}