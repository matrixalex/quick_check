let study_class_id = null;
function edit_class_form_show(id, name){
    study_class_id = id;
    document.getElementById("name_edit").value = name;
}

function edit_study_class(){
    let data = {
        id: study_class_id,
        name: document.getElementById("name_edit").value,
        teachers_id: collect_users_id("teachers_block_edit"),
        pupils_id: collect_users_id("pupils_block_edit"),
        org_id: document.getElementById("org_id").value
    }
    $.ajax({
        "url": '/classes/create-or-change',
        "type": "post",
        data: data,
        success: function (data){
            window.location.reload();
        },
        error: function (data){
            alert(data.responseJSON.result.message);
        }
    })
}

function collect_users_id(element_id){
    let result = [];
    let users_block = document.getElementById(element_id);
    let check_boxes = users_block.getElementsByTagName("input");
    for (let i = 0; i < check_boxes.length; i++){
        if (check_boxes[i].checked){
            if (check_boxes[i].parentNode.getElementsByTagName("span").length > 0) {
                let span = check_boxes[i].parentNode.getElementsByTagName("span")[0];
                if (span.innerText) result.push(span.innerText);
            }
        }
    }
    return result;
}

function create_study_class(){
    let data = {
        name: document.getElementById("name_create").value,
        teachers_id: collect_users_id("teachers_block_create"),
        pupils_id: collect_users_id("pupils_block_create"),
        org_id: document.getElementById("org_id").value
    }
    $.ajax({
        "url": '/classes/create-or-change',
        "type": "post",
        data: data,
        success: function (data){
            window.location.reload();
        },
        error: function (data){
            alert(data.responseJSON.result.message);
        }
    })
}