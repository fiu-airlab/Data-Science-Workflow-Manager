function openNav() {
    document.getElementById("mySidenav").style.width = "280px";
    document.getElementById("main").style.marginLeft = "280px";
    document.getElementById("myclosebtn").style.color = "white"
    document.getElementById("myList").style.pointerEvents = "auto";
    // x = document.getElementsByClassName("top-bar");
    // for(i = 0; i < x.length; i++){
    //     x[i].style.visibility = "hidden";
    // }
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.getElementById("myclosebtn").style.color = "#17252A";
    document.getElementById("myList").style.pointerEvents = "none";
    // x = document.getElementsByClassName("top-bar");
    // for(i = 0; i < x.length; i++){
    //     x[i].style.visibility = "visible";
    // }
}
