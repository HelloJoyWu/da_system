var confirmBox, allPicture;
var dateConfirmText, timezoneConfirmText, oidConfirmText, currencyConfirmText, gamecodeConfirmText;
$(function() {
  setTimeSelectableRange();
  setCurrencyOption();


  $("#currency_list").change(function() {
    var selectedItem = $('#currency_list').val();
    syncOwnersByRadioCurrency(selectedItem);
  });


  confirmBox = document.getElementById("confirmBox");
  allPicture = document.getElementById("allPicture");
  dateConfirmText = document.getElementById("dateConfirmText");
  timezoneConfirmText = document.getElementById("timezoneConfirmText");
  oidConfirmText = document.getElementById("oidConfirmText");
  currencyConfirmText = document.getElementById("currencyConfirmText");
  gamecodeConfirmText = document.getElementById("gamecodeConfirmText");
});

function setTimeSelectableRange() {
  var today = new Date();
  var tomorrow = new Date().setDate(today.getDate() + 1);
  tomorrow = new Date(tomorrow);

  //startDate
  $('#start-date').daterangepicker({
    "singleDatePicker": true,
    "timePicker": true,
    "timePicker24Hour": true,
    "timePickerIncrement": 60,
    "minDate": today,
    "startDate": today,
    "locale": {
      "format": 'YYYY/MM/DD HH:00',
      "applyLabel": "OK",
    }
  }, function(start) {
    start = start['_d'].setDate(start['_d'].getDate() + 1);
    start = new Date(start);
    $('#end-date').daterangepicker({
      "singleDatePicker": true,
      "timePicker": true,
      "timePicker24Hour": true,
      "timePickerIncrement": 60,
      "minDate": start,
      "locale": {
        "format": 'YYYY/MM/DD HH:00',
        "applyLabel": "OK",
      }
    })
  });

  //endDate
  $('#end-date').daterangepicker({
    "singleDatePicker": true,
    "timePicker": true,
    "timePicker24Hour": true,
    "timePickerIncrement": 60,
    "minDate": tomorrow,
    "startDate": tomorrow,
    "locale": {
      "format": 'YYYY/MM/DD HH:00',
      "applyLabel": "OK",
    }
  });
};

function getRadioCurrency() {
  var currency_radio = document.getElementsByName('currency-radio');
  var cur_length = currency_radio.length;
  for (var i = 0; i < cur_length; i++) {
    if (currency_radio[i].checked) {
      var currency = currency_radio[i].value;
      return currency;
    }
  }
};

function setCurrencyOption() {
  var optioin = '';
  var currencys = Object.keys(ownerInfo.c2o);
  currencys.forEach(function (name, _i) {
    optioin += "<option value='" + name + "'>" + name + "</option>";
  });


  $('#currency_list')[0].innerHTML = optioin;
  $('#currency_list').selectpicker('refresh');
  $('#currency_list').selectpicker('render');
}

function syncOwnersByRadioCurrency(currency) {
  var optioin = '';
  var owners = ownerInfo['c2o'][currency];
  for (var i in owners) {
    optioin += "<option value='" + owners[i] + "'>" + owners[i] + "</option>";
  }

  $('#owner-list')[0].innerHTML = optioin;
  $('#owner-list').selectpicker('refresh');
  $('#owner-list').selectpicker('render');
}

function checkGameCode(data) {
  var insertData = document.getElementById(data);
  var n =data.split('_')[1];
  var name_n = 'nameText_' + n;
  var name_text = document.getElementById(name_n)

  var value = insertData.value
  var name = gameCodeToName[value];

  if (name) {
    name_text.innerText = name;
    name_text.style.color = "#E0840E";
  } else {
    code = gameNameToCode[value]
    if (code) {
      name_text.innerText = value;
      name_text.style.color = "#E0840E";
      insertData.value = code;
      return;
    }
    name_text.innerText = '輸入錯誤';
    name_text.style.color = "red";
    insertData.value = "";
  }
};

function getSelectedTZ(is_diff) {
  var time_zone_radios = document.getElementsByName('time-zone-radios');
  var time_length = time_zone_radios.length;
  for (var i = 0; i < time_length; i++) {
    if (time_zone_radios[i].checked) {
      if (is_diff) {
        return time_zone_radios[i].value;
      } else {
        return time_zone_radios[i].id;
      }
    }
  }
};

function getSelectedOwners() {
  var selected_owners = $("#owner-list option:selected");
  var owners = [];
  var owner_name, owner_ssid;
  for (var a = 0; a < selected_owners.length; a++) {
    owner_name = selected_owners[a].value;
    owner_ssid = ownerInfo['o4ssid'][owner_name];
    owners.push([owner_name, owner_ssid]);
  };
  return owners;
};

var selectedStartDate, selectedEndDate, selectedTZ, selectedTZDiff, selectedCurrency, theCurrencyName;
// nested array: [[name, id/code], [], ...]
var selectedOwners = [], selectedGames = [];

function sendButton() {
  //日期
  selectedStartDate = document.getElementById('start-date').value;
  selectedEndDate = document.getElementById('end-date').value;
  //判斷時區
  selectedTZ = getSelectedTZ(tz_diff = false);
  selectedTZDiff = getSelectedTZ(tz_diff = true);
  //幣別
  selectedCurrency = $('#currency_list').val();

  theCurrencyName = ownerInfo['display_currency2n'][selectedCurrency]
  //owner
  var owners = getSelectedOwners();
  if (owners.length === 0) {
    alert("請選擇總代")
    return;
  };
  selectedOwners = owners;

  //game CODE
  var check_duplicate_gamecodes = [];
  var game_code;
  var game_name;
  selectedGames = [];
  for (var a = 1; a <= 15; a++) {
    game_code = document.getElementById('text_' + a).value;

    game_name = document.getElementById('nameText_' + a).innerHTML;

    if(game_code){
      game_name_en = gameCodeToNameEn[game_code];
      selectedGames.push([game_code, game_name, game_name_en]);
      check_duplicate_gamecodes.push(game_code);
    }

  };

  var res = [...(new Set(check_duplicate_gamecodes))];
  var repeat_res = check_duplicate_gamecodes.filter(function(element, index, arr){
      return arr.indexOf(element) !== index;
  });

  if(repeat_res.length >=1){
    var showText ='';
    for(var i=0; i<repeat_res.length;i++){
      showText+="代號："+repeat_res[i]+",遊戲名稱："+gameCodeToName[repeat_res[i]]+' ,重複囉 \r';
    }
    alert(showText);
    selectedGames = [];
    return;
  }

  if (res.length <= 10) {
    alert("最少請輸入11款遊戲");
    selectedGames = [];
    return;
  }

  showSelectedInfo();
}

function showSelectedInfo() {
  //最後輸出結果
  console.log("----------設定結果------------");
  console.log("start: " + selectedStartDate);
  console.log("end: " + selectedEndDate);
  console.log("時區: " + selectedTZ);
  console.log("選擇幣別: " + selectedCurrency);
  console.log("幣別: " + theCurrencyName);
  console.log("總代: ", selectedOwners);
  console.log("gamecode: ", selectedGames);

  var gamecode_text = "";
  for (var i = 0; i < selectedGames.length; i++) {
    gamecode_text += '<ol>' + selectedGames[i][1] + '&ensp;' + selectedGames[i][2] + '</ol>';
  };
  gamecode_text = '<ul>' + gamecode_text + '</ul>';

  var display_owners = '';
  for (var i = 0; i < selectedOwners.length; i++) {
    display_owners += '<li>' + selectedOwners[i][0] + '</li>';
  };
  display_owners = '<ul>' + display_owners + '</ul>';

  confirmBox.style.display = 'block';
  allPicture.style.display = 'block';
  dateConfirmText.innerText = selectedStartDate + ' - ' + selectedEndDate;
  timezoneConfirmText.innerText = selectedTZ;
  oidConfirmText.innerHTML = display_owners;
  currencyConfirmText.innerText = selectedCurrency;
  gamecodeConfirmText.innerHTML = gamecode_text;

};

function onConfirmBut() {
  confirmBox.style.display = 'none';
  setTimeout("postRecommendSetup()", 30);
}

function postRecommendSetup() {
  //receive server packet
  sendResultsText = document.getElementById("sendResults");

  var setup_data = {
    start_date: selectedStartDate,
    end_date: selectedEndDate,
    timezone: selectedTZ,
    timezone_diff: selectedTZDiff,
    currency: selectedCurrency,
    currency_name: theCurrencyName,
    owners: selectedOwners,
    games: selectedGames
  };


  $.ajax({
    type: "POST",
    headers: {'X-CSRFToken': CSRFtoken},
    url: "/recommender/setup",
    // dataType: "json",
    data: JSON.stringify(setup_data),
    contentType: "application/json;charset=utf-8",
    success: function(response) {
      var resp = $.parseJSON(JSON.stringify(response));
      console.log('post responce: ', resp);
      sendResultsText.innerText = "送出成功";
    },
    error: function(err) {
      console.log('Post recommend setup failed: ', err)
      sendResultsText.innerText = "送出失敗";
    }

  });

  setTimeout("resetScreen()", 3000);

};

function resetScreen() {
  allPicture.style.display = 'none';

  for (var a = 1; a <= 15; a++) {
    document.getElementById("text_" + a).value = "";
    document.getElementById("nameText_" + a).innerText = "gmae name";
  }

  document.getElementById("UTC+8").checked = true;
  document.getElementById("currency_list").options.selectedIndex = 0; 
  $("#currency_list").selectpicker('refresh');
  syncOwnersByRadioCurrency();


  var today = new Date();
  var tomorrow = new Date().setDate(today.getDate() + 1);
  tomorrow = new Date(tomorrow);

  setTimeSelectableRange();

};
