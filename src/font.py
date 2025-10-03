import customtkinter as ctk
import tkinter.font as tkfont
from pathlib import Path
from .data import font_family

bold_ttf = Path(__file__).resolve().parent / "assets/fonts/Montserrat-Bold.ttf"

def load_font(app, size):
    fams = set(tkfont.families(app))
    if bold_ttf.exists():  # Windows: Cargar archivo
        try:
            temp = tkfont.Font(file=str(bold_ttf), size=size)
            fam = temp.actual("family")
            return ctk.CTkFont(family=fam, size=size, weight="bold")
        except Exception:
            pass
    if font_family in fams:  # Mac: usar fuente instalada
        return ctk.CTkFont(family=font_family, size=size, weight="bold")
    if f"{font_family} Bold" in fams:
        return ctk.CTkFont(family=f"{font_family} Bold", size=size)
    return ctk.CTkFont(size=size)  # Fallback