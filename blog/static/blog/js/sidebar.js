// Clear everything
$('.load-more').hide();
$('section.blog').empty();

var sidebar_cell_template = $('#sidebar_cell_template').html();

function insertPosts(objects, method_name) {
  for (var i = 0; i < objects.length; i++) {
    var html = _.template(sidebar_cell_template, {'post': objects[i]});
    console.log(method_name);
    $(html)[method_name]($('section.blog')).hide().fadeIn();
  }
}

// Load initial rows
$.get(postListUrl + currentPostId + '/near/')
  .success(function (data) {
    insertPosts(data.objects, 'appendTo');

    // Update "load more" buttons
    $('.load-more:first').data('anchor', _.first(data.objects).id);
    $('.load-more:last').data('anchor', _.last(data.objects).id);
    if (data.meta.next)
      $('.load-more:last').show();
    else
      $('.load-more:last').hide();
    if (data.meta.previous)
      $('.load-more:first').show();
    else
      $('.load-more:first').hide();
});

// Load more
$('.load-more').click(function (e) {
  e.preventDefault();
  var that = this;
  var params = {};
  params[$(this).data('action')] = $(this).data('anchor');
  $.get(postListUrl, params, function (data) {
    insertPosts(data.objects, $(that).data('method'));

    // Update "load more" button
    $(that).data('anchor', _.last(data.objects).id);
    if (data.meta.next)
      $(that).show();
    else
      $(that).hide();
  });
});
