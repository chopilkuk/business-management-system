window.onload = function()
{
    // 시작 할 때 바로 실행 되는 code
    mdinform();
}

// 업체 정보 관리 버튼을 눌리면 실행되는 함수. (시작과 동일)
function mdinform()
{
    // 백신 갱신사 table 초기화.
    document.getElementById("t2").innerHTML = '';

    document.getElementById("mdinform").setAttribute("disabled", true);
    document.getElementById("clog").removeAttribute("disabled");

    //차트삽입
    var containerchart = document.getElementById("chartarea");
    while(containerchart.hasChildNodes()){
        containerchart.removeChild(containerchart.firstChild);
    }

    var chart1 = document.createElement('canvas');
    chart1.id = "myChart1"; //거래처별문의횟수
    chart1.width = "200";
    chart1.height = "200";

    var chart2 = document.createElement('canvas');
    chart2.id = "myChart2"; //누적문의횟수
    chart2.width = "400";
    chart2.height = "400";

    var chart3 = document.createElement('canvas');
    chart3.id = "myChart3";  //모듈문의횟스
    chart3.width = "400";
    chart3.height = "400";
    
    containerchart.appendChild(chart1);
    containerchart.appendChild(chart2);
    containerchart.appendChild(chart3);

    // 업체 정보 관리 table 생성.
    create_mdinform_table();

    mkchart('myChart1', 'bar', ["africa", "aisa", "Europe", "Latin America", "North America", ], [2478,5267,734,784,433], '챗봇로그bymkchart');
    mkchart('myChart2', 'pie', ["africa", "aisa", "Europe", "Latin America", "North America", ], [2478,5267,734,784,433], '챗봇로그bymkchart');
    mkchart('myChart3', 'doughnut', ["africa", "aisa", "Europe", "Latin America", "North America", ], [2478,5267,734,784,433], '챗봇로그bymkchart');
}

// 백신 갱신사 리스트 버튼을 눌렀을때 실행 되는 함수.
function clog()
{
    // 업체 정보 관리 table 초기화.
    document.getElementById("t1").innerHTML = '';
    document.getElementById("dst").innerHTML = '';
   
    document.getElementById("mdinform").removeAttribute("disabled");
    document.getElementById("clog").setAttribute("disabled", true);

    
    var containerdatesearch = document.getElementById("date_search");
    while(containerdatesearch.hasChildNodes()){
        containerdatesearch.removeChild(containerdatesearch.firstChild);
    }

    var containerchart = document.getElementById("chartarea");

    // node가 계속 생성 되는것을 막아주기 위한 삭제.
    while(containerchart.hasChildNodes()){
        containerchart.removeChild(containerchart.firstChild);
    }

    // 차트생성
    var chart1 = document.createElement('canvas');
    chart1.id = "myChart4"; //챗봇로그
    chart1.width = "400";
    chart1.height = "400";

    // 차트 div에 추가.
    containerchart.appendChild(chart1);

    //table 생성, 차트생성
    create_list_table();
    mkchart('myChart4', 'pie', ["1", "2", "3", "4", "5", ], [2478,5267,734,784,433], '챗봇로그bymkchart');
}

// 업체 정보 관리 table 생성.
function create_mdinform_table()
{
    document.getElementById("cb_list").innerHTML = '<table class="commuteBox" id="t2"></table>';

    //월별검색, 기간검색 테이블
    var dstable = document.getElementById("dst");
    var temp1 = '<td><span>월별검색</span><br> <input type="month" id="month" value="xxx" min="yyy" max="zzz"> <input type="submit" id="monthSub" onclick=inputMon() value="확인"></td>'
    temp1 += '<td><span>기간별검색</span><br> <input type="date" id="start" value="xxx" min="yyy" max="zzz"><input type="submit" id="startSub" onclick="inputStart()" value="확인"> - <input type="date" id="end" value="xxx" min="yyy" max="zzz"><input type="submit" id="endSub" onclick="inputEnd()" value="확인"> </td>'
    dstable.innerHTML += temp1;

    
    //모듈정보테이블
    var table = document.getElementById("t1");
    
    var table_data = new Array();
    var table_ind;
    var data = [['광양', '외주', 'PMS']];

    for(table_ind = 0; table_ind < data.length; table_ind++)
    {   
        console.log(data.length);

        var temp = '';
        for(col = 0; col < data[table_ind].length; col++)
        {
            temp += '<td>' + data[table_ind][col] + '</td>';
        }

        table_data.push(temp);
        table.innerHTML += temp;
    }
}

// 리스트 table 생성, 체크박스
function create_list_table()
{
    document.getElementById("mdinform_table").innerHTML = '<table class="commuteBox" id="t1"></table>';
    document.getElementById("date_search").innerHTML = '<table class="commuteBox" id="dst"></table>';

    var table = document.getElementById("t2");
    var table_data = new Array();
    var table_ind;
    var data = [['1이 안되요', 1000], ['2가 안되요', 2000], ['3이 안되요', 3000], ['4이 안되요', 1000], ['5가 안되요', 2000], ['6이 안되요', 3000]];

    for(table_ind = 0; table_ind < data.length; table_ind++)//행수
    {   
        var temp = '';
        temp += '<td><input type="checkbox" value="' + data[table_ind][1] + '" id="cbchecklist' + table_ind + '" onclick="dataadd(this)">' + data[table_ind][0] + '</td>';
        table_data.push(temp);
        table.innerHTML += temp;
    }
}

//체크박스 누를 시 데이터 추가 및 제거
function dataadd(checkvalue){
    var selectedtr = checkvalue.parentElement.innerText;//선택된 열의 텍스트내용
    var chart = document.getElementById('myChart4');
    alert(chart.type);
    chart.type = 'bar';
    alert(chart.type);
    //chart.update();
    //console.log(chart.data.labels[0]);
    // if(checkvalue.checked == true){
        
    //     chart.data.labels.push(selectedtr);
    //     chart.data.datasets.forEach((dataset) => {
    //         dataset.data.push(checkvalue.value);
    //     });
    //     chart.update();
    // }
    // else{
    //     alert("체크 안됨");

    // }
}

//차트생성 canvas id, 그래프타입(pie, bar, doughnut...), 데이터라벨, 각라벨의 데이터, 그래프title
function mkchart(cid, ctype, labelsary, cdata, ctitle){
    var mychart = new Chart(document.getElementById(cid), {
        type: ctype,
        data: {
        labels: labelsary,//종류
        datasets: [//내용, 색, 값, 소단위라벨
            {
            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
            data: cdata
            }
        ]
        },
        options: {//크기조절가능여부, 제목
            responsive: false,
            title: {
                display: true,
                text: ctitle
            }
        }
    });
}


function inputMon(){
    var monthDay = document.getElementById('month').value;

    alert(monthDay);
}

function inputStart(){
    var startDay = document.getElementById('start').value;

    alert(startDay);
}

function inputEnd(){
    var endDay = document.getElementById('end').value;

    alert(endDay);
}