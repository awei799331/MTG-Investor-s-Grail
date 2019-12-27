stringboi = "Ajani, Aminatou, Angrath, Arlinn, Ashiok, Bolas, Chandra, Dack, Daretti, Davriel, Domri, Dovin, Elspeth, Estrid, Freyalise, Garruk, Gideon, Huatli, Jace, Jaya, Karn, Kasmina, Kaya, Kiora, Koth, Liliana, Nahiri, Narset, Nissa, Nixilis, Oko, Ral, Rowan, Saheeli, Samut, Sarkhan, Serra, Sorin, Tamiyo, Teferi, Teyo, Tezzeret, Tibalt, Ugin, Venser, Vivien, Vraska, Will, Windgrace, Wrenn, Xenagos, Yanggu, Yanling"
stringboi = stringboi.split(", ")
dicty = {}
for each in stringboi:
    dicty.update({each: 0})

print(dicty)