## dentist-art-studio
Plataforma para clientes de dentist art studio 

## Descripción

DentistArt Studio es una aplicación diseñada para facilitar el proceso de ordenar prótesis dentales. Permite a los usuarios llenar un formato de orden para una pieza protésica, lo que agiliza y organiza el proceso de pedido.

## Instalación

Para instalar DentistArt Studio, sigue estos pasos:

```bash
# Clonar repositorio
git clone https://github.com/franktl1320/dentist-art-studio.git

# Navegar al directorio del proyecto
cd dentist-art-studio

```

## Configuración de la Base de Datos

Para configurar la base de datos localmente, sigue estos pasos:

1. Asegúrate de tener `sqlite3` instalado en tu sistema.
2. Navega al directorio del proyecto en tu terminal.
3. Ejecuta el siguiente comando para crear la base de datos utilizando el archivo `schema.sql`:

```bash
    sqlite3 database.db < schema.sql
```

Esto creará un archivo `database.db` en el directorio del proyecto basado en la estructura definida en `schema.sql`.

