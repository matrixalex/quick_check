let template_type = null;


function handle_upload_template(template_type_) {
    template_type = template_type_;
    document.getElementById("upload_template_form").style.display = 'flex';
    document.getElementById("upload_template_form").style.zIndex = 5;
    document.getElementById("upload_template_form").style.opacity = 100;
}


function close_upload_form() {
    document.getElementById("upload_template_form").style.display = 'none';
    document.getElementById("upload_template_form").style.zIndex = 5;
    document.getElementById("upload_template_form").style.opacity = 0;
}


function upload_pupil_template(){
    let data = new FormData();
    let file = null;
    try {
        file = document.getElementById("file").files[0];
    } catch (e){}
    if (file == null){
        alert("Выберите файл");
        return;
    }
    data.append("file", file);
    data.append("template_type", template_type);
    $.ajax({
        url: "/pupil/upload-template",
        type: "post",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        beforeSend: function (){
            document.getElementById("btn_upload_template").disabled = "disabled";
            document.getElementById("btn_upload_template").innerText = "Подождите"
        },
        success: function (data){
            window.location.reload();
        },
        error: function (data){
            // alert(data.responseJSON.result.message);
            console.log(data);
        }
    })
}