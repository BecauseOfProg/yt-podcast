<div align="center">
  <img
    src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/YouTube_Logo_2017.svg/langfr-420px-YouTube_Logo_2017.svg.png"
    alt="Youtube logo"
    height="50">
  <h1>Youtube Podcast</h1>
  <h3>Convert any YouTube channel into a downloadable podcast</h3>
</div>

- [How it works](#how-it-works)
- [Online](#online)
- [Install it on your own server](#install-it-on-your-own-server)
  - [Steps](#steps)
  - [Create a daemon](#create-a-daemon)
  - [Nginx reverse proxy](#nginx-reverse-proxy)
- [Note](#note)
- [Credits](#credits)

## How it works

This tool can convert any YouTube channel or a playlist into a downloadable podcast. You can choose audio or video format, and use it online or install it on your own server.

## Online

1. Head over to YouTube in your browser, and find the URL of your favorite user, channel, or playlist. The URL will look like one of these:

- `https://m.youtube.com/user/latenight`
- `https://www.youtube.com/channel/UCVTyTA7-g9nopHeHbeuvpRA`
- `https://www.youtube.com/playlist?list=PLUl4u3cNGP61Oq3tWYp6V_F-5jb5L2iHb`
- `https://www.youtube.com/c/NotJustBikes`

2. Open up your podcasts app and add a new podcast by URL. Copy and paste in the URL from step 1, except change the domain to youtube-podcast's one.
   Your modified URL should look like one of these:

- `https://podcast.becauseofprog.fr/user/latenight`
- `https://podcast.becauseofprog.fr/channel/UCVTyTA7-g9nopHeHbeuvpRA`
- `https://podcast.becauseofprog.fr/playlist?list=PLUl4u3cNGP61Oq3tWYp6V_F-5jb5L2iHb`
- `https://podcast.becauseofprog.fr/c/NotJustBikes`

3. youtube-podcast generates video podcasts by default. If you'd like an audio-only podcast instead, simply add `?a` to the end of the URL for users or channels, or add `&a` to the end of the URL for playlists:

- `https://podcast.becauseofprog.fr/user/latenight?a`
- `https://podcast.becauseofprog.fr/channel/UCVTyTA7-g9nopHeHbeuvpRA?a`
- `https://podcast.becauseofprog.fr/playlist?list=PLUl4u3cNGP61Oq3tWYp6V_F-5jb5L2iHb&a`
- `https://podcast.becauseofprog.fr/c/NotJustBikes?a`

4. Hit subscribe. You're all set. You can now download and refresh episodes, just like with any other podcast.

**If you enjoy this service, please consider making a donation to help keep it up and running.**

## Install it on your own server

If you don't want to use the online version, you can install youtube-podcast on your own server. It requires Python 3.7+ (tested on Python 3.7.2), pip, git and [youtube-dl](http://rg3.github.io/youtube-dl/download.html).

### Steps

- Clone the repository : `git clone https://github.com/avibrazil/yt-podcast.git`
- Install requirements : `pip3 install -r requirements.txt`
- You'll need a [YouTube API key](https://stackoverflow.com/questions/44399219/where-to-find-the-youtube-api-key), put it in a new file named `g.py` in /epi/ like this : `KEY = 'R4nd0mAp1k3y'`
- You must also add the domain or url for your yt-podcast instance in g.py : `DOMAIN = 'domain.tld'`
- Try `python3 run.py` to run yt-podcast

The software is now installed and listening on port 5003. Now we need to configure a daemon to let the software run in background, and expose it over the internet.

### Create a daemon

We need to run yt-podcast in the background. On Debian, create and edit a new systemd service :
`vi /etc/systemd/system/yt-podcast.service`
In this file, paste the following configuration :

```
[Unit]
Description=uWSGI instance to serve yt-podcast
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/path/to/yt-podcast
ExecStart=/usr/local/bin/uwsgi --ini youtube-podcast.ini

[Install]
WantedBy=multi-user.target
```

Make sure you edit user, group and the software path.

Then you can run `service yt-podcast start` to start the software.

### Nginx reverse proxy

I am using nginx on my server. If you know the configuration for other web servers, a pull request is welcome!
Put this configuration in a `server` block.

```nginx
location / {
    include uwsgi_params;
    uwsgi_pass unix:/path/to/yt-podcast/youtube-podcast.sock;
    # Some optional arguments:
    # uwsgi_cache mycache;
    # uwsgi_cache_valid any 1h;
    # uwsgi_cache_key $request_uri;
}
```

### Integration with Apache
Use `mod_wsgi` to publish this program under an Apache HTTP server URI.

Put the source under, say, `/var/www/html/ytpodcasts` and put the following into `/etc/httpd/conf.d/z-vhost-ytpodcasts.conf`:

```
<Macro force_https $hostname>
    <VirtualHost *:*>
        ServerName $hostname
        ServerAlias www.$hostname

        ServerAdmin hostmaster.domain.com

        Protocols h2 http/1.1

        RewriteEngine on
        RewriteCond %{HTTPS} off [OR]
        RewriteCond %{HTTP_HOST} ^www\.$hostname [NC]
        RewriteRule ^(.*)$ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
    </VirtualHost>
</Macro>


<Macro generic_wsgi $script $hostname $certificateHostname>
    <VirtualHost *:443>
        ServerName $hostname
        ServerAlias www.$hostname

        ServerAdmin hostmaster.domain.com

        Protocols h2 http/1.1

        WSGIScriptAlias / $script

        <Directory /var/www/html/$hostname>
            WSGIApplicationGroup %{GLOBAL}
            WSGIScriptReloading On
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
        </Directory>

        DocumentRoot /var/www/html/$hostname

        SSLCertificateFile /etc/letsencrypt/live/$certificateHostname/fullchain.pem
        SSLCertificateKeyFile /etc/letsencrypt/live/$certificateHostname/privkey.pem
        Include /etc/letsencrypt/options-ssl-apache.conf
        
        CustomLog "logs/access_log" vhost_combined
        ErrorLog "logs/ssl_error_log"
    </VirtualHost>
</Macro>

Use force_https ytpodcasts.domain.com
Use generic_wsgi /var/www/html/ytpodcasts/passenger_wsgi.py ytpodcasts.domain.com ytpodcasts.domain.com

UndefMacro force_https
UndefMacro generic_wsgi

```

This works in my Fedora server with included Apache HTTP server, mod_ssl and Let’s
Encrypt’s certbot. You probably need to change folder names o other things to make it
work in your environment.

You can now access yt-podcast from the address you set in nginx and in `g.py`. The rules to create a podcast will be the same (`http(s)://domain.tld/playlist?list=PLUl4u3cNGP61Oq3tWYp6V_F-5jb5L2iHb&a` for example).

## Note

You can also use EPI to download a single video :

- Video format : https://podcast.becauseofprog.fr/download/video/VideoID.mp4
- Audio format : https://podcast.becauseofprog.fr/download/audio/VideoID.m4a

## Credits

- Service : [Youtube API](https://developers.google.com/youtube/v3/)
- Maintainer : [Gildas GH](https://github.com/Gildas-GH)
