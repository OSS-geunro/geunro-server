
let data;
let IDs = [];
let worktable;
let startT;
let endT;

function getUrlParams() {
  var params = {};
  window.location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(
    str, key, value
  ) {
    params[key] = value;
  });
  return params;
}

$(document).ready(function() {
  param = getUrlParams();
  worktable = param.type;
  $("#name").text(decodeURI(worktable))
  $("#calendar").fullCalendar({
    //calendar 설정
    defaultView: "agendaWeek",
    allDaySlot: false,
    height: "auto",
    header: false,
    weekends: false,
    columnHeader: true,
    columnHeaderFormat: "dddd",
    slotLabelFormat: "hh:mm",
    minTime: "09:00:00",
    maxTime: "18:00:00",
    slotDuration: "00:10:00",
    slotLabelInterval: "00:30",
    slotEventOverlap: false,
    event: data,
    editable: true,
    selectable: true,
    defaultDate: moment("1970-01-05"),

    // 시간 지정시 업무 추가 modal
    select: function(startTime, endTime) {
      startT = startTime;
      endT = endTime;
      let start = startTime.format("dddd hh:mm");
      let end = endTime.format("dddd hh:mm");
      $("#start-time").text(start);
      $("#end-time").text(end);
      $("#modal").modal("show");
    },

    // 업무 클릭시 삭제 modal
    eventClick: function(eventObj) {
      $("#calendar").fullCalendar("removeEvents", eventObj._id);
    }
  });

  $("#modal").submit(function(startTime, endTime) {
    let Title = $("#work-name").val();
    let Minimum = $("#minimum").val();
    let Event = {
      title: Title,
      minimum: Minimum,
      start: startT,
      end: endT,
      minimum: 1,
    };
    $("#modal").modal("hide");
    $("#calendar").fullCalendar("renderEvent", Event);
    $("#work-name").val("");
  });
});

$("#next-pg").click(function() {
  let jsoned = JSON.stringify(
    $("#calendar")
      .fullCalendar("clientEvents")
      .map(function(e) {
        let startTime = e.start.format("HH:mm");
        let endTime = e.end.format("HH:mm");
        let day = e.start.format("ddd");
        return {
          start: startTime,
          end: endTime,
          day: day,
          minimum: e.minimum,
          name: e.title
        };
      })
      
  );
  $.ajax({
    url: "create",
    type: "post",
    data: {
      events: jsoned,
      worktable: worktable
    },
    success: function(xhr) {
      $(location).attr("href", "list");
    },
    error: function(xhr) {
    }
  });
});
//TODO: 다음날로 넘어가는 업무 필터링
