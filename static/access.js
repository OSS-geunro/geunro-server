$(document).ready(function() {
  let id = decodeURI(window.location.pathname.substring(1));

  $.ajax({
    url: "http://0.0.0.0:5009/api/work/access",
    type: "POST",
    data: {
      worktable_id: id
    },
    dataType: "json",
    success: function(data) {
      $("#calendar").fullCalendar({
        //calendar 설정
        defaultView: "listWeek",
        height: "auto",
        header: false,
        columnHeader: true,
        slotLabelFormat: "hh:mm",
        events: data,
        listDayAltFormat: false,
        defaultDate: moment("1970-01-05"),
        timezone: false,
        noEventsMessage: id + " 시간표가 아직 생성되지 않았습니다.",
        dayNames: ['일요일','월요일','화요일','수요일','목요일','금요일','토요일'],
        eventRender: function(event, element) {
          var students = "";
          var ids = "";
          $.each(data, function() {
            if (this["id"] == event.id) {
              students = this["studentid"];
              $.each(students, function(index, student) {
                 ids = ids + ", " + student.id
              });
              element.find(".fc-list-item-title")
                  .append("<br><div id=studentid> " + ids.substring(2) + "</div>");
            }
          });
        }
      });
    }
  });
});
