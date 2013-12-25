// Clear everything
$('.load-more').hide();
$('#Grid').empty();

var sidebar_cell_template = $('#sidebar_cell_template').html();

function insertPosts(objects, method_name) {
  for (var i = 0; i < objects.length; i++) {
    var object = objects[i];
    var tag_slugs = _.map(object.tags, function (tag) {
      return tag.slug;
    });
    var html = _.template(sidebar_cell_template, {
      'post': object, 'tag_slugs': tag_slugs
    });
    $(html)[method_name + 'To']($('#Grid'));
  }
  $('#Grid').mixitup({
    onMixStart: function () {
      $('.load-more:last').hide();
    },
    onMixEnd: function () {
      $('.load-more:last').delay(300).fadeIn();
    }
  });
}

// Load initial rows
$.get(postListUrl + currentPostId + '/near/')
  .success(function (data) {
    insertPosts(data.objects, 'append');

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

// Hover filter block
$('.item-choice').each(function () {
  $(this).data('height', $(this).height() + 3);
});
$('.item-choice').mouseenter(function () {
  $(this).css('height', 'auto');
  var autoHeight = $(this).height();
  $(this).height($(this).data('height'));
  $(this).animate({'height': autoHeight + 10}, 300);
}).mouseleave(function () {
  $(this).delay(100).animate({'height': $(this).data('height')}, 300);
});
