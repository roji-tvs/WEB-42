function getDetail(id){
    console.log(id)
  
    $.ajax({
            type: 'GET',
            // data: {
            //     "id": id,
            //     "domain": domain,
            //     "domain_id": domain_id,
            //     "account_email": account_email,
            //     "transaction_id": transaction_id
            // },
            // url: '/callcenter/add_karam/',
            url: "/account/user-permission/"+id,
            success: function (data) {
                console.log("hhhhhhh")
                a = $("#user_permission_div").html(data);
                $("#user_permission_modal").modal('show');
  
            },
            error: function (err) {
                console.log('err')
                console.log(err.responseText)
            },
            complete: function () {
                $.LoadingOverlay("hide");
            }
        });
  }



function setUserPermission(id){
    var inputs = $(".user-permission-checkbox");
    let permission_list = []

    for(var i = 0; i < inputs.length; i++){
        permission_list.push({
            "module":$(inputs[i]).attr("name"),
            "permission" : $(inputs[i]).is(":checked")
        })
        // console.log($(inputs[i]).is(":checked"),"=",$(inputs[i]).attr("name"))
    }

    console.log(permission_list)

    $.ajax({
        type: 'POST',
        data: {
            "permission_list":JSON.stringify(permission_list)
        },
        url: "/account/user-permission/"+id,
        success: function (data) {
            console.log("post success")
            // a = $("#user_permission_div").html(data);
            $("#user_permission_modal").modal('hide');

        },
        error: function (err) {
            console.log('err')
            console.log(err.responseText)
        },
        complete: function () {
            $.LoadingOverlay("hide");
        }
    });

}

function userStatus(id){
    $.ajax({
        type: 'POST',
        data: {
            "status": $("#user_status_"+id).is(":checked"),
            "user_id": id
        },
        url: "/account/user-list/",
        success: function (data) {
            console.log("post success")
            // a = $("#user_permission_div").html(data);
            // $("#user_permission_modal").modal('hide');

        },
        error: function (err) {
            console.log('err')
            console.log(err.responseText)
        },
        complete: function () {
            $.LoadingOverlay("hide");
        }
    });
}


function moduleStatus(id){
    $.ajax({
        type: 'POST',
        data: {
            "status": $("#module_status_"+id).is(":checked"),
            "module_id": id
        },
        url: "/account/module-list/",
        success: function (data) {
            location.reload()
            // a = $("#user_permission_div").html(data);
            // $("#user_permission_modal").modal('hide');

        },
        error: function (err) {
            console.log('err')
            console.log(err.responseText)
        },
        complete: function () {
            $.LoadingOverlay("hide");
            
        }
    });
}