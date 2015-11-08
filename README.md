# AudioGraber
This set of scripts reads RSS information from APS Physics online journal or Nature journals and converts them into .mp3 files. The aim is to extract News and Views type information and summaries of articles to listen on the go.

General Information
------------------------
RSS_Nature.py: Grabs the current issue of a Nature journal (tested on Nature Physics, Nature Photonics, Nature Materials etc., does not work on Nature which has a slightly different layout, since I usually just read the articles or listen to the podcast), loops through the issue content and generates .mp3 audio files. Longer articles only include abstract and figures in the audio.

RSS_Physics.py: Grabs all recent available APS Physics journal (https://physics.aps.org/) RSS feed information up to the date set in 'lastcheck' and generates .mp3 audio files.

RSS_Single.py: If there is a single article that you would like to generate audio, use this file and input the url of the webpage and title that you want. y: Nature journal, p: APS physics journal, n: terminate script.

Installation Requirements
------------------------
I have only tested this set of scripts with python 2.7 on my own laptop, which runs a Mac OS X system, and the code currently does not support other operating systems.

To run these script, please first install the following python packages:

    BeautifulSoup4 (to process html files)
    
    feedparser (to parse RSS feeds)
You might also need to create folders a level above to save the generated .mp3 files.

Potential Issues and Updates
------------------------
Possible changes in Nature journals and APS Physics online journal website layout may cause some of the results to change, but the code will be periodically updated as I use it and find issues.

Feel free to fork this repository, report issues and submit pull requests.
