const AVAILABLE_WEEK_DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const AVALIABLE_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

class Calendar {
    constructor(options) {
        this.options = options;
        this.elements = {
            days: document.querySelector('.calendar-day-list'),
            weekDays: document.querySelector('.calendar-weekdays-list'),
            weekDaysForWeekView: document.querySelector('.calendar-week-weekdays-list'),
            year: document.querySelector('.calendar-current-year'),
            eventList: document.querySelector('.current-day-events-list'),
            eventAddBtn: document.querySelector('.add-event-day-btn'),
            todayBtn: document.querySelector('.calendar-today-btn'),
            viewBtn: document.querySelector('.calendar-view-btn'),
            currentDay: document.querySelector('.current-day-number'),
            currentWeekDay: document.querySelector('.current-day-of-week'),
            prevMonth: document.querySelector('.calendar-change-month-slider-prev'),
            nextMonth: document.querySelector('.calendar-change-month-slider-next'),
            prevWeek: document.querySelector('.calendar-change-week-slider-prev'),
            nextWeek: document.querySelector('.calendar-change-week-slider-next'),
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
            eventTypeSelect: document.querySelector('#event_type'),
            repeatTypeSelect: document.querySelector('#repeat_type'),
            week: document.querySelector('.calendar-week-list'),
        };

        // Used to toggle modal event list and form states
        this.currentDayModalFormToggle = false;

        // Store the event list passed by the backend
        this.eventList = JSON.parse(document.getElementById('calendar-events').textContent) || {};

        // Visible events
        this.visibleEvents = {};

        // Current event on the modal
        this.currentEvent = {};

        // Current date
        this.date = new Date();

        // Number of days show in the calendar
        this.options.maxDays = 42;

        // Default calendar view mode
        this.monthView = true;

        // Initializes the events and draws all the days, weeks, years, and events
        this.init();
    }

    // App methods
    init() {
        if (!this.options.id) return false;
        this.eventsTrigger();
        this.drawWeekTemplate();
        this.drawAll();
    }

    // Draw Methods
    drawAll() {
        this.getAllEventInstancesInRange();
        this.drawWeekDays();
        this.drawCalendarDays();
        this.drawTopMonthYearAndCurrentDayNumberWeekday();
        this.drawCurrentDayEventList();

        this.drawWeekView();
    }

    // Draws week view template
    drawWeekTemplate(){
        let weekViewTemplate = '';
        for(let weekdayIndex = -1; weekdayIndex < 7; weekdayIndex++){
            weekViewTemplate += '<div class="weekday-item">';

            for(let hourIndex = 0; hourIndex < 24; hourIndex++){

                if(weekdayIndex === -1){
                    weekViewTemplate += `
                    <div class="hour-item text-center calendar-hour">
                        ${hourIndex < 10 ? '0' + hourIndex + ':00' : hourIndex + ':00'}
                    </div>`;
                    continue;
                }
                weekViewTemplate += `<div 
                class="hour-item"
                day="${weekdayIndex}" 
                hour="${hourIndex}"
                data-toggle="modal" 
                data-target="#current-day-modal">
                </div>`;
            }

            weekViewTemplate += '</div>';
        }

        this.elements.week.innerHTML = weekViewTemplate;
    }

    // Draws the event list for the current day modal
    drawCurrentDayEventList() {
        let calendar = this.getCalendar();

        let currentDayEventList = this.visibleEvents[calendar.active.formatted] ? this.visibleEvents[calendar.active.formatted] : undefined;

        if(!currentDayEventList){
            currentDayEventList = ['No events to display'];
        }

        let eventTemplate = "<ul class='list-group'>";
        currentDayEventList.forEach(event => {
            if(event.title !== undefined ){
                let startTime = this.convertAMPM(event.start_time);
                let endTime = this.convertAMPM(event.end_time);

                eventTemplate += `
                    <li class="${event.is_completed ? 'bg-info' : ''} current-event-item list-group-item list-group-item-action d-flex justify-content-between align-items-center" event-id="${event.id}" repeat-type="${event.repeat_type}">
                        (${startTime} - ${endTime}) ${event.title}
                        <div> 
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

    // Draws the month and year at the tops of the calendar. Also draws the day number and weekday in the current day section
    drawTopMonthYearAndCurrentDayNumberWeekday() {
        let calendar = this.getCalendar();
        this.elements.currentMonth.innerHTML = AVALIABLE_MONTHS[calendar.active.month];
        this.elements.year.innerHTML = calendar.active.year;
        this.elements.currentDay.innerHTML = calendar.active.day;
        this.elements.currentWeekDay.innerHTML = AVAILABLE_WEEK_DAYS[calendar.active.week];
    }

    // Draws the week view with events in their respective hours
    drawWeekView(){
        // Get current week days and their events
        let calendar = this.getCalendar();

        let curr = new Date(calendar.active.year, calendar.active.month, calendar.active.day);
        let week = [];

        for (let i = 0; i < 7; i++) {
            let first = curr.getDate() - curr.getDay() + i;
            let day = new Date(curr.setDate(first));
            week.push(this.getFormattedDate(day));
        }

        Array.from(document.querySelectorAll('.hour-item')).forEach(hourItem => {
            if(!hourItem.classList.contains('calendar-hour')){
                hourItem.innerHTML = '';
            }
        });

        let hourItemElement;

        let eventHours = {};
        let startTimeKey = '';
        let endHour;
        let endMin;
        let hour;
        let someKey;

        week.forEach( (day, index) => {
            if(day in this.visibleEvents){
                this.visibleEvents[day].forEach(event =>{
                    someKey = event.start_time.substring(0,2);
                    if(someKey in eventHours){
                        eventHours[someKey].push(event)
                    }
                    else{
                        eventHours[someKey] = [event];
                    }
                });

                hour = 0;
                while(hour < 24){
                    startTimeKey = hour < 10 ? '0' + hour : hour;

                    hourItemElement = document.querySelector(`[day="${index}"][hour="${hour}"]`);
                    hourItemElement.innerHTML = '';

                    // If weekday belongs to a different month, add gray color
                    // if(!alreadyAnotherMonth && true){
                    //     hourItemElement.parentElement.classList.add('another-month');

                    //     alreadyAnotherMonth = true;
                    // }

                    if(startTimeKey in eventHours){
                        endHour = hour;
                        endMin = 0;
                        for(let eventIndex = 0; eventIndex < eventHours[startTimeKey].length; eventIndex++) {
                            let event = eventHours[startTimeKey][eventIndex];

                            let startHour = Number(event.start_time.substring(0,2));
                            let endHour = Number(event.end_time.substring(0,2));
                            let endMin = Number(event.end_time.substring(3,5));

                            let hourDiff = endHour - startHour;

                            // If event overlaps other hours
                            if( hourDiff > 1 ||
                                (hourDiff === 1 && endMin > 0)
                            ){
                                hourItemElement.innerHTML += `
                                    <div 
                                    class="event event-large event-multiple spread-${hourDiff}" 
                                    start-hour="${startTimeKey}"
                                    data-toggle="modal" 
                                    data-target="#current-day-modal">
                                        ${event.title} 
                                        ${
                                            (eventHours[startTimeKey].length > 1 && eventIndex == 0) || 
                                            (eventHours[startTimeKey].length > 2 && eventIndex == 1) 
                                            ? 'and more' : ''}
                                    </div>
                                `;
                                break;
                            }

                            if(eventHours[startTimeKey].length > 2 && eventIndex == 1){
                                hourItemElement.innerHTML += `
                                    <div 
                                    class="event event-large text-center event-multiple" 
                                    start-hour="${startTimeKey}"
                                    data-toggle="modal" 
                                    data-target="#current-day-modal">
                                        ...
                                    </div>
                                `;
                                break;
                            }
                            else{
                                hourItemElement.innerHTML += `
                                    <div 
                                    class="event event-large event-single ${event.is_completed ? "bg-info text-dark" : "" }" 
                                    event-id="${event.id}"
                                    data-toggle="modal" 
                                    data-target="#current-day-modal">
                                        ${event.title}
                                    </div>
                                `;
                            }
                        }

                        hour++;
                    }
                    else{
                        hour++;
                    }
                }

                // Clear after use
                eventHours = {};
            }

        });
    }

    // Draws the calendar days with their events
    drawCalendarDays() {
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
            
            newDayParams.hasEvent = this.visibleEvents[newDayParams.formatedDate] ? [].concat(this.visibleEvents[newDayParams.formatedDate]) : null;
            return newDayParams;
        });

        let daysTemplate = "";

        let dayInnerHTML = ``;

        days.forEach(day => {

            if(day.hasEvent){
                for(let i = 0; i < day.hasEvent.length; i++){
                    // If more than 3 events, show a shortened version in the last event slot
                    if(day.hasEvent.length > 3 && i === 2){
    
                        dayInnerHTML += `
                            <div class="event event-large text-center">
                                ...
                            </div>
                        `;
    
                        break;
                    }
    
                    dayInnerHTML += `
                        <div class="event event-large ${day.hasEvent[i].is_completed ? 'bg-info text-dark' : ''}">
                            ${day.hasEvent[i].start_time} ${day.hasEvent[i].title}
                        </div>
                    `;
                }
    
                // Small event that's displayed on small screens
                // dayInnerHTML += `
                //     <div class="event event-small">
                //         ${day.hasEvent.length === 1 ? '1 event' : day.hasEvent.length + ' events'}
                //     </div>
                // `;
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
                    ${day.hasEvent ? dayInnerHTML : ''}
                </div>
            `

            dayInnerHTML = '';
        });

        this.elements.days.innerHTML = daysTemplate;
    }

    // Draws the calendar week days
    drawWeekDays() {
        let calendar = this.getCalendar();

        let curr = new Date(calendar.active.year, calendar.active.month, calendar.active.day);
        let weekList = [];

        for (let i = 0; i < 7; i++) {
            let first = curr.getDate() - curr.getDay() + i;
            let day = new Date(curr.setDate(first));
            weekList.push(day.getDate());
        }

        let weekTemplate = "";

        // Month View Weekdays
        AVAILABLE_WEEK_DAYS.forEach( (week, index) => {
            weekTemplate += `
            <div class="week-day-item">
                <p class="weekday-large">${week.slice(0, 3)}</p>
                <p class="weekday-small">${week.slice(0, 1)}</p>
            </div>
            `;
        });

        this.elements.weekDays.innerHTML = weekTemplate;

        // Week View weekdays

        weekTemplate = `<div class="week-day-item"></div>`;

        AVAILABLE_WEEK_DAYS.forEach( (week, index) => {
            weekTemplate += `
            <div class="week-day-item">
                <p class="weekday-large">
                    ${week.slice(0, 3)} 
                    <span class="weekday-number d-none'">
                        <br>
                        ${weekList[index]}
                    </span>
                </p>

                <p class="weekday-small">
                    ${week.slice(0, 1)}
                    <span class="weekday-number d-none'">
                            <br>
                            ${weekList[index]}
                    </span>
                </p>
                
            </div>`
        });

        this.elements.weekDaysForWeekView.innerHTML = weekTemplate;
    }

    // Convert 24 hour time to AM/PM
    convertAMPM(timeStr){
        // Get hour
        let hourStr = timeStr.substring(0,2);
        let hourNum = Number(hourStr);

        let newHour = hourNum - 12;
        let isAM = newHour < 0;

        if(isAM){
            return hourNum + timeStr.substring(2) + ' AM'
        }
        else{
            if(newHour === 0){
                newHour = 12;
            }
            
            return newHour + timeStr.substring(2) + ' PM'
        }
    }

    // Returns range for current month (includes prev and next month days that are visible in calendar)
    currentMonthRange(){
        let calendar = this.getCalendar();

        // Find date range
        let pMonthNumOfDays = this.range(calendar.active.startWeek).length;
        let day = this.countOfDaysInMonth(calendar.pMonth) - pMonthNumOfDays + 1;
        let month = new Date(calendar.pMonth).getMonth();
        let year = new Date(calendar.pMonth).getFullYear();

        let startDate = new Date(year, month, day);

        let cMonthNumOfDays = this.range(calendar.active.days).length;
        let countOfRemainingDays = this.options.maxDays - (pMonthNumOfDays + cMonthNumOfDays);

        day = this.range(countOfRemainingDays).length;
        month = new Date(calendar.nMonth).getMonth();
        year = new Date(calendar.nMonth).getFullYear();

        let endDate = new Date(year, month, day);

        return {
            startDate,
            endDate
        };
    }

    // Compares event  start_time in order to sort the list
    compareStartTimes(a, b) {
        if ( a.start_time < b.start_time ){
          return -1;
        }
        if ( a.start_time > b.start_time ){
          return 1;
        }
        return 0;
    }

    // Adds the event to the visibleEvents object
    addVisibleEvent(key, event){
        // New date
        event['start_date'] = key;

        if(key in this.visibleEvents){
            this.visibleEvents[key].push(event);
        }
        else{
            this.visibleEvents[key] = [event];
        }
    }

    // Constructs the visibleEvents list that conatins the events shown in the calendar
    getAllEventInstancesInRange(range = null){
        let calendar = this;

        // If range is null, use the current month range
        if(!range){
            range = this.currentMonthRange();
        }

        let startDate = range.startDate;
        let endDate = range.endDate;

        // 'Clone' eventList so that the event start_dates don't get overwritten when repeated events are added
        let cloneEventList = JSON.parse(JSON.stringify(this.eventList));

        // Get events in that would appear in this range
        let eventCollection = cloneEventList.filter(event => {
            return !event.is_hidden &&
            (
                (
                    event.repeat_type !== 1 &&
                    Date.parse(event.start_date) <= endDate.getTime() &&
                    (
                        event.end_date === null ||
                        Date.parse(event.end_date) >= startDate.getTime()
                    )
                ) ||
                (
                    event.repeat_type === 1 &&
                    Date.parse(event.start_date) >= startDate.getTime() &&
                    Date.parse(event.start_date) <= endDate.getTime()
                )
            )
        });

        this.visibleEvents = {}; // Clear events
        let currentDate = new Date(startDate.getTime());

        let event;
        let eventRepeatTypeId;
        let eventStartDate;
        let eventEndDate;
        let eventWeekday;
        let eventDay;
        let eventMonth;
        let eventYear;
        let key;

        // Insert into visibleEvents all the instances of the events that will be visible during the period
        // Interate until currentDate = endDate
        while(currentDate.getTime() !== endDate.getTime()){

            for(let i = 0; i < eventCollection.length; i++){
                event = eventCollection[i];
                eventRepeatTypeId = event.repeat_type;
                eventStartDate = new Date(event.start_date);
                eventEndDate = event.end_date !== null ? new Date(event.end_date) : null;
                eventWeekday = eventStartDate.getDay();
                eventDay = eventStartDate.getDate();
                eventMonth = eventStartDate.getMonth();
                eventYear = eventStartDate.getYear();
                key = calendar.getFormattedDate(currentDate);

                // If the event is not active, continue with the next iteration
                if(!(eventStartDate.getTime() <= currentDate.getTime() && 
                (eventEndDate === null || eventEndDate.getTime() >= currentDate.getTime()))){
                    continue;
                }

                // If event repeats daily, add it if start_date is gte date_record and end_date is lte daterecord or is null
                if(eventRepeatTypeId === 2){
                    calendar.addVisibleEvent(key, event);
                }
                // If event repats weekly, add it if week day matches daterecord weekday
                else if(eventRepeatTypeId === 3 && eventWeekday === currentDate.getDay()){
                    calendar.addVisibleEvent(key, event);
                }
                // If event repeats monthly, yearly or does not repeat at all, add when conditions match
                else{
                    // If repeats monthly, add if day number is the same
                    if(eventRepeatTypeId === 4 && eventDay === currentDate.getDate()){
                        calendar.addVisibleEvent(key, event);
                    }
                    // If repeats yearly, add if day number and month is the same 
                    else if(eventRepeatTypeId === 5 && eventDay === currentDate.getDate() && eventMonth === currentDate.getMonth()){
                        calendar.addVisibleEvent(key, event);
                    }
                    // If does not repeat, add if day number, month, and year is the same 
                    else if(eventRepeatTypeId === 1 && eventDay === currentDate.getDate() 
                    && eventMonth === currentDate.getMonth() && eventYear === currentDate.getYear()){
                        calendar.addVisibleEvent(key, event);
                    }
                }

            }

            // Increase current date by 1 day
            currentDate.setDate(currentDate.getDate() + 1);
        }

        // Sort events by startTime
        for(key in this.visibleEvents){
            if(this.visibleEvents[key].length !== 1){
                this.visibleEvents[key].sort(this.compareStartTimes);
            }
        }
    }

    // Clears the add evnt form, shows the event list state, and re-draws everything
    clearAddEventFormState(isNewEvent = false){
        // Clear fields
        document.querySelector('#event_id').value = "";
        document.querySelector('#title').value = "";
        document.querySelector('#description').value = "";
        document.querySelector('#event_type').value = "1";
        document.querySelector('#repeat_type').value = "1";
        document.querySelector('#start_time').value = "";
        document.querySelector('#end_time').value = "";

        this.elements.repeatTypeSelect.removeAttribute('disabled');

        // Hide end_date field if it was visible and show save button
        this.elements.eventEndDateField.classList.add('d-none');
        this.elements.examButton.classList.add('d-none');
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
            pWeek: new Date(time.getFullYear(), time.getMonth(), time.getDate() - 7 - time.getDay()),
            nWeek: new Date(time.getFullYear(), time.getMonth(), time.getDate() + 7 - time.getDay()),
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

    // TODO
    range(number) {
        return new Array(number).fill().map((e, i) => i);
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

        // Show pervious week
        this.elements.prevWeek.addEventListener('click', e => {
            let calendar = this.getCalendar();
            this.updateTime(calendar.pWeek);
            this.drawAll()
        });

        // Show next week
        this.elements.nextWeek.addEventListener('click', e => {
            let calendar = this.getCalendar();
            this.updateTime(calendar.nWeek);
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

        // Go to weekday
        this.elements.week.addEventListener('click', e => {
            let element = e.srcElement;

            // If current element does not have the attribute, use the parent element
            element = element.getAttribute('day') ? element : element.parentElement;

            let weekday = element.getAttribute('day');

            if (!weekday) {
                return false;
            }
            let calendar = this.getCalendar();

            let curr = new Date(calendar.active.year, calendar.active.month, calendar.active.day);
            let weekList = [];

            for (let i = 0; i < 7; i++) {
                let first = curr.getDate() - curr.getDay() + i;
                let day = new Date(curr.setDate(first));
                weekList.push(day);
            }

            let selectedDay = weekList[Number(weekday)];

            let strDate = this.getFormattedDate(selectedDay);
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
                    let eventData = JSON.parse(data);
                    let foundEvent = thisCalendar.eventList.find(event => event.id === eventData.id);

                    if(foundEvent){
                        // Update existing event data
                        foundEvent.title = eventData.title;
                        foundEvent.description = eventData.description;
                        foundEvent.event_type = eventData.event_type;
                        foundEvent.repeat_type = eventData.repeat_type;
                        foundEvent.start_time = eventData.start_time;
                        foundEvent.end_time = eventData.end_time;
                    }
                    else{
                        // Add new event to calendar
                        thisCalendar.eventList.push(eventData);
                    }

                    // Update current event
                    thisCalendar.currentEvent = foundEvent ? foundEvent : eventData;

                    // Clear form and state
                    thisCalendar.clearAddEventFormState(true);
                }
            });

            // TODO onError show something like a notif

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

                        // If exam, disable repeat type select
                        if(eventData.event_type === 4){
                            thisCalendar.elements.repeatTypeSelect.setAttribute('disabled', true);
                        }

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
                            thisCalendar.elements.examButton.classList.remove('d-none');
                        }

                    }
                });
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

                        // Mark the event as hidden
                        let deletedEvent = thisCalendar.eventList.find(event => event.id === Number(eventId));
                        deletedEvent.is_hidden = true;

                        thisCalendar.drawAll();
                    }
                });
            }
        });

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
                        // TODO Handle complete 

                        let eventEndDateData = JSON.parse(data);
                        
                        // Update event to is_completed = true
                        let completedEvent = thisCalendar.eventList.find(event => event.id === Number(eventId));
                        completedEvent.is_completed = true;
                        completedEvent.end_date = eventEndDateData.end_date;

                        thisCalendar.drawAll();
                    }
                });
            }
        });

        // Clear event form when the back button is clicked
        this.elements.eventFormBackArrow.addEventListener('click', e => {
            this.clearAddEventFormState();
        });

        // Go to today
        this.elements.todayBtn.addEventListener('click', e => {
            this.updateTime(new Date());
            this.drawAll();
        });

        // Change Calendar View Mode from Month to Week and vice versa
        this.elements.viewBtn.addEventListener('click', e => {
            // Show week
            if(this.monthView){
                this.elements.days.classList.add('d-none');
                this.elements.weekDays.classList.add('d-none');
                this.elements.week.classList.remove('d-none');
                this.elements.weekDaysForWeekView.classList.remove('d-none');
                Array.from(document.querySelectorAll('.change-month')).forEach(arrow => {
                    arrow.classList.add('d-none');
                });
                Array.from(document.querySelectorAll('.change-week')).forEach(arrow => {
                    arrow.classList.remove('d-none');
                });

                // Show weekday number
                this.elements.weekDays.classList.add('mb-3');
                let weekdayNumbers = Array.from(document.querySelectorAll('.weekday-number'));
                weekdayNumbers.forEach(weekday => {
                    weekday.classList.remove('d-none');
                });

                // Button text
                e.target.textContent = 'Month';

                this.monthView = !this.monthView;
            }
            // Show month
            else{
                this.elements.days.classList.remove('d-none');
                this.elements.weekDays.classList.remove('d-none');
                this.elements.week.classList.add('d-none');
                this.elements.weekDaysForWeekView.classList.add('d-none');
                Array.from(document.querySelectorAll('.change-month')).forEach(arrow => {
                    arrow.classList.remove('d-none');
                });
                Array.from(document.querySelectorAll('.change-week')).forEach(arrow => {
                    arrow.classList.add('d-none');
                });

                // Hide weekday number
                this.elements.weekDays.classList.remove('mb-3');
                let weekdayNumbers = Array.from(document.querySelectorAll('.weekday-number'));
                weekdayNumbers.forEach(weekday => {
                    weekday.classList.add('d-none');
                });

                // Button text
                e.target.textContent = 'Week';

                this.monthView = !this.monthView;
            }
        });

        // Disable Repeat Type if Event Type is exam
        this.elements.eventTypeSelect.addEventListener('click', e => {
            if(e.target.value === '4'){
                this.elements.repeatTypeSelect.value = '1';
                this.elements.repeatTypeSelect.setAttribute('disabled', true);
            }
            else{
                this.elements.repeatTypeSelect.removeAttribute('disabled');
            }
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
            document.querySelector('#exam-btn').classList.add('d-none');

            document.querySelector('#repeat_type').removeAttribute('disabled');

        });

    }

}

const calendar = (function () {
    return new Calendar({
        id: "calendar"
    })
})();

