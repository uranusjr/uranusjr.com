/* global $ FastClick */

// Fastclick
$(document).ready(function () {
  FastClick.attach(document.body)
})

// "Scroll to up" button in sidebar
$('a.scroll-top').click(function (e) {
  e.preventDefault()
  $.smoothScroll({'offset': 0})
})
