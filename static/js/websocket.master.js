/**
 * Created by hatsukiotowa on 2016/8/12.
 */
$(window).keyup('hashchange', function() {
    var tab= location.hash;
    console.log(location.hash);
    websocket.send(JSON.stringify({'tab' : tab}));
});