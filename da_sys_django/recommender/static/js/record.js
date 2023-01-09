function getRecordsAPI(on_page) {
  if(on_page >totalPage && totalPage>0){
    document.getElementById('current_page').value=totalPage;
    currentPage=totalPage;
    on_page=totalPage;
  }

  if(on_page===0){
    document.getElementById('current_page').value=1;
    on_page=1;
    totalPage=1;
  }

  on_page--;
  var param = {
    on_page: on_page,
    page_size: 10
  };

  $.ajax({
    type: "GET",
    headers: {
      'X-CSRFToken': CSRFtoken
    },
    url: "/recommender/get/records",
    data: param,
    contentType: "application/json;charset=utf-8",
    success: function(response) {
      the_responce = $.parseJSON(JSON.stringify(response));
      // console.log('setupLogs', the_responce["setup_logs"]);
      // console.log('max page', the_responce["max_page"]);

      //refresh table

      setRecordData(the_responce["setup_logs"])
      totalPage =the_responce["max_page"]
      currentPage=on_page+1
      setPage(totalPage,currentPage)
    },
    error: function(err) {
      console.log('GET records error!', err.responseJSON);
    }
  });
};

var totalPage =0;
var currentPage=0;

$(function() {
  resetDataBox();
  getRecordsAPI(1)
});

function setRecordData(dataBase) {
resetDataBox();
  var owner = '';
  var gamecode = '';
  var owner_id = '';
  var gamecode_id = '';
  var n = 0;
  for (var i = 0; i < dataBase.length; i++) {
    var data = dataBase[i];
    var write_time = new Date(data[8]);
    write_time = dateTransform(write_time);

    var box = '<div class="textBox01">填寫日期: ' + write_time + '</div>';
    box += '<div class="textBox02">日期範圍: ' + data[0] + "-" + data[1] + '</div>';
    box += '<div class="textBox03">時區: ' + data[2] + '</div>';
    box += '<div class="textBox03">幣別: ' + data[3] + '</div>';
    box += '<div class="textBox03">設定者: ' + data[9] + '</div>';

    owner = data[4].split(',');
    gamecode = data[5].split(',');
    gamename = data[6].split(',');
    gamenameE=data[7].split(',');
    owner_id = '';
    gamecode_id = '';

    for (var a = 0; a < owner.length; a++) {
      owner_id += '<li>' + owner[a] + '</li>';
    };
    owner_id = '<ul>' + owner_id + '</ul>';

    for (var b = 0; b < gamecode.length; b++) {
      gamecode_id += '<li>' + gamename[b] + '&ensp;' + gamecode[b]+ '&ensp;' +gamenameE[b] + '</li>';
    };
    gamecode_id = '<ol>' + gamecode_id + '</ol>';

    n = i + 1;
    document.getElementById("date-box-" + n).innerHTML = box;
    document.getElementById("ownerId-" + n).innerHTML = owner_id;
    document.getElementById("gmaeCodeId-" + n).innerHTML = gamecode_id;
  }
}

function changePage(int) {
  currentPage+=int;
  if(currentPage<1){
    currentPage=1;
    return ;
  }
  getRecordsAPI(currentPage);
}

function setPage(max_page,on_page) {
  document.getElementById('total_page').innerText=max_page;
  document.getElementById('current_page').value=on_page;
}

function dateTransform(date) {
  // YYYY-MM-DD hh:mm
  var y = date.getFullYear().toString();
  var m = dateformat((date.getMonth() + 1).toString());
  var d = dateformat(date.getDate().toString());
  var h = dateformat(date.getHours().toString());
  var mm = dateformat(date.getMinutes().toString());
  var dateText = y + "/" + m + "/" + d + " " + h + ":" + mm;
  return dateText;

}

function dateformat(time) {
  time = (time.length) < 2 ? '0' + time : time;
  return time;
}

function openBox(id) {
  var n = id.charAt(id.length - 1);
  n = (n === '0') ? '10' : n;
  var box = document.getElementById("record-box-" + n);
  box.style.height = "35%";

  document.getElementById("close-button-" + n).style.display = "block";
  document.getElementById(id).style.display = "none";

}

function closeBox(id) {
  var n = id.charAt(id.length - 1);
  n = (n === '0') ? '10' : n;
  var box = document.getElementById("record-box-" + n);
  box.style.height = "6%";

  document.getElementById("open-button-" + n).style.display = "block";
  document.getElementById(id).style.display = "none";
}

function resetDataBox() {
  var box = "";
  for (var a = 1; a <= 10; a++) {
    box += '<div class="record-box" class="close-but" id="record-box-' + a + '">';
    box += '<div id="date-box-' + a + '"class="date-box">無</div><div id="more-box-' + a + '"class="more-box">';
    box += '<div class="more-data-box-ttl"><font>總代:</font><div id="ownerId-' + a + '" class="owner-text"></div></div><div class="more-data-box-ttr"><font>遊戲名稱:</font><div id="gmaeCodeId-' + a + '" class="gmaeCode-text"></div></div></table></div>';
    box += '<div class="but-box"><button type="button" id="open-button-' + a + '"onclick="openBox(this.id)"><img src="/static/img/left.png" align="absmiddle"></button>';
    box += '<button type="button" class="close-but" id="close-button-' + a + '"onclick="closeBox(this.id)"><img src="/static/img/drop.png" align="absmiddle"></button></div></div>';
  }
  document.getElementById("show-box").innerHTML = box;

}
