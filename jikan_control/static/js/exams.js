document.querySelector('#predict-score').addEventListener('click', e => {
  // Validate pred study hours has value
  // todo

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

      document.querySelector('#predicted_score').value = scoreData.score;
    }
  });

  e.preventDefault();
});

document.querySelector('#predict-hours').addEventListener('click', e => {
  // Validate pred score has value
  // todo

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

      document.querySelector('#predicted_study_hours').value = hoursData.hours;
    }
  });

  e.preventDefault();
});