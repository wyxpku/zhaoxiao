$(".reviewform").submit(function(event) {
    // event.preventDefault();
    var flag = true;
    // var overall_rating = $("#overall_rating").val();
    if ($("#overall_rating").val() == -1) {
        $("#overall_rating").parent().addClass("has-danger");
        flag = false;
    } else {
        $("#overall_rating").parent().removeClass("has-danger");
    }

    if ($("#academic_rating").val() == -1) {
        $("#academic_rating").parent().addClass("has-danger");
        flag = false;
    } else {
        $("#academic_rating").parent().removeClass("has-danger");
    }

    if ($("#campus_rating").val() == -1) {
        $("#campus_rating").parent().addClass("has-danger");
        flag = false;
    } else {
        $("#campus_rating").parent().removeClass("has-danger");
    }

    if ($("#dining_rating").val() == -1) {
        $("#dining_rating").parent().addClass("has-danger");
        flag = false;
    } else {
        $("#dining_rating").parent().removeClass("has-danger");
    }
    if ($("#dorm_rating").val() == -1) {
        $("#dorm_rating").parent().addClass("has-danger");
        flag = false;
    } else {
        $("#dorm_rating").parent().removeClass("has-danger");
    }
    if ($("#administration_rating").val() == -1) {
        $("#administration_rating").parent().addClass("has-danger");
        flag = false;
    } else {
        $("#administration_rating").parent().removeClass("has-danger");
    }
    if ($("#facility_rating").val() == -1) {
        $("#facility_rating").parent().addClass("has-danger");
        flag = false;
    } else {
        $("#facility_rating").parent().removeClass("has-danger");
    }
    if ($("#organization_rating").val() == -1) {
        $("#organization_rating").parent().addClass("has-danger");
        flag = false;
    } else {
        $("#organization_rating").parent().removeClass("has-danger");
    }
    if ($("#location_rating").val() == -1) {
        $("#location_rating").parent().addClass("has-danger");
        flag = false;
    } else {
        $("#location_rating").parent().removeClass("has-danger");
    }
    if ($("#reviewer_relationship").val() == -1) {
        $("#reviewer_relationship").parent().addClass("has-danger");
        flag = false;
    } else {
        $("#reviewer_relationship").parent().removeClass("has-danger");
    }
    if ($("#reviewer_major").val() == "") {
        $("#reviewer_major").parent().addClass("has-danger");
        flag = false;
    } else {
        $("#reviewer_major").parent().removeClass("has-danger");
    }
    if ($("#review_content").val().length < 50) {
        $("#review_content").parent().addClass("has-danger");
        flag = false;
    } else {
        $("#review_content").parent().removeClass("has-danger");
    }
    console.log(flag);
    if (flag) return true;
    else {
        $('html, body').animate({ scrollTop: 0 }, 'slow');
        return false;
    }

})

$("#review_content").bind("input propertychange", function(){
	console.log("hello");
	var curlen = $("#review_content").val().length;
	console.log(curlen);
	$(".content-count").html("现 " + $("#review_content").val().length + " 字，不少于50字");
});
