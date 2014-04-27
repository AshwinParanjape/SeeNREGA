$( ".stateAccordion" ).accordion({header: "li.stateName", heightStyle: "content", collapsible:"true", active: false});
$( ".districtAccordion" ).accordion({header: "li.districtName", heightStyle: "content", collapsible: "true", active: false});
$( ".blockAccordion" ).accordion({header: "li.blockName", heightStyle: "content", collapsible: "true", active: false,
	beforeActivate: function(event, ui){
		console.log('der der');
		var that = ui.newHeader;
		jQuery.ajax({
			url: 'panchayatList/'+that.siblings('input').attr('value')+'/'}).done(function(server_data,text_status,jqXHR){
				var newul = that.next('ul');
				for(code in server_data){
					newul.append('<input class="panchayat-checkbox adm-checkbox" type="checkbox" value="'+code+'"/><li class="panchayatName">'+server_data[code]+ '</li></br>');
				}

			});
	}
});
$( ".indicatorAccordion" ).accordion({header: "h4", heightStyle: "content", collapsible: "true", active: false, icons: { "header": "ui-icon-plus", "activeHeader": "ui-icon-minus" } });
$('.indicator-unit>h5, .indicator-unit li').prepend('<input type="checkbox">');
$('#chart-selector>.thumbnail>.caption>p').each(function(){
	$(this).prepend('<input type="radio" name="chart" value='+$(this).parents('.thumbnail').attr('id')+'>&nbsp;');
});
$('.indicator-unit>h5').change(function(){
	checkboxes = $(this).next('.checkbox-group').find('input');
	for(var i=0, n=checkboxes.length;i<n;i++) {
		checkboxes[i].checked = $(this).children('input').prop("checked");
	}
});
//get panchayat names using ajax
/*$('.blockName').one('click',function(){

	var that = $(this)
	jQuery.ajax({
		url: 'panchayatList/'+that.siblings('input').attr('value')+'/'}).done(function(server_data,text_status,jqXHR){
			that.after($('<ul class="panchayatAccordion"></ul>'));
			var newul = that.next('ul.panchayatAccordion');
			for(code in server_data){
				newul.append('<input class="panchayat-checkbox adm-checkbox" type="checkbox" value='+code+'/><li class="panchayatName">'+server_data[code]+ '</li></br>');
			}
			newul.accordion({header: that, heightStyle: "content", collapsible: "true", active: true});

		});
	//add fail and always
});*/
//properties about the current selection for summarization
time_series = false;
geo_series = false;
single_measure = true;
nested_series = false;
multiple_measure = false;
data_series1=null;
data_series2=null;
//look at the id string for thumbnails and convert it into highcharts JSON format
function get_chart(thumbString){
	strs = thumbString.split("-");
	var stacked = null;
	chart = strs[0]
	if(strs.indexOf("percentage")>-1){
		stacked = "percentage";
	}
	else if(strs.indexOf("stacked")>-1){
		stacked = "normal";
	}
	chartDict={
		chart: {
			type: chart
		},
		plotOptions:{
			chart:{
				stacking: stacked
			}
		}
	}
	return chartDict;
}

//find out if multiple checkboxes are selected and take it as a dimention in the chart
$('.indicator-unit').change(function(){
	checkboxes = $(this).find('.checkbox-group input');
	boxesChecked=0;
	for(var i=0, n=checkboxes.length;i<n;i++) {
		if(checkboxes[i].checked){
			boxesChecked++;
		}
	}
	if(boxesChecked>1){
		var new_data_series=$(this).attr('id');
		
		if(!(data_series1 == new_data_series || data_series2 == new_data_series)){
			if(data_series1==null){
				data_series1= new_data_series;
				/*data_series1=[];
				  for(var i=0, n=checkboxes.length;i<n;i++) {
				  if(checkboxes[i].checked){
				  data_series1.push(checkboxes[i]);
				  }
				  boxesChecked++;
				  }
				  console.log(data_series1);*/
			}else if(data_series2==null){
				data_series2=$(this).attr('id');
				nested_series = check_nestedness(data_series1,data_series2);
			}
			else{
				refreshInfo();
				generate_alert("More than 2 series cannot be selected at time. Discarding this series");
			}
		}
	}
	else{
		if(data_series1 == $(this).attr('id')){
			data_series1 = null;
		}
		if(data_series2 == $(this).attr('id')){
			data_series2 = null;
		}
	}
		
	refresh();
});


//relations in dimentions which are nested in one another, ie can be pivoted along any dimention
nestedRelations = [["measure", "progress"],["measure","type"],["progress", "type"],];
function check_nestedness(type1 , type2){
	//expects two strings and return the appropriate compatibility of the two classes
	/*if(type1 == "measure" || type1 =="unit"){
		multiple_measure = true;
	}*/
	for(i=0;i<nestedRelations.length;i++){
		if((type1 == nestedRelations[i][0] && type2 == nestedRelations[i][1])|| (type1==nestedRelations[i][1] && type2 == nestedRelations[i][0])){
			return true;
		}
	}
}
exclusiveRelations = [["gender", "category"],];
function check_exclusivity(type1, type2){
	for(i=0;i<exclusiveRelations.length;i++){
		if((type1 == exclusiveRelations[i][0] && type2 == exclusiveRelations[i][1])|| (type1==exclusiveRelations[i][1] && type2 == exclusiveRelations[i][0])){
			return true;
		}
	}
}


//initialize year slider
$( "#year-slider" ).slider({
	range: false,
	min: 2006, 
	max: 2013,
	value: 2012,
	slide: function( event, ui ) {
		$( "#year-range" ).val( ui.value );
	}
});
$( "#year-range" ).val( $( "#year-slider" ).slider( "values", 0 ) );

//reinitialize year slider depending on whether year range is required
$('#range-check').change(function(){
	if(this.checked){
		$( "#year-slider" ).slider("destroy");
		$( "#year-slider" ).slider({
			range: true,
			min: 2006,
			max: 2013,
			values: [ 2010, 2013 ],
			slide: function( event, ui ) {
				$( "#year-range" ).val( + ui.values[ 0 ] + "-"+ ui.values[ 1 ] );
			}
		});
		$( "#year-range" ).val( $( "#year-slider" ).slider( "values", 0 ) +"-"+ $( "#year-slider" ).slider( "values", 1 ) );
		time_series=true;
		refresh();
	}
	else{
		$( "#year-slider" ).slider("destroy");
		$( "#year-slider" ).slider({
			range: false,
			min: 2006, 
			max: 2013,
			value: 2012,
			slide: function( event, ui ) {
				$( "#year-range" ).val( ui.value );
			}
		});
		$( "#year-range" ).val( $( "#year-slider" ).slider( "values", 0 ) );
		time_series=false;
		refresh();
	}
});

//different kinds of possible charts for different purposes
charts=["line","stacked-area","percentage-area","bar","stacked-bar","column","stacked-column", "stacked-percentage-column", "pie", "donut"];
time_series_charts = ["line","stacked-area","percentage-area"];
single_measure_charts = ["bar","stacked-bar","column","stacked-column", "stacked-percentage-column", "pie", "donut"];
multiple_measure_charts = ["line","bar","column"];
nested_series_charts = ["bar","stacked-bar","column","stacked-column", "stacked-percentage-column",  "donut"];

//refresh after options are changed to check compatibility and corresponding updates
function refresh(){
	if(time_series==true){
		for(i=0;i<charts.length;i++){
			$('#'+charts[i]+'-thumb').addClass("disabled-chart");
		}
		for(i=0;i<time_series_charts.length;i++){
			$('#'+time_series_charts[i]+'-thumb').removeClass("disabled-chart");
		}
	}
	else if(geo_series){

	}
	else if(single_measure){
		for(i=0;i<charts.length;i++){
			$('#'+charts[i]+'-thumb').addClass("disabled-chart");
		}
		if(nested_series){
			for(i=0;i<nested_series_charts.length;i++){
				$('#'+nested_series_charts[i]+'-thumb').removeClass("disabled-chart");
			}
		}else{

			for(i=0;i<single_measure_charts.length;i++){
				$('#'+single_measure_charts[i]+'-thumb').removeClass("disabled-chart");
			}
		}
	}
	else if(multiple_measure){
		for(i=0;i<charts.length;i++){
			$('#'+charts[i]+'-thumb').addClass("disabled-chart");
		}
		for(i=0;i<multiple_measure_charts.length;i++){
			$('#'+multiple_measure_charts[i]+'-thumb').removeClass("disabled-chart");
		}
	}
	refreshInfo();
}
function refreshInfo(){
	if(data_series1!=null){
		s1attr = $('#'+data_series1).find('.checkbox-group').find('input:checked').parents('li').map(function(i,e){ return $(e).text();}).toArray();
		$('#series1Info').text('Series 1: '+data_series1+' = ['+s1attr+']');
	}
	else{
		s1attr=null;
	}
	if(data_series2!=null){
		s2attr = $('#'+data_series2).find('.checkbox-group').find('input:checked').parents('li').map(function(i,e){ return $(e).text();}).toArray();
		$('#series2Info').text('Series 2: '+data_series2+' = ['+s2attr+']');
	}
	else{
		s2attr=null;
	}
}


//Alerts mechanism 
var noAlert = true;
var proceed = true;
function generate_alert(message){
	if($('#generate-alert').length>0){
		$('#generate-alert').removeClass('no-alert');
		$('#generate-alert').text(message);
	}
	noAlert = false;
}
function get_adm_level(inputCheckboxClass){
	//expects a jquery object for an input checkbox
	if(inputCheckboxClass.hasClass('state-checkbox'))
		return 'state';
	if(inputCheckboxClass.hasClass('district-checkbox'))
		return 'district';
	if(inputCheckboxClass.hasClass('block-checkbox'))
		return 'block';
	if(inputCheckboxClass.hasClass('panchayat-checkbox'))
		return 'panchayat';
}

//Generate!
$('#generate-button').click(function(){
	//tests
		
	charting = true;
	noAlert = true;
	proceed = true;
	chartString = $('input[name="chart"]:checked').attr('value');
	if( chartString == undefined){
		generate_alert("Chart Not Selected: Only Table will be generated");
		charting = false
	}

	if(noAlert){
		$('#generate-alert').addClass('no-alert');
	}

	if(data_series1 == null){
		generate_alert("No series selected");
		return -1;
	}
	
	yAxisIndicatorGroup = $('#'+data_series1).siblings('.y-axis');
	if(yAxisIndicatorGroup.length>0){
	//if no y-axis indicator group is checked return error
		if(yAxisIndicatorGroup.find('input:checked').length < 1){
			generate_alert("Select one "+yAxisIndicatorGroup.attr('id')+" for reporting");
			return -1;
		}

		//swap data series so that different series have different axes in case of multi axis
		if(data_series1 == yAxisIndicatorGroup.attr('id')){
			var temp = data_series1;
			data_series1 = data_series2;
			data_series2 = temp;
		}
		//list of axes (which can contain single element too
		yAxisList = yAxisIndicatorGroup.find('.checkbox-group').find('input:checked').parents('li').map(function(i,e){ return $(e).text();}).toArray();
	}

	//filters are defined by singleton elements selected in each indicator group corresponding to the current table
	filtersList = $('#'+data_series1).siblings('.indicator-unit')
		.map(function(i,e){
			if($(e).find('.checkbox-group').find('input:checked').length==1){			
				if(check_exclusivity($('#'+data_series1).attr('id'),$(e).attr('id'))){
					generate_alert($('#'+data_series1).attr('id')+","+$(e).attr('id')+"are exclusive relations and cannot by applied together");
					proceed = false;
				}
				return $(e).attr('id')+":"+$(e).find('.checkbox-group').find('input:checked').parents('li').text();
			}
		}).toArray();
		console.log(filtersList)

	if(!proceed)
		return -1;

	

	if($('input.adm-checkbox:checked').length==0){

		generate_alert('No administrative area selected. Please select one')
		proceed = false;
		return -1;
	}
	console.log(data_series2);
	jQuery.ajax({
		url: 'dataretrive/',
		data: {
		admLevel: get_adm_level($('.adm-checkbox:checked').first()),
		code: $('.adm-checkbox:checked').first().attr('value'),
		table: $('#'+data_series1).parents('.data-cat').attr('id'),
		s1: data_series1,
		s1a: s1attr,
		s2: data_series2,
		s2a: s2attr ,
		filters: filtersList
		}
	}).done(function(server_data, textStatus, jqXHR){
		if(charting){
			chartDict = get_chart(chartString);
			$.extend(chartDict, { 
				title: {
					//text: 'Monthly Average Temperature',
				},
				subtitle: {
					//text: 'Source: WorldClimate.com',
				},
				xAxis: {
					categories: s1attr
				},
				yAxis: {
					title: {
						//text: 'Temperature (°C)'
					},
				plotLines: [{
					value: 0,
				width: 1,
				color: '#808080'
				}]
				},
			legend: {
				layout: 'vertical',
				align: 'right',
				verticalAlign: 'middle',
				borderWidth: 0
			},
				series: server_data 
			}
			);

			$('#chart').highcharts(chartDict);
		}
		console.log(server_data);
		});

	//add fail and always
});
refresh();
$(function () {
});

