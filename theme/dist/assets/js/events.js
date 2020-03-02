document.querySelector('#event-list').addEventListener('click', e => {
  if(e.target.classList.contains('show-event-detail')){
    window.location.href = "event_detail.html";
  }
});