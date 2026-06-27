FROM composer:2 AS vendor

WORKDIR /app

COPY composer.json composer.lock ./
RUN composer install --no-dev --prefer-dist --no-interaction --no-progress

FROM php:8.3-apache

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        unzip \
        libcurl4-openssl-dev \
        libfreetype6-dev \
        libjpeg62-turbo-dev \
        libonig-dev \
        libpng-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install pdo pdo_mysql curl mbstring exif gd \
    && a2enmod rewrite headers \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html

COPY . /var/www/html/topcv_lite
COPY --from=vendor /app/vendor /var/www/html/topcv_lite/vendor

RUN printf '%s\n' '<?php header("Location: /topcv_lite/"); exit;' > /var/www/html/index.php \
    && rm -f /var/www/html/index.html \
    && mkdir -p /var/www/html/topcv_lite/uploads /var/www/html/topcv_lite/storage \
    && chown -R www-data:www-data /var/www/html/topcv_lite
