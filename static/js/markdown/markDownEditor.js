/* *
 * markdownEditor (http://gitcafe.com/Qianfeng/markdownEditor/)
 * Released under MIT license
 * Copyright (c) 2012-2012 Qianfeng <wu1990@gmail.com> (http://qianfeng.gitcafe.com/)
 * 时间关系，功能非常不全面。
 * 依赖 :
 *   * markdown-js - https://github.com/evilstreak/markdown-js
 *   * jQuery - https://jquery.com
 */  
(function( editorName ){


	/* ---------------------------
	 * Editor Class
	 */
 	function Editor(settings)
 	{

		var editor;
		var isIE = !-[1,];
		this.cmd = { };

		var trim = function (str) {
		  var m = str.length;
		  for (var i = 0; i < m; i++) {
		    if (str.charCodeAt(i) > 32) {
		      break;
		    }
		  }

		  for (var j = m - 1; j > i; j--) {
		    if (str.charCodeAt(j) > 32) {
		      break;
		    }
		  }

		  return str.slice(i, j + 1);
		};

 		var basePath = function(){
 			var scripts = $("script");
 			for(var k in scripts)
 			{
 				var src = scripts[k].src;
 				if(src && src.indexOf(editorName) >= 0 )
 				{
 					return src.substring(0, src.lastIndexOf('/') + 1)
 				}
 			}
 		}

 		this._init = function(settings)
 		{
 			this.settings = settings;

 			this.wrap = this.createWrap();			// 创建编辑器html对象
 			this.preview = this.wrap.find(".editor-preview");	//预览区域
 			this.toolbar = this.wrap.find(".editor-toolbar");	//工具栏
 			this.textarea = settings.textarea;		// 直接使用原本的textarea对象


 			this.textarea[0][editorName] = editor = this;	//
 			settings = undefined;

 			this.loadDepend();
			this.textarea.after(editor.wrap);			// 在页面中加入编辑器
			this.textarea.remove();					// 去掉原本的textarea
			this.wrap.find(".editor-textarea").append(editor.textarea);	//将原本的textarea加到编辑器中~
 			this.bindEvents();
 			this.cmd.textareaChange();
 			//return;
 		}

 		this.loadDepend = function(callback){
 			var _ = basePath();
 			var css = $('<link href="' + _ + editorName + '.css" rel="stylesheet" type="text/css" />');
 			$("head").append(css);
 		}

 		this.createWrap = function(){
 			var toolbarButtons = {
 				head3 : '<li class="editor-toolbar-button-head3"><a href="javascript:void(0)"><i class="editor-icon-head"></i></a></li>',
				bold : '<li class="editor-toolbar-button-bold"><a href="javascript:void(0)"><i class="editor-icon-blod"></i></a></li>',
				italic : '<li class="editor-toolbar-button-italic"><a href="javascript:void(0)"><i class="editor-icon-italic"></i></a></li>',
				quote : '<li class="editor-toolbar-button-quote"><a href="javascript:void(0)"><i class="editor-icon-quote"></i></a></li>',
				link : '<li class="editor-toolbar-button-link"><a href="javascript:void(0)"><i class="editor-icon-link"></i></a></li>',
				ul : '<li class="editor-toolbar-button-ul"><a href="javascript:void(0)"><i class="editor-icon-ul"></i></a></li>',
				ol : '<li class="editor-toolbar-button-ol"><a href="javascript:void(0)"><i class="editor-icon-ol"></i></a></li>',
				split : '<li class="split"></li>',
				picture : '<li class="editor-toolbar-button-picture"><a href="javascript:void(0)"><i class="editor-icon-picture"></i></a></li>'
 			}
 			var actionsHTML = [];
			if(this.settings.actions)
			{
				var actions = this.settings.actions
			}
			else
			{
 				var actions = ['head3', 'bold', 'italic', 'quote', 'link', 'ul', 'ol', 'split', 'picture'];
			}

			for(var k in actions)
			{
				toolbarButtons[actions[k]] && actionsHTML.push(toolbarButtons[actions[k]]);
			}
 			var editorHTML = 
			[
			'<div class="editor-wrap" id="eee">',
			'	<div class="editor-head">',
			'		<ul class="editor-toolbar">',
						actionsHTML.join(''),
			'		</ul>',
			'	</div>',
			'	<div class="editor-textarea"></div>',
			'	<div class="editor-preview active">',
			'		<a href="javascript:void(0);" class="editor-preview-toggle"></a>',
			'		<div class="editor-preview-body"></div>',
			'	</div>',
			'</div>'
			].join('');

			return $(editorHTML);
 		}

		this.bindEvents = function(){
			for(var func in this.bindEvents)
			{
				this.bindEvents[func]();
			}
		}


		/**
		 * 编辑器命令
		 */
		this.cmd.common = function( prefix, suffix, settings )
		{
			var defaultSettings = { rule : 'normal' , eachline : true, clearBR : false };
			if(settings)
			{
				for( k in defaultSettings)
				{
					if(settings[k] == undefined)
					{
						settings[k] = defaultSettings[k];
					}
				}
			}
			else
			{
				settings = defaultSettings;
			}
			var rangeData = editor.cursorPosition.get();
			var start = rangeData.start;
			var resultText = rangeData.text;
			if(settings.clearBR)
			{
				resultText = resultText.replace(/\n/g, " ");
			}
			if(settings.rule == 'replace')
			{
				resultText = '';
			}

			selectedTextLengh = resultText.length;
        	var lines = resultText.split("\n");


	        if(settings.eachline && lines.length > 1)
	        {
        		for(var n in lines)
        		{
        			if(trim(lines[n]).length > 0)
        			{
        				lines[n] = prefix + trim(lines[n]) + suffix;
        			}
        		}
        		resultText = lines.join("\n");
	        }
	        else
	        {
	        	resultText = prefix + resultText + suffix;
	        }

	        editor.cursorPosition.insert(rangeData, resultText, selectedTextLengh == 0 ? -suffix.length : 0);
			return true;
		}

		this.cursorPosition = {};
		this.cursorPosition.get = function() {
			var textarea = editor.textarea[0];
			var rangeData = { text: "", start: 0, end: 0 };  

			if (textarea.setSelectionRange) { // W3C      
				textarea.focus();  
				rangeData.start = textarea.selectionStart;  
				rangeData.end = textarea.selectionEnd;  
				rangeData.text = (rangeData.start != rangeData.end) ? textarea.value.substring(rangeData.start, rangeData.end) : "";  
			} else if (document.selection) { // IE  
				textarea.focus();  
				var i,  
				oS = document.selection.createRange(),  
				// Don't: oR = textarea.createTextRange()  
				oR = document.body.createTextRange();  
				oR.moveToElementText(textarea);  

				rangeData.text = oS.text;  
				rangeData.bookmark = oS.getBookmark();  
				// object.moveStart(sUnit [, iCount])   
				// Return Value: Integer that returns the number of units moved.  
				for (i = 0; oR.compareEndPoints('StartToStart', oS) < 0 && oS.moveStart("character", -1) !== 0; i++) {  
					// Why? You can alert(textarea.value.length)  
					if (textarea.value.charAt(i) == '\r') {  
						i++;  
					}  
				}  
				rangeData.start = i;  
				rangeData.end = rangeData.text.length + rangeData.start;  
			}  

			return rangeData;  
		}

		this.cursorPosition.set = function(rangeData){
			var textarea = editor.textarea[0];
	        var oR, start, end;  
	        if (!rangeData) {  
	            alert("You must get cursor position first.")  
	        }  
	        textarea.focus();  
	        if (textarea.setSelectionRange) { // W3C  

	            textarea.setSelectionRange(rangeData.start, rangeData.end);  
	        } else if (textarea.createTextRange) { // IE  
	            oR = textarea.createTextRange();  
	            // Fixbug : ues moveToBookmark()  
	            // In IE, if cursor position at` the end of textarea, the set function don't work  
	            if (textarea.value.length === rangeData.start) {  
	                //alert('hello')  
	                oR.collapse(false);  
	                oR.select();  
	            } 
	            else if(rangeData.bookmark !== undefined) {
	                oR.moveToBookmark(rangeData.bookmark);
	                oR.select();  
	            }  
	            else
	            {
		            oR.collapse(true);  
		            oR.moveEnd('character', rangeData.start); 
		            oR.moveStart('character', rangeData.end);  
		            oR.select();
	            }
	        }  
		}
        this.cursorPosition.insert = function (rangeData, text, offsetFocus) {  
			var textarea = editor.textarea[0];
            var oValue, nValue, oR, sR, nStart, nEnd, st;  
            this.set(rangeData);  

            if (textarea.setSelectionRange) { // W3C  
                oValue = textarea.value;  
                nValue = oValue.substring(0, rangeData.start) + text + oValue.substring(rangeData.end);  
                nStart = nEnd = rangeData.start + text.length;  
                st = textarea.scrollTop;  
                textarea.value = nValue;  
                // Fixbug:  
                // After textarea.values = nValue, scrollTop value to 0  
                if (textarea.scrollTop != st) {  
                    textarea.scrollTop = st;  
                }
                nStart += offsetFocus;
                nEnd += offsetFocus;
                textarea.setSelectionRange(nStart, nEnd);  
            } else if (textarea.createTextRange) { // IE  
                sR = document.selection.createRange();  
                sR.text = text;  
                sR.setEndPoint('StartToEnd', sR);
	            if(offsetFocus)
	            {
	            	sR.collapse(true);
	            	sR.moveStart('character', offsetFocus); 
	            	sR.moveEnd('character', offsetFocus); 
	            }
                sR.select();  
            }  
        }  

		this.cmd.bold = function(){
			this.common("**", "**")
		}
		this.cmd.italic = function(){
			this.common("_", "_")
		}
		this.cmd.quote = function(){
			this.common(">", "", { eachline : true })
		}
		this.cmd.head3 = function(){
			this.common("###", "")
		}
		this.cmd.link = function(){
    		var link = prompt( "Link to URL", "http://");
    		if(!link) return;
    		if(editor.cursorPosition.get().text.length > 0)
    		{
    			this.common("[", "](" + link + ")",  { clearBR : true });
			}
			else
			{
				this.common("<", link + ">",  { clearBR : true });
			}
		}
		this.cmd.ul = function(){
			this.common("- ", "")
		}
		this.cmd.ol = function(){
			this.common("0. ", "")
		}
		this.cmd.picture = function(url){
			if(url == undefined)
			{
				url = prompt( "图片地址", "http://" );
			}
			url && this.common("![", "](" + url + ")", { rule : 'replace' });
			//![](/path/to/img.jpg "Optional title")
		}
		this.cmd.textareaChange = function(){

			var value = editor.textarea.val();
			value = markdown.toHTML( value );
			editor.preview.find(".editor-preview-body").html(value);
		}
		this.cmd.previewToggle = function(){
			editor.preview.toggleClass("active");
		}


		/**
		 * 绑定事件
		 */
		this.bindEvents.setup = function(){
			if(editor.settings['previewBodyClass'])
			{
				editor.preview.find(".editor-preview-body").addClass(editor.settings['previewBodyClass'])
			}
		}

		this.bindEvents.textareaKeyup = function(){
			editor.textarea.keyup(editor.cmd.textareaChange);
			editor.textarea.keyup(function(e){
				if(e.keyCode == 13)
				{
					var lines = editor.textarea.val().split("\n");
					var lineTotal = lines.length;

					if(lineTotal > 1)
					{
						var linePrefix = /^\*\s+|^\-\s+|^_\s+|^[0-9]+\.\s+/.exec(lines[lineTotal-2]);
						if(linePrefix)
						{
							linePrefix = linePrefix[0];
							editor.cmd.common(linePrefix, "", { });
						}
					}
					return true;
				}
			});
		}

		this.bindEvents.previewToggleClick = function(){
			//alert(editor.textarea);
			editor.preview.find(".editor-preview-toggle").click(editor.cmd.previewToggle)

		}

		this.bindEvents.toolbarButtonClick = function(){
			editor.toolbar.find("li").click(function(){

				var cmdName = $(this).attr("class").replace("editor-toolbar-button-", "");
				if( cmdName in editor.cmd )
				{
					(editor.cmd[cmdName])();
				}

				editor.cmd.textareaChange();

			})
		}



		this._init(settings);
 	}

/*
	var editorFactory = {};
	editorFactory.create = function(settings)
	{
		return new Editor(settings);
	}
	window[editorName] = editorFactory;
*/
     
	jQuery.fn[editorName] = function(settings) {
		var editors = [];
		this.each(function(){
			if($(this)[0][editorName])
			{
				editors.push($(this)[0][editorName]);
			}
			else
			{
				var _settings = jQuery.extend({ textarea : $(this) }, settings, { previewBodyClass : 'editor-preview-body-default-style' });
				editors.push(new Editor(_settings));
			}
		})
		return editors;
	};


})('markDownEditor');
