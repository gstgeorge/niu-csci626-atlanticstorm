/*
    Gavin St. George
    CSCI 626
    Project 3
    Fall 2023
*/

// Listeners
$(document).ready(function() {

    // Filter the reports when a query is entered in the search bar
    $('#filter').on('input', function() {
        let query = $(this).val().toLowerCase(); // get search query
        filterReports(query);
    });

    // Clear the search query when the filter type is changed
    $('#filter-type').on('change', clearFilter)

    // Interaction with key values
    $('.key-value').on({

        // Highlight on hover
        mouseenter: function() {
            $(this).css('color', getComputedStyle(document.body).getPropertyValue('--bs-primary'));
        },
        mouseleave: function() {
            $(this).css('color', 'black');
        },

        // Search on click
        click: function() {
            let targetClass = $(this).attr('class').replace('key-value ', ''); // get filter type
            $('#filter-type').val(targetClass); // set filter type
            $('#filter').val($(this).text()); // put text in search box
            filterReports($(this).text().toLowerCase()); // filter reports
        }
    });
});

// Clear the search bar, and remove any filters
function clearFilter() {
    $('#filter').val('');
    filterReports('');
};

// Filter the reports
function filterReports(query) {
    $('#reports-container').find('.accordion-item').filter(function() {
        let target;
        switch($('#filter-type').val()) {   // get value to compare the query against
            case "person":
                target = $(this).find('.person');
                break;
            case "org":
                target = $(this).find('.org');
                break;
            case "place":
                target = $(this).find('.place');
                break;
            case "date":
                target = $(this).find('.date');
                break;
        }

        if (target) {
            $(this).toggle(target.text().toLowerCase().indexOf(query) > -1); // filter the results
        }

        else console.log('ERROR: Filter type not set');
    });
};
