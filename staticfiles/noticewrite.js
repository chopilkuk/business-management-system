window.onload = function(){
    var data = ['name1'];

    document.getElementById('write_id').value = data[0];
}

function reset_write(){
    document.getElementById('notice_name').value = '';
    document.getElementById('upfile').value = '';
    document.getElementById('notice_comments').value = '';
}

function check_input(){
    var notice_name = document.getElementById('notice_name').value;
    var notice_comments = document.getElementById('notice_comments').value;
    var file = document.getElementById('upfile').value;

    alert(notice_name + notice_comments + file);

    document.href = '../home';
}