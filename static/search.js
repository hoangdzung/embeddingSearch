$(function () {
    $('#search').click(function () {
    	$('#rs_wrapper').hide();
    	$('#loading').show();
        console.log("Press a button!")
        console.log(document.getElementById('query_type').value)
        console.log(document.getElementById('src_name').value)
        console.log(document.getElementById('target_type').value)
        $.ajax({
            url: '/api/search?src_type=' + document.getElementById('query_type').value +
             '&src_name=' + document.getElementById('src_name').value + 
             '&target_type=' + document.getElementById('target_type').value + 
             '&k=' + document.getElementById('num_return').value,
            success: function (data) {
                console.log(data)
                $('#result').html('');
                for (i = 0; i < data.length; i++) {
                    console.log(data[i])
                    $('#result').append('<p>' + data[i]+ '</p>');
                }
                $('#rs_wrapper').show();
                $('#loading').hide();
            }
        });
    });
})