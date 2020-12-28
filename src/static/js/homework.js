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