document.querySelector('#event-list').addEventListener('click', e => {
  // Remove
  if(e.target.classList.contains('remove-event')){
    const eventRow = e.target.parentElement.parentElement.parentElement;
    const eventId = eventRow.getAttribute("event-id");

    $.ajax({
        type: 'POST',
        url: '/events/remove',
        data:{
            event_id: eventId,
            // where is the csrf token coming from???
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
            // Remove from UI
            eventRow.remove();
        }
    });
  }
  
  // Mark as completed
  if(e.target.classList.contains('complete-event')){
    if(e.target.classList.contains('complete-event')){
      const eventRow = e.target.parentElement.parentElement.parentElement;
      const eventId = eventRow.getAttribute("event-id");
  
      $.ajax({
          type: 'POST',
          url: '/events/complete',
          data:{
              event_id: eventId,
              // where is the csrf token coming from???
              csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          success:function(){
              // Remove from UI
              e.target.remove(); // Green checkmark
          }
      });
    }
  }
});