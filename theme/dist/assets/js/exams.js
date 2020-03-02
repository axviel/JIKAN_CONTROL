document.querySelector('#exam-list').addEventListener('click', e => {
  if(e.target.classList.contains('show-exam-detail')){
    window.location.href = "exam_detail.html";
  }
});