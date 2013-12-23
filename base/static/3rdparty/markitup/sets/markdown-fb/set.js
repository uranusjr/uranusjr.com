// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// MarkDown tags example
// http://en.wikipedia.org/wiki/Markdown
// http://daringfireball.net/projects/markdown/
// -------------------------------------------------------------------
// Feel free to add more tags
// -------------------------------------------------------------------

// From http://stackoverflow.com/questions/946534/
$.fn.extend({
  insertAtCaret: function(myValue) {
    this.each(function() {
      if (document.selection) {
        $(this).focus();
        sel = document.selection.createRange();
        sel.text = myValue;
        $(this).focus();
      }
      else if (this.selectionStart || this.selectionStart == '0') {
        var startPos = this.selectionStart;
        var endPos = this.selectionEnd;
        var scrollTop = this.scrollTop;
        this.value = this.value.substring(0, startPos)
          + myValue + this.value.substring(endPos, this.value.length);
        $(this).focus();
        this.selectionStart = startPos + myValue.length;
        this.selectionEnd = startPos + myValue.length;
        this.scrollTop = scrollTop;
      } else {
        this.value += myValue;
        $(this).focus();
      }
    });
  }
});

var FileBrowserHelper = {
  markItUp: false,

  show: function(markItUp) {
    var $input = $('<div><input type="text" id="filebrowser_input">'
      + '<a id="previewlink_filebrowser_input"><div id="preview_filebrowser_input">'
      + '<img id="previewimage_filebrowser_input"></div></a></div>')
      .appendTo('body').hide();

    FileBrowser.show(
      'filebrowser_input', '/admin/filebrowser/browse/?pop=1&type=', function () {
        var path = $('#filebrowser_input').val();
        $(markItUp.textarea).insertAtCaret('![](/media/' + path + ')');
        $input.remove();
      }
    );
  }
};

mySettings = {
	onShiftEnter: {
    keepDefault: true,
    openWith: '\n'
  },
	markupSet: [
    {
      separator: '---------------'
    },
		{
      name: 'Picture',
      key: 'P',
      openWith: function (markItUp) {
        FileBrowserHelper.show(markItUp);
      },
      className: 'picture'
    },
		{
      name: 'Link',
      key: 'L',
      openWith: '[',
      closeWith: ']([![Url:!:http://]!] "[![Title]!]")',
      placeHolder: 'Your text to link here...',
      className: 'link'
    },
		{
      separator:'---------------'
    },
		{
      name: 'Preview',
      call: 'preview',
      className: 'preview'
    }
	]
};
