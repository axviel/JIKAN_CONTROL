document.querySelector('#note-list').addEventListener('click', e => {
  if(e.target.classList.contains('show-note-detail')){
    $('#note-form-modal').modal('toggle');
  }
});