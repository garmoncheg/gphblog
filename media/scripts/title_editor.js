/**
 * Title editor csripts.
 * 
 * Adds editing form with AJAX loading. Checks for user ability 
 * to edit photo title (both on server and in javascript) and then 
 * shows edit button if enabled. Edit button expands to Title 
 * editing form. 
 * Upon save title updates dynamically. 
 * Used simple textarea form.
 */
/*_______________________________________________________________________________________________
*   function to add AJAX handler to title edit form
* _______________________________________________________________________________________________
*/
function setTitleEditorformajax(pk) {
var options = { 
    target: ('.title-body[data-id="title-' + pk + '"]'),
    data: {image_pk: pk, action: "commit"},
    success: afterEditTitle,
    }
$('#title_edit_form[data-id="' + pk + '"]').ajaxForm(options);
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



/*///////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////MAIN TITLE EDITOR SYSTEM HANDLER////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/
$(document).ready(function(){
	//call editing duttons handler
	init_title_editing_handler()
	//call mouse events_handler
	init_title_hover();

});