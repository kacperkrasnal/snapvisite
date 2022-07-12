<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/group-three-sda/final-project">
    <img src="final_project/static/snapvisite/images/logo_color.png" alt="Logo" width="400" height="100">
  </a>


  <h3 align="center">
    Snap your visit right now!
    
  </h3>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#contact">Contact</a></li>
    
  </ol>
</details>


<img src="https://user-images.githubusercontent.com/93079515/178117431-4774a0aa-1f3b-469a-aebd-9e4b56b9ca4a.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/93079515/178117447-be8edbcc-e633-4a1d-b470-586bd3dda1d2.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/93079515/178117462-29bcba1a-6374-4349-9890-b130e0cc6027.png" width="30%"></img> 

<!-- ABOUT THE PROJECT --> 
![python-django-brightgreen](https://user-images.githubusercontent.com/93079515/178118071-cb77a995-32f7-4b39-8c8f-12eb62b69472.svg)
<h2 align="center"> About the project </h2>

This is a credit project for Software Development Academy courses. <br> 
A website was created to connect customers with service providers in the field of beauty and personal care services. 
The site allows the service provider to show available appointments and individual customers to find the right service at the right time. 
<p align="right">(<a href="#top">back to top</a>)</p>



<h2 align="center"> Build with </h2>

<div align="center"><img src="https://user-images.githubusercontent.com/93079515/178504798-6c72c216-638b-4919-8f0c-dea1f6706967.svg" width="90%"></img></div>
 
 <p align="right">(<a href="#top">back to top</a>)</p>




<!-- GETTING STARTED -->
<h2 align="center"> Getting started </h2>

Here are instructions on how to run the SnapVisite project locally. <br>
Describes how to get a local copy, what you need to run it and how to run it. 

<h2 align="center"> Prerequisites </h2>

<h4>Install python 3.9 or newer from <a href="https://www.python.org/">Python.org</a></h4>
<h4>If u don't have code editor install <a href="https://www.jetbrains.com/pycharm/">PyCharm</a> or <a href="https://code.visualstudio.com">Visual Studio Code</a></h4>



<h2 align="center"> Installation </h2>

1. Clone the repo with command:
   ```sh
   git clone https://github.com/kacperkrasnal/snapvisite.git
   ```
2. Remember to create virtual env and activate with following commands:
   ```sh
   pip install virtualenv
   
   virtualenv venv
   
   .\venv\Scripts\activate
   ``` 
3. Install python packages using terminal with command:
   ```sh
   pip install -r requirements.txt
   ```
4. Make your secret key in settings.py     
   ```js
   In the folder containing the manage.py file, create an .env file.

   Add to .env file variables used in settings.py config: 
       SECRET_KEY = example_name
       DEBUG = True
   ```
5. Migrate.     
   ```js
   Open Terminal and be sure that you are in folder 
   containing the manage.py file
   
   Use command:
   python manage.py migrate
   ```

6. Load data from fixtures.     
   ```js
   Open Terminal and be sure that you are in folder 
   containing the manage.py file
   
   Use command:
   python manage.py loaddata category_data.json
   ```
7. Run server.     
   ```js
   Open Terminal and be sure that you are in folder 
   containing the manage.py file
   
   Use command:
   python manage.py runserver 8000
   
   Open project in your website:
   http://127.0.0.1:8000/
   ```
   
### Tests


* pytest
  ```sh
  Put in your terminal command:
  pytest
  ```
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE -->
<h2 align="center"> Usage </h2>

The "SnapVisit" service is designed to make it easier for service providers to connect with their customers by speeding up the appointment booking and payment process. The service provider will be able to register their business, set services and their price list, create a calendar to manage appointments. The customer will have the freedom to choose appointments with the selected service provider based on their needs.


<p align="right">(<a href="#top">back to top</a>)</p>

<img src="https://user-images.githubusercontent.com/93079515/178117530-f63a7acc-5193-46f7-9a2c-bb87e9b1005e.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/93079515/178117532-29bc6201-e659-45c3-8817-c8527f511be8.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/93079515/178117540-f95fff75-6d2a-49f0-8a86-eb396ba3d1f1.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/93079515/178117543-22126651-6dc6-4057-afdc-01c280ff4527.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/93079515/178117550-ae23db7b-8753-4201-bc0d-60a076effe20.png" width="30%"></img> <img src="https://user-images.githubusercontent.com/93079515/178117566-197263c1-ddec-4da4-8dde-362113bb9794.png" width="30%"></img> 

<!-- FEATURES -->
<h2 align="center"> Features </h2>

- Registration of new service providers
- Creation of a corporate account management panel
- Personalization of the service provider panel
- Adding a list of services and a price list
- Adding a location and address
- Editing the schedule
- Check date and time details
- Registration of users as recipients of services 
- Deleting users as a recipient of services
- Booking appointments with a provider
- Option to pay for the service
- Ability to view future visits
- Finding service providers

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
<h2 align="center"> Contact </h2>

Contributors:

https://github.com/kacperkrasnal
<br>
https://github.com/Marcin-Chudzik

<p align="right">(<a href="#top">back to top</a>)</p>






