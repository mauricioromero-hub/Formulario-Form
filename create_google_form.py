import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURACIÓN ---
# Define los permisos que necesitará el script.
SCOPES = ["https://www.googleapis.com/auth/forms.body"]

# Título del formulario que se creará.
FORM_TITLE = "Cuestionario de Análisis de Datos en Azure"

# --- DATOS DE LAS PREGUNTAS ---
# Aquí se definen todas las preguntas y secciones del formulario.
SECTIONS_DATA = [
    {
        "title": "Sección 1: Implementar y Administrar una Solución de Análisis",
        "description": "Preguntas relacionadas con la implementación y administración de soluciones de análisis en Azure.",
        "questions": [
            {
                "text": "1. Una empresa está migrando su infraestructura de datos a Azure y necesita una plataforma unificada para el procesamiento de Big Data y el almacenamiento de datos relacionales. Requieres una solución que permita a ingenieros de datos, analistas y científicos de datos colaborar en un mismo entorno, utilizando SQL y Apache Spark. ¿Cuál es el servicio de Azure más adecuado para este requisito?",
                "options": ["Azure Data Lake Storage Gen2", "Azure Cosmos DB", "Azure Synapse Analytics", "Azure SQL Database"]
            },
            {
                "text": "2. Un equipo de analistas de datos necesita explorar rápidamente grandes volúmenes de datos semiestructurados (JSON) almacenados en un data lake en Azure Data Lake Storage Gen2 sin la necesidad de aprovisionar infraestructura de cómputo persistente. Quieren utilizar sus habilidades de SQL para realizar consultas ad-hoc. ¿Qué componente de Azure Synapse Analytics deberían utilizar?",
                "options": ["Grupo de SQL dedicado (Dedicated SQL pool)", "Grupo de Apache Spark (Apache Spark pool)", "Grupo de SQL sin servidor (Serverless SQL pool)", "Data Explorer pool"]
            },
            {
                "text": "3. Tu organización requiere una base de datos relacional altamente escalable en la nube para una nueva aplicación, con el objetivo de minimizar la administración y los costos. La aplicación experimentará cargas variables y necesitará escalar rápidamente de forma automática. ¿Qué servicio de Azure SQL es el más apropiado para este escenario?",
                "options": ["SQL Server en Azure Virtual Machines", "Azure SQL Managed Instance", "Azure SQL Database con configuración sin servidor (serverless)", "Azure SQL Edge"]
            },
            {
                "text": "4. Estás diseñando un sistema para una aplicación de comercio electrónico global que maneja millones de transacciones por día y requiere latencias de lectura y escritura de un solo milisegundo en múltiples regiones. Además, necesitas flexibilidad para almacenar datos semiestructurados (JSON) y una escalabilidad automática. ¿Qué servicio de base de datos de Azure no relacional es el más adecuado?",
                "options": ["Azure Table Storage", "Azure Cosmos DB", "Azure Blob Storage", "Azure Database for PostgreSQL"]
            },
            {
                "text": "5. Un ingeniero de datos está modelando un data warehouse para análisis de ventas históricas. La empresa requiere que las tablas de dimensiones pequeñas (como DimProductCategory) se repliquen en cada nodo de cómputo para minimizar el movimiento de datos durante las uniones con la tabla de hechos. ¿Qué opción de distribución de tabla debería aplicarse a estas tablas de dimensiones en un grupo de SQL dedicado de Azure Synapse Analytics?",
                "options": ["HASH", "ROUND_ROBIN", "REPLICATE", "CLUSTERED COLUMNSTORE INDEX"]
            },
            {
                "text": "6. Una empresa minorista utiliza Azure Cosmos DB para su sistema de inventario y seguimiento de pedidos, y ahora necesita analizar el comportamiento de compra de los clientes en tiempo casi real sin afectar el rendimiento transaccional de la aplicación. Quieren integrar esta capacidad analítica con Azure Synapse Analytics. ¿Cuál es la solución HTAP más adecuada para este escenario?",
                "options": ["Configurar un proceso ETL programado para exportar datos de Cosmos DB a un grupo de SQL dedicado en Synapse.", "Habilitar Azure Synapse Link para Azure Cosmos DB, creando un almacén analítico y conectándolo a Synapse.", "Utilizar Azure Data Factory para copiar datos de Cosmos DB a Azure Data Lake Storage Gen2 y luego procesarlos con Spark.", "Replicar los datos de Cosmos DB a Azure SQL Database y luego usar Synapse Link para SQL."]
            },
            {
                "text": "7. Un arquitecto de datos está planificando el diseño de un data lake en Azure. La solución debe soportar grandes volúmenes de datos estructurados, semiestructurados y no estructurados, y debe ser compatible con las principales tecnologías de procesamiento de Big Data como Apache Spark y Hadoop. ¿Qué servicio de Azure es la base fundamental para construir este data lake?",
                "options": ["Azure Blob Storage (sin configuración adicional)", "Azure Files", "Azure Data Lake Storage Gen2", "Azure SQL Database"]
            },
            {
                "text": "8. Estás diseñando un esquema de data warehouse donde los clientes pueden cambiar su dirección con el tiempo, y los informes históricos deben reflejar la dirección del cliente en el momento de cada venta. ¿Qué tipo de clave y estrategia de dimensión lenta cambiante (SCD) sería más apropiada para la tabla de dimensiones de clientes en un grupo de SQL dedicado de Azure Synapse Analytics?",
                "options": ["Usar una clave subrogada y una SCD Tipo 1 (actualización in-situ).", "Usar una clave subrogada y una SCD Tipo 2 (retención de versiones históricas con nuevas filas).", "Usar solo una clave alternativa y una SCD Tipo 0 (datos inmutables).", "Usar solo una clave alternativa y una SCD Tipo 3 (retención de un atributo limitado)."]
            },
            {
                "text": "9. Una organización necesita migrar una instancia de SQL Server local con múltiples bases de datos y dependencias a nivel de instancia (como linked servers o Service Broker) a la nube. El objetivo es minimizar los cambios de código en las aplicaciones existentes y reducir la carga administrativa del sistema operativo. ¿Qué servicio de Azure SQL es el más adecuado para esta migración?",
                "options": ["SQL Server en Azure Virtual Machines", "Azure SQL Managed Instance", "Azure SQL Database (Single Database)", "Azure SQL Database (Elastic Pool)"]
            },
            {
                "text": "10. Tu empresa necesita una base de datos globalmente distribuida para una aplicación móvil que requiere el modelado de interacciones sociales complejas, donde las entidades (usuarios, publicaciones) y sus relaciones (amigos, me gusta) son cruciales para el análisis. ¿Qué API de Azure Cosmos DB es la más apropiada para este escenario?",
                "options": ["Azure Cosmos DB for NoSQL", "Azure Cosmos DB for MongoDB", "Azure Cosmos DB for Apache Gremlin", "Azure Cosmos DB for Table"]
            },
            {
                "text": "11. Estás trabajando con un conjunto de datos en un data lake que contiene registros de eventos de sensores. Estos datos están particionados por año y mes en la estructura de carpetas (por ejemplo, /events/year=2023/month=01/). Quieres consultar solo los datos de enero y febrero de 2023 usando un grupo de SQL sin servidor en Azure Synapse Analytics. ¿Cómo deberías construir la ruta BULK para aprovechar el particionamiento?",
                "options": ["BULK '/events/year=2023/month=01/*.*', '/events/year=2023/month=02/*.*'", "BULK '/events/*/*/*.*' con WHERE filepath(1) = '2023' AND filepath(2) IN ('01', '02')", "BULK '/events/year=2023/month=*/'  con WHERE month = '01' OR month = '02'", "BULK '/events/year=2023/month=01/*.*' únicamente."]
            },
            {
                "text": "12. Un científico de datos necesita acceder a archivos de datos en un data lake para exploración y modelado. Los datos pueden ser de cualquier formato (estructurado, semiestructurado, no estructurado). ¿Cuál es la forma más directa para que este usuario trabaje con los datos en un data lake en Azure Synapse Analytics?",
                "options": ["Consultar tablas en un data warehouse relacional en un grupo de SQL dedicado.", "Consumir datos preagregados en un modelo analítico o cubo.", "Trabajar directamente con los archivos de datos en el data lake utilizando grupos de Spark.", "Utilizar Azure SQL Database para importar y consultar los datos."]
            },
            {
                "text": "13. Un equipo de desarrollo necesita una solución de base de datos no relacional que ofrezca compatibilidad con las API de MongoDB y una escalabilidad elástica, además de integración con Azure Synapse Link. ¿Qué servicio de Azure Cosmos DB es el más adecuado para sus necesidades?",
                "options": ["Azure Cosmos DB for NoSQL", "Azure Cosmos DB for MongoDB", "Azure Cosmos DB for Table", "Azure Cosmos DB for PostgreSQL"]
            },
            {
                "text": "14. Estás diseñando un data warehouse en Azure Synapse Analytics para un gran volumen de datos de hechos (fact data). Es crucial optimizar el rendimiento de las consultas para cargas de trabajo analíticas que involucran uniones y agregaciones de millones de registros. ¿Qué tipo de índice es el más recomendado para estas tablas de hechos grandes en un grupo de SQL dedicado?",
                "options": ["CLUSTERED INDEX", "NONCLUSTERED INDEX", "CLUSTERED COLUMNSTORE INDEX", "HEAP"]
            },
            {
                "text": "15. Tu empresa quiere utilizar Microsoft Fabric como su solución unificada de análisis de datos a gran escala. Han oído hablar de \"OneLake\". ¿Cuál es la principal característica y beneficio de OneLake en este contexto?",
                "options": ["Es un servicio de base de datos relacional altamente optimizado para OLTP.", "Es un data lake lógico unificado para toda la organización, construido sobre ADLS Gen2, que almacena datos en formato Delta Parquet.", "Es una herramienta de visualización de datos en tiempo real que se integra con Power BI.", "Es un servicio de procesamiento de streaming de datos que reemplaza a Azure Stream Analytics."]
            },
            {
                "text": "16. Un ingeniero de datos está implementando una solución analítica en Azure Synapse Analytics y necesita una forma de proporcionar una capa relacional sobre archivos en un data lake, permitiendo que las aplicaciones cliente consulten estos datos como si estuvieran en una base de datos relacional estándar, sin mover los datos. ¿Qué concepto de Azure Synapse Analytics describe mejor esta funcionalidad?",
                "options": ["Tablas internas en un grupo de SQL dedicado.", "Vistas sobre tablas internas de un grupo de Apache Spark.", "Almacén analítico de Azure Cosmos DB.", "Un almacén de datos lógico (Logical Data Warehouse) utilizando tablas externas y vistas en un grupo de SQL sin servidor."]
            },
            {
                "text": "17. Estás diseñando un proceso de ingesta de datos donde la integridad referencial y las restricciones de unicidad son críticas durante la carga de datos en un data warehouse relacional. ¿Qué característica de Azure Synapse Analytics debes considerar cuidadosamente al crear tablas en un grupo de SQL dedicado?",
                "options": ["Las tablas de hechos deben usar índices CLUSTERED COLUMNSTORE INDEX.", "Los grupos de SQL dedicados de Synapse Analytics no admiten restricciones de clave externa y única.", "La distribución ROUND_ROBIN es la opción predeterminada para todas las tablas.", "Solo se pueden usar claves subrogadas para garantizar la unicidad."]
            },
            {
                "text": "18. Tu organización ha implementado un data lake en Azure Data Lake Storage Gen2 y necesita habilitar un sistema de archivos jerárquico para una mejor organización de datos y optimización de costos. ¿Qué característica clave debes habilitar en tu cuenta de almacenamiento de Azure para lograr esto?",
                "options": ["La replicación global.", "El soporte para Blob Storage Hot tier.", "El espacio de nombres jerárquico (Hierarchical namespace).", "El soporte para la API de Table Storage."]
            },
            {
                "text": "19. Un equipo de desarrollo necesita almacenar grandes cantidades de datos semiestructurados que provienen de diferentes aplicaciones, donde la estructura de los documentos puede variar ligeramente entre las instancias. Quieren una solución de almacenamiento NoSQL flexible. ¿Qué formato de archivo o tipo de base de datos no relacional es comúnmente utilizado para este tipo de datos en Azure?",
                "options": ["Delimited text files (CSV)", "Avro", "JavaScript Object Notation (JSON)", "ORC (Optimized Row Columnar format)"]
            },
            {
                "text": "20. Una empresa de análisis de mercado necesita almacenar datos de ventas que consisten en medidas numéricas (ej. ingresos, cantidad vendida) y quieren agregarlas por diferentes dimensiones como cliente, producto y fecha. ¿Qué tipo de tabla es el más adecuado para almacenar estas medidas numéricas y sus claves dimensionales asociadas en un data warehouse?",
                "options": ["Tabla de dimensiones (Dimension table)", "Tabla de hechos (Fact table)", "Tabla de staging (Staging table)", "Tabla externa (External table)"]
            }
        ]
    },
    {
        "title": "Sección 2: Ingerir y Transformar Datos",
        "description": "Preguntas sobre la ingesta y transformación de datos en soluciones de Azure.",
        "questions": [
            {
                "text": "21. Estás diseñando una pipeline en Azure Synapse Analytics para ingerir datos desde diversas fuentes operativas a un data lake, realizando transformaciones de limpieza y reestructuración de los datos. La pipeline necesita orquestar actividades y utilizar servicios externos. ¿Qué elementos principales componen una pipeline en Azure Synapse Analytics para lograr esto?",
                "options": ["Azure Functions y Azure Logic Apps.", "Actividades, entornos de ejecución de integración (Integration Runtime), servicios vinculados (Linked Services) y conjuntos de datos (Datasets).", "Grupos de SQL dedicados y grupos de Apache Spark.", "Azure Event Hubs y Azure Stream Analytics."]
            },
            {
                "text": "22. Un ingeniero de datos está implementando un proceso ETL (Extract, Transform, Load) donde los datos se extraen de fuentes operacionales, se transforman para su análisis y luego se cargan en un data warehouse. Recientemente, el equipo ha comenzado a utilizar un enfoque ELT (Extract, Load, Transform). ¿Cuál es la diferencia clave entre ETL y ELT en el contexto de la ingesta de datos a gran escala?",
                "options": ["En ETL, la transformación ocurre después de la carga; en ELT, la transformación ocurre antes.", "ETL se usa solo para datos estructurados; ELT se usa para todos los tipos de datos.", "En ETL, los datos se transforman antes de cargarse en un almacén analítico; en ELT, los datos se copian al almacén y luego se transforman.", "ETL usa SQL; ELT usa Apache Spark."]
            },
            {
                "text": "23. Un conjunto de datos de ventas está almacenado en un data lake en formato CSV sin una fila de encabezado. Necesitas cargarlo en un dataframe de Spark y especificar un esquema explícito para las columnas (ID del Producto, Nombre del Producto, Precio). ¿Cuál es el enfoque correcto utilizando PySpark en un notebook de Azure Synapse Analytics?",
                "options": ["Usar spark.read.csv(..., header=True, inferSchema=True).", "Usar spark.read.load(..., format='csv', header=False) y definir un StructType para el schema.", "Usar OPENROWSET en un grupo de SQL sin servidor.", "Convertir el CSV a Parquet antes de cargarlo."]
            },
            {
                "text": "24. Necesitas transformar datos de ventas que están en un data lake. La transformación implica filtrar filas, crear nuevas columnas derivadas (por ejemplo, Año y Mes a partir de FechaPedido) y guardar los resultados como una tabla externa de Delta Lake particionada por Año y Mes. ¿Cuál es la secuencia de pasos más eficiente en un grupo de Apache Spark en Azure Synapse Analytics?",
                "options": ["Cargar los datos en un dataframe, usar withColumn para las columnas derivadas, luego saveAsTable con partitionBy.", "Usar la declaración CREATE EXTERNAL TABLE AS SELECT (CETAS) en un grupo de SQL sin servidor.", "Cargar los datos directamente en una tabla de SQL dedicado y luego usar INSERT INTO con GROUP BY.", "Utilizar una actividad de Data Flow en una pipeline para realizar todas las transformaciones y guardar los resultados."]
            },
            {
                "text": "25. Un ingeniero de datos está trabajando con un archivo JSON en un data lake que contiene objetos anidados, como información de dirección dentro de un objeto cliente. Necesitas consultar estos datos utilizando un grupo de SQL sin servidor en Azure Synapse Analytics y extraer los campos anidados directamente en columnas. ¿Qué característica de la función OPENROWSET es esencial para lograr esto?",
                "options": ["Usar el parámetro HEADER_ROW = TRUE.", "Especificar el FIELDTERMINATOR.", "Usar la cláusula WITH con rutas JSON explícitas (por ejemplo, $.address.street).", "Convertir el archivo JSON a CSV antes de la consulta."]
            },
            {
                "text": "26. Estás diseñando una pipeline de datos para cargar datos a gran escala desde un data lake en Azure Data Lake Storage Gen2 a un data warehouse relacional en un grupo de SQL dedicado de Azure Synapse Analytics. La pipeline debe ser capaz de orquestar el movimiento de datos y aplicar transformaciones complejas de limpieza y estandarización. ¿Qué actividad es la más adecuada en una pipeline de Azure Synapse Analytics para estas transformaciones complejas?",
                "options": ["Actividad de Copy Data (Copy Data activity).", "Actividad de Stored Procedure (Stored Procedure activity).", "Actividad de Data Flow (Data Flow activity).", "Actividad de Lookup (Lookup activity)."]
            },
            {
                "text": "27. Una empresa necesita almacenar grandes archivos binarios (imágenes, videos) en Azure que se acceden con poca frecuencia pero deben estar disponibles cuando se solicitan. ¿Qué tipo de blob de Azure Blob Storage y qué nivel de acceso serían más adecuados para este escenario?",
                "options": ["Block blobs en el nivel Hot.", "Page blobs en el nivel Cool.", "Block blobs en el nivel Archive.", "Append blobs en el nivel Hot."]
            },
            {
                "text": "28. Quieres realizar una transformación de datos utilizando un grupo de SQL sin servidor en Azure Synapse Analytics que implica filtrar y agregar datos, y luego guardar los resultados en una nueva tabla externa en el data lake en formato Parquet. ¿Qué tipo de declaración SQL es la más adecuada para este propósito?",
                "options": ["INSERT INTO ... SELECT ...", "UPDATE ... SET ... FROM ...", "CREATE EXTERNAL TABLE AS SELECT (CETAS)", "MERGE INTO ... USING ..."]
            },
            {
                "text": "29. Estás trabajando con un flujo continuo de datos de sensores (streaming data) en Azure Synapse Analytics. Necesitas unificar el almacenamiento para datos de streaming y por lotes, y aplicar consistencia transaccional y aplicación de esquemas. ¿Qué tecnología de código abierto, compatible con Apache Spark, ofrece estas capacidades en un data lakehouse?",
                "options": ["Apache Hadoop", "Apache Avro", "Delta Lake", "Apache Hive"]
            },
            {
                "text": "30. Un ingeniero de datos necesita automatizar la ejecución de un notebook de Spark que realiza transformaciones de datos complejas como parte de una solución ETL. ¿Cómo se puede integrar este notebook en un flujo de trabajo programado dentro de Azure Synapse Analytics?",
                "options": ["Ejecutando el notebook manualmente cada vez que se necesite.", "Utilizando una actividad de Stored Procedure para llamar al notebook.", "Incluyendo el notebook en una pipeline de Azure Synapse Analytics mediante una actividad de Notebook.", "Exportando el código del notebook a un script de Python y ejecutándolo como una Azure Function."]
            },
            {
                "text": "31. Tienes archivos Parquet en un data lake y necesitas consultarlos eficientemente usando un grupo de SQL sin servidor en Azure Synapse Analytics. ¿Cuál es el método más sencillo y eficaz, dado que el esquema ya suele estar incrustado en el archivo Parquet?",
                "options": ["Usar OPENROWSET con FORMAT = 'csv'.", "Usar OPENROWSET con FORMAT = 'parquet' y especificar la ruta.", "Crear primero una tabla externa de Delta Lake y luego consultarla.", "Cargar los datos en un grupo de SQL dedicado."]
            },
            {
                "text": "32. Una empresa necesita una solución para ingerir datos de un data lake, limpiarlos y transformarlos, y luego cargarlos en un data warehouse, con la capacidad de reutilizar la lógica de transformación en diferentes aplicaciones. ¿Qué objeto de base de datos es el más adecuado para encapsular esta lógica SQL compleja y permitir su reutilización en Azure Synapse Analytics?",
                "options": ["Vista (View)", "Función definida por el usuario (User-defined function)", "Procedimiento almacenado (Stored procedure)", "Índice (Index)"]
            },
            {
                "text": "33. Estás configurando una pipeline de Azure Synapse Analytics para orquestar la ingesta y transformación de datos. Algunos datos provienen de un servidor FTP y otros de una base de datos local. ¿Qué elemento de la pipeline se utiliza para establecer conexiones seguras a estos servicios externos?",
                "options": ["Datasets (Conjuntos de datos)", "Activities (Actividades)", "Linked Services (Servicios vinculados)", "Integration Runtime (Entorno de ejecución de integración)"]
            },
            {
                "text": "34. Una empresa está procesando datos de eventos en tiempo real desde dispositivos IoT. Quieren procesar cada evento a medida que llega para obtener información instantánea, sin esperar a que se acumule un lote de datos. ¿Qué paradigma de procesamiento de datos es el más adecuado para este escenario?",
                "options": ["Procesamiento por lotes (Batch processing).", "Procesamiento por streaming (Stream processing).", "Procesamiento transaccional (Transactional processing).", "Procesamiento OLAP (Online Analytical Processing)."]
            },
            {
                "text": "35. Tienes un dataframe de Spark en un notebook de Azure Synapse Analytics y quieres guardarlo como un conjunto de archivos particionados por una columna derivada (por ejemplo, Año). ¿Qué método de escritura del dataframe de Spark es el más adecuado para esta tarea?",
                "options": ["saveAsTable()", "write.csv()", "write.partitionBy().parquet()", "toPandas().to_csv()"]
            },
            {
                "text": "36. En el contexto de los data lakes, ¿cuál es la ventaja principal de utilizar formatos de archivo como Parquet o ORC en comparación con CSV o JSON, especialmente para cargas de trabajo analíticas?",
                "options": ["Son más fáciles de leer por humanos.", "Ofrecen mejor compresión y están optimizados para el procesamiento columnar, mejorando el rendimiento de las consultas.", "Permiten una mayor flexibilidad en el esquema de datos.", "Son formatos row-based, lo que los hace ideales para la ingesta de datos."]
            },
            {
                "text": "37. Estás construyendo una pipeline de Azure Synapse Analytics que necesita ejecutar un procedimiento almacenado en un grupo de SQL sin servidor. ¿Cuál es la secuencia de actividades dentro de la pipeline para eliminar una carpeta de datos existente y luego ejecutar el procedimiento almacenado que crea una tabla externa con datos transformados?",
                "options": ["Una actividad de Stored Procedure seguida de una actividad de Delete.", "Una actividad de Delete seguida de una actividad de Stored Procedure.", "Dos actividades de Stored Procedure, una para eliminar y otra para crear.", "Una actividad de Data Flow que contiene la lógica de eliminación y creación."]
            }
        ]
    },
    {
        "title": "Sección 3: Supervisar y Optimizar una Solución de Análisis",
        "description": "Preguntas sobre la supervisión, optimización y seguridad de soluciones analíticas en Azure.",
        "questions": [
            {
                "text": "38. Estás administrando un grupo de SQL dedicado en Azure Synapse Analytics. Durante los periodos de baja actividad, quieres minimizar los costos de cómputo. ¿Qué acción puedes realizar para lograr este objetivo sin eliminar la base de datos?",
                "options": ["Escalar el grupo de SQL dedicado a su nivel de rendimiento más bajo (DW100c).", "Pausar el grupo de SQL dedicado.", "Escalar el grupo de SQL dedicado a un grupo de SQL sin servidor.", "Deshabilitar el autoscale en el grupo de SQL dedicado."]
            },
            {
                "text": "39. En un entorno de Azure Synapse Analytics muy concurrido, el CEO se queja de que sus consultas a veces son lentas debido a otras cargas de trabajo pesadas. Quieres asegurar que las consultas del CEO tengan prioridad sobre otras tareas en espera. ¿Qué característica de gestión de cargas de trabajo en un grupo de SQL dedicado deberías configurar?",
                "options": ["Workload Classification (Clasificación de cargas de trabajo).", "Workload Importance (Importancia de cargas de trabajo).", "Workload Isolation (Aislamiento de cargas de trabajo).", "Escalar el grupo de SQL dedicado."]
            },
            {
                "text": "40. Estás monitoreando el rendimiento de las consultas en un grupo de SQL dedicado de Azure Synapse Analytics. Necesitas identificar las consultas que están tardando más tiempo en ejecutarse para poder optimizarlas. ¿Qué vista de administración dinámica (DMV) deberías consultar para obtener esta información?",
                "options": ["sys.dm_pdw_exec_sessions", "sys.dm_pdw_exec_requests", "sys.dm_pdw_sql_requests", "sys.dm_pdw_dms_workers"]
            },
            {
                "text": "41. Un administrador de Azure quiere optimizar el costo y el rendimiento de los recursos de Azure Synapse Analytics. Necesita recomendaciones personalizadas basadas en las mejores prácticas. ¿Qué servicio de Azure proporciona automáticamente estas recomendaciones?",
                "options": ["Azure Monitor", "Azure Advisor", "Azure Security Center", "Azure Cost Management"]
            },
            {
                "text": "42. Una empresa necesita asegurarse de que un representante de servicio al cliente solo pueda ver los últimos cuatro dígitos de un número de tarjeta de crédito, mientras que los usuarios privilegiados puedan ver el número completo. Esta restricción debe aplicarse a nivel de base de datos. ¿Qué característica de seguridad en Azure Synapse Analytics es la más adecuada para este requisito?",
                "options": ["Seguridad a nivel de fila (Row-Level Security - RLS).", "Seguridad a nivel de columna (Column-Level Security - CLS).", "Dynamic Data Masking (DDM).", "Transparent Data Encryption (TDE)."]
            },
            {
                "text": "43. Estás administrando un grupo de Apache Spark en Azure Synapse Analytics. Los requisitos de recursos para tus cargas de trabajo varían significativamente con el tiempo. ¿Qué característica puedes habilitar para ajustar automáticamente el número de nodos en el clúster, escalando hacia arriba y hacia abajo según la demanda?",
                "options": ["Establecer un número fijo de nodos.", "Habilitar la característica Autoscale (Autoescalado) para el grupo de Spark.", "Pausar y reanudar el grupo manualmente.", "Reducir el tamaño de la VM de los nodos."]
            },
            {
                "text": "44. Un ingeniero de datos está investigando una consulta de SQL dedicado que está tardando más de lo esperado. Sospecha que el problema puede estar relacionado con el movimiento de datos debido a una mala estrategia de distribución de la tabla. ¿Qué DMV sería la más útil para investigar las operaciones de movimiento de datos de los pasos de la consulta distribuida?",
                "options": ["sys.dm_pdw_exec_requests", "sys.dm_pdw_request_steps", "sys.dm_pdw_dms_workers", "sys.dm_pdw_sql_requests"]
            },
            {
                "text": "45. Una organización requiere que los datos en reposo de su data warehouse en Azure Synapse Analytics estén protegidos contra el acceso malicioso sin necesidad de modificar las aplicaciones. La solución debe realizar el cifrado y descifrado en tiempo real de la base de datos, las copias de seguridad y los archivos de registro de transacciones. ¿Qué característica de seguridad es la más adecuada para esto?",
                "options": ["Dynamic Data Masking (DDM).", "Seguridad a nivel de fila (RLS).", "Transparent Data Encryption (TDE).", "Virtual Networks (Redes Virtuales)."]
            },
            {
                "text": "46. Estás implementando una política de seguridad que restringe el acceso a las filas de datos en una tabla de ventas, de modo que cada vendedor solo pueda ver los registros de ventas de sus propios clientes. ¿Qué característica de seguridad a nivel de base de datos es la más apropiada para esta implementación en Azure Synapse Analytics?",
                "options": ["Seguridad a nivel de columna (CLS).", "Dynamic Data Masking (DDM).", "Seguridad a nivel de fila (Row-Level Security - RLS).", "Transparent Data Encryption (TDE)."]
            },
            {
                "text": "47. Un data engineer necesita optimizar una consulta lenta en un grupo de SQL dedicado. Los resultados de sys.dm_pdw_request_steps muestran que un paso DSQL está tardando mucho tiempo. Para obtener el plan estimado de SQL Server para ese paso específico en una distribución particular, ¿qué comando debería usar?",
                "options": ["SELECT * FROM sys.dm_pdw_exec_requests", "DBCC PDW_SHOWEXECUTIONPLAN", "ALTER INDEX ALL ON", "CREATE STATISTICS"]
            },
            {
                "text": "48. Tu organización ha implementado un Azure Synapse Analytics Workspace y quiere restringir el acceso a los puntos finales públicos (Dedicated SQL pools, Serverless SQL pool, etc.) utilizando reglas basadas en la dirección IP de los clientes. ¿Qué objeto de seguridad de red debería configurar primero?",
                "options": ["Virtual Network (Red Virtual).", "Private Endpoints (Puntos de conexión privados).", "Firewall rules (Reglas de firewall).", "Network Security Groups (Grupos de seguridad de red)."]
            },
            {
                "text": "49. Estás implementando el control de acceso a una base de datos en un grupo de SQL sin servidor de Azure Synapse Analytics. Quieres otorgar permisos a un usuario externo que no forma parte de tu Microsoft Entra ID. ¿Qué tipo de autenticación y objeto de base de datos serían los más adecuados para esto?",
                "options": ["Autenticación de Microsoft Entra ID y asignación directa del usuario.", "Autenticación SQL, creando un usuario directamente en la base de datos del grupo de SQL sin servidor.", "Managed Identity, asignada al usuario.", "Shared Access Signatures (SAS) para el usuario."]
            },
            {
                "text": "50. Una consulta en un grupo de SQL dedicado de Azure Synapse Analytics implica una función de agregación COUNT(DISTINCT...) sobre una columna con un gran volumen de datos, y está tardando mucho en ejecutarse. Para una exploración inicial de datos, no se requiere un recuento preciso, sino una estimación rápida. ¿Qué función puedes usar para optimizar el tiempo de respuesta de la consulta?",
                "options": ["SUM()", "AVG()", "APPROX_COUNT_DISTINCT()", "MAX()"]
            },
            {
                "text": "51. Un data engineer ha creado un grupo de SQL dedicado en Azure Synapse Analytics y necesita asegurarse de que el tiempo de inactividad de cómputo se minimice durante la noche para reducir costos. ¿Qué opción de configuración permite que el grupo se pause automáticamente después de un período de inactividad?",
                "options": ["Configurar un WORKLOAD CLASSIFIER con IMPORTANCE = Low.", "Utilizar Azure Advisor para recomendaciones de costos.", "Activar la función de auto-pausa para el grupo de SQL dedicado en Azure Synapse Studio.", "Configurar un MIN_PERCENTAGE_RESOURCE = 0 en el grupo de cargas de trabajo."]
            },
            {
                "text": "52. Tu equipo de seguridad requiere un aislamiento completo de los recursos para ciertas cargas de trabajo críticas que se ejecutan en un grupo de SQL dedicado de Azure Synapse Analytics, garantizando que siempre tengan una cantidad mínima de recursos disponibles, incluso bajo alta demanda del sistema. ¿Qué característica de gestión de cargas de trabajo proporciona esta capacidad?",
                "options": ["Workload Classification (Clasificación de cargas de trabajo).", "Workload Importance (Importancia de cargas de trabajo).", "Workload Isolation (Aislamiento de cargas de trabajo).", "Escalado dinámico del pool."]
            }
        ]
    }
]

def get_credentials():
    """Obtiene las credenciales del usuario.

    Se encarga del flujo de autenticación OAuth 2.0. Si el usuario ya se ha
    autenticado, carga las credenciales desde 'token.json'. De lo contrario,
    inicia un flujo de autenticación basado en navegador utilizando
    'credentials.json' y guarda las nuevas credenciales para el futuro.
    """
    creds = None
    # El archivo token.json almacena los tokens de acceso y actualización del usuario.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Si no hay credenciales válidas, permite que el usuario inicie sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Asegúrate de que el archivo 'credentials.json' descargado de Google Cloud exista.
            if not os.path.exists("credentials.json"):
                print("Error: El archivo 'credentials.json' no se encontró.")
                print("Por favor, sigue las instrucciones en INSTRUCCIONES.md para obtenerlo.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Guarda las credenciales para la próxima ejecución
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def create_form(creds):
    """Crea el formulario de Google Forms y añade las preguntas."""
    try:
        # Construye el servicio de la API de Google Forms
        forms_service = build("forms", "v1", credentials=creds)

        # 1. Crear el formulario con el título y la descripción de la primera sección
        first_section = SECTIONS_DATA[0]
        form_info = {
            "title": FORM_TITLE,
            "documentTitle": FORM_TITLE,
            "description": f"{first_section['title']}\n{first_section.get('description', '')}"
        }
        created_form = forms_service.forms().create(body={"info": form_info}).execute()
        form_id = created_form["formId"]
        print(f"Formulario '{FORM_TITLE}' creado con éxito.")
        print(f"ID del formulario: {form_id}")

        # 2. Construir la lista de solicitudes para añadir todas las preguntas y los saltos de sección
        requests = []

        # Iterar sobre todas las secciones
        for section_index, section in enumerate(SECTIONS_DATA):
            # Añadir un salto de página para crear una nueva sección (excepto antes de la primera)
            if section_index > 0:
                requests.append({
                    "createItem": {
                        "item": {
                            "title": section["title"],
                            "description": section.get("description", ""),
                            "pageBreakItem": {},
                        },
                        "location": {"index": len(requests)}, # Append at the end
                    }
                })

            # Añadir las preguntas de la sección actual
            for question_data in section["questions"]:
                requests.append({
                    "createItem": {
                        "item": {
                            "title": question_data["text"],
                            "questionItem": {
                                "question": {
                                    "required": False,
                                    "choiceQuestion": {
                                        "type": "RADIO",
                                        "options": [{"value": opt} for opt in question_data["options"]],
                                    },
                                }
                            },
                        },
                        "location": {"index": len(requests)}, # Append at the end
                    }
                })

        # 3. Ejecutar la solicitud por lotes para añadir todos los items
        if requests:
            forms_service.forms().batchUpdate(
                formId=form_id, body={"requests": requests}
            ).execute()

        print(f"Se han añadido {len(requests)} items (preguntas y saltos de página) al formulario.")
        print("\n¡Proceso completado!")
        print(f"Puedes ver y editar tu formulario en: {created_form['responderUri']}")

    except HttpError as err:
        # Provide more details on HttpError
        error_details = err.reason
        if err.content:
            try:
                error_details = f"{err.reason}: {err.content.decode()}"
            except (UnicodeDecodeError, AttributeError):
                pass
        print(f"Ocurrió un error con la API de Google Forms: {error_details}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    print("Iniciando la creación del formulario de Google Forms...")
    credentials = get_credentials()
    if credentials:
        create_form(credentials)
    else:
        print("No se pudieron obtener las credenciales. Abortando.")
