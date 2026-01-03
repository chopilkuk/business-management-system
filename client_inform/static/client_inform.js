window.onload = function()
{
    // 시작 할 때 바로 실행 되는 code
    document.getElementById("depart").innerHTML = "신사업 본부";

    // 기본 default 값은 업체정보관리
    // 선택된것은 다시 클릭할 수 없음.
    document.getElementById("inform").setAttribute("disabled", true);
    document.getElementById("vaccine").removeAttribute("disabled");

    // 업체 정보 관리를 눌렀을때, 버튼 생성 (업체 정보 관리)
    document.getElementById("content").innerHTML = "업체정보 관리";
    var buttona = document.createElement('button');
    buttona.type = 'button';
    buttona.innerText = '업체등록';
    buttona.className = 'btn_a';
    
    // 업체 등록 버튼을 눌렀을때, 실행 되는 함수.
    buttona.onclick = function(){
        document.write("a");
    };
    
    // 업체 정보 관리를 눌렀을때, 버튼 생성 (삭제)
    var buttonb = document.createElement('button');
    buttonb.type = 'button';
    buttonb.innerText = '삭제';
    buttonb.className = 'btn_a';
    
    // 삭제 버튼을 눌렀을때, 실행 되는 함수.
    buttonb.onclick = function(){

    };

    // 버튼 생성.
    var container1 = document.getElementById("btna");
    var container2 = document.getElementById('btnb');
    container1.appendChild(buttona);
    container2.appendChild(buttonb);

    // 업체 정보 관리 table 생성.
    create_inform_table();
}

// 업체 정보 관리 버튼을 눌리면 실행되는 함수. (시작과 동일)
function inform()
{
    // 백신 갱신사 table 초기화.
    document.getElementById("t2").innerHTML = '';

    var year = document.getElementById("year");
    year.removeChild(year.lastChild);
    
    var container1 = document.getElementById("btna");
    var container2 = document.getElementById('btnb');
    container1.removeChild(container1.lastChild);

    document.getElementById("inform").setAttribute("disabled", true);
    document.getElementById("vaccine").removeAttribute("disabled");

    document.getElementById("content").innerHTML = "업체정보 관리";
    var buttona = document.createElement('button');
    buttona.type = 'button';
    buttona.innerText = '업체등록';
    buttona.className = 'btn_a';
    buttona.onclick = function(){
        document.write("a");
    };
    var buttonb = document.createElement('button');
    buttonb.type = 'button';
    buttonb.innerText = '삭제';
    buttonb.className = 'btn_a';
    
    buttonb.onclick = function(){
         document.write("b");
    };

    container1.appendChild(buttona);
    container2.appendChild(buttonb);

    create_inform_table();
}

// 백신 갱신사 리스트 버튼을 눌렀을때 실행 되는 함수.
function vaccine()
{
    // 업체 정보 관리 table 초기화.
    document.getElementById("t1").innerHTML = '';

    // 년도 선택을 위한 array (현재로부터 10년)
    var year = new Array();
    var i = new Date().getFullYear();
    for(var j = 0; j < 10; j++){
        year.push(i + j);
    }

    // select tag 생성.
    var select = document.createElement("select");
    select.setAttribute("id", "select");
    // 변경 될때 실행되는 함수.
    select.setAttribute("onchange", "selectItemChange(this)");

    // 년도를 입력.
    for(var i=0; i<year.length; i++) {
        var createItemElement = document.createElement("option"); // 요소 생성
        createItemElement.innerText = String(year[i]); // 옵션 이름 지정
        createItemElement.value = i; // 옵션 value 지정

        select.appendChild(createItemElement); // select 부모에 개별 item 요소 추가 실시
    }

    // select를 div에 생성.
    var parantyear = document.getElementById("year");
    parantyear.appendChild(select);

    document.getElementById("inform").removeAttribute("disabled");
    document.getElementById("vaccine").setAttribute("disabled", true);

    var container1 = document.getElementById("btna");
    var container2 = document.getElementById('btnb');

    // node가 계속 생성 되는것을 막아주기 위한 삭제.
    container1.removeChild(container1.lastChild);
    container2.removeChild(container2.lastChild);

    document.getElementById("content").innerHTML = "백신갱신사 리스트 관리";

    // 백신갱신 버튼을 눌리면 생성되는 버튼 (수정)
    var button = document.createElement('button');
    button.type = 'button';
    button.innerText = '수정';
    button.className = 'btn_a';
    button.onclick = function(){
        document.write("a");
    };

    // 수정 버튼 div에 추가.
    container1.appendChild(button);

    // 백신 table 생성.
    create_vaccine_table();
}

// copy 버튼을 눌리면 클립보드에 복사.
function copy()
{
    var content = document.getElementById('inform_table').innerHTML;

    navigator.clipboard.writeText(content)
        .then(() => {
        alert("copied!");
    })
        .catch(err => {
        alert("not copied!");
    })
}

function excel()
{

}

function print()
{

}

function column_visibility()
{

}

function search()
{

}

// 년도 select가 변하면 실행되는 함수.
function selectItemChange(tagId){

    var tag = document.getElementById(String(tagId.id)); // 객체 id 지정

    var itemText = tag.options[tag.selectedIndex].text; // 선택된 text 확인
    var itemValue = tag.options[tag.selectedIndex].value; // 선택된 value 확인
};

//모든 체크박스 체크
function selectAll(selectAll)  {
    const checkboxes 
         = document.getElementsByName('project');
    
    checkboxes.forEach((checkbox) => {
      checkbox.checked = selectAll.checked;
    })
}

// 업체 정보 관리 table 생성.
function create_inform_table()
{
    var head_data = ['기업명', '구분', '지역', '변경', '순번'];

    document.getElementById("vaccine_list").innerHTML = '<table id="t2"></table>';
    var head = document.getElementById("inform_table");
    var btn_ind;

    for(btn_ind = 0; btn_ind < head_data.length; btn_ind++)
    {
        var button = document.createElement('button');
        button.type = 'button';
        button.innerText = head_data[btn_ind];
        button.className = 'btn_' + btn_ind;
        button.id = "btn_ind";
        button.onclick = function(){
            document.write("a");
        };
        head.prepend(button);
    }

    var table = document.getElementById("t1");
    
    var edit_button = '<button onclick=edit()>수정</button>';
    var table_data = new Array();
    var table_ind;

    var data = [['광양', '외주', 'PMS']];

    for(table_ind = 0; table_ind < data.length; table_ind++)
    {   
        console.log(data.length);

        var temp = '<td>' + '<input type="checkbox" id="check">' + String(table_ind + 1) + '</td>' + '<td>' + edit_button + '</td>';
        for(col = 0; col < data[table_ind].length; col++)
        {
            temp += '<td>' + data[table_ind][col] + '</td>';
        }

        table_data.push(temp);
        table.innerHTML += temp;
    }
}

// 백신 갱신사 리스트 table 생성.
function create_vaccine_table()
{
    var head_data = ['올해', '이전', '회사명', '구분'];

    document.getElementById("inform_table").innerHTML = '<table id="t1"></table>';
    var head = document.getElementById("vaccine_list");
    var btn_ind;
    for(btn_ind = 0; btn_ind < head_data.length; btn_ind++)
        {
        var button_menu = document.createElement('button');
        button_menu.type = 'button';
        button_menu.innerText = head_data[btn_ind];
        button_menu.className = 'btn2_' + btn_ind;
        button_menu.onclick = function(){
            document.write("a");
        };
        head.prepend(button_menu);
    }

  var table = document.getElementById("t2");
    var table_data = new Array();
    var table_ind;
    var data = [['ASP', '디엠', 'O', 'X']];

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