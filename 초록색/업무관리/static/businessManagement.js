window.onload = function(){
  
  var head_data = ['...', '홍석주'];

    document.getElementById("management_title_head").innerHTML = '<table id="t2"></table>';
    var head = document.getElementById("t2");
    var btn_ind;

    for(btn_ind = 0; btn_ind < head_data.length; btn_ind++)
    {
        var button = document.createElement('button');
        button.type = 'button';
        button.innerText = head_data[btn_ind];
        button.className = 'btn_' + btn_ind;
        button.onclick = function(){
            document.write("a");
        };
        head.prepend(button);
    }
  
  var i;
  for(i = 0; i < 3; i++){
    create_management_table();
    
  }
}

function create_management_table()
{
  var table = document.getElementById("t1");
  var tr = '<tr onmouseover="getRowIdx(this)"><td><input type="checkbox" name="project"/></td><td>업무번호</td><td>피드백</td><td>작성자</td><td>작성일자</td><td>업체</td><td>지역</td><td>모듈</td><td>QUESTION</td>'
  +'<td>SOLUTION</td><td>이관</td><td>상태</td></tr>';

  table.innerHTML += tr;
}

function selectAll(selectAll)  {
  const checkboxes 
       = document.getElementsByName('project');
  
  checkboxes.forEach((checkbox) => {
    checkbox.checked = selectAll.checked;
  })
  
}
