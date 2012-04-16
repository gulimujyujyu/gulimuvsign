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
        zoom: 10,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
};

$(document).ready(function(){
    //initial google map
    var map = new google.maps.Map(document.getElementById("map_indicator"), Globals.central_map_options);
    var marker = new google.maps.Marker({
        position: Globals.central_map_options.center,
        map: map,
        title: "You are here."
    });

    //add get geolocation support
    var browser_support_flag = false;

    var HandleNoGeoLocation = function(flag){
        alert(flag);
    };

    $('button#locator').click(function(e){

        if(navigator.geolocation) {
            browser_support_flag = true;
            navigator.geolocation.getCurrentPosition(function(position) {
                console.log(position);
                console.log(position.coords.latitude+","+position.coords.longitude);
                $('input#input_lat').val(position.coords.latitude);
                $('input#input_lon').val(position.coords.longitude);
                var current_location = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
                map.setCenter(current_location);
                marker.setPosition(current_location);
            }, function() {
                HandleNoGeoLocation(browser_support_flag);
            });
            // Try Google Gears Geolocation
        } else if (google.gears) {
            browser_support_flag = true;
            var geo = google.gears.factory.create('beta.geolocation');
            geo.getCurrentPosition(function(position) {
                console.log(position);
                $('input#input_lat').value(position.latitude);
                $('input#input_lon').value(position.longitude);
                var current_location = new google.maps.LatLng(position.latitude,position.longitude);
                map.setCenter(current_location);
                marker.setPosition(current_location);
            }, function() {
                HandleNoGeoLocation(browser_support_flag);
            });
            // Browser doesn't support Geolocation
        } else {
            browser_support_flag = false;
            HandleNoGeoLocation(browser_support_flag);
        }
    });

    $('div#image_upload_modal').modal();
    $('div#image_upload_modal').modal('hide');

    $("button#upload_image").click(function(){
        console.log("button#upload_image is fired");
        $('div#image_upload_modal').modal('show');
    });

    $("a#change_a_new_image").click(function(){
        console.log("button#upload_image is fired");
        $('div#image_upload_modal').modal('show');
    });

    $("button#image_upload_form_cancel").click(function(){
        $('div#image_upload_modal').modal('hide');
    });

});