document.querySelector('#note-list').addEventListener('click', e => {
  if(e.target.classList.contains('show-note-detail')){
    window.location.href = "note_detail.html";
  }
});