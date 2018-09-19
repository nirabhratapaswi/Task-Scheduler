var calendar;
var selected_task, selected_event;

function getCookie(name) {
	var cookieValue = null;
		if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

$(function() {
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
			let time_now = new Date();
			let today = (new Date(time_now.setMinutes(time_now.getMinutes() - time_now.getTimezoneOffset()))).toISOString();	// To convert local time now to UTC numeric-similar time(not equivalent)
			for (let x in schedule) {
				if (schedule[x].done == "false" || schedule[x].done == "False" || schedule[x].done === 0 || schedule[x].done == "0"){
					calendarSchedules.push({
						id: schedule[x].id,
						title: schedule[x].task_name,
						start: schedule[x].start_time.toISOString(),
						end: schedule[x].end_time.toISOString(),
						editable: false,
						backgroundColor: '#DC143C'
					});
				} else {
					if (today >= schedule[x].end_time.toISOString()) {
						calendarSchedules.push({
							id: schedule[x].id,
							title: schedule[x].task_name,
							start: schedule[x].start_time.toISOString(),
							end: schedule[x].end_time.toISOString(),
							editable: false,
							backgroundColor: '#008000'
						});
					} else {
						calendarSchedules.push({
							id: schedule[x].id,
							title: schedule[x].task_name,
							start: schedule[x].start_time.toISOString(),
							end: schedule[x].end_time.toISOString(),
							editable: false,
							backgroundColor: '#00BFFF'
						});
					}
				}
			}
			callback(calendarSchedules);
		}, eventClick: function(calEvent, jsEvent, view) {
			$("#modalOpenBtn").click();
			// console.log('Event: ', calEvent);
			selected_task = calEvent;
			selected_event = $(this);
			$(this).css('border-color', 'red');
		}
	});
	// calendar.next();

	$("#taskUndone").click(function(e) {
		console.log($(this));
		let data = {
			id: selected_task.id,
			done: false
		};
		console.log("Sending data: ", data);
		$.ajax({
			url: SERVER_URL.concat("/taskscheduler/reportundonetaskasperschedule"),
			contentType: "application/x-www-form-urlencoded",
			type: "POST",
			headers: {
				"X-CSRFToken": getCookie('csrftoken')
			},
			data: data,
			dataType: 'json',
			success: function (data) {
				if (data.error) {
					console.log("Error: ", data.error);
					$("#snackbarMessage").text(data.error);
				} else {
					if (!data.success || data.success == "False" || data.success == "false") {
						$("#snackbarMessage").text(data.msg);
					} else {
						console.log(data.msg);
						$("#snackbarMessage").text(data.msg);
						selected_event.css("backgroundColor", "#DC143C");
						// location.reload();
					}
				}
				$("#snackbarMessage").addClass("show");
				setTimeout(function() {
					$("#snackbarMessage").removeClass("show"); $("#snackbarMessage").addClass("");
				}, 3000);
			}
		});
	});
	$("#prepareSchedule").click(function(e) {
		$.ajax({
			url: SERVER_URL.concat("/taskscheduler/prepareschedule"),
			contentType: "application/x-www-form-urlencoded",
			type: "GET",
			headers: {
				"X-CSRFToken": getCookie('csrftoken')
			},
			data: [],
			dataType: 'json',
			success: function (data) {
				if (data.error) {
					$("#snackbarMessage").text(data.error);
					$("#snackbarMessage").addClass("show");
					setTimeout(function() {
						$("#snackbarMessage").removeClass("show"); $("#snackbarMessage").addClass("");
					}, 3000);
				} else {
					location.reload();
				}
			}
		});
	});
});
