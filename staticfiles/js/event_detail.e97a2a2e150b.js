document.addEventListener("DOMContentLoaded", e => {
  let eventType = document.querySelector('#event_type');
  if(eventType.value === "4"){
    document.querySelector('#exam-btn').classList.remove('d-remove');
  }
});

// Go to exam
this.elements.examButton.addEventListener('click', e => {

  let thisCalendar = this;
  let eventId = document.querySelector('#event_id').value;

  $.ajax({
      type: 'GET',
      url: '/exams/id',
      data: {
          event_id: eventId,
          is_calendar_form: true
      },
      success: function(data){
          let examData = JSON.parse(data);

          if(examData.exam_id !== null){
              window.location = '/exams/detail/' + examData.exam_id;
          }
          else{
              window.location = '/exams/detail/event/' + eventId;
          }

      }
  });

  e.preventDefault();
});