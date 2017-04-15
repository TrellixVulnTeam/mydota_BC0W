const CHART = document.getElementById("lineChart");

var kills = $('#graph-data p:eq(1)').val() ;


let barChart = new Chart(CHART, {
    type: 'bar',
    data: {
        labels: ['Jan'],
        datasets: [{
            label: 'Kills',
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1,
            data: kills,
        }, {
            label: 'Deaths',
            data:$('#graph-data p:eq(1)'),
        }, {
            label: 'Assists',
            data:$('#graph-data p:eq(2)'),
        }]
    },
    options:{
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    stepSize: 2,
                    max: 30,
                }
            }]
        }
    }
});

console.log($('#graph-data p:eq(0)').text());
console.log($('#graph-data p:eq(0)').val());
console.log(typeof kills);
console.log($('#graph-data p:eq(2)'));




$(function(){
    $('.nav.nav-tabs li').on('click', function(){
        $(this).attr('class', 'active');
        $(this).siblings().attr('class', '');
        var panelToShow = $(this).attr('rel');
        $('#myTabContent .active.in').slideUp(300, function(){
            $(this).removeClass('active in');
            $('#'+panelToShow).slideDown(300, function(){
                $(this).addClass('active in');
            });
        });

        // function showNextPanel() {
        //     $(this).removeClass('active');

        //     $('#'+panelToShow).slideDown(300, function() {
        //         $(this).addClass('active');
        //     });
        // }

  });
});