window.onload = function(){
    var table = document.getElementById('notice_table');
    var table_data = new Array();
    var table_ind;
    var data = [['15', '인터넷...', '2022-06-16......', '홍석주']];

    for(table_ind = 0; table_ind < data.length; table_ind++)
    {   
        console.log(data.length);

        //var temp = '<td>' + String(table_ind + 1) + '</td>';
        var temp = '';
        for(col = 0; col < data[table_ind].length; col++)
        {
            temp += '<td>' + data[table_ind][col] + '</td>';
        }

        table_data.push(temp);
        table.innerHTML += temp;
    }
}