/**
 * Script for simple voting method. Uses pk of the image,
 * incrementer receives 1 or 2 depending of the + or - vote
 * and url of the view, that must be generated in the template
 * (needed to make this script static)
 */
function voteClick(button, pk, incrementer, url)
{
    $.post(url, {
        pk: pk,
        incrementer: incrementer,
    }, function(data) {
        $('.rating-' + pk).html(data);//changing rating visually
        $('div.vote_block_' + pk).hide("slow");//hiding vote button
    });
    return false;
}
