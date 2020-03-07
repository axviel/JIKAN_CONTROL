const AVAILABLE_WEEK_DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const AVALIABLE_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

// todo
const localStorageName = 'calendar-events';

class CALENDAR {
    constructor(options) {
        this.options = options;
        this.elements = {
            days: document.querySelector('.calendar-day-list'),
            week: document.querySelector('.calendar-week-list'),
            year: document.querySelector('.calendar-current-year'),
            eventField: document.querySelector('.add-event-day-field'),
            eventList: document.querySelector('.current-day-events-list'),
            eventAddBtn: document.querySelector('.add-event-day-field-btn'),
            todayBtn: document.querySelector('.calendar-today-btn'),
            currentDay: document.querySelector('.current-day-number'),
            currentWeekDay: document.querySelector('.current-day-of-week'),
            prevMonth: document.querySelector('.calendar-change-month-slider-prev'),
            nextMonth: document.querySelector('.calendar-change-month-slider-next'),
            currentMonth: document.querySelector('.calendar-current-month')
        };

        // todo
        // this.eventList = JSON.parse(localStorage.getItem(localStorageName)) || {};
        this.eventList = JSON.parse(document.getElementById('calendar-events').textContent) || {};

        this.date = +new Date();
        this.options.maxDays = 42;
        this.init();
    }

    // App methods
    init() {
        if (!this.options.id) return false;
        this.eventsTrigger();
        this.drawAll();
    }

    // draw Methods
    drawAll() {
        this.drawWeekDays();
        this.drawDays();
        this.drawYearAndCurrentDay();
        this.drawEvents();

    }

    drawEvents() {
        let calendar = this.getCalendar();
        let eventList = this.eventList[calendar.active.formatted] || ['There is not any events'];
        let eventTemplate = "";
        eventList.forEach(item => {
            eventTemplate += `<a href="#" class="list-group-item list-group-item-action current-event-item">${item} <i class="fa fa-remove remove-event"></i></a>`;
        });

        this.elements.eventList.innerHTML = eventTemplate;
    }

    drawYearAndCurrentDay() {
        let calendar = this.getCalendar();
        this.elements.currentMonth.innerHTML = AVALIABLE_MONTHS[calendar.active.month];
        this.elements.year.innerHTML = calendar.active.year;
        this.elements.currentDay.innerHTML = calendar.active.day;
        this.elements.currentWeekDay.innerHTML = AVAILABLE_WEEK_DAYS[calendar.active.week];
    }

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

            let formatted = this.getFormattedDate(new Date(`${Number(day.month) + 1}/${day.dayNumber}/${day.year}`));

            newDayParams.hasEvent = this.eventList[formatted];
            return newDayParams;
        });

        let daysTemplate = "";
        let firstEvent = "";
        let secondEvent = "";
        let smallEvent = "";

        days.forEach(day => {

            if(day.hasEvent){
                firstEvent = `<div class="event event-large">${'06:00 ' + day.hasEvent[0]}</div>`;
                if(day.hasEvent.length > 1){
                    secondEvent = `<div class="event event-large">${day.hasEvent.length === 2 ? '06:00 ' + day.hasEvent[1] : (day.hasEvent.length - 1) + ' more events'}</div>`;
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

    drawWeekDays() {
        let weekTemplate = "";
        AVAILABLE_WEEK_DAYS.forEach(week => {
            weekTemplate += `<div class="week-day-item">${week.slice(0, 3)}</div>`
        });

        this.elements.week.innerHTML = weekTemplate;
    }

    // Service methods
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
            // Event propagation when click day-number
            element = element.getAttribute('data-day') ? element : element.parentElement;
            let day = element.getAttribute('data-day');
            let month = element.getAttribute('data-month');
            let year = element.getAttribute('data-year');
            if (!day) return false;
            let strDate = `${Number(month) + 1}/${day}/${year}`;
            this.updateTime(strDate);
            this.drawAll()
        });

        // Add event
        this.elements.eventAddBtn.addEventListener('click', e => {
            let fieldValue = this.elements.eventField.value;
            if (!fieldValue) return false;
            let dateFormatted = this.getFormattedDate(new Date(this.date));
            if (!this.eventList[dateFormatted]) this.eventList[dateFormatted] = [];
            this.eventList[dateFormatted].push(fieldValue);
            // localStorage.setItem(localStorageName, JSON.stringify(this.eventList));
            this.elements.eventField.value = '';
            this.drawAll();
        });

        // Remove event
        this.elements.eventList.addEventListener('click', e => {
            if(e.target.classList.contains('remove-event')){
                const eventElement = e.target.parentElement;
                const eventName = eventElement.textContent;
                const eventDate = this.getCalendar().active.formatted;

                // Remove from UI
                eventElement.remove();

                // Remove from local storage
                const eventDateList = this.eventList[eventDate];

                eventDateList.forEach( (eventItem, index) => {
                    if(eventItem === eventName || eventName.includes(eventItem)){
                        eventDateList.splice(index, 1);
                      }
                });

                //If eventDateList is empty,remove it from the eventList
                if(eventDateList.length === 0){
                    delete this.eventList[eventDate];
                }

                // localStorage.setItem(localStorageName, JSON.stringify(this.eventList));
                // django remove
                $.ajax({
                    type: 'POST',
                    url: '/events/remove',
                    data:{
                        title: eventName,
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success:function(){
                        alert('Event removed!')
                    }
                });


                this.drawAll();
            }
        })

        // Go to today
        this.elements.todayBtn.addEventListener('click', e => {
            this.updateTime(new Date());
            this.drawAll()
        });

    }


    updateTime(time) {
        this.date = +new Date(time);
    }

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

    countOfDaysInMonth(time) {
        let date = this.getMonthAndYear(time);
        return new Date(date.year, date.month + 1, 0).getDate();
    }

    getStartedDayOfWeekByTime(time) {
        let date = this.getMonthAndYear(time);
        return new Date(date.year, date.month, 1).getDay();
    }

    getMonthAndYear(time) {
        let date = new Date(time);
        return {
            year: date.getFullYear(),
            month: date.getMonth()
        }
    }

    getFormattedDate(date) {
        // return `${date.getDate()}/${date.getMonth()}/${date.getFullYear()}`;


        let day_digit = ( date.getDate() >= 10 ) ? date.getDate() : '0' + date.getDate();
        let month_digit = ( (date.getMonth() + 1) >= 10 ) ? (date.getMonth() + 1) : '0' + (date.getMonth() + 1)

        // let formated2 = `${day_digit}/${month_digit}/${day.year}`;

        return `${day_digit}/${month_digit}/${date.getFullYear()}`;
    }

    range(number) {
        return new Array(number).fill().map((e, i) => i);
    }
}


// (function () {
//     new CALENDAR({
//         id: "calendar"
//     })
// })();

let calendar = (function () {
    return new CALENDAR({
        id: "calendar"
    })
})();

//-------------


$('#event-form-modal').on('show.bs.modal', function (event) {
    var activeDate = calendar.getCalendar().active.formatted; 
    var modal = $(this)
    modal.find('#active-date').val(activeDate)
  })