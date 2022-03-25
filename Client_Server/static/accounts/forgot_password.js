var emailid = "";

const performOnLoad = () => {
    document.querySelector("#emailField").value = "";
    document.querySelector("#emailField").addEventListener("input", validateInput);
    document.querySelector("#sendemail-btn").addEventListener("click", sendEmail);
    document.querySelector("#sendemail-btn").disabled = true;
    document.querySelector("#resendvemail-btn").addEventListener("click", resendVerificationEmail);
};

const validateInput = (event) => {
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(event.target.value)){
        emailid = event.target.value;
        document.querySelector("#sendemail-btn").disabled = false;
    }else{
        document.querySelector("#sendemail-btn").disabled = true;
    }
}

const sendEmail = (event) => {
    event.preventDefault();
    let postdata = {
        "email": document.querySelector('#emailField').value,
    }
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'post',
        url: resendfmailurl,
        dataType: 'json',
        data: JSON.stringify(postdata),
        headers: { "X-CSRFToken": csrftoken},
        beforeSend: function() {
            document.querySelector("#sendemail-btn").disabled = true;
            document.querySelector("#info-message").classList.add("invisible");
            document.querySelector("#error-message").classList.add("invisible");
            document.querySelector("#resend-vemail").classList.add('invisible');
            document.querySelector("#resend-vemail-result").classList.add('invisible');
            document.querySelector("#sendemail-btn").innerHTML = "<div class='spinner-border text-light' role='status'></div>"
        },
        success: function (response){
            document.querySelector("#sendemail-btn").disabled = false;
            document.querySelector("#sendemail-btn").innerHTML = "Submit";
            if (response['message'] == 'success'){
                document.querySelector("#info-message").classList.remove("invisible");
            }else if (response['message'] == 'error'){
                document.querySelector("#error-message").classList.remove("invisible");
            } else{
                document.querySelector("#resend-vemail").classList.remove("invisible");
            }
        },
        error: function(){
            document.querySelector("#sendemail-btn").disabled = false;
            document.querySelector("#sendemail-btn").innerHTML = "Submit";
            window.location.href = homeurl;
        }
    })
}

const resendVerificationEmail = (event) => {
    event.preventDefault();
    let postdata = {
        "email": emailid,
    }
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'post',
        url: resendvmailurl,
        dataType: 'json',
        data: JSON.stringify(postdata),
        headers: { "X-CSRFToken": csrftoken},
        beforeSend: function() {
            document.querySelector("#resendvemail-btn").removeEventListener("click", resendVerificationEmail);
            document.querySelector("#resend-vemail-result").classList.add('invisible');
        },
        success: function (response){
            document.querySelector("#resendvemail-btn").addEventListener("click", resendVerificationEmail);
            if (response['message'] == 'success'){
                document.querySelector("#resend-vemail-result").innerHTML = "(Email has been re-sent successfullly!)";
                document.querySelector("#resend-vemail-result").classList.remove("invisible");
            }else if (response['message'] == 'error'){
                document.querySelector("#resend-vemail-result").innerHTML = "<span class='text-danger'>(An error occured while sending the email. Please try again later.)</span>";
                document.querySelector("#resend-vemail-result").classList.remove("invisible");
            } else{
                window.location.href = homeurl;
            }
        },
        error: function(){
            document.querySelector("#resendvemail-btn").addEventListener("click", resendVerificationEmail);
            window.location.href = homeurl;
        }
    })
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