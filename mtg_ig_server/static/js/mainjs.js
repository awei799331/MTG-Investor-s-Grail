getCardId = document.getElementById("getCard")
getNavbarClasses = document.getElementsByClassName("navtext")
getNavbarClasses = [...getNavbarClasses]

function getImage() {
    var urlSearch = "https://api.scryfall.com/cards/named?fuzzy=" + getCardId.value
    console.log(urlSearch)
    var request = new XMLHttpRequest()
    request.open('GET', urlSearch, false)
    request.send(null)
    var blob = request.responseText
    var blobJSON = JSON.parse(blob)
    console.log(blobJSON)

    if (blobJSON.object == "error") {
        alert("Error: card does not exist or search is too ambiguous")
    }
}

getCardId.addEventListener("focusin", (e)=>{
    getCardId.classList.remove("searchBorderUnfocused")
    getCardId.classList.add("searchBorderHighlighted")
})
getCardId.addEventListener("focusout", (e)=>{
    getCardId.classList.remove("searchBorderHighlighted")
    getCardId.classList.add("searchBorderUnfocused")
})

getNavbarClasses.forEach(element => {
    element.addEventListener("mouseover", (e)=>{
        element.classList.remove("navbarUnhovered")
        element.classList.add("navbarHovered")
    })

    element.addEventListener("mouseout", (e)=>{
        element.classList.add("navbarUnhovered")
        element.classList.remove("navbarHovered")
    })
});

document.getElementById("search").addEventListener("mouseover", (e)=>{
    document.getElementById("search").classList.remove("searchUnhovered")
    document.getElementById("search").classList.add("searchHovered")
})

document.getElementById("search").addEventListener("mouseout", (e)=>{
    document.getElementById("search").classList.remove("searchHovered")
    document.getElementById("search").classList.add("searchUnhovered")
})