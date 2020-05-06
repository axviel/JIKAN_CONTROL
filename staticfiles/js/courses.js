document.querySelector('#course-list').addEventListener('click', e => {
  //Remove
  if(e.target.classList.contains('remove-course')){
    const courseRow = e.target.parentElement.parentElement.parentElement;
    const courseId = courseRow.getAttribute("course-id");

    $.ajax({
        type: 'POST',
        url: '/courses/remove',
        data:{
	    course_id: courseId,
	    //where is the csrf token coming from???
	    csrfmiddlewaretoken: $(input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
	    //Remove from UI
	    courseRow.remove();
        }
    });
  }
