document.querySelector('#exam-list').addEventListener('click', e => {
  // Remove
  if(e.target.classList.contains('remove-exam')){
    const examRow = e.target.parentElement.parentElement.parentElement;
    const examId = examRow.getAttribute("exam-id");

    $.ajax({
        type: 'POST',
        url: '/exams/remove',
        data:{
            exam_id: examId,
            // where is the csrf token coming from???
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
            // Remove from UI
            examRow.remove();
        }
    });
  }
});