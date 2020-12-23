function handle_delete(url, id){
    document.getElementById("delete_button").setAttribute(
        "onclick", "delete_object(\"" + url + "\"," + id + ")"
    );
}

function delete_object(url, id){
    $.ajax({
        url: url,
        type: "post",
        data: {id: id},
        success: function (data){
            window.location.reload();
        },
        error: function (data){
            console.log(data);
            alert(data.responseJSON.result.message);
        }
    })
}