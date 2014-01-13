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

  // Automatically scroll to show the current entry
  var y = $('.media[data-id="' + currentPostId + '"]').offset().top;
  $('#content_sidebar').scrollTop(y - $('#Grid').offset().top);
});

// Load more
$('.load-more').click(function (e) {
  e.preventDefault();
  $(this).hide();

  var that = this;
  var dir = $(this).data('direction') || '';
  var params = {};
  params[$(this).data('action')] = $(this).data('anchor');
  params.order_by = [dir + 'published_at', dir + 'id'];
  $.getJSON(postListUrl, params).success(function (data) {
    if (data.objects.length === 0)
      return;

    // Remember the current first element and its position.
    var currentTop = $('.blog').children('.media-href').first();
    var currentOffset =
      currentTop.offset().top -
      $('#content_sidebar').scrollTop();

    // Scroll some extra distance toward the loaded contents.
    var padding = -100 * parseInt($(that).data('direction') + '1');

    insertPosts(data.objects, $(that).data('method'));

    // Scroll to match the previous position.
    $('#content_sidebar').scrollTop(
      currentTop.offset().top - currentOffset + padding
    );

    // Update "load more" button.
    $(that).data('anchor', _.last(data.objects).id);
    if (data.meta.next)
      $(that).show();
  });
});

// Hover filter block
$(window).load(function () {
  $('.item-choice').each(function () {
    var autoHeight = $(this).height() + 10;
    $(this).data({
      'height-auto': autoHeight,
      'height': 50
    }).animate({'height': 50}, 600);
  }).mouseenter(function () {
    $(this).stop(true).animate({'height': $(this).data('height-auto')}, 300);
  }).mouseleave(function () {
    $(this).delay(100).stop(true).animate({
      'height': $(this).data('height')
    }, 300);
  });
});

// Hover article block expands title
$('.blog').on('mouseenter', '.media', function () {
  var ele = $('.media-heading', this);
  if (ele.data('nowrap-height') === undefined)
    ele.data('nowrap-height', ele.height());
  ele.css('white-space', 'normal');
  if (ele.data('normal-height') === undefined)
    ele.data('normal-height', ele.height());
  ele.height(ele.data('nowrap-height')).stop(true).animate({
    'height': ele.data('normal-height')
  });
}).on('mouseleave', '.media', function () {
  var ele = $('.media-heading', this);
  ele.delay(100).stop(true).animate({
    'height': ele.data('nowrap-height')
  }, function () {
    $(this).css('white-space', 'nowrap');
  });
});
