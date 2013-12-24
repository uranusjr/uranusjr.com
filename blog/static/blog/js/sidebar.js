$.get(post_list_url + current_post_id + '/near/').success(function (data) {
    for (var i = 0; i < data.objects.length; i++) {
        var obj = data.objects[i];
        var template = $('#sidebar_article_template').html();
        var html = _.template(template, {'post': obj});
        $(html).appendTo($('section.blog'));
    }
});
