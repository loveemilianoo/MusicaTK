import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.pausado = False
        self._seek_offset = 0.0

    def reproducir(self, ruta_relativa):
        """Carga y reproduce un archivo. ruta_relativa desde la raíz del proyecto."""
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta = os.path.join(base, ruta_relativa)

        if not os.path.exists(ruta):
            print(f"✗ Archivo no encontrado: {ruta}")
            return False

        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play()
        self.pausado = False
        self._seek_offset = 0.0
        print(f"▶ Reproduciendo: {ruta}")
        return True

    def seek(self, segundos):
        """Salta a una posición específica en segundos."""
        pygame.mixer.music.play(start=float(segundos))
        self._seek_offset = float(segundos)
        if self.pausado:
            pygame.mixer.music.pause()

    def pausar(self):
        if pygame.mixer.music.get_busy() and not self.pausado:
            pygame.mixer.music.pause()
            self.pausado = True

    def reanudar(self):
        if self.pausado:
            pygame.mixer.music.unpause()
            self.pausado = False

    def detener(self):
        pygame.mixer.music.stop()
        self.pausado = False
        self._seek_offset = 0.0

    def set_volumen(self, valor_0_a_100):
        """Recibe un valor entre 0 y 100"""
        pygame.mixer.music.set_volume(valor_0_a_100 / 100)

    def get_posicion_segundos(self):
        """Retorna la posición actual en segundos"""
        ms = pygame.mixer.music.get_pos()
        if ms < 0:
            return 0.0
        return ms / 1000 + self._seek_offset

    def esta_reproduciendo(self):
        return pygame.mixer.music.get_busy()