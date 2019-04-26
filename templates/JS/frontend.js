$(function () {
    $('#help-modal').on('click', function () {
        $('#welcome-modal').modal('show');
    });
});

$(function () {
    $('a#turn-on').on('click', function () {
        $.getJSON('/turn-on',
            function (data) {});
        return false;
    });
});

$(function () {
    $('a#turn-off').on('click', function () {
        $.getJSON('/turn-off',
            function (data) {});
        return false;
    });
});

$(function () {
    $('a#flow').on('click', function () {
        $.getJSON('/flow',
            function (data) {});
        return false;
    });
});

$(function () {
    $('a#show-times').on('click', function () {
        $.getJSON('/show-tide-extrema',
            function (data) {});
        window.location.reload();
        return false;
    });
});

// Display arrows next to tide data
$(function () {
    $('.tide-extrema-data-tide').each(function () {
        if ($(this).text().indexOf('high') >= 0) {
            $(this).nextAll().eq(1).children().addClass('fas fa-chevron-circle-up');
        } else {
            $(this).nextAll().eq(1).children().addClass('fas fa-chevron-circle-down');
        }
    });
});


// Get region location from dropdown and append it to tidal information
$(function () {
    $('.region').on('click', function (e) {
        var name = e.currentTarget;

        var station_data = [];
        station_data.push(name.getAttribute("data-name").replace(/ .*/, ''));
        station_data.push(name.getAttribute("data-name"));

        var $region = $('.current_region');

        $region.html('');
        $region.append(name.getAttribute("data-name"));
        $(".graph-title").html(name.getAttribute("data-name"));

        $.ajax({
            type: "POST",
            contentType: "application/json;charset=utf-8",
            url: "/",
            traditional: "true",
            data: JSON.stringify({station_data: station_data}),
            dataType: "json"
        });

        $('#station-loader').show();
        setTimeout(function () {
            $('#station-loader').hide();
            $('#station-success').show();
            window.location.reload();
        }, 7000);
    });
});


$(function () {
    $(document).ready(function () {
        $('.dropdown-submenu a.station').on("click", function (e) {
            e.stopPropagation();
            e.preventDefault();
            $(this).next('ul').toggle();
        });
    });
});

// TODO: Probably use ajax requests to get the data for the graphs
// A dummy template for how the tide data will be graphed
$(function () {
    $(document).ready(function () {
        var height_points = [];
        var time_points = [];

        $(".tide-extrema-data-height").each(function () {
            height_points.push($(this).text().replace(' ft.',''));
        });

        $(".tide-extrema-data-time").each(function () {
            time_points.push($(this).text());
        });

        var ctxL = document.getElementById("lineChart").getContext('2d');
        var myLineChart = new Chart(ctxL, {
            type: 'line',
            data: {
                labels: time_points,
                datasets: [{
                    label: "Predicted tide heights",
                    data: height_points,
                    backgroundColor: [
                        'rgba(255, 142, 22, .1)',
                    ],
                    borderColor: [
                        'rgba(0, 25, 127, .7)',
                    ],
                    borderWidth: 2
                },
                    // {
                    //     label: "Actual",
                    //     data: [0.87, 1.15, 1.08, 0.71],
                    //     backgroundColor: [
                    //         'rgba(0, 137, 132, .2)',
                    //     ],
                    //     borderColor: [
                    //         'rgba(0, 10, 130, .7)',
                    //     ],
                    //     borderWidth: 2
                    // }
                ]
            },
            options: {
                responsive: true
            }
        });
    });
});
