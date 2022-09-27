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

## Using Altas

## Acknowledgements

- Icon credit: https://github.com/alexandresanlim/Badges4-README.md-Profile
- README template credit: https://github.com/othneildrew/Best-README-Template
