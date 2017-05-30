var bsSearch_nav = $("input#nav_search").bsSuggest({
    allowNoKeyword: false,
    multiWord: true,
    separator: ",",
    getDataMethod: "url",
    url: '/autocomplete/?q=',
    // jsonp: 'cb',
    showBtn: false,
    fnProcessData: function(json) {
        console.log(json);
        var index, len, data = {
            value: []
        };
        len = json.length;

        if (!json || json.length === 0) {
            return false;
        }
        if (len >= 10)
            len = 10;
        for (index = 0; index < len; index++) {
            // console.log(index);
            data.value.push({
                word: json[index].fields.name
            });
        }
        console.log(data);
        return data;
    }
}).on('onDataRequestSuccess', function(e, result) {
    // console.log('onDataRequestSuccess: ', result);
}).on('onSetSelectValue', function(e, keyword, data) {
    // console.log('onSetSelectValue: ', keyword, data);
}).on('onUnsetSelectValue', function() {
    // console.log("onUnsetSelectValue");
});

var bsSearch_main = $("input#main-search").bsSuggest({
    allowNoKeyword: false,
    multiWord: true,
    separator: ",",
    getDataMethod: "url",
    url: '/autocomplete/?q=',
    // jsonp: 'cb',
    showBtn: false,
    fnProcessData: function(json) {
        console.log(json);
        var index, len, data = {
            value: []
        };
        len = json.length;

        if (!json || json.length === 0) {
            return false;
        }
        if (len >= 10)
            len = 10;
        for (index = 0; index < len; index++) {
            // console.log(index);
            data.value.push({
                word: json[index].fields.name
            });
        }
        console.log(data);
        return data;
    }
}).on('onDataRequestSuccess', function(e, result) {
    // console.log('onDataRequestSuccess: ', result);
}).on('onSetSelectValue', function(e, keyword, data) {
    // console.log('onSetSelectValue: ', keyword, data);
}).on('onUnsetSelectValue', function() {
    // console.log("onUnsetSelectValue");
});
particlesJS.load('particles-js', '/static/particlesjs-config.json', function() {
    console.log('callback - particles.js config loaded');
});

window.onload = function() {
    var wh = $(document).height();
    var ww = $(document).width();
    $(".main-container").css("min-height", wh - 90);
};
