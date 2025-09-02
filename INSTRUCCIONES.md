# Instrucciones para Generar el Formulario de Google Forms

Sigue estos pasos para ejecutar el script de Python y crear tu formulario de Google Forms automáticamente.

Este método utiliza un **entorno virtual**, que es la forma recomendada de manejar dependencias en Python para evitar conflictos con los paquetes del sistema.

## Prerrequisitos

- Tener Python 3 instalado en tu computadora. Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
- Tener una cuenta de Google.

---

## Paso 1: Preparar el Entorno y las Dependencias

Abre una terminal o línea de comandos y navega a la carpeta donde tienes el archivo `create_google_form.py`.

1.  **Crear un Entorno Virtual:**
    Ejecuta este comando para crear un entorno virtual llamado `form_env`. Solo necesitas hacer esto una vez.
    ```bash
    python3 -m venv form_env
    ```

2.  **Activar el Entorno Virtual:**
    Debes activar el entorno cada vez que abras una nueva terminal para trabajar con el script.
    -   **En macOS y Linux:**
        ```bash
        source form_env/bin/activate
        ```
    -   **En Windows (CMD):**
        ```bash
        form_env\Scripts\activate
        ```
    Sabrás que funcionó porque tu prompt de la terminal cambiará para mostrar `(form_env)` al principio.

3.  **Instalar las Librerías Necesarias:**
    Con el entorno activado, instala las librerías de Google. Se instalarán de forma segura dentro del entorno virtual.
    ```bash
    pip install google-api-python-client google-auth-oauthlib
    ```

---

## Paso 2: Habilitar la API de Google Forms y Obtener Credenciales

Este paso es para autorizar al script a crear formularios en tu nombre.

1.  **Ir a la Consola de Google Cloud:** Abre tu navegador y ve a la [Consola de Google Cloud](https://console.cloud.google.com/). Inicia sesión con tu cuenta de Google.

2.  **Crear o seleccionar un proyecto:**
    *   Si es tu primera vez, crea un nuevo proyecto.
    *   Si ya tienes proyectos, puedes usar uno existente o crear uno nuevo.

3.  **Habilitar la API de Google Forms:**
    *   En el menú de navegación (☰), ve a **APIs y servicios > Biblioteca**.
    *   Busca `Google Forms API` y haz clic en **Habilitar**.

4.  **Configurar la Pantalla de Consentimiento:**
    *   En el menú, ve a **APIs y servicios > Pantalla de consentimiento de OAuth**.
    *   Selecciona **Externo** y haz clic en **Crear**.
    *   Rellena los campos obligatorios (Nombre de la aplicación, Correo de asistencia, Correo de contacto del desarrollador) y haz clic en **Guardar y continuar** hasta finalizar.

5.  **Crear las Credenciales:**
    *   En el menú, ve a **APIs y servicios > Credenciales**.
    *   Haz clic en **+ CREAR CREDENCIALES** y selecciona **ID de cliente de OAuth**.
    *   En **Tipo de aplicación**, selecciona **Aplicación de escritorio**.
    *   Haz clic en **Crear**.

6.  **Descargar el archivo de credenciales:**
    *   Después de crear las credenciales, aparecerá una ventana. Ciérrala.
    *   En la lista de IDs de cliente, haz clic en el **ícono de descarga** (↓) al lado de la credencial que creaste.
    *   **Renombra el archivo descargado a `credentials.json`** y colócalo en la **misma carpeta** que el script `create_google_form.py`.

---

## Paso 3: Ejecutar el Script

1.  **Asegúrate de que tu entorno virtual esté activo.** Si no ves `(form_env)` al principio de tu terminal, vuelve al Paso 1 y actívalo.

2.  **Verifica que los archivos estén en su lugar:** El script `create_google_form.py` y el archivo `credentials.json` deben estar en la misma carpeta.

3.  **Ejecuta el script:**
    ```bash
    python3 create_google_form.py
    ```

4.  **Autoriza el script:**
    *   La primera vez que lo ejecutes, se abrirá una pestaña en tu navegador pidiéndote que inicies sesión y concedas permisos.
    *   Es posible que veas una advertencia de "Google no ha verificado esta aplicación". Es normal. Haz clic en "Configuración avanzada" y luego en "Ir a [tu app] (no seguro)".
    *   Después de autorizar, el script continuará en la terminal.

## ¡Listo!

El script te mostrará la URL del formulario creado. Para futuras ejecuciones, solo necesitas activar el entorno virtual (Paso 1.2) y ejecutar el script (Paso 3.3). No necesitarás crear el entorno ni instalar las librerías de nuevo.
