/*var Calendar = tui.Calendar; // CommonJS
var calendar;
window.onload = function() {
	document.getElementById("calendar").style.width = window.innerWidth * 0.9;

	window.addEventListener("resize", function() {
		document.getElementById("calendar").style.width = window.innerWidth * 0.9;
	});

	var calendar = new Calendar('#calendar', {
		defaultView: 'month',
		taskView: true,
		template: {
			monthGridHeader: function(model) {
				var date = new Date(model.date);
				var template = '<span class="tui-full-calendar-weekday-grid-date">' + date.getDate() + '</span>';
				return template;
			}
		},
		month: {
			daynames: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
			moreLayerSize: {
			    height: 'auto'
			},
			grid: {
			    header: {
			        header: 34
			    },
			    footer: {
			        height: 10
			    }
			},
			narrowWeekend: false,
			startDayOfWeek: 1, // monday
			visibleWeeksCount: 6,
			visibleScheduleCount: 100
	    },
	    week: {
	        daynames: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
	        narrowWeekend: false,
	        startDayOfWeek: 0 // monday
	    },
	    template: {
		    milestone: function(schedule) {
		        return '<span style="color:red;"><i class="fa fa-flag"></i> ' + schedule.title + '</span>';
		    },
		    milestoneTitle: function() {
		        return 'Milestone';
		    },
		    task: function(schedule) {
		        return '&nbsp;&nbsp;#' + schedule.title;
		    },
		    taskTitle: function() {
		        return '<label><input type="checkbox" />Task</label>';
		    },
		    allday: function(schedule) {
		        return schedule.title + ' <i class="fa fa-refresh"></i>';
		    },
		    alldayTitle: function() {
		        return 'All Day';
		    },
		    time: function(schedule) {
		        return schedule.title + ' <i class="fa fa-refresh"></i>' + schedule.start;
		    },
		    monthMoreTitleDate: function(date) {
		        date = new Date(date);
		        return tui.util.formatDate('MM-DD', date) + '(' + daynames[date.getDay()] + ')';
		    },
		    monthMoreClose: function() {
		        return '<i class="fa fa-close"></i>';
		    },
		    monthGridHeader: function(model) {
		        var date = new Date(model.date);
		        var template = '<span class="tui-full-calendar-weekday-grid-date">' + date.getDate() + '</span>';
		        var today = model.isToday ? 'TDY' : '';
		        if (today) {
		            template += '<span class="tui-full-calendar-weekday-grid-date-decorator">' + today + '</span>';
		        }
		        if (tempHolidays[date.getDate()]) {
		            template += '<span class="tui-full-calendar-weekday-grid-date-title">' + tempHolidays[date.getDate()] + '</span>';
		        }
		        return template;
		    },
		    monthGridHeaderExceed: function(hiddenSchedules) {
		        return '<span class="calendar-more-schedules">+' + hiddenSchedules + '</span>';
		    },
		    monthGridFooter: function() {
		        return '<div class="calendar-new-schedule-button">New Schedule</div>';
		    },
		    monthGridFooterExceed: function(hiddenSchedules) {
		        return '<span class="calendar-footer-more-schedules">+ See ' + hiddenSchedules + ' more events</span>';
		    },
		    weekDayname: function(dayname) {
		        return '<span class="calendar-week-dayname-name">' + dayname.dayName + '</span><br><span class="calendar-week-dayname-date">' + dayname.date + '</span>';
		    },
		    monthDayname: function(dayname) {
		        return '<span class="calendar-week-dayname-name">' + dayname.label + '</span>';
		    },
		    timegridDisplayPrimayTime: function(time) {
		        var meridiem = time.hour < 12 ? 'am' : 'pm';
		        return time.hour + ' ' + meridiem;
		    },
		    timegridDisplayTime: function(time) {
		        return time.hour + ':' + time.minutes;
		    }
		}
	});
	// calendar.setOptions({disableDblClick: true}, true);
	
	let calendarSchedules = new Array();
	let index = 0;
	for (let x in schedule) {
		// console.log(schedule[x]);
		index++;
		calendarSchedules.push({
			id: index.toString(),
			calendarId: '1',
			title: schedule[x].task_name,
			category: "time",
			dueDateClass: "",
			start: schedule[x].start_time.toISOString(),	//'2018-01-18T22:30:00+09:00',
			end: schedule[x].end_time.toISOString()//'2018-01-19T02:30:00+09:00'
		});
	}
	console.log(calendarSchedules);
	calendar.createSchedules(calendarSchedules);
}*/

/*window.onload = function() {	
	let calendarSchedules = new Array();
	let index = 0;
	for (let x in schedule) {
		// console.log(schedule[x]);
		index++;
		calendarSchedules.push({
			id: index.toString(),
			calendarId: '1',
			title: schedule[x].task_name,
			category: "time",
			dueDateClass: "",
			start: schedule[x].start_time.toISOString(),	//'2018-01-18T22:30:00+09:00',
			end: schedule[x].end_time.toISOString()//'2018-01-19T02:30:00+09:00'
		});
	}
	console.log(calendarSchedules);
}*/
var calendar;

$(function() {
	console.log("Document is ready");
	document.getElementById("calendar").style.width = window.innerWidth * 0.9;
	window.addEventListener("resize", function() {
		document.getElementById("calendar").style.width = window.innerWidth * 0.9;
	});

	// var utc = $.fullCalendar.moment.utc('2014-05-01T12:00:00');
	calendar = $('#calendar').fullCalendar({
		dayClick: function(day_moment, e) {
			console.log(day_moment, e);
		}, header: {
			center: 'month,agendaWeek,agendaDay',
			left: 'title'
		}, views: {
			month: {
				titleFormat: 'YYYY, MM, DD'
			},
			day: { // name of view
				titleFormat: 'YYYY, MM, DD'
			}
		}, events: function(start, end, timezone, callback) {
			let calendarSchedules = new Array();
			let index = 0;
			for (let x in schedule) {
				// console.log(schedule[x]);
				index++;
				calendarSchedules.push({
					title: schedule[x].task_name,
					start: schedule[x].start_time.toISOString(),	//'2018-01-18T22:30:00+09:00',
					end: schedule[x].end_time.toISOString()//'2018-01-19T02:30:00+09:00'
				});
			}
			callback(calendarSchedules);
		}
	});
	// calendar.next();

});
