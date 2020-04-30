$(function () {
    $('#search').click(function () {
    	$('#result').hide();
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
                $('#result').append('<div style="font-size: 0.95em; text-align: center;margin: 20px;">NEAREST KEYWORDS</div>');
                for (i = 0; i < data.length; i++) {
                    console.log(data[i])
                    // $('#result-wrapper').append('<p>' + data[i]+ '</p>');
                    $('#result').append(
                        `
                        <div class="item-keyword">
                        <div style="padding: 5px 5px 0px 0">
                            <img src="http://icons.iconarchive.com/icons/double-j-design/childish/128/Key-icon.png"
                                width="18px"
                                height="18px"
                            >
                        </div>
                        <div style="padding: 4px;">` + data[i] + `</div>
                    </div>
                    `
                    );
                }
                $('#result').show();
                $('#loading').hide();
            }
        });
    });
})