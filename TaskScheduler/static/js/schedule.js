var calendar;
var selected_task;

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
			for (let x in schedule) {
				calendarSchedules.push({
					id: schedule[x].id,
					title: schedule[x].task_name,
					start: schedule[x].start_time.toISOString(),	//'2018-01-18T22:30:00+09:00',
					end: schedule[x].end_time.toISOString()//'2018-01-19T02:30:00+09:00'
				});
			}
			callback(calendarSchedules);
		}, eventClick: function(calEvent, jsEvent, view) {
			$("#modalOpenBtn").click();
			console.log('Event: ', calEvent);
			selected_task = calEvent;
			console.log('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
			console.log('View: ' + view.name);
			// change the border color just for fun
			$(this).css('border-color', 'red');
		}
	});
	// calendar.next();

	$("#taskUndone").click(function(e) {
		console.log("Task: ", selected_task, " is marked as undone!");
	});
});
