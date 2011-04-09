/**
 * Script for Uploading a Photo.
 */
var closed_text = 'Upload Photo!'
var open_text = 'Close'

//use ajax Form Plugin
//setting this form as an ajax form
// used ajaxform from 
function setFormajax() {
var options = { 
    target: '#ajaxwrapper',
}; 
$('#uploadForm').ajaxForm(options);
}


//making sliding animations 
//and overriding ajax form submission
$(document).ready(function(){
	//sliding and loading upload form
	$(".btn-slide").click(function(){
	    // toggle sliding of the upload photo form
		$("#panel").slideToggle("slow");
		 $('.slide a').text(closed_text); 
		if ($(this).hasClass('active')){}
		else{
		//get view data
		$.get(
				//get url from attribute "url", set by template
				$('div.slide-inside').attr("url"), 
				function(data) {
					//insert data to this div
					$('div.slide-inside').html(data);
					$('.slide a').text(open_text);
					//$('div.slide-inside').append('<a href="#">Upload</a>')
					//setFormajax();
				}
		);
	    //add class active to Button (can be closed)
		$(this).toggleClass('active'); 
		};
		return false;
	});
	return false;
});