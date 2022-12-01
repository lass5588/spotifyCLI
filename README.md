# spotifyCLI
Thid application serves as a command line interface for Spotify, to run active instance of Spoify from your CLI
The application is written in Pyhton.

## Disclaimer
The application has been developed in a macOS enironvent and has at this point only been tested with macOS Ventura.

# Technologies
Require Python and pip installed, apllication is build with python 3 and is therefore recomended.
The application uses Spotify web API through the python library Spotipp https://spotipy.readthedocs.io/en/2.21.0/ 
download here: https://pypi.org/project/spotipy/

# Getting started
There is a few prerequisites for using this applcations, especially pertaining to the use of the Spotify Web API. 

## Spotify account
Using the Spotify web API demands a premium spotify account, non-premium account will recieve a failure response.

## Spotify developer dashboard
As a part of the setup, Spotify requires you to setup a application dashboard to manage the Spotify integration with your Spotify account.

### Step 1: 
Go to https://developer.spotify.com/dashboard and login with your Spotify account.

### Step 2
Create and APP, you only need to provide a name for it (will be used to connect with the API.)

### Step 3
Go to "Edit Settings" and add/change the Redirect URIs, could just be localhost as long as the application is run locally.

### Step 4
Get the below values from the Developer Dashboard to connect the Web API.

- Client ID
- Client Secret
- Redirect URIs

For a complete guide on finding these see this article: https://support.heateor.com/get-spotify-client-id-client-secret/

### Step 5
Insert these in an enironment file as shown here: https://pypi.org/project/python-dotenv/ 
The variables in your environment file should match those imported in the main.py file.
Furthermore you need to add your Spotify username to the environment file. OBS if you are logged in with facebook, your username is a generated string of numbers, which can be found at your profile in Spotify.

## Run the application
Clone the repository and rund the command python3 main.py

