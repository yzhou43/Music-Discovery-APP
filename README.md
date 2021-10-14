# Music Discovery APP
## Milestone1 and Milestone2
The app can be found at https://music-discovery-app-yzhou43.herokuapp.com/

## Part 1: How to set up and run
### Create account for APIs
1. Create account in `https://developer.spotify.com/` and create a new app
2. Create account for genius API and follow the instruction in `https://docs.genius.com/`
### Install Requirements
1. `pip install python-dotenv`  
2. `pip install requests`  
3. `pip install flask`  
4. install flask_login using `pip install flask-login`
5. install flask_sqlalchemy using `pip install -U Flask-SQLAlchemy`
6. install flask_wtf using `pip install -U Flask-WTF`
7. install wtforms using `pip install -U WTForms`
8. install psycopg2 using `psycopg2`
### Set up
1. Create `.env` file inside the project directory  
2. Write the client ID and client secret of Spotify developer API, and the access token of Genius API in the `.env` file as following:  
CLIENT_SECRET = 'YOUR_SECRET'  
CLIENT_ID = 'YOUR_ID'    
genius_access_token = 'YOUR_TOKEN'  
DATABASE_URL = 'YOUR_DATABASE_URL'   
SECRET = 'YOUR_SECRET'   
### Run Application
Use command `python3 app.py`

# Milestone2
## Part 2: Existing problems
1. The process time is too long after the user input their favorite artist's ID and click on the 'sava' button. The program may take several seconds to process the artist's ID adding, and one of the reasons why it's slow is that the program has to check the ID using several functions, and call the Spotify API to see if the artist's ID is valid, which requires time. 
2. After reload the music discover page, the form inside the page will be submitted again, and the POST method will also be called again. One possible solution is to apply the Post/Redirect/Get(PRG) pattern for the programs, and I will fix the program if I have more time.
3. The relationship between the tables inside the database is not well designed. I'm not very familiar with the database, so I have to use the naive way to store the information inside the database, and it should be improved in the future.

## Part 3: Technical issues I've solved
1. I planed to create a login system with both username and password, but I was not sure where to start at first. I learned about how to build the login pages from the youtube tutorial `https://www.youtube.com/watch?v=pvUUidK1zuw&t=0s`.
2. I use the flask wtform to build my login system. However, when I first wrote the login pages, it could not run success and showed error message related to CSRF Protection. I checked answers on stackoverflow and then added {{ form.csrf_token }} to the end of my html page. The detailed theory to do this is complicated, but I know it's related to security reason, and I have to add this code to make my programs work.
3. First I allowed the users the save the artist's ID as long as the ID is valid and can fetch data from Spotify API, but the result for this design is that there could be many same data stored inside the database. So I then added the ID checker `Artist.query.filter_by(artistid=artist_id, user_id=current_user.id).first()` to make sure that duplicated data would not be added to the database.

## Part 4: Difference between planning and reality
Building the login system is harder than I thought, and it took me much longer time than I expected. I think it's because that I'm not familiar with database, so I have to spend a lot of time dealing with unexpected errors. 

# Milestone1
## Part 2: Existing problems
1. In my current app, I use the Genius API to search for the song's artist, and then display the artist's image and provide the artist's url. However, the Genius search API sometimes 
gives the first answer as an incorrect one, and the correct answer maybe in the latter. Hence, if I have more time, I will try to use not only the first answer, but check the correctness of the first one. If the first answer is not correct, then check the following ones until find the real result for the song.  
2. The progress bar for the music player does not correspond to the actual progress of the music.
3. I hope to add user input as an additional feature if I have more time. The users will be allowed to choose which artist they want to listen to, and then the app will display the 
artist's song in random.
## Part 3: Technical issues I've solved
1. I first failed to push my code to Heroku using `git push heroku main`, then I found this link `https://stackoverflow.com/questions/26595874/i-want-make-push-and-get-error-src-refspec-master-does-not-match-any`, and used the command `git push heroku HEAD:master` instead.
2. One problem I had is the Genius search API may offer incorrect artist's image to the song, and it's weird if the user hovers on the name of artist A, but the app shows picture of artist B.
So I compare the artist's name fetched from Spotify API and Genius API, if these two are different, then the picture and link of the song's artist won't be displayed.
3. I tried to create a artist's picture that only shows when the user hovers in the artist's name but I was not sure what to do. Thhen I searched online and found the webpage `https://www.websitecodetutorials.com/code/photo-galleries/css-popup-image.php`, 
which is useful for me to write the css of the picture.
