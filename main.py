import os
import requests
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

# 🔑 Configuración con variables de entorno
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# 📡 Obtener todos los repositorios del usuario (incluye privados, si tienes acceso)
repos_url = "https://api.github.com/user/repos?per_page=100&type=all"  # Esta URL obtiene repos privados y públicos
repos = requests.get(repos_url, headers=headers).json()

# Filtrar solo los repos creados por el usuario
repos_creados = [repo for repo in repos if repo['owner']['login'] == GITHUB_USERNAME]

# Verificar que estamos obteniendo solo tus repositorios creados
print(f"Repositorios creados por {GITHUB_USERNAME}:")
for repo in repos_creados:
    print(f"- {repo['name']} (URL: {repo['html_url']})")

# 📊 Diccionario para contar bytes por lenguaje
languages_count = {}

# 🔍 Recorrer cada repo creado por el usuario y obtener sus lenguajes
for repo in repos_creados:
    lang_url = repo["languages_url"]
    languages = requests.get(lang_url, headers=headers).json()

    for lang, bytes_used in languages.items():
        languages_count[lang] = languages_count.get(lang, 0) + bytes_used

# 🔢 Calcular porcentajes
total_bytes = sum(languages_count.values())
percentages = {lang: (bytes_used / total_bytes) * 100 for lang, bytes_used in languages_count.items()}

# 🔝 Obtener los 10 lenguajes más usados
top_languages = sorted(percentages.items(), key=lambda x: x[1], reverse=True)[:10]  # Solo los 10 primeros
langs, percents = zip(*top_languages)

# Mostrando los graficos del color de los lenguajes y aplicarlos al color en CMD y en el gráfico
# 🎨 Colores para cada lenguaje
colors = {
    "JavaScript": "#f1e05a", "Python": "#3572A5", "HTML": "#e34c26", "CSS": "#563d7c", "TypeScript": "#2b7489",
    "Shell": "#89e051", "Ruby": "#701516", "Java": "#b07219", "C": "#555555", "C++": "#f34b7d", "PHP": "#4F5D95",
    "C#": "#178600", "Go": "#00ADD8", "Swift": "#ffac45", "Kotlin": "#F18E33", "Rust": "#dea584",
    "Scala": "#c22d40", "Perl": "#0298c3", "Vue": "#2c3e50", "Astro": "#ff0080", "Dart": "#00B4AB",
    "R": "#198CE7",
}
colors_readed_by_terminal = {
    "JavaScript": "\33[33m", "Python": "\33[34m", "HTML": "\33[31m", "CSS": "\33[35m", "TypeScript": "\33[36m",
    "Shell": "\33[32m", "Ruby": "\33[31m", "Java": "\33[33m", "C": "\33[34m", "C++": "\33[35m", "PHP": "\33[36m",
    "C#": "\33[32m", "Go": "\33[33m", "Swift": "\33[34m", "Kotlin": "\33[35m", "Rust": "\33[36m",
    "Scala": "\33[32m", "Perl": "\33[33m", "Vue": "\33[34m", "Astro": "\33[35m", "Dart": "\33[36m",
    "R": "\33[32m",
}
# Determinando color en base al lenguaje
color = [colors.get(lang, "#333333") for lang in langs]

print("\n📌 Top 10 lenguajes más usados:")
for lang, percentage in top_languages:
    # 📊 Mostrar porcentaje de uso con su respectivo color en la consola que abarque toda la linea escrita sin que afecte al color de la consola del usuario por default
    print(f"{colors_readed_by_terminal.get(lang, '')}{lang}: {percentage:.2f}%\33[0m ", end="\n")

print("\nMostrando gráfico...")
# 📊 Generar gráfico de barras
plt.figure(figsize=(10, 6))
plt.barh(langs, percents, color=color)
plt.xlabel("Porcentaje de uso (%)")
plt.ylabel("Lenguajes")
plt.title("Top 10 Lenguajes más usados en GitHub")
plt.gca().invert_yaxis()  # Invertir el orden para que el más usado quede arriba
plt.grid(axis="x", linestyle="--", alpha=0.7)

# 📌 Mostrar el gráfico
plt.show()
