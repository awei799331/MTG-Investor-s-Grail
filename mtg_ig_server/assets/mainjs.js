function getImage() {
    var urlSearch = "https://api.scryfall.com/cards/named?fuzzy=" + document.getElementById("getCard").value
    console.log(urlSearch)
    var request = new XMLHttpRequest()
    request.open('GET', urlSearch, false)
    request.send(null)
    var blob = request.responseText
    var blobJSON = JSON.parse(blob)
    console.log(blob)

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