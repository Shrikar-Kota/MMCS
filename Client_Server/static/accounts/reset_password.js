const performOnLoad = () => {
    document.querySelectorAll(".info-symbol").forEach(ele => {
        ele.addEventListener("mouseenter", displayInfo);
        ele.addEventListener("mouseleave", hideInfo);
    })
    document.querySelectorAll(".input-field").forEach(ele => {
        ele.value = '';
        ele.addEventListener("input", validateInput);
    })
    document.querySelector("#resetp-btn").addEventListener("click", resetPassword)
};

const displayInfo = (event) => {
    let infos = {
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
            document.querySelector("#resetp-btn").disabled = false;
        }
    }else{
        event.target.classList.add("red-border");
        document.querySelector("#resetp-btn").disabled = true;
    }
}

const validateFields = (fieldname) => {
    var count = 0;
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
    return (count == 2);
}

const resetPassword = (event) => {
    event.preventDefault();
    if (validateFields("all")){
        let postdata = {
            "token": token,
            "password": document.querySelector("#passwordField").value
        }
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'post',
            url: accountsresetpasswordurl,
            dataType: 'json',
            data: JSON.stringify(postdata),
            headers: { "X-CSRFToken": csrftoken},
            beforeSend: function() {
                document.querySelector("#resetp-btn").disabled = true;
                document.querySelector("#resetp-btn").innerHTML = "<div class='spinner-border text-light' role='status'></div>";
            },
            success: function (response){
                document.querySelector("#resetp-btn").disabled = false;
                document.querySelector("#resetp-btn").innerHTML = "Reset";
                if (response['message'] == 'invalid'){
                    document.querySelector("#invalid-token").classList.remove("invisible");
                    document.querySelector("#reset-password-window").classList.add("invisible");
                    document.querySelector("#reset-password-window").innerHTML = "";
                    document.querySelector("#reset-successful").classList.add("invisible");
                    document.querySelector("#reset-successful").innerHTML = "";
                }else{
                    document.querySelector("#invalid-token").classList.add("invisible");
                    document.querySelector("#invalid-token").innerHTML = "";
                    document.querySelector("#reset-password-window").classList.add("invisible");
                    document.querySelector("#reset-password-window").innerHTML = "";
                    document.querySelector("#reset-successful").classList.remove("invisible");
                }
            },
            error: function(){
                document.querySelector("#resetp-btn").disabled = false;
                document.querySelector("#resetp-btn").innerHTML = "Reset";
                window.location.href = homeurl;
            }
        })
    }else{
        document.querySelector("#resetp-btn").disabled = true;
    }
}

const getCookie = (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}