## Github

1. git pull
2. ... fix part ...
3. git add ... git commit --author "your name <email>"
4. git push

All this updates the Git repository, and maybe (at some point)
"push-to-deploy" will work.

Right now, I think it does not. Hence, update AppEngine via:

## to deploy to app engine

At some point, it should work via `git push origin master`, but this requires to hook up those services and it's not sure if it works well with appengine right now. Anyhow, the command below is the "official" deploy method. It should list a few lines including a check that the deployed version has been deployed and everything works (takes about a minute).

    $ appcfg.py --oauth2 update .

## to load the AppEngine webserver locally, for development

This also activates displaying the email bodies when sending the form.
(There are many other options for `dev_appserver` available)

    $ dev_appserver.py --show_mail_body=yes .

## to compress the png files to -nq

This is not really necessary, as long as pagespeed is activated it compresses the images.
But shouldn't hurt to do so ...

    $ pngnq -v -f -s 1 pattern-grey-squares.png
