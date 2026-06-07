import tkinter as tk
from tkinter import messagebox
from views.colores import *
from views.componentes import Componentes
from controller.ArtistaDAO import ArtistaDAO
from controller.IdentidadGeneroDAO import IdentidadGeneroDAO
from models.Artista import Artista

class VentanaRegistroArtista:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("WavePlay - Registro de Artista")
        self.ventana.geometry("450x700")
        self.ventana.configure(bg=BG_DARK)
        self.setup_ui()

    def setup_ui(self):
        root = tk.Frame(self.ventana, bg=BG_DARK)
        root.pack(fill="both", expand=True, padx=30, pady=20)

        Componentes.label(root, "Registro de artista", font=FONT_TITLE,
                         fg=TEXT_PRI, bg=BG_DARK, anchor="center").pack(pady=(0, 4))
        Componentes.label(root, "Crea tu perfil para subir música", font=FONT_SMALL,
                         fg=TEXT_SEC, bg=BG_DARK, anchor="center").pack(pady=(0, 16))

        form = tk.Frame(root, bg=BG_DARK)
        form.pack(fill="both", expand=True)

        # Nombre
        Componentes.label(form, "Nombre artístico / Nombre *", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_nombre = Componentes.entry(form, "", width=40)
        self.entry_nombre.pack(fill="x", ipady=6)

        # Apellido Paterno
        Componentes.label(form, "Apellido Paterno *", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_ap = Componentes.entry(form, "", width=40)
        self.entry_ap.pack(fill="x", ipady=6)

        # Apellido Materno
        Componentes.label(form, "Apellido Materno", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_am = Componentes.entry(form, "", width=40)
        self.entry_am.pack(fill="x", ipady=6)

        # Fecha nacimiento
        Componentes.label(form, "Fecha de nacimiento * (YYYY-MM-DD)", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_fecha = Componentes.entry(form, "", width=40)
        self.entry_fecha.pack(fill="x", ipady=6)

        # Fecha de fallecimiento (opcional, para artistas fallecidos)
        Componentes.label(form, "Fecha de fallecimiento (YYYY-MM-DD, opcional)",
                         font=FONT_H3, fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.entry_fecha_fin = Componentes.entry(form, "", width=40)
        self.entry_fecha_fin.pack(fill="x", ipady=6)

        # Identidad de género
        Componentes.label(form, "Identidad de género", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 2))
        self.identidades = IdentidadGeneroDAO.listar_todas()
        self.identidad_ids = {i.identidad: i.id_identidad for i in self.identidades}
        self.identidad_var = tk.StringVar()
        nombres = list(self.identidad_ids.keys()) or ["Sin especificar"]
        if "Sin especificar" not in self.identidad_ids:
            self.identidad_ids.setdefault("Sin especificar", None)
        self.identidad_var.set(nombres[0])
        combo = tk.OptionMenu(form, self.identidad_var, *nombres)
        combo.config(bg=BG_CARD, fg=TEXT_PRI, font=FONT_BODY,
                     activebackground=BG_HOVER, relief="flat", highlightthickness=0)
        combo.pack(fill="x", ipady=4)

        Componentes.divider(form)

        # Tipo de artista
        Componentes.label(form, "Tipo de artista", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(8, 4))
        self.banda_var = tk.StringVar(value="0")
        tipo_row = tk.Frame(form, bg=BG_DARK)
        tipo_row.pack(fill="x")
        for texto, val in [("Solista", "0"), ("Banda", "1")]:
            tk.Radiobutton(tipo_row, text=texto, variable=self.banda_var,
                          value=val, bg=BG_DARK, fg=TEXT_PRI,
                          selectcolor=BG_DARK, activebackground=BG_DARK,
                          font=FONT_BODY, borderwidth=0,
                          highlightthickness=0).pack(side="left", padx=(0, 20))

        # Disquera
        Componentes.label(form, "Disquera / Sello (opcional)", font=FONT_H3,
                         fg=TEXT_SEC).pack(anchor="w", pady=(12, 2))
        self.entry_disquera = Componentes.entry(form, "", width=40)
        self.entry_disquera.pack(fill="x", ipady=6)

        # Botones
        Componentes.btn(form, "CREAR CUENTA DE ARTISTA", self._registrar,
                        bg=ACCENT, fg="white",
                        font=("Helvetica", 11, "bold")).pack(fill="x", pady=(20, 6))
        Componentes.btn(form, "← Volver al login", self._volver_login,
                        bg=BG_CARD, fg=ACCENT2).pack(fill="x")

    def _registrar(self):
        nombre   = self.entry_nombre.get().strip()
        ap       = self.entry_ap.get().strip()
        am       = self.entry_am.get().strip()
        fecha    = self.entry_fecha.get().strip()
        disquera = self.entry_disquera.get().strip()
        banda    = int(self.banda_var.get())

        if not all([nombre, ap, fecha]):
            messagebox.showerror("Error", "Completa los campos obligatorios (*)",
                                 parent=self.ventana)
            return

        if not self._fecha_valida(fecha):
            messagebox.showerror("Error", "Fecha inválida. Usa YYYY-MM-DD",
                                 parent=self.ventana)
            return

        from datetime import datetime
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()

        # Fecha de fallecimiento (opcional)
        fecha_fin_str = self.entry_fecha_fin.get().strip()
        fecha_fin_obj = None
        if fecha_fin_str:
            if not self._fecha_valida(fecha_fin_str):
                messagebox.showerror("Error",
                                     "Fecha de fallecimiento inválida. Usa YYYY-MM-DD",
                                     parent=self.ventana)
                return
            fecha_fin_obj = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
            if fecha_fin_obj < fecha_obj:
                messagebox.showerror("Error",
                                     "La fecha de fallecimiento no puede ser anterior "
                                     "a la de nacimiento",
                                     parent=self.ventana)
                return

        artista = Artista(
            nombre           = nombre,
            apellido_paterno = ap,
            apellido_materno = am or None,
            fecha_nacimiento = fecha_obj,
            fecha_fin        = fecha_fin_obj,
            banda            = banda,
            disquera         = disquera or None
        )

        resultado = ArtistaDAO.crear_artista(artista)

        if resultado:
            # Guardar identidad de género seleccionada
            id_identidad = self.identidad_ids.get(self.identidad_var.get())
            if id_identidad is not None:
                IdentidadGeneroDAO.asignar_a_persona(resultado, id_identidad)

            messagebox.showinfo("Éxito",
                                f"Cuenta de artista creada.\n¡Bienvenido {nombre}!",
                                parent=self.ventana)
            self._volver_login()
        else:
            messagebox.showerror("Error",
                                 "No se pudo crear la cuenta. Intenta de nuevo.",
                                 parent=self.ventana)

    def _fecha_valida(self, fecha):
        from datetime import datetime
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _volver_login(self):
        self.ventana.destroy()
        from views.ventana_login import VentanaLogin
        VentanaLogin().ejecutar()

    def ejecutar(self):
        self.ventana.mainloop()