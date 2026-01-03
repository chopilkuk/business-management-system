window.onload=function(){
    var t1 = document.getElementById("report");
    var t2 = document.getElementById("project");

    {
    t1.style.display="block";
    t2.style.display="none";
    }
}
  
  
  
function innerSample1()
    {
    var t1 = document.getElementById("report");
    var t2 = document.getElementById("project");
    {
    t1.style.display="block";
    t2.style.display="none";
    }
}
  
function innerSample2()
    {
    var t1 = document.getElementById("report");
    var t2 = document.getElementById("project");

    {
    t1.style.display="none";
    t2.style.display="block";
    }
}

function inputDate(){
    var datesel = document.getElementById('date').value;

    alert(datesel);
}

function inputStart(){
    var startsel = document.getElementById('startDay').value;

    alert(startsel);
}
function inputFin(){
    var finsel = document.getElementById('finDay').value;

    alert(finsel);
}