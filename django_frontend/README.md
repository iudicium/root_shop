![Stylus](https://img.shields.io/badge/Stylus-333333?logo=stylus)
![HTML](https://img.shields.io/badge/HTML-E34F26?logo=html5)
![CSS](https://img.shields.io/badge/CSS-1572B6?logo=css3)
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?logo=vue.js)
![jQuery](https://img.shields.io/badge/jQuery-0769AD?logo=jquery)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript)
![Git](https://img.shields.io/badge/Git-F05032?logo=git)
![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github)

## OverView
This project represents a plug-in Django application that handles the display of web pages, while data retrieval occurs through an API, which needs to be implemented as part of a task.



## Package Integration
1. Build the package: in the frontend directory, run the command python setup.py sdist. 
3. Install the generated package into the virtual environment: `pip install frontent.version.version.tar.gz`
4.  Replace X and Y with the version numbers, which can vary depending on the current package version.
4. Add the application to settings.py 'settings.py' of the project

```python
INSTALLED_APPS = [
        ...
        'frontend',
    ]
```
4. Add to `urls.py` :
```python
urlpatterns = [
    path("", include("frontend.urls")),
    ...
]
```
5. Run the server, and done! python manage.py runserver, default :8000