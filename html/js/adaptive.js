$(function() {
    viewport = document.querySelector("meta[name=viewport]");
    if (viewport != null) {
        var intendedWidth = 962;
        var windowWidth = window.screen.width;
        var scale = (windowWidth / intendedWidth).toFixed(3);
        init_str = "initial-scale=".concat(scale.toString());
        min_str = "minimum-scale=".concat(scale.toString());
        max_str = "maximum-scale=".concat(scale.toString());
        viewport.setAttribute("content", init_str.concat(",").concat(min_str).concat(",").concat(max_str));
    }
});

    // Pre Document Ready
$(document).ready(function() {
    //This makes the Pages work from anywhere - use http://198.18.0.1/apps/appname while on the robot
    var host = window.location.hostname;
    var session = new QiSession(function(session) {
        console.log("connected");
    }, console.log("disconnected"), host);
    var selectedPic
    var questionName = ""
    session.service("ALMemory").then(function(memory) {
        //Events
        memory.getData("MemG/selectedPerson").then(function (data) {
          $("#Family h1").text("Can you find a picture of " + data + "?");
          });

        $("body").click(function() {
            memory.raiseEvent("PepperTablet/Interaction", "Touch");
        });
        $("input").keyup(function() {
            memory.raiseEvent("PepperTablet/Interaction", "Keyboard Key");
        });
        $("#resetBtn").click(function() {
            memory.raiseEvent("PepperTablet/Reset", "Reset");
        });
        $("div[data-fireEvent]").click(function() {
            var personName = $(this).attr("data-item").toString()
            memory.raiseEvent($(this).attr("data-fireEvent").toString(), personName);
            selectedPic =  personName
        });
        $("#Employees").on('click', '.item', function() {
            memory.raiseEvent("ERReceptionist/AppointmentWith", $(this).attr("data-name").toString());
        });
        memory.subscriber("TabletView").then(function(subscriber) {
            subscriber.signal.connect(function(page) {
                if (page == "wrongAnswer") {  
                    $("#"+selectedPic).addClass("hidden")
                    return
                }
                $(".active").removeClass("active");
                $("#" + page).addClass("active");
            });
        });
    }, function(error) {
        console.log("An error occurred:", error);
    });
}); //end document ready