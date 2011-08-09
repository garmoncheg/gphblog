/**
 * Social poster scripts.
 * 
 * user can post images to social networks by using those scripts.
 */
/*_______________________________________________________________________________________________
*   function to add AJAX handler to socialposter form
* _______________________________________________________________________________________________
*/
function setSocialPosterFormAjax() {
var options = { 
    target: ('#socialposter_console'),
    data: {image_pk: pk},
    //success: afterEditTitle,
    }
$('#social_posting_form').ajaxForm(options);
return false;
};

/*_______________________________________________________________________________________________
* operations after EDIT comment form submit
* cleanup and getting ready for next comments
* _______________________________________________________________________________________________
*/
function afterEditTitle(responseText, statusText, xhr, $form)
{
	$('body').addClass('free');
};

//_______________________________________________________________________________________________
//functions to show/hide TITLE EDIT button
//_______________________________________________________________________________________________
function title_editor_button_show(comment_pk) {
	$('.title_edit_btn[data-id="'+ comment_pk + '"]').show();
}
function title_editor_button_hide(comment_pk) {
	$('.title_edit_btn[data-id="'+ comment_pk + '"]').hide();
};

/*___________________________________________________________________________________________
*    functions to SHOW and HIDE "edit" and "delete" comment buttons upon :hover
*    permit check
* ___________________________________________________________________________________________
*/
function init_title_hover(){
$('div.photo_title').mouseenter(function(){
	//if not editing check
	if ($('body').hasClass('free')) {
		if ($(this).hasClass('permit')) {
			var $title=$(this).attr("title-id");
			title_editor_button_show($title);
		};
	};
}).mouseleave(function(){
	//if not editing check
	if ($('body').hasClass('free')) {
		if ($(this).hasClass('permit')) {
			var $title=$(this).attr("title-id");
			title_editor_button_hide($title);
		};
	};
});
};


/*___________________________________________________________________________________________
*   function of EDITING TITLE of a photo
* ___________________________________________________________________________________________
*/
function init_title_editing_handler(){
$('a.title_edit_btn').click(function(){
	//if not editing other title or comment now check
	if ($('body').hasClass('free')) {
	$('body').removeClass('free');
	//comment_pk
	var image_pk = $(this).attr("data-id");
	//form_url
	var get_url = $('.title_form_place').attr("url");
	//saving old title in case of title editing canceling
	var old_title = $('.title-body[data-id="title-' + image_pk + '"]').html();
	$('.title-body[data-id="title-' + image_pk + '"]').hide();
	$('.title-body[data-id="title-' + image_pk + '"]').text('Editing...');
	//getting AJAX edit-title form
	$.post(
		//url to get
		get_url, { image_pk: image_pk, title_text: old_title, action: "receive" },
		function(data){
			//inserting post data into title
			$('.title-body[data-id="title-' + image_pk + '"]').html(data);
			// setting edit comment form ajax
			setTitleEditorformajax(image_pk);
			// setting intercepter on Cancel button
			setCancelEditTitle(image_pk, old_title);
			title_editor_button_hide(image_pk);
		});
	$('.title-body[data-id="title-' + image_pk + '"]').show("slow");
	$('.title_edit_btn').hide();
	return false;
	};//endif
});
};

//simple function to set delay
function wait_console(time) {
	$.delay(time);
}



/*___________________________________________________________________________________________
*   function for posting to FLICKR current photo
*   called by onclick event in single image view
* ___________________________________________________________________________________________
*/
//variable to disable processing click
var flickr_post_ready = 1;
function post_to_flickr(button, image_pk, url){
	//checking for processing switch
	if (flickr_post_ready == 1) {
		//making button disabled and 
		//posting into flickr
		flickr_post_ready = 2;
		$('#flickr_post_btn').addClass("bisy");
		//printing status to console
		$('div#social_posting_buttons').append('<span id="socialposter_console"> </span>');
		$('span#socialposter_console').html('<span class="green"><img src="/site_media/site_graphics/waiting_scroller_small.gif" width="25" height="25"></img>Posting photo to your flickr. Please wait...</span>');
		$('span#socialposter_console').show();
		$.post(//url to post to
				url, 
				//data array to send
				{ image_pk: image_pk },
				//function to handle successful callback
				function(data){
					var feedback = '<span class="green"><img src="/site_media/site_graphics/ok_small.png" width="25" height="25"></img>'+data+'</span>'
					$('a#flickr_post_btn').replaceWith('<img class="flickr_post_btn_disabled" src="/site_media/site_graphics/social/flickr-icon.png" width="50" height="50"></img>');
					$('span#socialposter_console').html(feedback);
					$('span#socialposter_console').delay(3000).slideUp(300);
					$('span#socialposter_console').attr('id','none');
					$('span#socialposter_console').show();
					flickr_post_ready = 1;
				});//end function and post
	} else { //not allowed to use this button due to processing
		return false;
	};
		return false;
};//end function


/*///////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////MAIN SOCIAL POSTER HANDLER///////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/
$(document).ready(function(){
	//call editing duttons handler
	//setSocialPosterFormAjax()
	
	
	//call mouse events_handler
	//init_title_hover();

});