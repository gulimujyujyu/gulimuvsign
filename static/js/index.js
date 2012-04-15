/**
 * Created with PyCharm.
 * User: xlzhu
 * Date: 12-4-15
 * Time: 下午9:21
 * To change this template use File | Settings | File Templates.
 */

var Globals = {
    "author": 'xlzhu',
    "version_major": 0,
    "version_minor": 1,
    "central_map_options": {
        center: new google.maps.LatLng(-34.397, 150.644),
        zoom: 8,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
};

$(document).ready(function(){
    //initial google map
    var map = new google.maps.Map(document.getElementById("central_map_canvas"), Globals.central_map_options);
});