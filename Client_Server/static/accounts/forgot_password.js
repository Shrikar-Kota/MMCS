const performOnLoad = () => {
    document.querySelector("#sendemail-btn").addEventListener("click", sendEmail);
};

const sendEmail = (event) => {
    event.preventDefault();
    let postdata = {
        "email": email,
    }
    let csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'post',
        url: resendfmailurl,
        dataType: 'json',
        data: JSON.stringify(postdata),
        headers: { "X-CSRFToken": csrftoken},
        beforeSend: function() {
            document.querySelector("#info-message").classList.add("invisible");
            document.querySelector("#error-message").classList.add("invisible");
            document.querySelector("#resend-vemail").classList.add('invisible');
            document.querySelector("#sendemail-btn").innerHTML = "<div class='spinner-border text-light' role='status'></div>"
        },
        success: function (response){
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
            document.querySelector("#sendemail-btn").innerHTML = "Submit";
            alert("Something went wrong! Try again later!");
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