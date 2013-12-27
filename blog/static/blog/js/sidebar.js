// Clear everything
$('.load-more').hide();
$('.blog').empty().removeData('loaded');

$.ajaxSetup({'traditional': true});

// Filters in sidebar (handled by mixitup)
$(".item-choice a").click(function (e) {
  e.preventDefault();
});

function insertPosts(objects, methodName) {
  var getTagName = function (tag) { return tag.slug; };

  for (var i = 0; i < objects.length; i++) {
    var object = objects[i];
    var tag_slugs = _.map(object.tags, getTagName);
    var html = _.template($('#sidebar_cell_template').html(), {
      'post': object, 'tag_slugs': tag_slugs,
      'active': (object.id == currentPostId ? 'active' : '')
    });
    $('.blog')[methodName]($(html));
  }
  if ($('.blog').data('loaded')) {
    $('#Grid').mixitup('remix', $('.filter.active').data('filter'));
  }
  else {
    $('#Grid').mixitup({'layoutMode': 'list'});
    $('.blog').data('loaded', true);
  }
}

// Load initial rows
$.getJSON(postListUrl + currentPostId + '/near/').success(function (data) {
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
  var autoHeight = $(this).height() + 5;
  $(this).data('height-auto', autoHeight).height(50).data('height', 50);
}).mouseenter(function () {
  $(this).animate({'height': $(this).data('height-auto')}, 300);
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
