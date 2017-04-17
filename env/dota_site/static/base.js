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
  });
});

Chart.defaults.global.maintainAspectRatio = false;
