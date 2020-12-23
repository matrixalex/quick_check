function login(){
    let email = document.getElementById("email_login").value;
    let password = document.getElementById("password_login").value;
    $.ajax({
        url: "/auth/login",
        type: "post",
        data: {email: email, password: password},
        success: function (data){
            var result = data.result;
            if (result.is_superuser){
                window.location.href = "/admin";
            } else {
                window.location.href = "/";
            }
        },
        beforeSend: function (){
            document.getElementById("login_error_block").innerText = "";
        },
        error: function (data){
             document.getElementById("login_error_block").innerText = data.responseJSON.result.message;
        }
    })
}

function registration(){
    let email = document.getElementById("email_registration").value;
    let first_name = document.getElementById("first_name").value;
    let last_name = document.getElementById("last_name").value;
    let middle_name = document.getElementById("middle_name").value;
    let birth_date = document.getElementById("birth_date").value;
    let phone_number = document.getElementById("phone_number").value;
    let registration_reason = document.getElementById("registration_reason").value;
    let user_type = document.getElementById("user_type").value;
    let password = document.getElementById("password_registration").value;
    let password_confirm = document.getElementById("password_registration_confirm").value;
    $.ajax({
        url: "/auth/registration",
        type: "post",
        data: {
            email: email,
            password: password,
            password_confirm: password_confirm,
            user_type: user_type,
            registration_reason: registration_reason,
            birth_date: birth_date,
            middle_name: middle_name,
            first_name: first_name,
            last_name: last_name,
            phone_number: phone_number
        },
        success: function (data){
            alert(data.result.message);
            window.location.href = "/";
        },
        beforeSend: function (){
            document.getElementById("registration_error_block").innerText = "";
        },
        error: function (data){
             document.getElementById("registration_error_block").innerText = data.responseJSON.result.message;
        }
    })
}