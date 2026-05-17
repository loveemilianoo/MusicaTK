"""
PLAN DETALLADO DE IMPLEMENTACIÓN
Basado en MaquetaArtista.py
"""

FUNCIONALIDADES_A_IMPLEMENTAR = {
    "FASE 1 - PRIORITARIA": [
        {
            "nombre": "Portal de Artista",
            "archivo": "ventana_portal_artista.py",
            "descripcion": "Dashboard con:
                - Estadísticas (oyentes, reproducciones, seguidores)
                - Tabla de canciones con estados
                - Botones de acción (Subir, Crear álbum, Editar perfil)",
            "componentes": ["Canvas para banner", "Estadísticas grid", "Tabla canciones"],
            "DAOs": ["CancionDAO", "ArtistaDAO"],
            "estado": "NO IMPLEMENTADO"
        },
        {
            "nombre": "Subir Canción",
            "archivo": "ventana_subir_cancion.py",
            "descripcion": "Formulario para:
                - Drag & drop (simulado con botón)
                - Metadatos: Título, Artista, Álbum, Año, Género, Letra
                - Visibilidad (Pública/Privada/Solo enlace)
                - Etiquetas
                - Progreso de subida",
            "componentes": ["Canvas drop zone", "Entry fields", "Text area", "Radiobuttons"],
            "DAOs": ["CancionDAO"],
            "estado": "NO IMPLEMENTADO"
        },
        {
            "nombre": "Crear Álbum",
            "archivo": "ventana_crear_album.py",
            "descripcion": "Formulario para:
                - Portada (simulada)
                - Tipo (Álbum/EP/Single)
                - Metadatos: Nombre, Artista, Año, Género
                - Tracklist (agregar/eliminar pistas)
                - Publicar",
            "componentes": ["Canvas portada", "Radiobuttons", "Tracklist frame"],
            "DAOs": ["AlbumDAO", "CancionDAO"],
            "estado": "NO IMPLEMENTADO"
        },
        {
            "nombre": "Popup Agregar a Playlist",
            "archivo": "popup_agregar_playlist.py",
            "descripcion": "Modal reutilizable para:
                - Buscar playlists
                - Seleccionar playlists (checkbox)
                - Crear nueva playlist
                - Guardar cambios",
            "componentes": ["Toplevel", "Entry búsqueda", "Checkbuttons"],
            "DAOs": ["PlaylistDAO"],
            "estado": "NO IMPLEMENTADO"
        }
    ],
    
    "FASE 2 - IMPORTANTE": [
        {
            "nombre": "Editar Canción",
            "archivo": "ventana_editar_cancion.py",
            "descripcion": "Editar metadatos y estado de canción",
            "DAOs": ["CancionDAO"],
            "estado": "NO IMPLEMENTADO"
        },
        {
            "nombre": "Editar Álbum",
            "archivo": "ventana_editar_album.py",
            "descripcion": "Editar álbum y tracklist",
            "DAOs": ["AlbumDAO"],
            "estado": "NO IMPLEMENTADO"
        }
    ],
    
    "FASE 3 - MEJORAS": [
        {
            "nombre": "Perfil de Usuario",
            "archivo": "ventana_perfil_usuario.py",
            "descripcion": "Ver y editar datos del usuario",
            "DAOs": ["UsuarioDAO"],
            "estado": "NO IMPLEMENTADO"
        }
    ]
}

print(__doc__)
print("\n✓ Total de tareas: ", sum(len(v) for v in FUNCIONALIDADES_A_IMPLEMENTAR.values()))
print("\n¿Cuál es tu prioridad?")
print("  [1] Implementar FASE 1 completa")
print("  [2] Implementar solo lo más crítico (Portal + Subir)")
print("  [3] Implementar todo de una vez")
