const AVAILABLE_WEEK_DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const AVALIABLE_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

class Calendar {
    constructor(options) {
        this.options = options;
        this.elements = {
            days: document.querySelector('.calendar-day-list'),
            week: document.querySelector('.calendar-week-list'),
            year: document.querySelector('.calendar-current-year'),
            eventList: document.querySelector('.current-day-events-list'),
            eventAddBtn: document.querySelector('.add-event-day-btn'),
            todayBtn: document.querySelector('.calendar-today-btn'),
            currentDay: document.querySelector('.current-day-number'),
            currentWeekDay: document.querySelector('.current-day-of-week'),
            prevMonth: document.querySelector('.calendar-change-month-slider-prev'),
            nextMonth: document.querySelector('.calendar-change-month-slider-next'),
            currentMonth: document.querySelector('.calendar-current-month'),
            currentDayModal: document.querySelector('#current-day-modal'),
            currentDayFooter: document.querySelector('.current-day-footer'),
            currentDayEventsList: document.querySelector('#current-day-event-list'),
            currentDayAddEventFormContent: document.querySelector('#current-day-add-event-form'),
            eventForm: document.querySelector('#event-form'),
            eventFormBackArrow: document.querySelector('#event-form-back'),
            modalHeaderLabel: document.querySelector('#current-day-modal-label'),
            eventEndDateField: document.querySelector('#end_date_field'),
            saveEventFormButton: document.querySelector('#save-event-form-btn'),
            examButton: document.querySelector('#exam-btn'),
        };

        // Used to toggle modal event list and form states
        this.currentDayModalFormToggle = false;

        // Store the event list passed by the backend
        this.eventList = JSON.parse(document.getElementById('calendar-events').textContent) || {};

        // Contains the events that repeat 
        this.dailyRepeatEventList = []; 
        this.weeklyRepeatEventList = []; 
        this.monthlyRepeatEventList = []; 
        this.yearlyRepeatEventList = []; 
        this.tempEventRepeatList = {};

        // Sort event list based on start_time
        const eventDates = Object.keys(this.eventList)
        eventDates.forEach(date => {
            this.eventList[date].sort(this.compareStartTimes);
            let theEventDate;
            let key;

            this.eventList[date].forEach(event => {
                theEventDate = new Date(event.start_date);

                // Daily
                if(event.repeat_type === 2){
                    this.dailyRepeatEventList.push(event);
                }
                // Weekly
                else if(event.repeat_type === 3){
                    this.weeklyRepeatEventList.push(event);
                }
                // Monthly
                else if(event.repeat_type === 4){
                    this.monthlyRepeatEventList.push(event);
                }
                // Yearly
                else if(event.repeat_type === 5){
                    this.yearlyRepeatEventList.push(event);
                }
            });
            
        });

        // Current event on the modal
        this.currentEvent = {};

        // Current date
        this.date = new Date();

        // Number of days show in the calendar
        this.options.maxDays = 42;

        // Initializes the events and draws all the days, weeks, years, and events
        this.init();
    }

    // App methods
    init() {
        if (!this.options.id) return false;
        this.eventsTrigger();
        this.drawAll();
    }

    // Compares event list start_time in order to sort the list
    compareStartTimes( a, b ) {
        if ( a.start_time < b.start_time ){
          return -1;
        }
        if ( a.start_time > b.start_time ){
          return 1;
        }
        return 0;
    }

    // Returns an object/list of repeat event days
    currentMonthRepeatedEvents(days){
        let dayDate;
        let eventDate;

        // Clear temp list
        this.tempEventRepeatList = {}

        days.forEach(day => {
            dayDate = new Date(day.formatedDate);

            // Check for daily repeats
            this.dailyRepeatEventList.forEach(event => {
                // update event date?
                // i think i need it pa que salgan en el modal

                // Add if the day date is after to event start date and before event end date
                eventDate = new Date(event.start_date);
                if( ( eventDate.getTime() < dayDate.getTime() && !event.end_date ) || 
                    (   event.end_date && 
                        eventDate.getTime() < dayDate.getTime() &&
                        new Date(event.end_date).getTime() > dayDate.getTime() ) ){

                    if(day.hasEvent){
                        day.hasEvent.push(event);
                    }
                    else{
                        day.hasEvent = [event];
                    }

                    // Add to temp list
                    if(day.formatedDate in this.tempEventRepeatList){
                        this.tempEventRepeatList[day.formatedDate].push(event);
                    }
                    else{
                        this.tempEventRepeatList[day.formatedDate] = [event];
                    }
                }
            })

            // Check for weekly repeats
            this.weeklyRepeatEventList.forEach(event => {
                eventDate = new Date(event.start_date);

                // Add if it's the same weekday
                if( eventDate.getDay() === dayDate.getDay() &&
                    ( ( eventDate.getTime() < dayDate.getTime() && !event.end_date ) || 
                        (   event.end_date && 
                            eventDate.getTime() < dayDate.getTime() &&
                            new Date(event.end_date).getTime() > dayDate.getTime() ) ) ){

                    if(day.hasEvent){
                        day.hasEvent.push(event);
                    }
                    else{
                        day.hasEvent = [event];
                    }

                    // Add to temp list
                    if(day.formatedDate in this.tempEventRepeatList){
                        this.tempEventRepeatList[day.formatedDate].push(event);
                    }
                    else{
                        this.tempEventRepeatList[day.formatedDate] = [event];
                    }
                }
            })

            // Check for monthly repeats
            this.monthlyRepeatEventList.forEach(event => {
                eventDate = new Date(event.start_date);

                // Add if it's the same day number
                if( eventDate.getDate() === dayDate.getDate() &&
                    ( ( eventDate.getTime() < dayDate.getTime() && !event.end_date ) || 
                        (   event.end_date && 
                            eventDate.getTime() < dayDate.getTime() &&
                            new Date(event.end_date).getTime() > dayDate.getTime() ) ) ){

                    if(day.hasEvent){
                        day.hasEvent.push(event);
                    }
                    else{
                        day.hasEvent = [event];
                    }

                    // Add to temp list
                    if(day.formatedDate in this.tempEventRepeatList){
                        this.tempEventRepeatList[day.formatedDate].push(event);
                    }
                    else{
                        this.tempEventRepeatList[day.formatedDate] = [event];
                    }

                }
            })
            
            // Check for yearly repeats
            this.yearlyRepeatEventList.forEach(event => {
                eventDate = new Date(event.start_date);

                // Add if it's the same day number
                if( eventDate.getMonth() === dayDate.getMonth() &&
                    eventDate.getDate() === dayDate.getDate() &&
                    ( ( eventDate.getTime() < dayDate.getTime() && !event.end_date ) || 
                        (   event.end_date && 
                            eventDate.getTime() < dayDate.getTime() &&
                            new Date(event.end_date).getTime() > dayDate.getTime() ) ) ){

                    if(day.hasEvent){
                        day.hasEvent.push(event);
                    }
                    else{
                        day.hasEvent = [event];
                    }

                    // Add to temp list
                    if(day.formatedDate in this.tempEventRepeatList){
                        this.tempEventRepeatList[day.formatedDate].push(event);
                    }
                    else{
                        this.tempEventRepeatList[day.formatedDate] = [event];
                    }

                }
            })


            // Sort the list
            if(day.hasEvent){
                day.hasEvent.sort(this.compareStartTimes);
            }
        });


    }

    // draw Methods
    drawAll() {
        this.drawWeekDays();
        this.drawDays();
        this.drawYearAndCurrentDay();
        this.drawEvents();
    }

    // Draws the event list for the current day modal
    drawEvents() {
        let calendar = this.getCalendar();

        let mainList = this.eventList[calendar.active.formatted] ? [].concat(this.eventList[calendar.active.formatted]) : undefined;
        let repeatList = this.tempEventRepeatList[calendar.active.formatted] ? [].concat(this.tempEventRepeatList[calendar.active.formatted]) : undefined;
        let eventList;
        if(mainList && repeatList){
            eventList = mainList.concat(repeatList);
        }
        else if(mainList && !repeatList){
            eventList = mainList;
        }
        else{
            eventList = repeatList;
        }

        if(eventList){
            // Sort
            eventList.sort(this.compareStartTimes);
        }
        else{
            eventList = ['No events to display'];
        }


        let eventTemplate = "<ul class='list-group'>";
        eventList.forEach(event => {
            if(event.title !== undefined ){
                eventTemplate += `
                    <li class="${event.is_completed ? 'bg-info' : ''} current-event-item list-group-item list-group-item-action d-flex justify-content-between align-items-center" event-id="${event.event_id}" repeat-type="${event.repeat_type}">
                        (${event.start_time}) ${event.title}
                        <div>
                            ${!event.is_completed ? '<i class="fas fa-check complete-event cursor-pointer text-success mr-4"></i>' : ''}
                            <i class="fas fa-trash-alt remove-event cursor-pointer text-danger"></i>
                        </div>
                    </li>
                `;
            }
            else{
                eventTemplate = `
                    <li class="current-event-item list-group-item d-flex justify-content-between align-items-center">
                        ${event}
                    </li>
                `;
            }
        });

        eventTemplate += "</ul>";

        this.elements.eventList.innerHTML = eventTemplate;
    }

    // Draws month, year and the current day modal day number and week day
    drawYearAndCurrentDay() {
        let calendar = this.getCalendar();
        this.elements.currentMonth.innerHTML = AVALIABLE_MONTHS[calendar.active.month];
        this.elements.year.innerHTML = calendar.active.year;
        this.elements.currentDay.innerHTML = calendar.active.day;
        this.elements.currentWeekDay.innerHTML = AVAILABLE_WEEK_DAYS[calendar.active.week];
    }

    // Draws the calendar days with their events
    drawDays() {
        let calendar = this.getCalendar();

        let latestDaysInPrevMonth = this.range(calendar.active.startWeek).map((day, idx) => {
            return {
                dayNumber: this.countOfDaysInMonth(calendar.pMonth) - idx,
                month: new Date(calendar.pMonth).getMonth(),
                year: new Date(calendar.pMonth).getFullYear(),
                currentMonth: false
            }
        }).reverse();

        let daysInActiveMonth = this.range(calendar.active.days).map((day, idx) => {
            let dayNumber = idx + 1;
            let today = new Date();
            return {
                dayNumber,
                today: today.getDate() === dayNumber && today.getFullYear() === calendar.active.year && today.getMonth() === calendar.active.month,
                month: calendar.active.month,
                year: calendar.active.year,
                selected: calendar.active.day === dayNumber,
                currentMonth: true
            }
        });


        let countOfDays = this.options.maxDays - (latestDaysInPrevMonth.length + daysInActiveMonth.length);
        let daysInNextMonth = this.range(countOfDays).map((day, idx) => {
            return {
                dayNumber: idx + 1,
                month: new Date(calendar.nMonth).getMonth(),
                year: new Date(calendar.nMonth).getFullYear(),
                currentMonth: false
            }
        });

        let days = [...latestDaysInPrevMonth, ...daysInActiveMonth, ...daysInNextMonth];

        days = days.map(day => {
            let newDayParams = day;

            newDayParams.formatedDate = this.getFormattedDate(new Date(`${Number(day.month) + 1}/${day.dayNumber}/${day.year}`));
            
            newDayParams.hasEvent = this.eventList[newDayParams.formatedDate] ? [].concat(this.eventList[newDayParams.formatedDate]) : null;
            return newDayParams;
        });

        // Concat repeated days to this month's items
        this.currentMonthRepeatedEvents(days);

        let daysTemplate = "";
        let firstEvent = "";
        let secondEvent = "";
        let smallEvent = "";
        let titleFormated = "";

        days.forEach(day => {

            if(day.hasEvent){
                titleFormated = day.hasEvent[0].title.length <= 10 ? day.hasEvent[0].title : day.hasEvent[0].title.substring(0, 7) + '...'
                firstEvent = `<div class="event event-large ${day.hasEvent[0].is_completed ? 'bg-info text-dark' : ''}">${day.hasEvent[0].start_time} ${titleFormated}</div>`;
                if(day.hasEvent.length > 1){
                    titleFormated = day.hasEvent[1].title.length <= 10 ? day.hasEvent[1].title : day.hasEvent[1].title.substring(0, 7) + '...'
                    secondEvent = `<div class="event event-large ${day.hasEvent[1].is_completed ? 'bg-info text-dark' : ''}">${day.hasEvent.length === 2 ? day.hasEvent[1].start_time + ' ' + titleFormated : (day.hasEvent.length - 1) + ' more events'}</div>`;
                }
                smallEvent = `<div class="event event-small">${day.hasEvent.length === 1 ? '1 event' : day.hasEvent.length + ' events'}</div>`;
            }

            daysTemplate += `
                <div 
                class="day-item 
                ${day.currentMonth ? 'current-month' : 'another-month'}${day.today ? ' active-day ' : ''}
                ${day.selected ? ' selected-day' : ''}${day.hasEvent ? ' event-day' : ''}" 
                data-day="${day.dayNumber}" 
                data-month="${day.month}" 
                data-year="${day.year}"
                data-toggle="modal" data-target="#current-day-modal"
                >
                    <div class="day-number">${day.dayNumber}</div>
                    ${day.hasEvent ? firstEvent + secondEvent + smallEvent : ''}
                </div>
            `

            firstEvent = '';
            secondEvent = '';
            smallEvent = '';
        });

        this.elements.days.innerHTML = daysTemplate;
    }

    // Draws the calendar week days (Mon, Tue, etc)
    drawWeekDays() {
        let weekTemplate = "";
        AVAILABLE_WEEK_DAYS.forEach(week => {
            weekTemplate += `<div class="week-day-item">${week.slice(0, 3)}</div>`
        });

        this.elements.week.innerHTML = weekTemplate;
    }

    // Clears the add evnt form, shows the event list state, and re-draws everything
    clearAddEventFormState(isNewEvent = false){
        // Clear fields
        document.querySelector('#title').value = "";
        document.querySelector('#description').value = "";
        document.querySelector('#event_type').value = "1";
        document.querySelector('#repeat_type').value = "1";
        document.querySelector('#start_time').value = "";
        document.querySelector('#end_time').value = "";

        // Hide end_date field if it was visible and show save button
        this.elements.eventEndDateField.classList.add('d-none');
        this.elements.saveEventFormButton.classList.remove('d-none');

        // Hide form and show event list
        this.toggleModalEventForm();

        // Redraw if new event was added
        if(isNewEvent){
            this.drawAll();
        }
    }

    // Toggles the current day modal state between event list and add event form
    toggleModalEventForm(){
        this.currentDayModalFormToggle = !this.currentDayModalFormToggle;

        if(this.currentDayModalFormToggle){
            this.elements.currentDayEventsList.classList.add('d-none');
            this.elements.currentDayFooter.classList.add('d-none');
            this.elements.modalHeaderLabel.classList.add('d-none');
            this.elements.currentDayAddEventFormContent.classList.remove('d-none');
            this.elements.eventFormBackArrow.classList.remove('d-none');
        }
        else{
            this.elements.currentDayEventsList.classList.remove('d-none');
            this.elements.currentDayFooter.classList.remove('d-none');
            this.elements.modalHeaderLabel.classList.remove('d-none');
            this.elements.currentDayAddEventFormContent.classList.add('d-none');
            this.elements.eventFormBackArrow.classList.add('d-none');
        }
    }

    // Updates current selected date
    updateTime(time) {
        this.date = new Date(time);
    }

    // Returns a calendar object
    getCalendar() {
        let time = new Date(this.date);

        return {
            active: {
                days: this.countOfDaysInMonth(time),
                startWeek: this.getStartedDayOfWeekByTime(time),
                day: time.getDate(),
                week: time.getDay(),
                month: time.getMonth(),
                year: time.getFullYear(),
                formatted: this.getFormattedDate(time),
                tm: +time
            },
            pMonth: new Date(time.getFullYear(), time.getMonth() - 1, 1),
            nMonth: new Date(time.getFullYear(), time.getMonth() + 1, 1),
            pYear: new Date(new Date(time).getFullYear() - 1, 0, 1),
            nYear: new Date(new Date(time).getFullYear() + 1, 0, 1)
        }
    }

    // Returns the number of days in the month
    countOfDaysInMonth(time) {
        let date = this.getMonthAndYear(time);
        return new Date(date.year, date.month + 1, 0).getDate();
    }

    // Returns the first day of the week for that month
    getStartedDayOfWeekByTime(time) {
        let date = this.getMonthAndYear(time);
        return new Date(date.year, date.month, 1).getDay();
    }

    // Returns month and year
    getMonthAndYear(time) {
        let date = new Date(time);
        return {
            year: date.getFullYear(),
            month: date.getMonth()
        }
    }

    // Returns a formated date that can be used to rwd lists from the event list
    getFormattedDate(date) {
        let day_digit = ( date.getDate() >= 10 ) ? date.getDate() : '0' + date.getDate();
        let month_digit = ( (date.getMonth() + 1) >= 10 ) ? (date.getMonth() + 1) : '0' + (date.getMonth() + 1)

        return `${month_digit}/${day_digit}/${date.getFullYear()}`;
    }

    // todo
    range(number) {
        return new Array(number).fill().map((e, i) => i);
    }

    // Returns the repeat event list
    getReturnEventList(eventType){
        if(eventType === 2){
            return this.dailyRepeatEventList;
        }
        // Weekly
        else if(eventType === 3){
            return this.weeklyRepeatEventList;
        }
        // Monthly
        else if(eventType === 4){
            return this.monthlyRepeatEventList;
        }
        // Yearly
        else if(eventType === 5){
            return this.yearlyRepeatEventList;
        }
    }

    // Initializes the events
    eventsTrigger() {

        // Show pervious month
        this.elements.prevMonth.addEventListener('click', e => {
            let calendar = this.getCalendar();
            this.updateTime(calendar.pMonth);
            this.drawAll()
        });

        // Show next month
        this.elements.nextMonth.addEventListener('click', e => {
            let calendar = this.getCalendar();
            this.updateTime(calendar.nMonth);
            this.drawAll()
        });

        // Go to day
        this.elements.days.addEventListener('click', e => {

            let element = e.srcElement;

            // If current element does not have the attribute, use the parent element
            element = element.getAttribute('data-day') ? element : element.parentElement;

            let day = element.getAttribute('data-day');
            let month = element.getAttribute('data-month');
            let year = element.getAttribute('data-year');

            if (!day) {
                return false;
            }

            let strDate = `${Number(month) + 1}/${day}/${year}`;
            this.updateTime(strDate);
            this.drawAll()
        });

        // Display event form
        this.elements.eventAddBtn.addEventListener('click', e => {
            this.toggleModalEventForm();
        });

        // Save event
        this.elements.eventForm.addEventListener('submit', e => {
            let thisCalendar = this;

            $.ajax({
                type: 'POST',
                url: '/events/detail',
                data: {
                    event_id: document.querySelector('#event_id').value,
                    title: document.querySelector('#title').value,
                    description: document.querySelector('#description').value,
                    event_type: document.querySelector('#event_type').value,
                    repeat_type: document.querySelector('#repeat_type').value,
                    start_date: document.querySelector('#start_date').value,
                    start_time: document.querySelector('#start_time').value,
                    end_time: document.querySelector('#end_time').value,
                    is_calendar_form: true,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(data){
                    let newEvent = JSON.parse(data);

                    // Update the event if it exists in the event list
                    let isNotUpdate = true
                    const eventDate = thisCalendar.getCalendar().active.formatted;
                    const eventDateList = thisCalendar.eventList[eventDate];
                    const repeatEventDateList = thisCalendar.tempEventRepeatList[eventDate];

                    if(eventDateList){
                        eventDateList.forEach( (eventItem, index) => {
                            if(eventItem.event_id === newEvent.event_id ){
                                eventDateList[index].title = newEvent.title;
                                eventDateList[index].description = newEvent.description;
                                eventDateList[index].event_type = newEvent.event_type;
                                eventDateList[index].repeat_type = newEvent.repeat_type;
                                eventDateList[index].start_time = newEvent.start_time;
                                eventDateList[index].end_time = newEvent.end_time;
                                eventDateList[index].is_completed = newEvent.is_completed;

                                isNotUpdate = false;
                            }
                        });
                    }

                    if(repeatEventDateList){
                        repeatEventDateList.forEach( (eventItem, index) => {
                            if(eventItem.event_id === newEvent.event_id ){
                                repeatEventDateList[index].title = newEvent.title;
                                repeatEventDateList[index].description = newEvent.description;
                                repeatEventDateList[index].event_type = newEvent.event_type;
                                repeatEventDateList[index].repeat_type = newEvent.repeat_type;
                                repeatEventDateList[index].start_time = newEvent.start_time;
                                repeatEventDateList[index].end_time = newEvent.end_time;
                                repeatEventDateList[index].is_completed = newEvent.is_completed;

                                isNotUpdate = false;
                            }
                        });
                    }

                    // Remove from repeat list
                    let repeatList = thisCalendar.getReturnEventList(thisCalendar.currentEvent.repeat_type);
                    if(repeatList){
                        let eventIndex; 
                        repeatList.forEach( (event, index) => {
                            if(event.event_id === newEvent.event_id){
                                eventIndex = index;
                            }
                        });
                        if(eventIndex){
                            repeatList.splice(eventIndex, 1);
                        }
                    }

                    // Add to repeat list
                    if(Number(newEvent.repeat_type) !== 1){
                        repeatList = thisCalendar.getReturnEventList(newEvent.repeat_type);
                        repeatList.push(newEvent);
                    }

                    // Update current event
                    thisCalendar.currentEvent = newEvent;

                    // Save the event if it doesn't exist in the event list
                    if(isNotUpdate){
                        let dateFormatted = thisCalendar.getFormattedDate(new Date(thisCalendar.date));
                        if (!thisCalendar.eventList[dateFormatted]) thisCalendar.eventList[dateFormatted] = [];
                        thisCalendar.eventList[dateFormatted].push(newEvent);

                        // Sort list again
                        thisCalendar.eventList[dateFormatted].sort(thisCalendar.compareStartTimes);
                    }

                    // Clear form and state
                    thisCalendar.clearAddEventFormState(true);
                }
            });

            // Prevent form submission with redirect
            e.preventDefault();
        });

        // Load event fields
        this.elements.currentDayEventsList.addEventListener('click', e => {
            // Check if an event was clicked
            if(e.target.classList.contains('current-event-item') && e.target.hasAttribute('event-id')){
                // Get event id from attribute
                let eventId = e.target.getAttribute('event-id');

                // Save this value to calendar variable in order to use it inside the success callback
                let thisCalendar = this;

                $.ajax({
                    type: 'GET',
                    url: '/events/detail',
                    data: {
                        event_id: eventId,
                        is_calendar_form: true
                    },
                    success: function(data){
                        let eventData = JSON.parse(data);

                        // Keep the current event
                        thisCalendar.currentEvent = eventData;

                        let eventStartDate = eventData.start_date.substring(0,10);

                        // Populate form fields
                        document.querySelector('#event_id').value = eventData.event_id;
                        document.querySelector('#title').value = eventData.title;
                        document.querySelector('#description').value = eventData.description;
                        document.querySelector('#event_type').value = eventData.event_type;
                        document.querySelector('#repeat_type').value = eventData.repeat_type;
                        document.querySelector('#start_date').value = eventStartDate;
                        document.querySelector('#start_time').value = eventData.start_time;
                        document.querySelector('#end_time').value = eventData.end_time;

                        // If event is completed, add end_date and display the field
                        if(eventData.end_date){
                            let eventEndDate = eventData.end_date.substring(0,10);
                            document.querySelector('#end_date').value = eventEndDate;
                            thisCalendar.elements.eventEndDateField.classList.remove('d-none');
                            thisCalendar.elements.saveEventFormButton.classList.add('d-none');
                        }

                        // Show form
                        thisCalendar.toggleModalEventForm();

                        // Add Exam button attributes and make it visible if event is Exam
                        if(eventData.event_type === 4){
                            thisCalendar.examButton.classList.remove('d-none')
                            thisCalendar.examButton.textContent = 'Go to Exam'
                            // thisCalendar.examButton
                        }

                    }
                });
            }
        })

        // Remove event
        this.elements.eventList.addEventListener('click', e => {
            if(e.target.classList.contains('remove-event')){
                const eventElement = e.target.parentElement.parentElement;
                let eventDate = this.getCalendar().active.formatted;
                const eventId = eventElement.getAttribute("event-id");
                const repeatType = eventElement.getAttribute("repeat-type");

                let thisCalendar = this;

                $.ajax({
                    type: 'POST',
                    url: '/events/remove',
                    data:{
                        event_id: eventId,
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success:function(){
                        // Remove from UI
                        eventElement.remove();

                        // Remove from repeat list
                        if(Number(repeatType) !== 1){
                            let repeatList = thisCalendar.getReturnEventList(Number(repeatType));
                            if(repeatList){
                                let eventIndex; 
                                repeatList.forEach( (event, index) => {
                                    if(event.event_id === Number(eventId)){
                                        eventDate = event.start_date;
                                        eventIndex = index;
                                    }
                                });
                                repeatList.splice(eventIndex, 1);
                            }
                        }

                        // Remove from the eventDateList
                        let eventDateList = thisCalendar.eventList[eventDate];

                        eventDateList.forEach( (eventItem, index) => {
                            if(eventItem.event_id === Number(eventId) ){
                                eventDateList.splice(index, 1);
                            }
                        });

                        //If eventDateList is empty, remove it from the eventList
                        if(eventDateList.length === 0){
                            delete thisCalendar.eventList[eventDate];
                        }

                        thisCalendar.drawAll();
                    }
                });
            }
        })

        // Complete event
        this.elements.eventList.addEventListener('click', e => {
            if(e.target.classList.contains('complete-event')){
                const eventElement = e.target.parentElement.parentElement;
                const eventDate = this.getCalendar().active.formatted;
                const eventId = eventElement.getAttribute("event-id");

                let thisCalendar = this;

                $.ajax({
                    type: 'POST',
                    url: '/events/complete',
                    data:{
                        event_id: eventId,
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function(data){
                        let eventEndDateData = JSON.parse(data);
                        
                        // Update event to is_complete = true
                        let eventDateList = thisCalendar.eventList[eventDate];

                        // If not found on main list, get in repeat list
                        if(!eventDateList){
                            eventDateList = thisCalendar.tempEventRepeatList[eventDate];
                        }

                        eventDateList.forEach( eventItem => {
                            if(eventItem.event_id === Number(eventId) ){
                                eventItem.is_completed = true;
                                eventItem.end_date = eventEndDateData.end_date;
                            }
                        });

                        thisCalendar.drawAll();
                    }
                });
            }
        })

        // Clear event form when the back button is clicked
        this.elements.eventFormBackArrow.addEventListener('click', e => {
            this.clearAddEventFormState();
        })

        // Go to today
        this.elements.todayBtn.addEventListener('click', e => {
            this.updateTime(new Date());
            this.drawAll()
        });

        // -- Current Day Modal Events --

        // Open the current day modal
        $('#current-day-modal').on('show.bs.modal', function(e) {
            let activeDate = calendar.getCalendar().active; 
        
            let day = activeDate.day;
            let month = activeDate.month + 1;
            let year = activeDate.year;
        
            if (day < 10){
                day = "0" + day;
            }
            if (month < 10){
                month = "0" + month;
            }
        
            let formatedDate = year + '-' + month + '-' + day;
            
            // Pass the current day date to the start_date field of the event form
            let modal = $(this)
            modal.find('#start_date').val(formatedDate)
          });
        
        // Close the current day modal
        $('#current-day-modal').on('hide.bs.modal', function(e) {
            // Clear form
            document.querySelector('#event_id').value = null;
            document.querySelector('#title').value = null;
            document.querySelector('#description').value = null;
            document.querySelector('#event_type').value = 1;
            document.querySelector('#repeat_type').value = 1;
            document.querySelector('#start_date').value = null;
            document.querySelector('#start_time').value = null;
            document.querySelector('#end_time').value = null;
        
            // Hide form
            document.querySelector('#current-day-event-list').classList.remove('d-none');
            document.querySelector('.current-day-footer').classList.remove('d-none');
            document.querySelector('#current-day-modal-label').classList.remove('d-none');
            document.querySelector('#save-event-form-btn').classList.remove('d-none');
            document.querySelector('#current-day-add-event-form').classList.add('d-none');
            document.querySelector('#event-form-back').classList.add('d-none');
            document.querySelector('#end_date_field').classList.add('d-none');

        });

    }

}

const calendar = (function () {
    return new Calendar({
        id: "calendar"
    })
})();

