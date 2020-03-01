document.querySelector('#event-list').addEventListener('click', e => {
  if(e.target.classList.contains('show-event-detail')){
    $('#event-form-modal').modal('toggle');
  }
});