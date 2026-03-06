window.onload = function()
{
    var date = new Date(); 
    var month = date.getMonth() + 1;
    var day = date.getDate();

    document.getElementById('date').innerHTML = 'abc';
    document.getElementById("date").innerHTML = month + "월" + day + "일";
}
function write_department()
{
    document.getElementById("department").innerHTML = department + "부"; 
}
function write_date()
{
    document.getElementById("date").innerHTML = month + "월" + day + "일" + todayLabel;
}

function filter(){

    var serch, name, item, i;

    value = document.getElementById("serch").value.toUpperCase();
    item = document.getElementsByClassName("item");

    for(i=0;i<item.length;i++){
      name = item[i].getElementsByClassName("name");
      if(name[0].innerHTML.toUpperCase().indexOf(value) > -1){
        item[i].style.display = "flex";
      }else{
        item[i].style.display = "none";
      }
    }
  }
/*
    window.onload = function() {
        function onClick() {
            document.querySelector('.modal_wrap').style.display ='block';
            document.querySelector('.black_bg').style.display ='block';
        }
        function offClick() {
            document.querySelector('.modal_wrap').style.display ='none';
            document.querySelector('.black_bg').style.display ='none'; }
            document.getElementById('modal_btn').addEventListener('click', onClick)
            document.querySelector('.modal_close').addEventListener('click', offClick);
    }*/


function anciennete(){
    document.write("anciennete");
}
function name(){
    document.write("name");
}
function attendance(){
    document.write("attendance");
}
function leave (){
    document.write("leave ");
}
function state(){
    document.write("state");
}
function reason(){
    document.write("reason");
}
function update(){
    document.write("update");
}

function PopWin(url, w, h, sb) {
    var newWin;
    var setting = "width=800px", height="1000px", top=5, left=20, scrollbars="+sb";
    newWin = window.open (url, "", setting);
    newWin.focus();
}
