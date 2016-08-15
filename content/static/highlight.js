        $(function() {
            // let's init the plugin, that we called "highlight".
            // We will highlight the words "hello" and "world", 
            // and set the input area to a widht and height of 500 and 250 respectively.
            $("#container0").highlight({
                words:  [["hello","hello"],["world","world"],["(\\[b])(.+?)(\\[/b])","$1$2$3"]],
                width:  500,
                height: 125,
        count:0
            });
            $("#container1").highlight({
                words:  [["hello","hello"],["world","world"],["(\\[b])(.+?)(\\[/b])","$1$2$3"]],
                width:  500,
                height: 125,
        count: 1
            });
        });

        // the plugin that would do the trick
        (function($){
            $.fn.extend({
                highlight: function() {
                    // the main class
                    var pluginClass = function() {};
                    // init the class
                    // Bootloader
                    pluginClass.prototype.__init = function (element) {
                        try {
                            this.element = element;
                        } catch (err) {
                            this.error(err);
                        }
                    };
                    // centralized error handler
                    pluginClass.prototype.error = function (e) {
                        // manage error and exceptions here
                        //console.info("error!",e);
                    };
                    // Centralized routing function
                    pluginClass.prototype.execute = function (fn, options) {
                        try {
                            options = $.extend({},options);
                            if (typeof(this[fn]) == "function") {
                                var output = this[fn].apply(this, [options]);
                            } else {
                                this.error("undefined_function");
                            }
                        } catch (err) {
                            this.error(err);
                        }
                    };
                    // **********************
                    // Plugin Class starts here
                    // **********************
                    // init the component
                    pluginClass.prototype.init = function (options) {
                        try {
                            // the element's reference ( $("#container") ) is stored into "this.element"
                            var scope                   = this;
                            this.options                = options;

                            // just find the different elements we'll need

                            this.highlighterContainer   = this.element.find('#highlighterContainer'+this.options.count);
                            this.inputContainer         = this.element.find('#inputContainer'+this.options.count);
                            this.textarea               = this.inputContainer.find('textarea');
                            this.highlighter            = this.highlighterContainer.find('#highlighter'+this.options.count);

                            // apply the css
                            this.element.css({'position':'relative',
                'overflow':'auto',
                'background':'none repeat scroll 0 0 #FFFFFF',
                'height':this.options.height+2,
                'width':this.options.width+19,
                'border':'1px solid'
                });

                            // place both the highlight container and the textarea container
                            // on the same coordonate to superpose them.
                            this.highlighterContainer.css({
                                'position':         'absolute',
                                'left':             '0',
                                'top':              '0',
                                'border':           '1px dashed #ff0000', 
                                'width':            this.options.width,
                                'height':           this.options.height,
                                'cursor':           'text',
                'z-index':      '1'
                            });
                            this.inputContainer.css({
                                'position':         'absolute',
                                'left':             '0',
                                'top':              '0',
                                'border':           '0px solid #000000',
                'z-index':      '2',
                'background':   'none repeat scroll 0 0 transparent'
                            });
                            // now let's make sure the highlit div and the textarea will superpose,
                            // by applying the same font size and stuffs.
                            // the highlighter must have a white text so it will be invisible
            var isWebKit = navigator.userAgent.indexOf("WebKit") > -1,
            isOpera = navigator.userAgent.indexOf("Opera") > -1,
isIE /*@cc_on = true @*/,
isIE6 = isIE && !window.XMLHttpRequest; // Despite the variable name, this means if IE lower than v7

if (isIE || isOpera){
var padding = '6px 5px';
}
else {
var padding = '5px 6px';
}
                           this.highlighter.css({
                                'padding':      padding,
                                'color':            '#eeeeee',
                                'background-color': '#ffffff',
                                'margin':           '0px',
                                'font-size':        '11px' ,
                                'line-height':      '12px' ,
                                'font-family':      '"lucida grande",tahoma,verdana,arial,sans-serif'
                            });

                            // the textarea must have a transparent background so we can see the highlight div behind it
                            this.textarea.css({
                                'background-color': 'transparent',
                                'padding':          '5px',
                                'margin':           '0px',
                                'width':            this.options.width,
                                'height':           this.options.height,
                                'font-size':        '11px',
                                'line-height':      '12px' ,
                                'font-family':      '"lucida grande",tahoma,verdana,arial,sans-serif',
                'overflow':     'hidden',
                                'border':           '0px solid #000000'
                            });

                            // apply the hooks
                            this.highlighterContainer.bind('click', function() {
                                scope.textarea.focus();
                            });
                            this.textarea.bind('keyup', function() {
                                // when we type in the textarea, 
                                // we want the text to be processed and re-injected into the div behind it.
                                scope.applyText($(this).val());
                            });

            scope.applyText(this.textarea.val());

                        } catch (err) {
            this.error(err)
                        }
                        return true;
                    };
                    pluginClass.prototype.applyText = function (text) {
                        try {
                            var scope                   = this;

                            // parse the text:
                            // replace all the line braks by <br/>, and all the double spaces by the html version &nbsp;
                            text = this.replaceAll(text,'\n','<br/>');
                            text = this.replaceAll(text,'  ','&nbsp;&nbsp;');
                            text = this.replaceAll(text,' ','&nbsp;');

                            // replace the words by a highlighted version of the words
                            for (var i=0;i<this.options.words.length;i++) {
                                text = this.replaceAll(text,this.options.words[i][0],'<span style="background-color: #D8DFEA;">'+this.options.words[i][1]+'</span>');
                                //text = this.replaceAll(text,'(\\[b])(.+?)(\\[/b])','<span style="font-weight:bold;background-color: #D8DFEA;">$1$2$3</span>');
                            }

                            // re-inject the processed text into the div
                            this.highlighter.html(text);
            if (this.highlighter[0].clientHeight > this.options.height) {
                // document.getElementById("highlighter0")
                this.textarea[0].style.height=this.highlighter[0].clientHeight +19+"px";
            }
            else {
                this.textarea[0].style.height=this.options.height;
            }

                        } catch (err) {
                            this.error(err);
                        }
                        return true;
                    };
                    // "replace all" function
                    pluginClass.prototype.replaceAll = function(txt, replace, with_this) {
                        return txt.replace(new RegExp(replace, 'g'),with_this);
                    }

                    // don't worry about this part, it's just the required code for the plugin to hadle the methods and stuffs. Not relevant here.
                    //**********************
                    // process
                    var fn;
                    var options;
                    if (arguments.length == 0) {
                        fn = "init";
                        options = {};
                    } else if (arguments.length == 1 && typeof(arguments[0]) == 'object') {
                        fn = "init";
                        options = $.extend({},arguments[0]);
                    } else {
                        fn = arguments[0];
                        options = $.extend({},arguments[1]);
                    }

                    $.each(this, function(idx, item) {
                        // if the component is not yet existing, create it.
                        if ($(item).data('highlightPlugin') == null) {
                            $(item).data('highlightPlugin', new pluginClass());
                            $(item).data('highlightPlugin').__init($(item));
                        }
                        $(item).data('highlightPlugin').execute(fn, options);
                    });
                    return this;
                }
            });

        })(jQuery);
