/**
 * Scripts for commenting a Photo.
 */

/*///////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////COMMENT EDITING///////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/

/*_______________________________________________________________________________________________
*  making comment EDIT form ajax ready
* _______________________________________________________________________________________________
*/
function setCommentEditformajax(pk) {
var options = { 
    target: ('.comment_body[comment-id="' + pk + '"]'),
    data: {comment_pk: pk, action: "comment"},
    success: afterEditComment,
    }
$('#comment_edit_form[comment-id="' + pk + '"]').ajaxForm(options);
return false;
};

/*_______________________________________________________________________________________________
*   function to close the EDIT comment form and show comment (not edited one)
* _______________________________________________________________________________________________
*/
function setCancelEditComment(pk, old_comment){
	
	$('#edit_cancel[comment-id="' + pk + '"]').live("click", function(){
		$('#comment_edit_form[comment-id="' + pk + '"]').hide("slow");
		$('#ajaxwrapper_edit_comment[comment-id="' + pk + '"]').remove();
		$('.comment_body[comment-id="' + pk + '"]').html(old_comment);
		//trigger enabling editing
		$('body').addClass('free');
	});

	return false;
};

/*_______________________________________________________________________________________________
* operations after EDIT comment form submit
* cleanup and getting ready for next comments
* _______________________________________________________________________________________________
*/
function afterEditComment(responseText, statusText, xhr, $form)
{
	$('body').addClass('free');
};

//_______________________________________________________________________________________________
//functions to show comment edit/delete buttons
//_______________________________________________________________________________________________
function comment_buttons_show(comment_pk) {
	$('.comment_delete_btn[comment-id="'+ comment_pk + '"]').show();
	$('.comment_edit_btn[comment-id="'+ comment_pk + '"]').show();
}
function comment_buttons_hide(comment_pk) {
	$('.comment_delete_btn[comment-id="'+ comment_pk + '"]').hide();
	$('.comment_edit_btn[comment-id="'+ comment_pk + '"]').hide();
};

/*___________________________________________________________________________________________
*    functions to SHOW and HIDE "edit" and "delete" comment buttons
* ___________________________________________________________________________________________
*/
function init_mouse_buttons(){
$('div.comment').mouseenter(function(){
	//if not editing check
	if ($('body').hasClass('free')) {
		if ($(this).hasClass('permit')) {
			var $comment=$(this).attr("commment-id");
			comment_buttons_show($comment);
		};
	};
}).mouseleave(function(){
	//if not editing check
	if ($('body').hasClass('free')) {
		if ($(this).hasClass('permit')) {
			var $comment=$(this).attr("commment-id");
			comment_buttons_hide($comment);
		};
	};
});
};



/*///////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////COMMENTING///////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/

/*_______________________________________________________________________________________________
*   making comment form ajax ready
* _______________________________________________________________________________________________
*/
function setCommentformajax(pk)
{
var options = { 
    //target: ('.last_comment[data-id="' + pk + '"]'),
    data: {pk: pk},
    success: afterComment,
    }; 
$('#comment_form[data-id="' + pk + '"]').ajaxForm(options);
//intercepting form cancel comment
$('#cancel').click(function(){
	cancelComment(pk);
});
};


/*_______________________________________________________________________________________________
* operations after COMMENT form submit
* cleanup and getting ready for next comments
* _______________________________________________________________________________________________
*/
function afterComment(responseText, statusText, xhr, $form)
{
	//getting item pk from response
	var pk=$(responseText).attr("data-id");
	if (responseText.indexOf("ajaxwrapper_comment") > -1)
	{
		//_________actions if function receives form with errors in response_________
		//alert(responseText);
		$('div.form_place[data-id="' + pk + '"]').html(responseText);
		//adding this form pk atribute
		$('form#comment_form').attr("data-id", pk);
		setCommentformajax(pk);
		$('div#ajaxwrapper_comment').attr("data-id", pk);
	}
	else
	{
		//__________actions if function receives comment in response__________
	//inserting comment into place and removing placer for last comment
	$('.last_comment[data-id="' + pk + '"]').remove();
	$('div.comments-block[data-id="' + pk + '"]').append(responseText);
	//comment already written so we removing class last comment from it
	$('div.last_comment[data-id="' + pk + '"]').removeClass("last_comment");
	//showing comment button
	$('.comment-btn[data-id="' + pk + '"]').show("slow");
	//hiding and removing form
	$('#ajaxwrapper_comment[data-id="' + pk + '"]').hide("slow");
	$('#ajaxwrapper_comment[data-id="' + pk + '"]').remove();
	//adding place for new comment
	$('div.comments-block[data-id="' + pk + '"]').append('<div class="last_comment" data-id="'+pk+'"></div>');
	//call editing duttons handler
	init_editing_handler()
	//call delete buttons handler
	init_delete_handler()
	//call mouse events_handler
	init_mouse_buttons();
	};
};

/*_______________________________________________________________________________________________
*   function to close the comment form and show hidden comment button
* _______________________________________________________________________________________________
*/
function cancelComment(pk){
	$('#comment_form[data-id="' + pk + '"]').hide("slow");
	$('#ajaxwrapper_comment[data-id="' + pk + '"]').remove();
	$('.comment-btn[data-id="' + pk + '"]').show("slow");
	return false;
};

/*___________________________________________________________________________________________
*   function of EDITING a comment
* ___________________________________________________________________________________________
*/
function init_editing_handler(){
$('a.comment_edit_btn').click(function(){
	//if not editing comment now check
	if ($('body').hasClass('free')) {
	$('body').removeClass('free');
	//comment
	//var $comment = this;
	//comment_pk
	var comment_pk = $(this).attr("comment-id");
	//form_url
	var get_url = $('.comments-block').attr("url");
	//saving old comment in case of comment editing cancel
	var old_comment = $('.comment_body[comment-id="' + comment_pk + '"]').html();
	$('.comment_body[comment-id="' + comment_pk + '"]').hide();
	$('.comment_body[comment-id="' + comment_pk + '"]').text('Loading...');
	//getting AJAX edit-comment form
	$.post(
		//url to get
		get_url, { comment_pk: comment_pk, comment_text: old_comment, action: "receive" },
		function(data){
			//inserting post data into text
			$('.comment_body[comment-id="' + comment_pk + '"]').html(data);
			// setting edit comment form ajax
			setCommentEditformajax(comment_pk);
			// setting intercepter on Cancel button
			setCancelEditComment(comment_pk, old_comment);
			comment_buttons_hide(comment_pk);
		});
	$('.comment_body[comment-id="' + comment_pk + '"]').show("slow");
	
	return false;
	};//endif
});
};






/*///////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////// DELETE COMMENT EVENTS HANDLER /////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/
/*___________________________________________________________________________________________
*   function of DELETING a comment
* ___________________________________________________________________________________________
*/
function init_delete_handler(){
$('a.comment_delete_btn').click(function(){
		if ($('body').hasClass('free')) {
			$('body').removeClass('free');
			//getting used comment pk into variable to use
			var comment_pk = $(this).attr("comment-id");
			//delete comment url
			var del_url = $('.comments-block').attr("del");
			//changing temporary request text
			$('.permit' + comment_pk).text("Processing...");
			
			$.post(
					//url to get
					del_url, { comment_pk: comment_pk, },
					function(data){
						//visually removing comment
						$('.permit' + data).hide("slow");
						//removing dom object here
						$('.permit' + data).remove();
						//setting free the handler
						$('body').addClass('free');
					});
		};//end if free (body)
});
};


/*///////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////MAIN COMMENT SYSTEM HANDLER//////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/
$(document).ready(function(){
	/*___________________________________________________________________________________________
	*       click on COMMENT button under photo
	* ___________________________________________________________________________________________
	*/
	$(".comment-btn").click(function(){
		//getting interacting block Pk
		var $pk = $(this).attr("data-id");
		//getting comment form
		$.get(
			//div inside the form containing post url
			$('div.form_place[data-id="' + $pk + '"]').attr("url"),
			function(data) {
				//inserting form into place
				$('div.form_place[data-id="' + $pk + '"]').html(data);
				//showing div with form
				$('div.form_place[data-id="' + $pk + '"]').show("slow");
				//adding this form pk atribute
				$('form#comment_form').attr("data-id", $pk);
				//adding ajax form wrapper to this form
				setCommentformajax($pk);
				$('div#ajaxwrapper_comment').attr("data-id", $pk);
				$('#comment_form[data-id="' + $pk + '"] button.red').attr("data-id", $pk);
			}
		);
		//hiding the comment button
		$('.comment-btn[data-id="' + $pk + '"]').hide("slow");
	});
	//call editing duttons handler
	init_editing_handler()
	//call delete buttons handler
	init_delete_handler()
	//call mouse events_handler
	init_mouse_buttons();

});
