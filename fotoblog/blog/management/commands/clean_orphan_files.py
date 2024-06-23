import os
from django.conf import settings
from django.core.management.base import BaseCommand
from blog.models import Photo


class Command(BaseCommand):
    """It is also possible that image files remain orphaned if, for example, images are deleted
    manually or if files are left behind during a migration.
    You can write a script to clean up these orphaned files."""

    help = 'Clean orphan files'

    def handle(self, *args, **kwargs):
        media_path = settings.MEDIA_ROOT
        # Vérification des fichiers utilisés :
        # Nous récupérons les chemins des fichiers actuellement utilisés dans la base de données
        used_files = set(Photo.objects.values_list('image', flat=True))
        # Parcours du répertoire des photos :
        # Nous utilisons os.walk pour parcourir tous les fichiers dans le répertoire photos.
        for dirpath, _, filenames in os.walk(os.path.join(media_path, 'photos')):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(file_path, media_path)

                # Suppression des fichiers orphelins :
                # Pour chaque fichier, nous vérifions s'il est référencé dans la base de données.
                # Si ce n'est pas le cas, nous le supprimons.
                if relative_path not in used_files:
                    os.remove(file_path)
                    self.stdout.write(f'Deleted orphan file: {file_path}')

        self.stdout.write(self.style.SUCCESS('Finished cleaning orphan files.'))

# Explication des étapes :
# Importation des modules nécessaires : Nous importons os, settings, BaseCommand et le modèle Photo.
# Définition de la classe de commande : La classe Command hérite de BaseCommand.
# Définition de la méthode handle : Cette méthode contient la logique pour nettoyer les fichiers orphelins.
# Exécution de la commande de gestion : Après avoir défini la commande, vous pouvez l'exécuter
# en utilisant la commande manage.py : ython manage.py clean_orphan_files
# /fotoblog/blog/management/commands/clean_orphan_files.py
