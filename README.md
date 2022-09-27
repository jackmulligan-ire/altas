<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/jackmulligan-ire/altas">
    <img src="readme-images/altas-logo.png" alt="Altas Logo" height=250 width=250>
  </a>

<h3 align="center">Altas</h3>

  <p align="center">
    Python package to scrape webpages and transcribe video content from a video sharing platform.
  </p>
</div>

## **About Altas**

Altas is a Python package that was developed to gather data on a video sharing platform. The focus here was on the videos posted on the platform themselves, with speech data and metadata (e.g. video views, hashtags) gathered from each video. The aim of the package is to enable the analysis of the data gathered and to allow this to be done for a large sample of creators. Analysis questions to be answered include identifying topics discussed by each creator, determining how these topics shifted over time, as well as co-occurrence of topics.

The package gathers data in three stages: In the first stage, a channel is scraped for a history of videos published using Selenium and BeautifulSoup, with the webpage associated with each video being gathered. In the second stage, each webpage associated with that video is scraped using BeautifulSoup for the URL associated with the video file as well as video metadata. Finally, the video file is downloaded and then transformed to audio, with the audio being sent up to Google Cloud Speech API. The end product is an audio transcription and its associated metadata.

Please note that this repository exists for demonstration purposes and isn't functional as the video sharing website has been anonymised. This has been done to protect the integrity of the project that continues to utilise Altas in its work. A separate, private repository is used in practice.

### Built With

![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![google cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=Selenium&logoColor=white)
![ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![conda](https://img.shields.io/badge/conda-342B029.svg?&style=for-the-badge&logo=anaconda&logoColor=white)

## Getting Started

The following is required to use the repo:

- A clone of the repository `git clone <HTTPS link/SSH link>`
- A virtual environment manager (Anaconda/Miniconda recommended)
- Google Chrome or a Chromium browser and chromedriver for browser version (Windows, Mac OS) / chromedriver (Linux)
- A Google Cloud Platform account and a credentials.json file for the Speech API.

### Package structure

The following folder structure must be created to use altas.

<!-- prettier-ignore -->
├── altas  
├── data
    ├── logs                # Error logs
    ├── tmp                 # Converting video to audio
    ├── channel-sample.csv  # Channels to scrape
├── environment.yml  
├── requirements.txt  
├── run-pipeline.sh  
├── .gitignore
└── README.md

.gitignore prevents the data file from being pushed to the repository.

### Creating an initial channel sample

The channel-sample.csv file must be initialised with the follow columns: `id,channel_name,date_scraped`.

These correspond as follows:

- ID: The id associated with that channel on the platform (required).
- Channel_name: An optional alias for the channel.
- Date_scraped: Initially left blank.

A minimum valid entry into the channel-sample.csv file is as follows : `123abcd,,`

### Installing the virtual environment

To install the environment using conda, simply run `conda env create -f environment.yml`

To activate the environment, run `conda activate altas`.

A `requirements.txt` file is also available should you wish to use another virtual environment manager.

### Installing chromedriver.

A version of [chromedriver](https://chromedriver.chromium.org/downloads) compatible with your version of Chrome must be downloaded and made available when running the program. This is best placed in the `bin` folder of your conda environment file e.g. on Mac OS `/path/to/anaconda/envs/covid-19-narrative/bin`.

For Linux users, the latest version of chromedriver for your Linux distribution must be downloaded and place in a binary folder on the PATH.

### Getting credentials to use the Google Cloud Speech API

An account on the Google Cloud Platform is required to use [Google Cloud Speech](https://cloud.google.com/speech-to-text/). After setting up a Google Cloud Platform account, the [set up instructions](https://cloud.google.com/speech-to-text/docs/before-you-begin) for using the platform should be followed.

The end result of set up is a `credentials.json` file required to make API requests, which must be available in your environment's PATH. The most convenient way to do this is to add the line `export GOOGLE_APPLICATION_CREDENTIALS="path\to\credentials.json"` directly to your `~\.bash_profile` \ `~\.bashrc` file (or equivalent for your shell).

## Using Altas

## Acknowledgements

- Icon credit: https://github.com/alexandresanlim/Badges4-README.md-Profile
- README template credit: https://github.com/othneildrew/Best-README-Template
