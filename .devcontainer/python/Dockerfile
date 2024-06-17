FROM python:3.12
USER root

RUN apt-get update && \
    apt-get upgrade && \
    apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

RUN apt-get install -y vim less

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y \
    wget \
    build-essential \
    yasm \
    nasm \
    libx264-dev \
    libx265-dev \
    libnuma-dev \
    libmp3lame-dev \
    libopus-dev \
    libvpx-dev \
    libfreetype6-dev \
    libass-dev \
    libfontconfig1-dev \
    pkg-config \
    libfribidi-dev \
    libharfbuzz-dev \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# OpenSSL のインストール
RUN apt-get install -y libssl-dev

# ffmpegのソースコードをダウンロード
RUN wget https://ffmpeg.org/releases/ffmpeg-7.0.1.tar.bz2 && \
    tar -xjf ffmpeg-7.0.1.tar.bz2 && \
    cd ffmpeg-7.0.1 && \
    ./configure \
    --enable-gpl \
    --enable-libx264 \
    --enable-libx265 \
    --enable-libmp3lame \
    --enable-libopus \
    --enable-libvpx \
    --enable-libfreetype \
    --enable-libass \
    --enable-libfribidi \
    --enable-libfontconfig \
    --enable-libharfbuzz \
    --enable-openssl \
    --enable-version3 \
    && make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf ffmpeg-7.0.1 ffmpeg-7.0.1.tar.bz2

# PATHにffmpegを追加
ENV PATH="/usr/local/bin:$PATH"

RUN pip install --upgrade pip

RUN pip install discord.py yt-dlp python-dotenv PyNaCl ffmpeg youtube-search-python