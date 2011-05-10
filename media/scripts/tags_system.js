/**
 * Scripts for handling TAGS.
 */

/*_______________________________________________________________________________________________
*  function to update tag data getting it from input
*  and posting them to view
* _______________________________________________________________________________________________
*/
function update_tags(tag){
	//getting post url
	var post_url = $('div#tags_block').attr('url');
	//getting item pk
	var image_pk = $('input').attr('data-id');
	//updated string capturing
	var cleaned_tags = $('input.tags').attr('value');
	//posting changes to base and rewriting tags string
	
	//trying to modify tags string
	if (!tag) {tag=''};
	tags=cleaned_tags+', '+tag;
	$.post(
			post_url, 
			{'image_pk':image_pk, 'body':tags},
			function(data){
				$('div.tags'+image_pk+' span#all_tags').text(data);
			}
	);
};

/*_______________________________________________________________________________________________
*  Actions after TAF add
* _______________________________________________________________________________________________
*/
function onAddTag(tag) {
	update_tags(tag);
};

/*_______________________________________________________________________________________________
*  Actions after TAG removed
* _______________________________________________________________________________________________
*/
function onRemoveTag(tag) {
	update_tags();
	
};

/*_______________________________________________________________________________________________
*  making form ready for tags editing
* _______________________________________________________________________________________________
*/
function setTagsEditable() {
	
	$('input.tags').tagsInput({
		'onAddTag':onAddTag,
		'onRemoveTag':onRemoveTag,
		'interactive':true,
		'height':'100px',
		'width':'750px',
		'minChars' : 3,
		'maxChars' : 50
	});
};


/*///////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////MAIN TAGS HANDLER//////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////*/
$(document).ready(function(){
	setTagsEditable();
	$('a#tags-edit-btn').click(function(){
		//getting item pk
		var item_pk = $(this).attr('data-id');
		//status dependent event actions
		if ($(this).hasClass('orange')) {
			//edit_tags click to open
			//making button green and showing tags edit form
			$('#tags-edit-btn[data-id="' + item_pk + '"]').removeClass('orange');
			$('#tags-edit-btn[data-id="' + item_pk + '"]').addClass('green');
			$('#tags-edit-btn[data-id="' + item_pk + '"]').text('Done');
			$('form.tags'+item_pk).show("slow");
			$('div.tags'+item_pk+' b').text('');
		} else { 
			//edit_tags click to close
			$('#tags-edit-btn[data-id="' + item_pk + '"]').removeClass('green');
			$('#tags-edit-btn[data-id="' + item_pk + '"]').addClass('orange');
			$('#tags-edit-btn[data-id="' + item_pk + '"]').text('Edit tags >>>');
			$('form.tags'+item_pk).hide("slow");
		}
	})
	


});