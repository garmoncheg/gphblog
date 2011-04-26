/**
 * Scripts for commenting a Photo.
 */

//making comment form ajax ready
function setCommentformajax(pk)
{
var options = { 
    //target: ('.last_comment[data-id="' + pk + '"]'),
    data: {pk: pk},
    success: afterSubmit,
    }; 
$('#comment_form[data-id="' + pk + '"]').ajaxForm(options);
//intercepting form cancel comment
$('#cancel').click(function(){
	cancelComment(pk);
});
};

//operations after form submit
//cleanup and getting ready for next comments
function afterSubmit(responseText, statusText, xhr, $form)
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
	//inserting comment into place
	$('.last_comment[data-id="' + pk + '"]').html(responseText);
	//comment already written so we removing class last comment from it
	$('div.last_comment[data-id="' + pk + '"]').removeClass("last_comment");
	//showing comment button
	$('.comment-btn[data-id="' + pk + '"]').show("slow");
	//hiding and removing form
	$('#ajaxwrapper_comment[data-id="' + pk + '"]').hide("slow");
	$('#ajaxwrapper_comment[data-id="' + pk + '"]').remove();
	//adding place for new comment
	$('div.comments-block[data-id="' + pk + '"]').append('<div class="last_comment" data-id="'+pk+'"></div>');
	};
};



// function to close the comment form and show hidden comment button
function cancelComment(pk){
	$('#comment_form[data-id="' + pk + '"]').hide("slow");
	$('#ajaxwrapper_comment[data-id="' + pk + '"]').remove();
	$('.comment-btn[data-id="' + pk + '"]').show("slow");
	return false;
};

//MAIN comment function
$(document).ready(function(){
	//click on comment button under photo
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
});
