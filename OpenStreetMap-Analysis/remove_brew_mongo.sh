#!/usr/bin/env sh

# checks to see if running 
launchctl list | grep mongo
 
launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.mongodb.plist
launchctl remove homebrew.mxcl.mongodb

pkill -f mongod

rm -f ~/Library/LaunchAgents/homebrew.mxcl.mongodb.plist

brew uninstall mongodb

# double check existence
ls -al /usr/local/bin/mong*
ls -al ~/Library/LaunchAgents