function user_create_form_show(){
    document.getElementById("user_add_form").style.display = "block";
}

function create_user(){
    let first_name = document.getElementById("first_name_create").value;
    let last_name = document.getElementById("last_name_create").value;
    let middle_name = document.getElementById("middle_name_create").value;
    let phone_number = document.getElementById("phone_number_create").value;
    let birth_date = document.getElementById("birth_date_create").value;
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
    $.ajax({
        url: "/users/create-or-change",
        type: "post",
        data: {
            first_name: first_name,
            last_name: last_name,
            middle_name: middle_name,
            phone_number: phone_number,
            birth_date: birth_date,
            org_id: org_id,
            study_class_id: study_class_id
        }
    })
}