/**
 * Script for simple image rotation. Uses pk of the image,
 * direction receives 1 or 2 depending of the + or - vote
 * and url of the view, that must be generated in the template
 * (needed to make this script static)
 */
function rotate(button, pk, direction, url)
{
    $.post(url, {
        pk: pk,
        direction: direction,
    }, function(data) {
        $('.main_image').html('<center><img src="'+data+'"></center>');//inserting new thumbnail
        
    });
    return false;
}
