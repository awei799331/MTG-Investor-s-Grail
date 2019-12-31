function generateBackground() {
    var totalImages = 10
    var randomNum = Math.ceil(Math.random() * totalImages)
    var filePath = '/static/background' + randomNum + '.jpg'
    document.getElementById("background").style.backgroundImage = "url(\'" + filePath + "\')"
    document.getElementById("background").style.zIndex = "1"
}
generateBackground()