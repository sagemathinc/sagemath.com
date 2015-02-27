## to deploy to app engine

(it should work via git push origin master, but no idea why it isn't. until then:)

$ appcfg.py --oauth2 update .


## to compress the png files to -nq

pngnq -v -f -s 1 pattern-grey-squares.png
