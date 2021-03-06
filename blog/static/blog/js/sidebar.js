/* global $ _ Spinner currentPostId postListUrl */

// Clear everything
$('.blog').empty().removeData('loaded')

$.ajaxSetup({'traditional': true})

// Filters in sidebar (handled by mixitup)
$('.item-choice a').click(function (e) {
  e.preventDefault()
})

var insertPosts = function (objects, methodName) {
  var getTagName = function (tag) { return tag.slug }

  for (var i = 0; i < objects.length; i++) {
    var object = objects[i]
    var tagSlugs = _.map(object.tags, getTagName)
    var html = _.template($('#sidebar_cell_template').html(), {
      'post': object,
      'tag_slugs': tagSlugs,
      'active': (object.id === currentPostId ? 'active' : '')
    })
    $('.blog')[methodName]($(html))
  }
  if ($('.blog').data('loaded')) {
    $('#Grid').mixitup('remix', $('.filter.active').data('filter'))
  } else {
    $('#Grid').mixitup({'layoutMode': 'list'})
    $('.blog').data('loaded', true)
  }
}

// Load initial rows
$.getJSON(postListUrl + currentPostId + '/near/').success(function (data) {
  insertPosts(data.objects, 'append')

  // Update "load more" buttons
  $('.load-more:first').data('anchor', _.first(data.objects).id)
  $('.load-more:last').data('anchor', _.last(data.objects).id)
  if (data.meta.next) {
    $('.load-more:last').show()
  } else {
    $('.load-more:last').hide()
  }
  if (data.meta.previous) {
    $('.load-more:first').show()
  } else {
    $('.load-more:first').hide()
  }

  // Automatically scroll to show the current entry
  var currentOffset = $('.media[data-id="' + currentPostId + '"]').offset()
  if (currentOffset) {
    var y = currentOffset.top - $('#Grid').offset().top
    $('#content_sidebar').scrollTop(y)
  }
})

// Load more
$('.load-more').click(function (e) {
  e.preventDefault()

  if ($(this).hasClass('disabled')) {
    return
  }
  $(this).addClass('disabled')
  $('.text', this).css('visibility', 'hidden')
  var spinner = new Spinner({'radius': 9, 'top': -3, 'width': 4}).spin(this)

  var that = this
  var dir = $(this).data('direction') || ''
  var params = {}
  params[$(this).data('action')] = $(this).data('anchor')
  params.order_by = [dir + 'published_at', dir + 'id']
  $.getJSON(postListUrl, params).success(function (data) {
    if (data.objects.length !== 0) {
      // Remember the current first element and its position.
      var currentTop = $('.blog').children('.media-href').first()
      var currentOffset =
        currentTop.offset().top -
        $('#content_sidebar').scrollTop()

      insertPosts(data.objects, $(that).data('method'))

      // Scroll to match the previous position.
      $('#content_sidebar').scrollTop(
        currentTop.offset().top - currentOffset
      )
    }

    // Update "load more" button.
    $(that).data('anchor', _.last(data.objects).id)
    if (!data.meta.next) {
      $(that).hide()
    } else {
      $(that).show()
    }
    $(that).removeClass('disabled')
    spinner.stop()
    $('.text', that).css('visibility', 'visible')
  })
})

// Hover filter block
$(window).load(function () {
  $('.item-choice').each(function () {
    var autoHeight = $(this).height() + 10
    $(this).data({
      'height-auto': autoHeight,
      'height': 50
    }).animate({'height': 50}, 600)
  }).mouseenter(function () {
    $(this).stop(true).animate({'height': $(this).data('height-auto')}, 300)
  }).mouseleave(function () {
    $(this).delay(100).stop(true).animate({
      'height': $(this).data('height')
    }, 300)
  })
})

// Hover article block expands title
$('.blog').on('mouseenter', '.media', function () {
  var ele = $('.media-heading', this)
  if (ele.data('nowrap-height') === undefined) {
    ele.data('nowrap-height', ele.height())
  }
  ele.css('white-space', 'normal')
  if (ele.data('normal-height') === undefined) {
    ele.data('normal-height', ele.height())
  }
  ele.height(ele.data('nowrap-height')).stop(true).animate({
    'height': ele.data('normal-height')
  })
}).on('mouseleave', '.media', function () {
  var ele = $('.media-heading', this)
  ele.delay(100).stop(true).animate({
    'height': ele.data('nowrap-height')
  }, function () {
    $(this).css('white-space', 'nowrap')
  })
})
