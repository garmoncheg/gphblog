/**
 * Script for simple image rotation. Uses pk of the image
 * and direction descriptor.
 */
var disabled = false;
function rotate(button, pk, direction, url)
{
    if (disabled)
        return false;
    disabled = true;
    $('a#rotator_btn').fadeTo("fast", 0.20);
    $('.main_image center img').fadeTo("fast", 0.33);
    $.post(url, {
        pk: pk,
        direction: direction,
    }, function(data) {
        $('.main_image').html('<center><img src="'+data+'"></center>');//inserting new thumbnail
        $('a#rotator_btn').fadeTo("fast", 1.00);
        $('a.main_image center img').fadeTo("fast", 1.00);
        disabled = false;
        return false;
    });
    return false;
}