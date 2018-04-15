$(document).ready(function(){
    document.session = $('#session').val();
    setTimeout(requestInventory,100);

    $('#add-button').click(function(event){
        $.ajax({
            url:"/cart",
            type:'POST',
            data:{
                session:document.session,
                action:'add'
            },
            dataType:'json',
            beforeSend: function(xhr,settings){
                $(event.target).attr('disable','disable');
                // alert('beforeSend1');
            },
            success: function(data,status,xhr){
                // alert('add-button');
                console.log('add_button');
                $('#add-to-cart').hide();
                $('#remove-from-cart').show();
                $(event.target).removeAttr('disable');
                
            }
        });
    });

    $('#remove-button').click(function(event){
        $.ajax({
            url:"/cart",
            type:'POST',
            data:{
                session:document.session,
                action:'remove'
            },
            dataType:'json',
            beforeSend: function(xhr,settings){
                $(event.target).attr('disable','disable');

            },
            success: function(data,status,xhr){
                // alert('remove button');
                console.log(remove-button);
                $('#remove-from-cart').hide();
                $('#add-to-cart').show();
                $(event.target).removeAttr('disable');
               
            }
        });
    });

});

function requestInventory(){
    $.getJSON('/cart/status',{session:document.session},
        function(data,status,xhr){
            $('#count').html(data['inventoryCount']);
            console.log(data);
            console.log(status);
            console.log(xhr);
            setTimeout(requestInventory,0);
        }
    );
}