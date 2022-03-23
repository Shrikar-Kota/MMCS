const performOnLoad = () => {
    document.querySelectorAll(".input-field").forEach(ele => {
        ele.value = '';
        ele.addEventListener("input", validateInput);
    })
    document.querySelector("#signin-btn").addEventListener("click", loginUser);
};
const validateInput = (event) => {
    if (validateFields(event.target.id)){
        event.target.classList.remove("red-border");
        if (validateFields("all")){
            document.querySelector("#signin-btn").disabled = false;
        }
    }else{
        event.target.classList.add("red-border");
        document.querySelector("#signin-btn").disabled = true;
    }
}
const validateFields = (fieldname) => {
    var count = 0; 
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
    return (count == 2);
}

const loginUser = (event) => {
    event.preventDefault();
    if (validateFields("all")){
        let registrationdata = {
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
                    alert("Login done!")
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