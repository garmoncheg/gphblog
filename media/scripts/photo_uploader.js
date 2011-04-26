/**
 * Script for Uploading a Photo.
 */
var closed_text = 'Upload'
var open_text =   'Close!'

//use ajax Form Plugin
//setting this form as an ajax form
// used ajaxform from 
function setFormajax() {
var options = { 
    target: '#ajaxwrapper',
    success: setform_with_errors_ajax,
	}; 
$('#uploadForm').ajaxForm(options);
};

function setform_with_errors_ajax(){
	var options = { 
		    target: '#ajaxwrapper',
		    success: setform_with_errors_ajax,
	}; 
$('#uploadForm').ajaxForm(options);
};

//making sliding animations 
//and overriding ajax form submission
$(document).ready(function(){
	//sliding and loading upload form
	$(".btn-slide").click(function(){
	    // toggle sliding of the upload photo form
		$("#panel").slideToggle("slow");
		//$('.slide a').text(open_text); 
		
		if ($(".btn-slide").hasClass('active')){
			//actions on "close button click!
			$('.slide a').text(closed_text);
			$(".btn-slide").removeClass('active');
			$('div#panel div div#ajaxwrapper').remove();
			$('div.slide-inside').html('Loading...');
			
		}
		else{
		//get view data
		$.get(
				//get url from attribute "url", set by template
				$('div.slide-inside').attr("url"), 
				function(data) {
					//insert data to this div
					$('div.slide-inside').html(data);
					$('.slide a').text(open_text);
					//add class active to Button (can be closed)
					$(".btn-slide").addClass('active'); 
					setFormajax();
				}
		);
		};
		return false;
	});
	return false;
});