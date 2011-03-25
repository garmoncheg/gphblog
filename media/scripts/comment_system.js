/**
 * Script for commenting a Photo.
 */
function get_textarea_body()
{
    return $('textarea').val();
}
function insert_comment(data) {
    alert(data);
    $('.comment:last').append(data);
}

//post comment to base and insert response
function post_comment(button, pk, body, url)
{
    $.post(url, {
        pk: pk,
        body: get_textarea_body(),
    }, function(data) {
        $('.comments-block[data-id="' + pk + '"] .comments-header').show();
        $('.comments-block[data-id="' + pk + '"]').append(data);
    });
    return false;
}