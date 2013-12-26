// Clear everything
$('.load-more').hide();
$('.blog').empty();

$.ajaxSetup({'traditional': true});
$('#Grid').mixitup({'layoutMode': 'list'});

// Filters in sidebar (handled by mixitup)
$(".item-choice a").click(function (e) {
  e.preventDefault();
});

function insertPosts(objects, method_name) {
  var getTagName = function (tag) { return tag.slug; };

  for (var i = 0; i < objects.length; i++) {
    var object = objects[i];
    var tag_slugs = _.map(object.tags, getTagName);
    var html = _.template($('#sidebar_cell_template').html(), {
      'post': object, 'tag_slugs': tag_slugs,
      'active': (object.id == currentPostId ? 'active' : '')
    });
    $('.blog')[method_name]($(html));
  }
  $('#Grid').mixitup('remix', $('.filter.active').data('filter') || 'all');
}

// Load initial rows
$.getJSON(postListUrl + currentPostId + '/near/').success(function (data) {
  if (data.objects.length === 0)
    return;

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
  var dir = $(this).data('direction') || '';
  var params = {};
  params[$(this).data('action')] = $(this).data('anchor');
  params.order_by = [dir + 'published_at', dir + 'id'];
  $.getJSON(postListUrl, params).success(function (data) {
    if (data.objects.length === 0)
      return;

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

// Hover article block expands title
$('.blog').on('mouseenter', '.media', function () {
  var ele = $('.media-heading', this);
  if (ele.data('nowrap-height') === undefined)
    ele.data('nowrap-height', ele.height());
  ele.css('white-space', 'normal');
  if (ele.data('normal-height') === undefined)
    ele.data('normal-height', ele.height());
  ele.height(ele.data('nowrap-height')).animate({'height': ele.data('normal-height')});
}).on('mouseleave', '.media', function () {
  var ele = $('.media-heading', this);
  ele.animate({'height': ele.data('nowrap-height')}, function () {
    $(this).css('white-space', 'nowrap');
  });
});
