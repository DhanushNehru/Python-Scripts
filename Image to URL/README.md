Image to URL using imgbb api

## Description

Had a bit of problem while handling the functionality in mac. 
On windows it was okay, but mac apparently has a lot of problems if you want to listen to keyboard inputs ( to trigger the shortcut) 
So the solution was to not listen for the trigger on mac, but instead use the automator.app and create a workflow using the python file. 

## How to use it  ? 


### Windows : 
Install all the required python libraries 
change `device` to "windows".
Get api key from imgbb, and put it in .env in the root of this repository.
Change shortcut to whatever you want, by default its set to Ctrl + Shift + Z 
Change your escape button ( to close the script using keyboard ) , default is "Esc"


### Mac
For Mac users : 
Change the `device` to "mac" 
Get API key , put it in .env in the root of this repository. 

( Theoretically you should be able to do this but I was not able to for some reason ) 

1. Open Automator > Create a new Quick Action Workflow
2. Drag "Run Shell Script" to the right side  > Change Workflow Receives to "no input"
3. Keep the shell as it is, change the script to `python3 <full path to script>` ( use python or python3 , whichever you have ) 
4. Save it, Go to Keyboard Shortcuts > Services > General > Set the Keyboard shortcut for this saved workflow 

But since I had a problem with this , this is how I did it : 

1. Open Automator > create new Quick Action workflow 
2. Drag "Run Shell Script" to the right side > Change Workflow Receives to "no input"
3. Change the shell to "python3" ( for me , could be different for you) , and then paste the entire script into automator 
4. Keep in mind , in doing so the api key has to be in the code , and not in the .env file., also comment out all the dotenv stuff.