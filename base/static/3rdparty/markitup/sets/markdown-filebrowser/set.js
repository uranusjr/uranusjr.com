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

var FileBrowserHelper = {
  markItUp: false,

  show: function(markItUp) {
    this.markItUp = markItUp
    var textarea_id = $(markItUp.textarea).attr('id');
    FileBrowser.show(textarea_id, '/admin/filebrowser/browse/?pop=1&type=');
  },

  triggerInsert: function(url) {
    $(this.markItUp.textarea).trigger('insertion',
      [{replaceWith: '!(left)' + url + '(beschrijving)!'}]);
  }
};

mySettings = {
	onShiftEnter:		{keepDefault:false, openWith:'\n\n'},
	markupSet: [
    {
      separator: '---------------'
    },
		{
      name: 'Picture',
      key: 'P',
      replaceWith: function (markItUp) {
			  FileBrowserHelper.show(markItUp);
			  return false;
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
}

// mIu nameSpace to avoid conflict.
miu = {
	markdownTitle: function(markItUp, char) {
		heading = '';
		n = $.trim(markItUp.selection||markItUp.placeHolder).length;
		// work around bug in python-markdown where header underlines must be at least 3 chars
		if (n < 3) { n = 3; }
		for(i = 0; i < n; i++) {
			heading += char;
		}
		return '\n'+heading;
	}
}
