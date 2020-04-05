document.addEventListener("DOMContentLoaded", e => {
  let examId = document.querySelector('#exam_id');
  if(examId.value === null){
    getNextExamNumber();
  }
});

document.querySelector('#predict-score').addEventListener('click', e => {
  // Validate pred study hours has value
  if(document.querySelector('#predicted_study_hours').value === '0'){
    showMessage('Please enter values for predicted study hours');
    return;
  }

  $.ajax({
    type: 'GET',
    url: '/exams/score',
    data: {
        predicted_study_hours: document.querySelector('#predicted_study_hours').value,
        course_id: document.querySelector('#course').value,
        exam_number: document.querySelector('#exam_number').value,
    },
    success: function(data){
      let scoreData = JSON.parse(data);

      // If score = -1, show alert.
      if(scoreData.score === -1){
        showMessage('Previous exam not graded');
      }
      else{
        document.querySelector('#predicted_score').value = scoreData.score;
      }

    }
  });

  e.preventDefault();
});

document.querySelector('#predict-hours').addEventListener('click', e => {
  // Validate pred score has value
  if(document.querySelector('#predicted_score').value === '0'){
    showMessage('Please enter values for predicted score');
    return;
  }

  $.ajax({
    type: 'GET',
    url: '/exams/hours',
    data: {
        predicted_score: document.querySelector('#predicted_score').value,
        course_id: document.querySelector('#course').value,
        exam_number: document.querySelector('#exam_number').value,
    },
    success: function(data){
      let hoursData = JSON.parse(data);

      // If hours = -1, show alert.
      if(hoursData.hours === -1){
        showMessage('Previous exam not graded');
      }
      else{
        document.querySelector('#predicted_study_hours').value = hoursData.hours;
      }
    }
  });

  e.preventDefault();
});

function showMessage(message){
  let mainPage = document.querySelector('#main-page');
  let breadcrumb = document.querySelector('#bc');

  // Create message alert

  let messageDiv = document.createElement('div');
  messageDiv.classList = 'container';

  messageDiv.innerHTML = `
    <div class="alert alert-danger alert-dismissible text-center mt-2" role="alert">
      <button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">×</span></button>
      <strong>
          Error
      </strong>

      ${message}
    </div>
  `;
  
  // Insert message alert
  mainPage.insertBefore(messageDiv, breadcrumb);
}

function getNextExamNumber(){
  $.ajax({
    type: 'GET',
    url: '/exams/number',
    data: {
        exam_id: document.querySelector('#exam_id').value,
        course_id: document.querySelector('#course').value
    },
    success: function(data){
      let numberData = JSON.parse(data);
      document.querySelector('#exam_id').value = numberData.number;
    }
  });
}