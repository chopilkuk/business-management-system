function save(){
    var name = document.getElementById('name').value;
    var date = document.getElementById('date').value;
    var arrive_time = document.getElementById('arrive_time').value;
    var leave_time = document.getElementById('leave_time').value;
    var status = document.getElementById('status').value;
    var ect = document.getElementById('ect').value;
    alert(name + date + arrive_time + leave_time + status + ect);
}