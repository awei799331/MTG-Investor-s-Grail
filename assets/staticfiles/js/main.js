getNavbarClasses = document.getElementsByClassName("navtext")
getNavbarClasses = [...getNavbarClasses]

function generateBackground() {
    var totalImages = 10
    var randomNum = Math.ceil(Math.random() * totalImages)
    var filePath = '/static/images/background' + randomNum + '.jpg'
    document.getElementById("background").style.backgroundImage = "url(\'" + filePath + "\')"
    document.getElementById("background").style.zIndex = "1"
}


getNavbarClasses.forEach(element => {

    if (!element.classList.contains("navtext-active")) {
            element.addEventListener("mouseover", (e)=>{
            element.classList.remove("navbarUnhovered")
            element.classList.add("navbarHovered")
        })
    
        element.addEventListener("mouseout", (e)=>{
            element.classList.add("navbarUnhovered")
            element.classList.remove("navbarHovered")
        })
    }
});

generateBackground()