from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import urllib.request
import json
from AppPokemon.forms import formatraparPokemon
from AppPokemon.models import Pokemon

def home(request):
    return render(request, "AppPokemon/home.html")

def pokedex(request):
    if request.method == 'POST':
        pokemon = request.POST['pokemon'].lower()
        pokemon = pokemon.replace(' ','%20')
        url_pokeapi = urllib.request.Request(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        url_pokeapi.add_header("User-Agent","charmander")

        try:

            source = urllib.request.urlopen(url_pokeapi).read()
            list_of_data = json.loads(source)

           # Altura de decímetros a metros
            height_obtained = (float(list_of_data['height']) * 0.1)
            height_rounded = round(height_obtained, 2)

            # Peso de hectogramos a kilogramos
            weight_obtained = (float(list_of_data['weight']) * 0.1)
            weight_rounded = round(weight_obtained, 2)

            data = { 
                "number": str(list_of_data['id']),
                "name": str(list_of_data['name']).capitalize(),
                "height": str(height_rounded)+ " m",
                "weight": str(weight_rounded)+ " kg",
                "sprite": str(list_of_data['sprites']['front_default']),
                "types": str(list_of_data['types'][0]['type']['name']),
            }

            print(data)
    
        except urllib.error.HTTPError as e:
            error_message = f"Error al buscar el Pokémon: {e.code} - {e.reason}"
            data = {
                "error": error_message
            }

    else:
        data = {}

    return render(request, "AppPokemon/pokedex.html", data)

def atraparPokemones(request):
    if request.method == "POST":
        miFormulario = formatraparPokemon(request.POST)
        print(miFormulario)
        if miFormulario.is_valid():
            data = miFormulario.cleaned_data
            pokemon = Pokemon(nivel=data["nivel"], nombre=data["nombre"], mote=data["mote"])
            pokemon.save()
            return render(request, "AppPokemon/home.html")
    else:
        miFormulario = formatraparPokemon()
    
    return render(request, "AppPokemon/atraparPokemon.html", {"miFormulario":miFormulario})

def consultarEquipos(request):
    return render(request, "AppPokemon/consultarEquipo.html")

def getEquipo(request):
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        pokemones = Pokemon.objects.filter(nombre = nombre)
        return render(request, "AppPokemon/consultarEquipo.html", {"pokemones":pokemones})
    else:
        respuesta = "No se enviaron datos"
    return HttpResponse(respuesta)

def pokemones(request):
    return render(request, "AppPokemon/pokemones.html")



# Create your views here.
