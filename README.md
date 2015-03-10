## Github

1. git pull
2. ... fix part ...
3. git add ... git commit --author "your name <email>"
4. git push

All this updates the Git repository, and maybe (at some point)
"push-to-deploy" will work.

Right now, I think it does not. Hence, update AppEngine via:

## to deploy to app engine

(it should work via git push origin master, but no idea why it isn't. until then:)

      appcfg.py --oauth2 update .


## to compress the png files to -nq

    pngnq -v -f -s 1 pattern-grey-squares.png
