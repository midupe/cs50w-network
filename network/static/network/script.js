function editPost(id){
    document.getElementById("editPost").value = document.getElementById("postText"+id).innerHTML;
    document.getElementById("saveChangesButton").setAttribute("onclick","event.preventDefault(); savePost("+id+")");
}

function savePost(id){
    document.getElementById("postText"+id).innerHTML = document.getElementById("editPost").value;
    $('#exampleModal').modal('hide');

    form = document.getElementById("editPostForm");
    //form.setAttribute("action","/post/"+id);
    //form.submit();

    $.post("/post/"+id, $(form).serialize(), function(data){});
}