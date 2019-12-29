function generateBackground() {
    var totalImages = 5
    var randomNum = Math.ceil(Math.random() * totalImages)
    var filePath = '/static/background' + randomNum + '.jpg'
    document.getElementById("background").style.backgroundImage = "url(\'" + filePath + "\')"
    document.getElementById("background").style.zIndex = "1"
}

function getImage() {
    var urlSearch = "https://api.scryfall.com/cards/named?fuzzy=" + document.getElementById("getCard").value
    console.log(urlSearch)
    var request = new XMLHttpRequest()
    request.open('GET', urlSearch, false)
    request.send(null)
    var blob = request.responseText
    var blobJSON = JSON.parse(blob)
    console.log(blobJSON)

    if (blobJSON.object != "error") {
        var im = document.createElement("img")
        im.setAttribute("src", blobJSON.image_uris.normal)
        im.draggable = false
    
        var imageHTML = document.getElementById("image")
        imageHTML.innerHTML = ""
    
        document.getElementById("cardAbility").innerHTML = blobJSON.oracle_text

        imageHTML.appendChild(im)
    } else {
        alert("Error: card does not exist or search is too ambiguous")
    }

}

generateBackground()