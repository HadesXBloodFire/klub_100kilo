document.addEventListener('DOMContentLoaded', function () {
  var calendarEl = document.getElementById('calendar');
  var interactButton = document.getElementById('interactButton');
  var selectedInfo = null;
  var today = new Date();

  var calendar = new FullCalendar.Calendar(calendarEl, {
    locale: 'pl',
    initialView: 'timeGridWeek',
    slotDuration: '02:00:00',
    minTime: '00:00:00',
    maxTime: '24:00:00',
    selectable: true,
    allDaySlot: false,
    validRange: {
      start: today.toISOString().substring(0, 10),
    },
    datesAboveResources: true,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'timeGridWeek,timeGridDay',
    },
    slotLabelFormat: {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    },
    select: function (info) {
      selectedInfo = info;
      interactButton.style.display = 'block';
    },
    unselect: function () {
      selectedInfo = null;
      interactButton.style.display = 'none';
    },
  });

  interactButton.addEventListener('click', function () {
    handleSelection(selectedInfo);
    calendar.unselect();
  });

function handleSelection(info) {
    if (info !== null) {
        var start = info.startStr;
        var end = info.endStr;

        fetch('/api/add_reservation/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Pobierz token CSRF
            },
            body: JSON.stringify({
                start: start,
                end: end
            })
        })
        .then(response => response.json())
        .then(data => {
            // Obsłuż odpowiedź
            if (data.message) {
                alert(data.message);
            }
        });
    } else {
        console.log("No selection made on the calendar.");
    }
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

  calendar.render();
});
