let user_id = null;
function user_create_form_show(){
    document.getElementById("user_add_form").style.display = "block";
}

function create_user(){
    let first_name = document.getElementById("first_name_create").value;
    let last_name = document.getElementById("last_name_create").value;
    let middle_name = document.getElementById("middle_name_create").value;
    let phone_number = document.getElementById("phone_number_create").value;
    let birth_date = document.getElementById("birth_date_create").value;
    let user_type = document.getElementById("user_type").value;
    let email = document.getElementById("email_create").value;
    let org_id = null;
    try {
        org_id = document.getElementById("org_id_create").value;
    } catch (e){
        try {
            org_id = document.getElementById("org_id").value;
        } catch (e){

        }
    }
    let study_class_id = null;
    try {
        study_class_id = document.getElementById("study_class_id_create").value;
    } catch (e){

    }
    let data = {
            first_name: first_name,
            last_name: last_name,
            middle_name: middle_name,
            phone_number: phone_number,
            birth_date: birth_date,
            status: user_type,
            email: email
    };
    if (org_id != null) data['org_id'] = org_id;
    if (study_class_id != null) data['study_class_id'] = study_class_id;
    $.ajax({
        url: "/users/create-or-change",
        type: "post",
        data: data,
        success: function (data){
            window.location.reload();
        },
        error: function (data){
            alert(data.responseJSON.result.message);
        }
    })
}

function registration_form_accept_show(user_id){
    $.ajax({
        url: "/users/accept/" + user_id,
        type: "get",
        success: function (data){
            console.log(data);
            document.getElementById("registration_request_text_block").innerText = data.result.text;
            document.getElementById("button_accept_registration").setAttribute("onclick", "accept_registration(" + user_id +",1)");
            document.getElementById("button_reject_registration").setAttribute("onclick", "accept_registration(" + user_id +",0)");
        },
        error: function (data){
            alert("Необратываемая ошибка");
        }
    })
}

function accept_registration(user_id, status){
    $.ajax({
        url: "/users/accept/" + user_id,
        type: "post",
        data: {status: status},
        success: function (data){
            console.log(data);
            document.getElementById("registration_request_text_block").innerText = "";
            document.getElementById("button_accept_registration").removeAttribute("onclick");
            document.getElementById("button_reject_registration").removeAttribute("onclick");
            window.location.reload();
        },
        error: function (data){
            alert("Необратываемая ошибка");
        }
    })
}

function block_user(element, id, is_accepted){
    let new_status = is_accepted === 1 ? 0 : 1;
    $.ajax({
        url: "/users/block/" + id,
        type: "post",
        data: {status: new_status},
        success: function (data){
            window.location.reload();
        }
    })
    element.setAttribute("onclick", "block_user(" + element + "," + id + ',' + new_status + ")");

}

function edit_user_form_show(id, first_name, last_name, middle_name, email, phone_number, birth_date, org_id=null, study_class_id=null){
    user_id = id;
    document.getElementById("first_name_edit").value = first_name;
    document.getElementById("last_name_edit").value = last_name;
    document.getElementById("middle_name_edit").value = middle_name;
    document.getElementById("phone_number_edit").value = phone_number;
    document.getElementById("birth_date_edit").value = birth_date;
    document.getElementById("email_edit").value = email;
    if (org_id != null){
        let options = document.getElementById("org_id_edit").getElementsByTagName("option");
        for (let i = 0; i < options.length; i++){
            if (parseInt(""+options[i].value) === org_id){
                options[i].selected = "selected";
            } else {
                options[i].selected = "";
            }
        }
    }
    if (study_class_id != null){
        let options = document.getElementById("study_class_id_edit").getElementsByTagName("option");
        for (let i = 0; i < options.length; i++){
            if (parseInt(""+options[i].value) === study_class_id){
                options[i].selected = "selected";
            } else {
                options[i].selected = "";
            }
        }
    }
}

function edit_user(){
    let id = user_id;
    let first_name = document.getElementById("first_name_edit").value;
    let last_name = document.getElementById("last_name_edit").value;
    let middle_name = document.getElementById("middle_name_edit").value;
    let phone_number = document.getElementById("phone_number_edit").value;
    let birth_date = document.getElementById("birth_date_edit").value;
    let user_type = document.getElementById("user_type").value;
    let email = document.getElementById("email_edit").value;
    let org_id = null;
    try {
        org_id = document.getElementById("org_id_create").value;
    } catch (e){

    }
    let study_class_id = null;
    try {
        study_class_id = document.getElementById("study_class_id_create").value;
    } catch (e){

    }
    let data = {
            id: id,
            first_name: first_name,
            last_name: last_name,
            middle_name: middle_name,
            phone_number: phone_number,
            birth_date: birth_date,
            status: user_type,
            email: email
    };
    if (org_id != null) data['org_id'] = org_id;
    if (study_class_id != null) data['study_class_id'] = study_class_id;
    $.ajax({
        url: "/users/create-or-change",
        type: "post",
        data: data,
        success: function (data){
            window.location.reload();
        },
        error: function (data){
            alert(data.responseJSON.result.message);
        }
    })
}