 # *R00T SHOP*

*
I've designed a versatile ecommerce framework. It comes equipped with an intuitive user interface and a powerful set of features, ensuring a seamless shopping experience for customers. This framework represents a significant step in enhancing my own skills while providing a valuable resource for others to build their successful online businesses.*




<p align="center">
  <img src="logo_md.png" width="660" height="" alt="R00TK3Y">
</p>


<div style="text-align: center;">
  <img src="https://img.shields.io/badge/Django-3.x-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Vue.js-2.x-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" alt="Vue.js">
  <img src="https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML">
  <img src="https://img.shields.io/badge/Django%20Rest%20Framework-3.x-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django Rest Framework">
  <img src="https://img.shields.io/badge/Stylus-0.x-FF6347?style=for-the-badge&logo=stylus&logoColor=white" alt="Stylus">
  <img src="https://img.shields.io/badge/Grafana-8.x-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana">
  <img src="https://img.shields.io/badge/Loki-2.x-FF5722?style=for-the-badge&logo=loki&logoColor=white" alt="Loki">
</div>


## Table of Contents

- [Introduction](#r00t-shop)
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)




## Features

1. **Custom Cart Integration** 🛒
   Experience seamless and personalized shopping with our custom-built cart feature. Add, modify, and track your selected products effortlessly. Whether you're shopping for one item or a whole wishlist, our cart has got you covered!

2. **ViewSets for Enhanced Functionality** 🚀
   I've harnessed the power of Django Rest Framework's ViewSets to provide you with dynamic and efficient API endpoints. Our ViewSets offer a streamlined way to interact with the backend, ensuring smooth data retrieval and updates.

3. **User-Friendly API** 🤝
   Embrace the simplicity and ease of use with our API. I've crafted it to be intuitive and developer-friendly, making it a breeze for you to integrate, consume, and extend the functionalities of our E-commerce website. 


## Getting Started

To set up the project locally for development, follow these steps:

1. **Clone the Repository:**
   ````
    git clone https://github.com/r00tk3y/root_shop.git
   ````

2. **Navigate to the Project Directory:**
    ````
    cd root_shop
    ````

## Installation

1. **Create a virtual environment && Activate it:**
     ```
     python -m venv venv 
     source venv/bin/activate
    ```

2. **Install Dependencies**
    ```
    cd webshop
    pip install -r requirements.txt
    ```
3. **Frontend**
   ```
   Enter the django_frontend directory and find a detailed README.md about
   installation of the frontend
   ```
4. **Migrate Database**
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
5. **Create a superuser**
   ```
   python mange.py createsuperuser
   ```
6. **Set up env variables**
   ```
   1. Remove the .template in webshop/.env.template
   2. Set desired environment variables
   ```
7. ```
   python manage.py shell
   
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   
   >>>gw^9ej(l4vq%d_06xig$vw+b(-@#00@8l7jlv77=sq5r_sf3nu
   Random key generator, obviosly do not use the one above.
   ```
   
## Usage
1. **Running server**
   ```
   python manage.py runserver
   ```
2. **Fixtures**
   ```
   python manage.py loaddata fixtures/data.json
   superuser -> admin:admin
   ```
3. ***Docker***
   ```
    Apply migrations before running
    docker-compose up -d
   ```


## Notes
1. Install dark reader so that the white theme does not hurt your eyes :D
