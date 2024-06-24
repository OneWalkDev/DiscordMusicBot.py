FROM python:3.12
USER root

RUN apt-get update && \
    apt-get upgrade && \
    apt-get -y install locales ffmpeg && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

RUN pip install --upgrade pip

RUN pip install discord.py yt-dlp python-dotenv PyNaCl ffmpeg youtube-search-python