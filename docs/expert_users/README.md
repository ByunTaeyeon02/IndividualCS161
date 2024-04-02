## __Building product instructions (Tile Flip)__ ##

- ### __No Installation Needed (Using Heroku)__ ##
	- go to http://www.tileflip-monogram.com/
  	- or https://tile-flip-monogram-4b24b968e494.herokuapp.com/
 	- I'm working on getting domain from http to https

- ### __Building Using Docker (NEW WIP)__ ###
	- Download Docker
 	- docker pull anhton20/tileflip:latest
  	- docker run -d -p 8080:8080 anhton20/tileflip:latest
 	- open http://localhost:8080/ on the browser to see the website

- ### __Cloning GitHub project to computer__ ###
	- (Option 1) Using GitHub Desktop
		- Download the GitHub Desktop app and log in
		- Clone our project by selecting clone project by URL and paste this URL
			- https://github.com/ByunTaeyeon02/TileFlip.git
		- Select a folder you want the project to be in and wait for the cloning to complete
	- (Option 2) Using command line
		- Open cmd
		- cd into the desired folder
		- git clone https://github.com/ByunTaeyeon02/TileFlip.git
- ### __Building website (OLD)__ ###
	- Download VS Code and open the project inside the previously selected folder
	- cd into dev
	- Instal things like Flask and Python if you don’t have it on your machine
	- cd into /client and run
		- Install node.js
			- npm install (install npm on machine)
  			- npm install -D tailwindcss@latest postcss@latest
    			- npm install -D autoprefixer
      			- npm i -D @sveltejs/adapter-static
		- npm run build (to check and make sure there’s no error with the svelte code)
		- npm run dev (to see the website not connected to the backend)
			- Once this is run it will give you a local host link
			- Paste and enter that link into the internet browser
   			- THIS IS NOT CONNECTED TO THE BACKEND
	- cd into /server and run the server by typing 
		- python offline.py
  			- This will give you a link to the website (Connected to the backend)
     			- Run this if you want to see the most updated version of the project
  		- Other dependencies (Install if needed):
		    - pip install cachelib
		    - pip install flask-session
		    - pip install flask-cors
		    - pip install flask flask-login flask-sqlalchemy
	
