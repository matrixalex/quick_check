let homework_id = null;
function upload_homework(){
    let pupils_id = get_pupils_id();
    if (pupils_id.length === 0) {
        alert("Выберите учеников");
        return;
    }
    let file = null;
    try {
        file = document.getElementById("file_create").files[0];
    } catch (e){}
    if (file == null){
        alert("Выберите файл");
        return;
    }
    let data = new FormData();
    data.append("homework_document", file);
    data.append("pupils_id", pupils_id);
    data.append("name", document.getElementById("name_create").value);
    data.append("description", document.getElementById("description_create").value);
    data.append("criterion_id", document.getElementById("criterion_id").value);
    console.log(data);
    $.ajax({
        url: "/teacher/homework/create-or-change",
        type: "post",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data){
            window.location.reload();
        },
        error: function (data){
            alert(data.responseJSON.result.message);
        }
    })
}

function get_pupils_id(){
    let result = [];
    let checkboxes = document.getElementById("pupils_list_block").getElementsByTagName("input");
    for (let i = 0; i < checkboxes.length; i++){
        if (
            checkboxes[i].checked &&
            checkboxes[i].parentNode.getElementsByTagName("span").length > 0 &&
            checkboxes[i].parentNode.getElementsByTagName("span")[0].innerText !== ""
        ) {
            try {
                result.push(parseInt(checkboxes[i].parentNode.getElementsByTagName("span")[0].innerText))
            } catch (e){

            }
        }
    }
    return result;
}

function upload_pupil_homework(){
    let data = new FormData();
    let file = null;
    try {
        file = document.getElementById("file").files[0];
    } catch (e){}
    if (file == null){
        alert("Выберите файл");
        return;
    }
    data.append("homework_id", homework_id);
    data.append("file", file);
    $.ajax({
        url: "/pupil/homework/upload",
        type: "post",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        beforeSend: function (){
            document.getElementById("btn_upload_homework").disabled = "disabled";
            document.getElementById("btn_upload_homework").innerText = "Подождите"
        },
        success: function (data){
            window.location.reload();
        },
        error: function (data){
            alert(data.responseJSON.result.message);
        }
    })
}

function upload_pupil_homework_form_show(id){
    homework_id = id;
}

function upload_appeal_pupil(){
    let hw_id = document.getElementById("homework_id").value;
    let data = new FormData();
    let file = null;
    try {
        file = document.getElementById("file_appeal").files[0];
    } catch (e){}
    if (file == null){
        alert("Выберите файл");
        return;
    }
    data.append("homework_id", hw_id);
    data.append("file", file);
    data.append("text", document.getElementById("text").value);
    $.ajax({
        url: "/pupil/homework/appeal",
        type: "post",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data){
            window.location.reload();
        },
        error: function (data){
            alert(data.responseJSON.result.message);
        }
    })
}

function upload_appeal_teacher(){
    let id = document.getElementById("homework_id").value;
    let text = document.getElementById("appeal_text").value;
    let appeal_id = document.getElementById("appeal_id").value;
    $.ajax({
        url: "/teacher/homework/appeal",
        type: "post",
        data: {
            homework_id: id,
            text: text,
            appeal_id: appeal_id
        },
        success: function (data){
            window.location.reload();
        },
        error: function (data){
            alert(data.responseJSON.result.message);
        }
    })
}

function load_appeal_result(appeal_id){
    $.ajax({
        url: '/pupil/appeal/' + appeal_id,
        type: 'get',
        success: function (data){
            let appeal_result_block = document.getElementById("appeal_result_block");
            appeal_result_block.style.opacity = "100";
            appeal_result_block.style.display = "flex";
            document.getElementById("appeal_result_text").innerText = data.result.text;
            document.getElementById("delete_appeal_button").setAttribute("onclick", "delete_appeal(" + appeal_id + ")");
        },
        error: function (data){
            alert(data.responseJSON.result.message);
        }
    })
}

function delete_appeal(appeal_id){
    $.ajax({
        url: '/pupil/appeal/' + appeal_id,
        type: 'post',
        success: function (data){
            window.location.reload();
        },
        error: function (data){
            alert(data.responseJSON.result.message);
        }
    })
}

function upload_homeworks_by_teacher(){
    let data = new FormData();
    let file = null;
    try {
        file = document.getElementById("homeworks_file").files[0];
    } catch (e){}
    if (file == null){
        alert("Выберите файл");
        return;
    }
    data.append("homework_id", homework_id);
    data.append("file", file);
    $.ajax({
        url: "/teacher/homework/upload",
        type: "post",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: data,
        success: function (data){
            window.location.reload();
        },
        error: function (data){
            alert(data.responseJSON.result.message);
        }
    })
}

function upload_homeworks_by_teacher_form_show(id){
    homework_id = id;
    document.getElementById("upload_homeworks_by_teacher_form").style.display = 'flex';
    document.getElementById("upload_homeworks_by_teacher_form").style.zIndex = 5;
    document.getElementById("upload_homeworks_by_teacher_form").style.opacity = 100;
}

function upload_homeworks_by_teacher_form_show_hide(){
    document.getElementById("upload_homeworks_by_teacher_form").style.display = 'none';
    document.getElementById("upload_homeworks_by_teacher_form").style.zIndex = 5;
    document.getElementById("upload_homeworks_by_teacher_form").style.opacity = 0;
}