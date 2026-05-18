# DB Query - Visualización de Programas Sociales

Aplicación desarrollada en **Streamlit** para consultar, transformar y visualizar información relacionada con programas sociales, beneficiarios, viviendas y registros del Sistema CHECS.

## Descripción

Este proyecto contiene herramientas para conectarse a fuentes de datos institucionales, procesar información de programas sociales y mostrar indicadores en tableros interactivos.

La aplicación permite visualizar información por individuo o por vivienda, generar tablas resumen, aplicar filtros y descargar resultados en Excel o CSV.

El proyecto utiliza conexiones a **SQL Server** para consultar vistas de datos y **MongoDB** para manejar usuarios y autenticación.

## Funcionalidades principales

- Inicio de sesión con usuario y contraseña.
- Consulta de información desde SQL Server.
- Consulta de usuarios desde MongoDB.
- Visualización de indicadores de programas sociales.
- Visualización de registros por individuo.
- Visualización de registros por vivienda.
- Análisis por estatus de beneficiario.
- Análisis por tipo de pobreza o carencia.
- Filtros por sexo, edad, municipio y origen.
- Descarga de resultados en Excel o CSV.
- Inicialización de usuarios desde archivo CSV hacia MongoDB.

## Archivos principales

```text
.
├── app.py
├── app_pi.py
├── checs.py
├── connection.py
├── initialize_mongo_users.py
├── visualization.py
├── experimentation.ipynb
├── auxiliar
└── utils
    ├── authentication.py
    ├── config.py
    ├── data.py
    ├── database.py
    └── dict_utils.py
```

### `app.py`

Aplicación en Streamlit para consultar información general del Sistema CHECS.

Incluye módulos para visualizar:

- Estatus del Sistema CHECS.
- Algoritmo de pobreza o carencia.
- Filtros por sexo, edad, municipio y origen.
- Tablas resumen por programa y estatus.

### `app_pi.py`

Aplicación en Streamlit enfocada en información de **primera infancia**.

Permite consultar datos desde la vista SQL `VW_PRIMERA_INFANCIA`, aplicar filtros y descargar información en formato CSV.

### `visualization.py`

Aplicación principal de visualización de datos.

Permite elegir entre:

- Visualización por individuo.
- Visualización por vivienda.

Genera tablas resumen y archivos descargables en Excel con indicadores de programas sociales y situación socioeconómica.

### `connection.py`

Script auxiliar para probar la conexión a SQL Server y consultar información desde la vista `VW_PRIMERA_INFANCIA`.

### `checs.py`

Script de prueba para consultar información del Sistema CHECS desde SQL Server.

### `initialize_mongo_users.py`

Script para cargar usuarios desde un archivo CSV hacia MongoDB.

Lee usuarios desde:

```text
auxiliar/users.csv
```

y los inserta en la base de datos:

```text
query_database.users
```

### `utils/authentication.py`

Contiene la lógica de autenticación de usuarios.

Consulta los usuarios almacenados en MongoDB y valida correo, contraseña y rol.

### `utils/config.py`

Contiene la clase `Config`, encargada de leer el archivo de configuración `config.yml`.

### `utils/database.py`

Contiene funciones auxiliares para:

- Crear conexión con MongoDB.
- Convertir cursores de MongoDB a DataFrames.
- Preparar diccionarios de datos para tickets o registros.

### `utils/data.py`

Contiene funciones para cargar, transformar y exportar datos.

Incluye transformaciones para generar:

- Indicadores por individuo.
- Indicadores por tipo de pobreza.
- Indicadores por vivienda.
- Indicadores de pobreza por vivienda.
- Archivos Excel descargables.

### `utils/dict_utils.py`

Contiene diccionarios auxiliares para traducir claves numéricas a etiquetas legibles.

Por ejemplo, transforma estatus de beneficiario como:

- Validando.
- Validado.
- Solicitud de Apoyo.
- Beneficiado(a).
- Cancelada.
- Duplicado.
- Rechazado.
- Por solicitar.

## Requisitos

Para ejecutar el proyecto se recomienda contar con Python 3.8 o superior.

Instala las dependencias principales con:

```bash
pip install streamlit pandas pymongo pymssql sqlalchemy plotly pillow pyyaml xlsxwriter pyxlsb
```

También puede ser necesario instalar un driver compatible para SQL Server, dependiendo del entorno donde se ejecute la aplicación.

## Configuración requerida

Para que el proyecto funcione correctamente, es necesario crear un archivo llamado:

```text
config.yml
```

en la raíz del repositorio.

El archivo debe incluir credenciales para MongoDB y, si se utilizará conexión a SQL Server, también credenciales SQL.

Formato sugerido:

```yaml
db_mongo:
  user: "TU_USUARIO_MONGO"
  password: "TU_PASSWORD_MONGO"
  cluster: "TU_CLUSTER_MONGO"

sql:
  USERNAME: "TU_USUARIO_SQL"
  PASSWORD: "TU_PASSWORD_SQL"
  SERVER: "TU_SERVIDOR_SQL"
  DATABASE: "TU_BASE_DE_DATOS"
  DRIVER: "TU_DRIVER_SQL"
```

Ejemplo:

```yaml
db_mongo:
  user: "usuario_demo"
  password: "password_demo"
  cluster: "cluster0.xxxxx.mongodb.net"

sql:
  USERNAME: "usuario_sql"
  PASSWORD: "password_sql"
  SERVER: "servidor.database.windows.net"
  DATABASE: "base_datos"
  DRIVER: "ODBC Driver 17 for SQL Server"
```

La conexión a MongoDB se construye con el siguiente formato:

```python
mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority
```

La conexión a SQL Server se construye con el siguiente formato:

```python
mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}
```

## Ejecución

Para ejecutar la visualización principal:

```bash
streamlit run visualization.py
```

Para ejecutar la aplicación general de CHECS:

```bash
streamlit run app.py
```

Para ejecutar la aplicación de primera infancia:

```bash
streamlit run app_pi.py
```

Para inicializar usuarios en MongoDB:

```bash
python initialize_mongo_users.py
```

## Uso esperado

1. Crear el archivo `config.yml` con las credenciales necesarias.
2. Instalar las dependencias del proyecto.
3. Cargar usuarios en MongoDB, si aún no existen.
4. Ejecutar la aplicación deseada con Streamlit.
5. Iniciar sesión con correo y contraseña.
6. Seleccionar el tipo de visualización.
7. Consultar tablas, filtros e indicadores.
8. Descargar los resultados en Excel o CSV.

## Base de datos MongoDB esperada

El sistema de autenticación espera una base de datos en MongoDB con la siguiente estructura:

```text
query_database
└── users
```

La colección `users` debe contener documentos con un formato similar a:

```json
{
  "user": "correo@ejemplo.com",
  "pass": "password",
  "role": "admin"
}
```

## Vistas SQL esperadas

El proyecto hace referencia a vistas SQL como:

```text
VW_PRIMERA_INFANCIA
VW_PROGRAMAS_SOCIALES_CHECS
visor_sii
```

Estas vistas deben existir en la base de datos configurada para que las consultas funcionen correctamente.

## Archivos auxiliares esperados

Algunas partes del proyecto dependen de archivos locales dentro de la carpeta `auxiliar`, por ejemplo:

```text
auxiliar/users.csv
auxiliar/muns.json
```

También existen rutas absolutas de Windows en algunos scripts, por ejemplo:

```python
C:\NL\visor\visor\auxiliar\users.csv
C:\NL\auxiliar\sii.png
C:\NL\auxiliar\leon.png
```

Para ejecutar el proyecto en otra computadora, se recomienda reemplazar estas rutas absolutas por rutas relativas dentro del repositorio.

Ejemplo recomendado:

```python
pd.read_csv("auxiliar/users.csv")
```

y

```python
Image.open("auxiliar/sii.png")
```

## Consideraciones importantes

El archivo `config.yml` contiene credenciales sensibles, por lo que no debe subirse al repositorio público.

Se recomienda agregarlo al archivo `.gitignore`:

```text
config.yml
```

También se recomienda crear un archivo de ejemplo sin credenciales reales:

```text
config.example.yml
```

Ejemplo de `config.example.yml`:

```yaml
db_mongo:
  user: "TU_USUARIO_MONGO"
  password: "TU_PASSWORD_MONGO"
  cluster: "TU_CLUSTER_MONGO"

sql:
  USERNAME: "TU_USUARIO_SQL"
  PASSWORD: "TU_PASSWORD_SQL"
  SERVER: "TU_SERVIDOR_SQL"
  DATABASE: "TU_BASE_DE_DATOS"
  DRIVER: "TU_DRIVER_SQL"
```

## Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- MongoDB
- PyMongo
- SQL Server
- SQLAlchemy
- PyMSSQL
- Plotly
- Pillow
- YAML
- XlsxWriter

## Objetivo del proyecto

Centralizar la consulta y visualización de información de programas sociales, beneficiarios y viviendas del Sistema CHECS, facilitando la generación de indicadores y archivos descargables para análisis institucional.

## Estado del proyecto

Proyecto en desarrollo para uso interno en actividades de consulta, análisis y visualización de información social e institucional.