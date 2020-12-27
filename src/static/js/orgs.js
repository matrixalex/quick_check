let org_id = null;

function create_org(){
    let name = document.getElementById("name_create").value;
    let admins_id = get_admins_id("admins_create_block");
    $.ajax({
        url: "/organizations/create-or-change",
        type: "post",
        data: {
            name: name,
            admins_id: admins_id
        },
        success: function (data){
            console.log(data);
            window.location.reload();
        },
        error: function (data){
            console.log(data);
            alert(data.responseJSON.result.message)
        }
    })
}

function get_admins_id(element_id){
    let result = [];
    let admins_div = document.getElementById(element_id);
    let check_boxes = admins_div.getElementsByTagName("input");
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

function change_org_form_show(id, name){
    document.getElementById("name_change").value = name;
    org_id = id;
}

function change_org(){
    let id = org_id;
    let name = document.getElementById("name_change").value;
    let admins_id = get_admins_id("admins_change_block");
    $.ajax({
        url: "/organizations/create-or-change",
        type: "post",
        data: {
            id: id,
            name: name,
            admins_id: admins_id
        },
        success: function (data){
            console.log(data);
            window.location.reload();
        },
        error: function (data){
            console.log(data);
            alert(data.responseJSON.result.message)
        }
    })
}