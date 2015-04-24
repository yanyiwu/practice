/* $.jsonView() 0.1 - jQuery-based Json to html pretty printer
 *
 * Copyright (c) 2010 Francois Lafortune  (quickredfox.at)
 * Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php 
 *
 * Example: 
 *  <html><head>
 * 	<link rel="stylesheet" href="jsonview.jquery.css" type="text/css" />
 *	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.0/jquery.min.js" type="text/javascript"></script>
 *	<script src="jquery.jsonview.js" type="text/javascript"></script>
 *  <script type="text/javascript" charset="utf-8">
 *  	// wait for document ready
 *  	$(function(){
 *  		// load some json data
 *  		$.getJSON('data.json',function(json){
 *  			// inject contents in document body
 *  			$(document.body).jsonView(json);
 *  		})
 *  	});
 *  </script></head><body></body></html>
*/

(function(){
	// the JQUERY plguin.
	$.fn.jsonView=function(jsonData){
		var $this = $(this);
		var treeHTML  = "<div class=\"jquery-jsonview\">"+json2markup(jsonData)+"</div>";
		return $this.html(treeHTML);
	}		
	// the ACTUAL plugin
	var json2markup = function(json,lvl){
		var markup = [],lvl = (lvl+1)||0;
		if(typeof json == 'object' && json instanceof Array){
			// handle array
			if(json.length == 0) markup.push('<div class="empty-array-wrapper lvl-"'+lvl+'">[ ]</div>');
			else{
				markup.push('<div class="array-wrapper lvl-'+lvl+'"><ol title="Array with '+json.length+' items" class="array-item-list">');
				// if empty
				for(var i=0,item;item = json[i++];) markup.push('<li class="array-item"><a href="#" class="list-toggle-button">[-]</a>'+(typeof item == 'string' || typeof item == 'number' ? '<p class="string-value">'+item+'</p>' : json2markup(item,lvl))+'</li>');
				markup.push('</ol></div>');
			}
		}else if(typeof json == 'object'){
			// handle real object			
			markup.push('<div class="object-wrapper lvl-'+lvl+'"><ul class="object-property-list">');
			var ml = markup.length
			for(var k in json){
				markup.push('<li class="object-property"><dl class="property-definition"><dt class="property-name">'+k+':<a href="#" class="property-toggle-button">[-]</a></dt><dd class="property-value">'+json2markup(json[k],lvl)+'</dd></dl></li>')
			};
			if(markup.length == ml){
			  // rewind
			  markup.shift();
			  markup.push('<div class="empty-object-wrapper lvl-'+lvl+'">');
			}else markup.push('</ul>');
			markup.push('</div>');			
		}else if(json){
			// handle string
			json = $('<div/>').text(json).html();
			markup.push('<p class="string-value">'+json+'</p>');
		}else if(typeof json === 'number'){
			// handle numbers
			markup.push('<p class="string-value">'+json.toString()+'</p>');
		}else{ 
		
			// handle null
			markup.push('<p class="null-value">null</p>');
		}
		return markup.join('');
	}
	
	/** folder, un-folder array */
	$('.list-toggle-button').live('click', function(e){
		e.preventDefault();e.stopPropagation();
		var $this = $(this);
		if(!$this.data('li')){
			$this.data('li', $this.parents('li').first());
			$this.data('div', $this.data('li').children('div'));
			var type = 	($this.data('li').find('> .array-wrapper').length > 0 ? 'array' : $this.data('li').find('> .object-wrapper').length > 0 ? 'object' : 'string');				
			$this.data('type', type);
		}
		
		if(!$this.data('div').length){$this.text(''); return;} /** array of number, string does not need folder or unfolder */
		//toggle
		if($this.data('div').is(':visible')){
			$this.text('[+]');	
			$this.data('div').hide(0,function(){
				$this.data('li').addClass('closed-'+$this.data('type'));
			});	
		}else{
			$this.text('[-]');
			$this.data('div').show(0,function(){
				$this.data('li').removeClass('closed-'+$this.data('type'));
			});
		} 
	});
	
	// only register this once... will work everywhere
	$('.property-toggle-button').live('click',function(e){
		e.preventDefault();e.stopPropagation();
		var $this = $(this);
		// first time acces this element, store relationships 			
		if(!$this.data('dt')){
			$this.data('dt',$this.parents('dt'));
			$this.data('dd',$this.data('dt').next('dd'));
			var type = 	($this.data('dd').find('> .array-wrapper').length > 0 ? 'array' : $this.data('dd').find('> .object-wrapper').length > 0 ? 'object' : 'string');				
			$this.data('type', type);
		}
		// toggle
		if($this.data('dd').is(':visible')){
			$this.text('[+]');	
			$this.data('dd').hide(0,function(){
				$this.data('dt').addClass('closed-'+$this.data('type'))									
			});	
		}else{
			$this.text('[-]');
			$this.data('dd').show(0,function(){
				$this.data('dt').removeClass('closed-'+$this.data('type'))										
			});
		} 
	});
})();