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
               var title = prompt("Enter Event Title");
               var startDate = new Date(start);
               var endDate = new Date(end);
               var currentDate = new Date();

               if (startDate < currentDate || endDate < currentDate) {
                   alert("Start and end times cannot be in the past");
                   return;
               }

               $.ajax({
                type: "GET",
                url: '/check_overlap',
                data: {'start': startDate, 'end': endDate},
                dataType: "json",
                success: function (data) {
                    if (data.overlap) {
                        alert("You have another reservation at the same time");
                        return;
                    }
                },
                error: function (data) {
                    alert('There is a problem!!!');
                }
               });
                if (startDate < currentDate || endDate < currentDate) {
                    alert("Cannot book for past dates");
                    return;
                }

               if (title) {
                   var start = $.fullCalendar.formatDate(start, "Y-MM-DD HH:mm:ss");
                   var end = $.fullCalendar.formatDate(end, "Y-MM-DD HH:mm:ss");

                   $.ajax({
                       type: "GET",
                       url: '/add_event',
                       data: {'title': title, 'start': start, 'end': end},
                       dataType: "json",
                       success: function (data) {
                           calendar.fullCalendar('refetchEvents');
                           alert("Added Successfully");
                       },
                       error: function (data) {
                           alert('There is a problem!!!');
                       }
                   });
               }
           },
           eventResize: function (event) {
               var start = $.fullCalendar.formatDate(event.start, "Y-MM-DD HH:mm:ss");
               var end = $.fullCalendar.formatDate(event.end, "Y-MM-DD HH:mm:ss");
               var title = event.title;
               var id = event.id;
               $.ajax({
                   type: "GET",
                   url: '/update',
                   data: {'title': title, 'start': start, 'end': end, 'id': id},
                   dataType: "json",
                   success: function (data) {
                       calendar.fullCalendar('refetchEvents');
                       alert('Event Update');
                   },
                   error: function (data) {
                       alert('There is a problem!!!');
                   }
               });
           },

           eventDrop: function (event) {
               var start = $.fullCalendar.formatDate(event.start, "Y-MM-DD HH:mm:ss");
               var end = $.fullCalendar.formatDate(event.end, "Y-MM-DD HH:mm:ss");
               var title = event.title;
               var id = event.id;
               $.ajax({
                   type: "GET",
                   url: '/update',
                   data: {'title': title, 'start': start, 'end': end, 'id': id},
                   dataType: "json",
                   success: function (data) {
                       calendar.fullCalendar('refetchEvents');
                       alert('Event Update');
                   },
                   error: function (data) {
                       alert('There is a problem!!!');
                   }
               });
           },

           eventClick: function (event) {
               if (confirm("Are you sure you want to remove it?")) {
                   var id = event.id;
                   $.ajax({
                       type: "GET",
                       url: '/remove',
                       data: {'id': id},
                       dataType: "json",
                       success: function (data) {
                           calendar.fullCalendar('refetchEvents');
                           alert('Event Removed');
                       },
                       error: function (data) {
                           alert('There is a problem!!!');
                       }
                   });
               }
           },

       });
   });
