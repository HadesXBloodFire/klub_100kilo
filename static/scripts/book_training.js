$(document).ready(function () {
       var calendar = $('#calendar').fullCalendar({
           header: {
               left: 'prev,next today',
               center: 'title',
               right: 'month,agendaWeek,agendaDay'
           },
           events: '/all_events',
           selectable: true,
           selectHelper: true,
           editable: true,
           eventLimit: true,
           select: function (start, end, allDay) {
               var title = prompt("Nazwa rezerwacji:");
               var startDate = new Date(start);
               var endDate = new Date(end);
               var currentDate = new Date();
               var gym_id = document.getElementById("gym-select").value;


                if (startDate < currentDate || endDate < currentDate) {
                    alert("Nie mozesz zarezerwowac treningu na przeszlosc");
                    return;
                }

               if (title) {
                   var start = $.fullCalendar.formatDate(start, "Y-MM-DD HH:mm:ss");
                   var end = $.fullCalendar.formatDate(end, "Y-MM-DD HH:mm:ss");

                   $.ajax({
                       type: "GET",
                       url: '/add_event',
                       data: {'title': title, 'start': start, 'end': end, 'gym_id': gym_id},
                       dataType: "json",
                       success: function (data) {
                           calendar.fullCalendar('refetchEvents');
                           alert("Rezerwacaj zostala dodana!!!");
                       },
                       error: function (data) {
                           alert('Cos poszlo nie tak!!!');
                       }
                   });
               }
           },
           eventResize: function (event) {
               var start = $.fullCalendar.formatDate(event.start, "Y-MM-DD HH:mm:ss");
               var end = $.fullCalendar.formatDate(event.end, "Y-MM-DD HH:mm:ss");
               var title = event.title.split('\n')[0];
               var id = event.id;
               var gym_id = document.getElementById("gym-select").value;
               $.ajax({
                   type: "GET",
                   url: '/update',
                   data: {'title': title, 'start': start, 'end': end, 'id': id, 'gym_id': gym_id},
                   dataType: "json",
                   success: function (data) {
                       calendar.fullCalendar('refetchEvents');
                       alert('Rezerwacja zostala zaktualizowana!!!');
                   },
                   error: function (data) {
                       alert('Cos poszlo nie tak!!!');
                   }
               });
           },

           eventDrop: function (event) {
               var start = $.fullCalendar.formatDate(event.start, "Y-MM-DD HH:mm:ss");
               var end = $.fullCalendar.formatDate(event.end, "Y-MM-DD HH:mm:ss");
               var title = event.title.split('\n')[0]; // This will get the title without the gym name
               var id = event.id;
               var gym_id = document.getElementById("gym-select").value;
               $.ajax({
                   type: "GET",
                   url: '/update',
                   data: {'title': title, 'start': start, 'end': end, 'id': id, 'gym_id': gym_id},
                   dataType: "json",
                   success: function (data) {
                       calendar.fullCalendar('refetchEvents');
                       alert('Rezerwacja zostala zaktualizowana!!!');
                   },
                   error: function (data) {
                       alert('Cos poszlo nie tak!!!');
                   }
               });
           },

           eventClick: function (event) {
               if (confirm("Na pewno chcesz usunac rezerwacje?")) {
                   var id = event.id;
                   $.ajax({
                       type: "GET",
                       url: '/remove',
                       data: {'id': id},
                       dataType: "json",
                       success: function (data) {
                           calendar.fullCalendar('refetchEvents');
                           alert('Rezerwacja usunieta!!!');
                       },
                       error: function (data) {
                           alert('Cos poszlo nie tak!!!');
                       }
                   });
               }
           },

       });
   });
