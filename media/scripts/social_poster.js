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


/*___________________________________________________________________________________________
*   function for posting to FLICKR current a photo
* ___________________________________________________________________________________________
*/
function post_to_flickr(button, image_pk, url){
		//making button disabled and 
		//posting into flickr
		$('#flickr_post_btn').attr("disabled", "disabled");
		$('#flickr_post_btn').addClass("bisy");
		$('span#socialposter_console').html('Posting photo to your flickr. Please wait...');
		$.post(//url to post to
				url, 
				//data array to send
				{ image_pk: image_pk },
				//function to handle callback
				function(data){
					$('span#socialposter_console').html(data);
				});//end function and post
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