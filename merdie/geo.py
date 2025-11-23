import folium
import requests

# ------------------------------
# Coordonnées des points
# ------------------------------
points = [
    {"name": "Rond Point Ngaba", "coord": (-4.385000, 15.345000), "color": "green"},
    {"name": "Palais du Peuple", "coord": (-4.332200, 15.303100), "color": "red"},
    {"name": "Université Révérend Kim Ndjili", "coord": (-4.385900, 15.364800), "color": "purple"}
]

# ------------------------------
# Création de la carte
# ------------------------------
m = folium.Map(location=[-4.35, 15.33], zoom_start=12, control_scale=True)

# ------------------------------
# Ajouter les marqueurs avec icônes différentes
# ------------------------------
for point in points:
    folium.Marker(
        location=point["coord"],
        popup=folium.Popup(f"<b>{point['name']}</b><br>Click pour zoom", max_width=250),
        tooltip=point["name"],
        icon=folium.Icon(color=point["color"], icon="info-sign")
    ).add_to(m)

# ------------------------------
# Fonction pour récupérer trajet OSRM entre deux points
# ------------------------------
def osrm_route(start, end):
    url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=geojson"
    r = requests.get(url).json()
    coords = [(c[1], c[0]) for c in r["routes"][0]["geometry"]["coordinates"]]
    distance_km = r["routes"][0]["distance"] / 1000  # km
    duration_min = r["routes"][0]["duration"] / 60    # min
    return coords, distance_km, duration_min

# ------------------------------
# Tracer le trajet réel segment par segment
# ------------------------------
for i in range(len(points)-1):
    start = points[i]
    end = points[i+1]
    coords, distance, duration = osrm_route(start["coord"], end["coord"])
    
    folium.PolyLine(
        coords,
        color="blue",
        weight=5,
        tooltip=f"{start['name']} → {end['name']}: {distance:.2f} km, {duration:.1f} min"
    ).add_to(m)
    
    print(f"{start['name']} → {end['name']} : {distance:.2f} km, {duration:.1f} min")

# ------------------------------
# Légende interactive
# ------------------------------
legend_html = """
<div style="position: fixed; bottom: 50px; left: 50px; width: 280px; height: 130px; 
background-color: white; border:2px solid grey; z-index:9999; font-size:14px; padding:10px;">
<b>Trajet réel :</b><br>
• Rond Point Ngaba → Palais du Peuple<br>
• Palais du Peuple → Révérend Kim Ndjili<br>
<small>Distance et durée calculées via OSRM</small>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# ------------------------------
# Enregistrement de la carte
# ------------------------------
m.save("trajet_osrm_kinshasa_avance.html")
print("Carte avancée générée → trajet_osrm_kinshasa_avance.html")
