document.addEventListener('DOMContentLoaded', () => {
    updateUILikes();
});

function updateUILikes() {
    fetch('/likes', {
        method: 'GET'
      }).then(response => response.json())
      .then(result => {
          for(let i=0; i < result.results.length; i++) {
            try {
                icon = document.getElementById("iconLikes"+result.results[i]);
                icon.classList.remove("far"); 
                icon.classList.add("fas"); 
            }
            catch (e) {}
            //pass
          }
      });
}

function editPost(id){
    document.getElementById("editPost").value = document.getElementById("postText"+id).innerHTML;
    document.getElementById("saveChangesButton").setAttribute("onclick","event.preventDefault(); savePost("+id+")");
}

function savePost(id){
    document.getElementById("postText"+id).innerHTML = document.getElementById("editPost").value;
    $('#exampleModal').modal('hide');
    // submit form
    form = document.getElementById("editPostForm");
    $.post("/post/"+id, $(form).serialize(), function(data){});
}

function like(id) {
    likes = document.getElementById("Likes"+id);
    icon = document.getElementById("iconLikes"+id);

    if (icon.classList.contains("fas")){
        icon.classList.remove("fas"); 
        icon.classList.add("far"); 
        likes.innerHTML = parseInt(document.getElementById("Likes"+id).innerHTML) - 1;
    } else {
        icon.classList.remove("far"); 
        icon.classList.add("fas"); 
        likes.innerHTML = parseInt(document.getElementById("Likes"+id).innerHTML) + 1;
    }

    fetch('/like/'+id, {
        method: 'GET'
      });
}

