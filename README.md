## Red | Online clotching store | Python(Django) project

# Architecture
> HTML

> CSS<sub>(Bootstrap 4)</sub>

> JS<sub>(JQuery)</sub>

> Django

> PostgreSQL

> Redis

> Celery


# Photo

<a href="https://ibb.co/mc3F02V"><img src="https://i.ibb.co/1mkJMPt/2022-09-26-134210121.png" alt="Home Page" width="500px" border="0" /></a>
<a href="https://ibb.co/YdDfVdf"><img src="https://i.ibb.co/T0KPN0P/2022-09-26-134408123.png" alt="Home Page" width="500px" border="0" /></a>
<a href="https://ibb.co/zPm5Tkr"><img src="https://i.ibb.co/P1rYvSN/2022-09-26-134438693.png" alt="Home Page" width="500px" border="0" /></a>
<a href="https://ibb.co/8jj0Fr3"><img src="https://i.ibb.co/Q66fsPB/2022-09-26-134454608.png" alt="Home Page" width="500px" border="0" /></a>
<a href="https://ibb.co/mC7yT61"><img src="https://i.ibb.co/PZ8Wjw3/2022-09-26-134506475.png" alt="Home Page" width="500px" border="0" /></a>
<a href="https://ibb.co/ckNzv53"><img src="https://i.ibb.co/wBKDLHg/2022-09-26-134237245.png" alt="Shop" width="500px" border="0" /></a>
<a href="https://ibb.co/NsWRws1"><img src="https://i.ibb.co/qdm6bd0/2022-09-26-134535551.png" alt="Cart Page" width="500px" border="0" /></a>
<a href="https://ibb.co/wRT1V0R"><img src="https://i.ibb.co/drSyFWr/2022-09-26-134652171.png" alt="Checkout Page" width="500px" border="0" /></a>
<a href="https://ibb.co/10CS9HJ"><img src="https://i.ibb.co/2FzbjXY/2022-09-26-134714675.png" alt="Purchases Page" width="500px" border="0" /></a>
<a href="https://ibb.co/PNd2RQv"><img src="https://i.ibb.co/SPzk2r4/2022-09-26-134315444.png" alt="Contact Page" width="500px" border="0" /></a>
<a href="https://ibb.co/Jx1pvyd"><img src="https://i.ibb.co/Q8gHPCc/2022-09-26-135205498.png" alt="Login Page" width="500px" border="0" /></a>
<a href="https://ibb.co/D8hb0NM"><img src="https://i.ibb.co/yYtRHDk/2022-09-26-135222662.png" alt="Sign Up Page" width="500px" border="0" /></a>
<a href="https://ibb.co/hx0tTMp"><img src="https://i.ibb.co/WNCYR3S/2022-09-26-134742949.png" alt="Settings Page" width="500px" border="0" /></a>

# Instructions for run the project <sub>(It is assumed that you have already downloaded Python(My version - 3.10) and Postgresql.)</sub>
1. git clone https://github.com/Djama1GIT/red.git
2. pip install -r requirements.txt
3. Start PostgreSQL, Redis and Celery
4. Change data to connect to postgresql in /red/red/settings.py<sub>(88-92)</sub>
<a href="https://ibb.co/hx0tTMp"><img src="https://i.ibb.co/W2pgYCz/2022-09-26-183623681.png" alt="settings" width="500px" border="0" /></a>

5. Comment the same way I did it (Ctrl+Alt+L)
red/main/urls.py
<a href="https://ibb.co/nL8z5p1"><img src="https://i.ibb.co/SdQchyx/2022-09-26-183707849.png" alt="red/main/urls.py" width="500px" border="0" /></a>

red/red/urls.py
<a href="https://ibb.co/Rh6kqVH"><img src="https://i.ibb.co/7gpdq6y/2022-09-26-183654900.png" alt="red/red/urls.py" width="500px" border="0" /></a>

red/main/views.py - Comment out the entire file
6. Run run_server.py
7. Waiting for the server to start
8. Stop run_server.py
9. Uncomment last changes
10. Run run_server.py
11. Visit the website http://localhost/
