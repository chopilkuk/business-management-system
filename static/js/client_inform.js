document.addEventListener('DOMContentLoaded', function() {
  // 안전한 참조
  var createUrlEl = document.getElementById('clientCreateUrl');
  var createUrl = createUrlEl ? createUrlEl.value : null;

  function safeText(s){ return (s||'').toString(); }

  // 초기화
  try{
    var depart = document.getElementById('depart');
    if(depart) depart.innerText = '신사업 본부';
  }catch(e){}

  // 기본 default 값은 업체정보관리
  var informBtn = document.getElementById('inform');
  var vaccineBtn = document.getElementById('vaccine');
  if(informBtn) informBtn.disabled = true;
  if(vaccineBtn) vaccineBtn.disabled = false;

  // 업체등록 버튼 (서버 사이드 링크 사용)
  var container1 = document.getElementById('btna');
  var container2 = document.getElementById('btnb');
  if(container1){
    var buttona = document.createElement('button');
    buttona.type = 'button';
    buttona.innerText = '업체등록';
    buttona.className = 'btn_a';
    buttona.onclick = function(){ if(createUrl) window.location.href = createUrl; };
    container1.appendChild(buttona);
  }
  if(container2){
    var buttonb = document.createElement('button');
    buttonb.type = 'button';
    buttonb.innerText = '삭제';
    buttonb.className = 'btn_a';
    buttonb.onclick = function(){ /* 삭제는 선택된 항목에 대해 서버 호출 필요 */ };
    container2.appendChild(buttonb);
  }

  // 표 생성
  function create_inform_table(){
    var head_data_str = document.getElementById('tempVar') ? document.getElementById('tempVar').value : '';
    var head_data = head_data_str ? head_data_str.split(',') : [];
    var head = document.getElementById('inform_table');
    if(!head) return;

    // 예시 데이터(서버에서 데이터를 넣도록 리팩터 권장)
    var data = [['광양', '외주', 'PMS']];

    // 헤더 버튼
    for(var i=0;i<head_data.length;i++){
      var btn = document.createElement('button');
      btn.type='button'; btn.innerText = head_data[i]; btn.className = 'btn_' + i;
      head.prepend(btn);
    }

    var table = document.getElementById('t1');
    if(!table) return;

    for(var r=0;r<data.length;r++){
      var row = document.createElement('tr');
      var td0 = document.createElement('td');
      td0.innerHTML = '<input type="checkbox" name="project"> ' + (r+1);
      row.appendChild(td0);

      var td1 = document.createElement('td');
      var editBtn = document.createElement('button');
      editBtn.type='button'; editBtn.innerText='수정'; editBtn.className='btn_a';
      editBtn.onclick = function(){ alert('수정 기능은 서버 연동 필요'); };
      td1.appendChild(editBtn);
      row.appendChild(td1);

      for(var c=0;c<data[r].length;c++){
        var td = document.createElement('td'); td.innerText = safeText(data[r][c]); row.appendChild(td);
      }
      table.appendChild(row);
    }
  }

  function create_vaccine_table(){
    var head_data = ['올해','이전','회사명','구분'];
    var table = document.getElementById('t2');
    if(!table) return;
    var data = [['ASP','디엠','O','X']];
    for(var r=0;r<data.length;r++){
      var tr = document.createElement('tr');
      for(var c=0;c<data[r].length;c++){
        var td = document.createElement('td'); td.innerText = safeText(data[r][c]); tr.appendChild(td);
      }
      table.appendChild(tr);
    }
  }

  // 초기 생성
  try{ create_inform_table(); }catch(e){}

  // 기타 UI 핸들러 최소 구현
  window.create_inform_table = create_inform_table;
  window.create_vaccine_table = create_vaccine_table;

});
