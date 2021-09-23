# Music Discovery APP
The app can be found at https://music-discovery-app-yzhou43.herokuapp.com/

## Part 1: How to set up and run
### Create account for APIs
1. Create account in `https://developer.spotify.com/` and create a new app
2. Create account for genius API and follow the instruction in `https://docs.genius.com/`
### Install Requirements
1. `pip install python-dotenv`  
2. `pip install requests`  
3. `pip3 install flask`  
### Set up
1. Create `.env` file inside the project directory  
2. Write the client ID and client secret of Spotify developer API, and the access token of Genius API in the `.env` file as following:  
CLIENT_SECRET = 'YOUR_SECRET'  
CLIENT_ID = 'YOUR_ID'  
genius_access_token = 'YOUR_TOKEN'
### Run Application
Use command `python3 app.py`
## Part 2: Existing problems
1. In my current app, I use the Genius API to search for the song's artist, and then display the artist's image and provide the artist's url. However, the Genius search API sometimes 
gives the first answer as an incorrect one, and the correct answer maybe in the latter. Hence, if I have more time, I will try to use not only the first answer, but check the correctness 
of the first one. If the first answer is not correct, then check the following ones until find the real result for the song.  
2. The progress bar for the music player does not correspond to the actual progress of the music.
3. I hope to add user input as an additional feature if I have more time. The users will be allowed to choose which artist they want to listen to, and then the app will display the 
artist's song in random.
## Part 3: Technical issues I've solved
1. I first failed to push my code to Heroku using `git push heroku main`, then I found this link `https://stackoverflow.com/questions/26595874/i-want-make-push-and-get-error-src-refspec-master-does-not-match-any`, and used the command `git push heroku HEAD:master` instead.
2. One problem I had is the Genius search API may offer incorrect artist's image to the song, and it's weird if the user hovers on the name of artist A, but the app shows picture of artist B.
So I compare the artist's name fetched from Spotify API and Genius API, if these two are different, then the picture and link of the song's artist won't be displayed.
3. I tried to create a artist's picture that only shows when the user hovers in the artist's name but I was not sure what to do. Thhen I searched online and found the webpage `https://www.websitecodetutorials.com/code/photo-galleries/css-popup-image.php`, 
which is useful for me to write the css of the picture.
