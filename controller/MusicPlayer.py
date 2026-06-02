import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.pausado = False

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
        print(f"▶ Reproduciendo: {ruta}")
        return True

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

    def set_volumen(self, valor_0_a_100):
        """Recibe un valor entre 0 y 100"""
        pygame.mixer.music.set_volume(valor_0_a_100 / 100)

    def get_posicion_segundos(self):
        """Retorna la posición actual en segundos"""
        ms = pygame.mixer.music.get_pos()
        return ms / 1000 if ms >= 0 else 0

    def esta_reproduciendo(self):
        return pygame.mixer.music.get_busy()