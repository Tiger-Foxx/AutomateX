@echo off

REM Vérifier si Python est installé
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installé. Veuillez installer Python et réessayer.
    exit /b
)

REM Vérifier si pip est installé
where pip >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo pip n'est pas installé. Veuillez installer pip et réessayer.
    exit /b
)

REM Installer virtualenv si nécessaire
pip show virtualenv >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo virtualenv n'est pas installé. Installation en cours...
    pip install virtualenv
)

REM Créer un environnement virtuel
IF NOT EXIST env (
    echo Création de l'environnement virtuel...
    python -m venv env
)

REM Activer l'environnement virtuel
call env\\Scripts\\activate

REM Installer les dépendances
IF EXIST requirements.txt (
    echo Installation des dépendances...
    pip install -r requirements.txt
) ELSE (
    echo Le fichier requirements.txt n'existe pas. Assurez-vous d'avoir un fichier de dépendances.
    exit /b
)

REM Appliquer les migrations
echo Application des migrations de la base de données...
python manage.py migrate

REM Lancer le serveur Django
echo Lancement du serveur Django...
python manage.py runserver

echo Le projet est prêt et le serveur est en cours d'exécution.
