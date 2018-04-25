$(document).ready(function(){
    $.get("/myhouselist",function(data){
        // console.log(data);
        if(data.ret == "1"){
            $('#house_list').html(template('house_item',{houses:data.house_data}))
        }
        else{
            alert(data.msg);
        }
    })
})