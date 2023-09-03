# Python Fortress

Python Fortress es una librería que facilita la interacción con la API para recuperar un archivo `.env`. Está diseñada para cargar de forma segura y eficiente las variables de entorno desde una fuente remota.

[![codecov](https://codecov.io/gh/magestree/python_fortress/branch/main/graph/badge.svg)](https://codecov.io/gh/magestree/python_fortress)

## Características

- Carga fácil de credenciales y configuraciones desde variables de entorno.
- Recuperación segura del contenido del archivo `.env` desde una API.
- Uso sencillo y eficiente con métodos intuitivos.

## Instalación

Para instalar las dependencias del proyecto, ejecuta:

```bash
pip install -r requirements.txt
```

## Uso básico

El módulo principal fortress.py proporciona la clase `Fortress` y una función de conveniencia `load_env()`.

Ejemplo:
```python
from fortress import load_env

# Carga las variables del archivo .env en las variables de entorno.
load_env()
```

## Tests
El proyecto viene con un conjunto de tests para garantizar que todo funcione correctamente. Puedes ejecutar los tests usando pytest:
```bash
pytest
```

Para obtener un informa de cobertura:
```bash
coverage run -m pytest
coverage report
```

## CI/CD
Gracias a GitHub Actions, cada push o pull request activará la pipeline de CI que ejecutará los tests y calculará la cobertura de código.


## Contribución
Si estás interesado en contribuir al proyecto, por favor, sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu característica o corrección.
3. Implementa tu cambio o corrección.
4. Ejecuta los tests para asegurarte de que todo funciona como se espera.
5. Abre un pull request.


## Licencia
MIT
