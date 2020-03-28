document.querySelector('#note-list').addEventListener('click', e => {
  //Remove
  if(e.target.classList.contains('remove-event')){
    const noteRow = e.target.parentElement.parentElement.parentElement;
    const noteId = noteRow.getAttribute("note-id");

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
