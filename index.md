## Introduction

Covid19 has impacted the world in a way previously unimaginable. Yet if you were to try and gather information about this pandemic - ranging from simple things like number of daily cases to more complicated ones like Positivity ratio over the last 3 months - you'd find that there is no central database for easy access. 

Our Telegram Bot aims to fix that problem. Just message [@MyTelegramCovidBot](https://web.telegram.org/#/im?p=@MyTelegramCovidBot) on Telegram, and get started

We also have a video explaining our project, which can be viewed [here](https://www.youtube.com/watch?v=Kt52n5t-yMY)

## Problems

At the heart of this project is our desire to make everyone more aware of the pandemic. Keeping this in mind, we aim to do the following- 

1. Counter fake news spread by mainstream and fringe news organizations
2. Let the user make their own assessment by presenting them with accurate data in the form of easy to understand graphs
3. Decrease the time spent by people to research about various aspects of the pandemic
4. Reduce the number of dependencies to make sure older devices can use the app quickly and efficiently

## Why Us

We realize that public trust in news organizations is at an all time low. With the rapid spread of fake news over the internet, its very difficult to tell facts from fiction. 

For this reason, we decided that all our data would come either from The Ministry of Health, or the WHO. This ensures trust in our services, and reduces chances of errors. 

## APIs

The Ministry of Health and the WHO unfortunately don't have a public API for requesting data related to the pandemic. This means that you can only access a day or two old data using their website. [Covid19India](https://www.covid19india.org/) has a free and [open source API](https://github.com/covid19india/api) Their data is taken from the [Ministry of Health](https://www.mohfw.gov.in/) and other state governments. 

Similarly, a user named Pomber has a [public API](https://github.com/pomber/covid19) which keeps tracks of Covid data around the world sourced from the [WHO](https://www.who.int/) and [John Hopkins University](https://coronavirus.jhu.edu/map.html)

Without these public APIs our project would not have been possible and we thank them for the same. 

## How To Use

The commands the bot takes, and their various parameters can be viewed by sending `/help` to the Telegram bot. However, for new users we recommend using the query builder which provides a hassle free approach to getting your desired information. To use the in built query builder, type `/helpmode`

## Contact us

Think you have encountered a bug? Found some inconsistency in our data? Or have a suggestion for our Bot? Write to us at shashwatkhanna312@gmail.com. We appreciate every response we receive. 
