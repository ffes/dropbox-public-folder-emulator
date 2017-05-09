# Dropbox Public Folder Emulator #

Dropbox Public Folder Emulator is an emulator that mimics the old "Public" 
folder that was retired by Dropbox.

## Dropbox Public Folder ##

### A bit of history ###

In previous times every account had a folder named "Public". All the content 
in this folder was automatically shared to everybody on the Internet if you 
knew the URL.

For accounts created after October 2012 this feature was not available anymore 
and in March 2017 it was completely removed from Dropbox.

### How I used the public folder ###

I used this feature to host my downloads. It was a simple redirect in my 
nginx configuration files. I manually created the download links that I put 
on my website and give to people (via email). Now that the feature is gone, 
I needed a replacement.

Inspired by https://github.com/andreafabrizi/Dropbox-Uploader I created 
this Python project (from scratch) that I run on my site to emulate the public 
folder by querying the Dropbox-API.

## Overview ##

This script has to run on your own webserver, in my case behind nginx. 
It can probably run on any webserver or cloud service, but I haven't tested 
that at all.

Setup the OAuth authentication and select a directory where all the 
downloadable files live, defaults to `/Public`.

You manually create a URL for the file to download, like: 
http://downloads.example.com/dir/file.ext

This URL/request is parsed by the Python script and the full filename is 
given to the API. The API gives a URL of the downloadable file.

`/Public/dir/file.ext` will be translated to https://www.dropbox.com/s/Som3R4ndomH4sh/file.ext?dl=1

This is new URL given to nginx that return a HTTP status 302 with this new URL.

## Installation ##

### Webserver ###

Make sure Python 3 is installed.

```bash
sudo apt install python3
```

In `/etc/nginx/XXX.conf` add the following lines:

```
```

### Authenticate on Dropbox.com ###

To setup OAuth you need to do the next steps:

* Copy `conf_sample.py` to `conf.py`. You will need to store the OAuth token in that file.
* Go to https://www.dropbox.com/developers/apps and log in with your account.
* Click on the **Create App** button and then select **Dropbox API app**.
* Now go on with the configuration and choose **App folder**.
* Enter the **App Name** that you prefer (e.g. MyPythonProxy).
* Accept the terms and click on the **Create App** button.
* When your new App is successfully created, please click on the Generate button 
  under the **Generated access token** section, then copy and paste the new access token 
  in `conf.py`.
