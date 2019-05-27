//json-genarator.com for mock data
$.get("https://next.json-generator.com/api/json/get/V1cGoKmDV", function(data){
    console.log(data);
    // use a data source with 'id' and 'name' keys
    $("#query").typeahead({ source:data });
},'json');
