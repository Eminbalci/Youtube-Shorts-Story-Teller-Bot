# Youtube-Shorts-Story-Teller-Bot
Automatic Youtube Shorts Story teller Video maker python bot

required libraries:
gtts, moviepy

requirments for moviepy:
https://imagemagick.org/


how to use:

Install Dependencies:
Ensure you have Python installed on your system. Additionally, you need to install the required packages using the following command in your terminal or command prompt:
pip install gtts moviepy

and install imagemagick
https://imagemagick.org/

Folder Structure:
Create a folder structure as shown below:
c:\videos\ (folder containing video files)
c:\output\ (folder for output files)
and the script file wherever you want

Provide Text Input:
After running the script, it will prompt you to enter the text you want to be voiced. Enter the desired text and press Enter.

Video Processing:
The script will randomly select a video from the videos folder and perform the following steps:

Crop the video to a 9:16 aspect ratio if needed.
Process the audio file using the Google Text-to-Speech API or the specified audio file.
Format and add the text to the video.
Output Video:
The final video with the added text will be saved in the output folder with a filename that includes the current date and time.

Cleanup:
The temporary audio file generated for text-to-speech will be deleted.

Finished:
Once the script finishes execution, it will display a success message along with the path to the generated video file.