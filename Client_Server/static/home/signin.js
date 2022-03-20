const performOnLoad = () => {
    document.querySelectorAll(".input-field").forEach(ele => {
        ele.value = '';
        ele.addEventListener("input", validateInput);
    })
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