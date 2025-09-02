# Instrucciones para Generar el Formulario de Google Forms

Sigue estos pasos para ejecutar el script de Python y crear tu formulario de Google Forms automáticamente.

## Prerrequisitos

- Tener Python instalado en tu computadora. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
- Tener una cuenta de Google.

## Paso 1: Instalar las librerías necesarias

Abre una terminal o línea de comandos en tu computadora y ejecuta el siguiente comando para instalar las librerías de Google que el script necesita:

```bash
pip install google-api-python-client google-auth-oauthlib
```

## Paso 2: Habilitar la API de Google Forms y obtener credenciales

Este es el paso más importante. Necesitas autorizar al script para que pueda crear formularios en tu nombre.

1.  **Ir a la Consola de Google Cloud:** Abre tu navegador y ve a la [Consola de Google Cloud](https://console.cloud.google.com/). Inicia sesión con tu cuenta de Google si es necesario.

2.  **Crear o seleccionar un proyecto:**
    *   Si es la primera vez que usas la consola, es posible que debas aceptar los términos de servicio y crear un nuevo proyecto. Dale un nombre como "Mis Scripts" o algo similar.
    *   Si ya tienes proyectos, puedes usar uno existente o crear uno nuevo desde el selector de proyectos en la parte superior de la página.

3.  **Habilitar la API de Google Forms:**
    *   En el menú de navegación de la izquierda (el ícono de hamburguesa ☰), ve a **APIs y servicios > Biblioteca**.
    *   En la barra de búsqueda, escribe `Google Forms API` y presiona Enter.
    *   Selecciona "Google Forms API" de la lista y haz clic en el botón **Habilitar**.

4.  **Configurar la pantalla de consentimiento (si es necesario):**
    *   Antes de crear credenciales, puede que necesites configurar la "Pantalla de consentimiento de OAuth".
    *   En el menú de la izquierda, ve a **APIs y servicios > Pantalla de consentimiento de OAuth**.
    *   Selecciona el tipo de usuario **Externo** y haz clic en **Crear**.
    *   Rellena los campos obligatorios:
        *   **Nombre de la aplicación:** `Script para Forms` (o el nombre que prefieras).
        *   **Correo electrónico de asistencia del usuario:** Selecciona tu dirección de correo.
        *   **Datos de contacto del desarrollador:** Ingresa tu dirección de correo nuevamente.
    *   Haz clic en **Guardar y continuar** en los siguientes pasos (permisos y usuarios de prueba) hasta que vuelvas al panel. No necesitas añadir nada más.

5.  **Crear las credenciales:**
    *   En el menú de la izquierda, ve a **APIs y servicios > Credenciales**.
    *   Haz clic en **+ CREAR CREDENCIALES** en la parte superior y selecciona **ID de cliente de OAuth**.
    *   En **Tipo de aplicación**, selecciona **Aplicación de escritorio**.
    *   Dale un nombre si lo deseas (ej. "Credenciales Script Forms") y haz clic en **Crear**.

6.  **Descargar el archivo de credenciales:**
    *   Aparecerá una ventana con tu ID y secreto de cliente. Ciérrala.
    *   En la lista de "ID de cliente de OAuth", busca la credencial que acabas de crear y haz clic en el **ícono de descarga** (una flecha hacia abajo) a la derecha.
    *   Esto descargará un archivo JSON. **Cámbiale el nombre a `credentials.json`**.

## Paso 3: Ejecutar el script

1.  **Coloca los archivos juntos:** Asegúrate de que el script `create_google_form.py` y el archivo `credentials.json` que acabas de descargar estén en la **misma carpeta**.

2.  **Abre una terminal:** Navega con la terminal hasta la carpeta donde guardaste los dos archivos.

3.  **Ejecuta el script:** Escribe el siguiente comando y presiona Enter.

    ```bash
    python create_google_form.py
    ```

4.  **Autoriza el script:**
    *   La primera vez que ejecutes el script, se abrirá una pestaña en tu navegador pidiéndote que inicies sesión con tu cuenta de Google y que concedas permisos al script.
    *   Es posible que veas una advertencia de "Google no ha verificado esta aplicación". Esto es normal porque es tu propio script. Haz clic en "Configuración avanzada" o "Continuar" y luego en "Ir a [nombre de tu app] (no seguro)" para permitir el acceso.
    *   Después de autorizar, la pestaña del navegador se cerrará y el script continuará su ejecución en la terminal.

## ¡Listo!

Una vez que el script termine, verás un mensaje en la terminal con la URL de tu nuevo formulario de Google Forms. Puedes copiar y pegar esa URL en tu navegador para verlo.

Para futuras ejecuciones, el script usará un archivo `token.json` que se creará automáticamente, por lo que no tendrás que autorizarlo de nuevo a menos que elimines ese archivo.
