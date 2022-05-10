const performOnLoad = () => {
    document.querySelector("#header-home").classList.add("active");
    document.querySelector('#uploadbtn').addEventListener('click', uploadOnClick);
    document.querySelector("#info-symbol").addEventListener('mouseenter', displayInfo);
    document.querySelector("#info-symbol").addEventListener('mouseleave', hideInfo);
    document.querySelector(".custom-file-input").addEventListener("change", (event) => {
        document.querySelector("#success-message").classList.add("invisible");
        document.querySelector("#error-message").classList.add("invisible");
        var fileName = event.target.value.split("\\").pop();
        event.target.nextElementSibling.innerHTML = fileName;
    });
    addEventsToGenerateSummaryButtons();
}

const uploadOnClick = () => {
    document.querySelector("#success-message").classList.add("invisible");
    document.querySelector("#error-message").classList.add("invisible");
    if (document.querySelector('#fileinput').files.length == 0) {
        document.querySelector("#error-message").innerHTML = "No file selected.";
        document.querySelector("#error-message").classList.remove("invisible");
        return;
    }
    let file = document.querySelector('#fileinput').files[0];
    let allowed_mime_types = ['audio/mpeg', 'audio/wav', 'video/mp4', 'video/mkv', 'video/mov', 'video/mpeg','application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'application/pdf'];
    let allowed_size_mb = 1024;

    if (allowed_mime_types.indexOf(file.type) == -1) {
        document.querySelector("#error-message").innerHTML = "Incorrect file type";
        document.querySelector("#error-message").classList.remove("invisible");
        return;
    }

    if (file.size > allowed_size_mb * 1024 * 1024) {
        document.querySelector("#error-message").innerHTML = "Exceeded size";
        document.querySelector("#error-message").classList.remove("invisible");
        return;
    }

    uploadToServer();
}

const displayInfo = (event) => {
    let info = "Allowed file types:<br> - <b>Text: </b>doc, docx, pdf, odt, txt<br> -<b> Video: </b>mp4, mkv, mov<br> - <b>Audio: </b>mp3, wav, mpeg<br><br>Maximum file size:<br> - <b>1GB</b>";
    let infodialog = document.querySelector("#info-dialog");
    infodialog.innerHTML = info;
    infodialog.style.left = event.clientX + "px", infodialog.style.top = event.clientY + "px";
    infodialog.classList.remove('invisible');
}

const hideInfo = (event) => {
    let infodialog = document.querySelector("#info-dialog");
    infodialog.classList.add('invisible');
    infodialog.innerHTML = '';
}

const uploadToServer = () => {
    const input = document.querySelector("#fileinput");
    const cancelBtn = document.querySelector("#cancelbtn");
    const uploadBtn = document.querySelector("#uploadbtn");
    const progressBox = document.querySelector("#progressdiv");

    const media_data = input.files[0];
    const media_type = media_data.type.split("/")[0] === 'application' ? "TEXT" : media_data.type.split("/")[0].toUpperCase();
    const media_extension = getMediaExtension(media_data.type);
    const csrftoken = getCookie('csrftoken');
    const fd = new FormData();
    fd.append('uploadedFile', media_data);
    fd.append('type', media_type);
    fd.append('extension', media_extension);
    $.ajax({
        type: 'POST',
        url: homeurl,
        enctype: 'multipart/form-data',
        headers: { "X-CSRFToken": csrftoken },
        data: fd,
        beforeSend: function () {
            uploadBtn.classList.add('invisible');
            cancelBtn.classList.remove('invisible');
            input.files = new DataTransfer().files;
            progressBox.classList.remove("invisible");
            document.querySelector(".custom-file-input").nextElementSibling.innerHTML = "Choose file";
        },
        xhr: function () {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e => {
                if (e.lengthComputable) {
                    const percent = e.loaded / e.total * 100;
                    progressBox.innerHTML = `<div class="progress">
                                                <div class="progress-bar progress-bar-striped" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100">${percent.toFixed(1)}%</div>
                                            </div>`;
                }
            })
            cancelBtn.addEventListener('click', () => {
                xhr.abort();
                progressBox.innerHTML = "";
                cancelBtn.classList.add('invisible');
                uploadBtn.classList.remove('invisible');
            })
            return xhr;
        },
        success: function (response) {
            progressBox.innerHTML = "";
            if (response['notsummarizedpresent'])
                reloadFileUploads(response['files_details']);
            document.querySelector("#success-message").classList.remove("invisible");
            cancelBtn.classList.add('invisible')
            uploadBtn.classList.remove('invisible')
            progressBox.classList.remove("invisible")
        },
        error: function (err) {
            progressBox.innerHTML = "";
            alert("Internal server error!");
            cancelBtn.classList.add('invisible')
            uploadBtn.classList.remove('invisible')
            progressBox.classList.remove("invisible")
            return;
        },
        cache: false,
        contentType: false,
        processData: false,
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

const getMediaExtension = (mimetype) => {
    console.log(mimetype)
    const extensions = { 'audio/mpeg': 'mp3', 'audio/wav': 'wav', 'video/mpeg': 'mpeg', 'video/mp4': 'mp4', 'video/mkv': 'mkv', 'video/mov': 'mov', 'application/msword': 'doc', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx', 'text/plain': 'txt', 'application/pdf': 'pdf'};
    return extensions[mimetype];
}

const reloadFileUploads = (files_details) => {
    let fileuploadscontent = "";
    files_details.forEach(filedata => {
        fileuploadscontent += `<div class="file-card p-3 my-3 col-md-5 col-12 mx-auto">
                                <div class="file-card-header">
                                    <a href="${filedata.fileurl}"  target="_blank">${filedata.filename}</a>
                                </div>
                                <hr>
                                <div class="file-card-body">
                                    Uploaded on: ${filedata.uploaddate}<br><br>
                                    File type: ${filedata.filetype}<br>
                                </div>
                                <hr>
                                <div class="file-card-footer">
                                    <button class="summary-btn btn btn-sm btn-primary" id="${filedata.fileid}">Generate Summary</button>
                                </div>
                            </div>`
    });
    document.querySelector("#filesuploadedarea").innerHTML = fileuploadscontent;
    if (files_details.length == 0)
        document.querySelector("#filesuploadeddiv").classList.add("invisible");
    else
        document.querySelector("#filesuploadeddiv").classList.remove("invisible");
    addEventsToGenerateSummaryButtons();
}

const generateSummary = (event) => {
    const fileid = event.target.id;
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        url: addtoqueueurl,
        datatype: 'json',
        headers: { "X-CSRFToken": csrftoken },
        data: JSON.stringify({"fileid": fileid}),
        beforeSend: function () {
            $("#summary-queued-modal").modal('show');
        },
        success: function (response) {
            if (!response['alreadyqueued']){
                document.querySelector('.modal-body').innerHTML = `${response['filename']} has been queued for summarization.`;
                $("#summary-queued-modal").modal('show');
            }
            reloadFileUploads(response['files_details']);
        },
        error: function (err) {
            alert("Internal server error!");
        },
        cache: false,
        contentType: false,
        processData: false,
    })
}

const addEventsToGenerateSummaryButtons = () => {
    document.querySelectorAll(".summary-btn").forEach((btn) => {
        btn.addEventListener("click", generateSummary);
    })
}