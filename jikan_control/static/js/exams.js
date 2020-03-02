document.querySelector('#exam-list').addEventListener('click', e => {
  if(e.target.classList.contains('show-exam-detail')){
    $('#exam-form-modal').modal('toggle');
  }
});