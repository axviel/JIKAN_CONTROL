document.querySelector('#note-list').addEventListener('click', e => {
  //Remove
  if(e.target.classList.contains('remove-note')){
    const noteeRow = e.target.parentElement.parentElement.parentElement;
    const noteId = noteRow.getAttribute("notee-id");

    $.ajax({
        type: 'POST',
        url: '/notes/remove',
        data:{
	    note_id: noteId,
	    //where is the csrf token coming from???
	    csrfmiddlewaretoken: $(input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
	    //Remove from UI
	    noteRow.remove();
        }
    });
  }

