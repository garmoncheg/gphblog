/**
 * Script for commenting a Photo.
 */

//post comment to base and insert response
function post_comment(button, pk, body, url)
{
    $.post(url, {
        pk: pk,
        body: $('textarea').val(),
    }, function(data) {
    	//alert(data);
        $('.comment:last').after(data);
    });
    return false;
}