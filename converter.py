import os
from typing import Type
import win32com.client as win32


class Rtf2docxConverter:
    def __init__(self):
        # on définit un path source par défaut
        self.path = 'C:/Users/bulam/Documents/modeles'
        self.target_dir = 'C:/Users/bulam/Documents/docxFiles'

    def set_path(self, path: str) -> None:
        self.path = path

    def get_target_path(self, file_path: str) -> str:
        """Méthode qui retourne le chemin utilisé pour la sauvegarde du fichier au format docx"""
        # extrait le nom du fichier et change son extension
        filename = os.path.basename(file_path).replace('.rtf', '.docx')
        return f"{self.target_dir}/{filename}"

    def convert_rtf_to_docx(self, file_path, word: Type[win32]) -> None:
        """
        Utilise l'instance Word fournie en paramètre pour ouvrir un fichier au format rtf depuis le chemin fourni,
        puis le sauvegarde dans un répertoire cible au format docx
        """
        # ouverture, depuis le répertoire source, du document au format .rtf...
        doc = word.Documents.Open(file_path)
        # appel la méthode pour créer le chemin de destination à partir du nom du fichier
        target_dir = self.get_target_path(file_path)
        # ...puis sauvegarde dans le répertoire cible au format .docx
        doc.SaveAs(target_dir, FileFormat=wdFormatDocumentDefault)
        doc.Close()

    def convert_all(self, path=None) -> None:
        """converti en docx tous les fichiers rtf contenus dans un répertoire fourni en paramètre"""
        if path:
            self.set_path(path)
        # ouverture et configuration d'une instance Word unique pour convertir le fichier rtf en docx
        word = win32.Dispatch('Word.Application')
        wdFormatDocumentDefault = 16
        wdHeaderFooterPrimary = 1
        # utilisation d'une 'Generator Expression' pour itérer sur la liste des fichiers à convertir
        for filename in (file for file in os.listdir(self.path)):
            # appel de la méthode de conversion avec en argument le chemin vers le fichier et l'instance word
            self.convert_rtf_to_docx(f"{self.path}/{filename}", word)
        # une fois tous les fichiers convertis, on quitte l'instance word
        word.quit()


converter = Rtf2docxConverter()
converter.convert_all('C:/Users/bulam/Documents/modeles')


