function openNav() {
    document.getElementById("mySidenav").style.width = "280px";
    document.getElementById("main").style.marginLeft = "280px";
    document.getElementById("myclosebtn").style.color = "white"
    document.getElementById("myList").style.pointerEvents = "auto";
    x = document.getElementsByClassName("vertical-slider");
    for(i = 0; i < x.length; i++){
        x[i].style.display = "none";
    }
    y = document.getElementsByClassName("graph-buttons");
    for(i = 0; i < y.length; i ++){
        y[i].style.display = "none";
    }
}

function changeButtons(){
    x = document.getElementsByClassName("vertical-slider");
    y = document.getElementsByClassName("graph-buttons");
    for(i = 0; i < x.length; i++){
        x[i].style.display = "inline-block";
    }
    y = document.getElementsByClassName("graph-buttons");
    for(i = 0; i < y.length; i ++){
        y[i].style.display = "block";
    }
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginLeft = "10px";
    document.getElementById("myclosebtn").style.color = "#17252A";
    document.getElementById("myList").style.pointerEvents = "none";
    setTimeout(changeButtons,400);
    
    
}
