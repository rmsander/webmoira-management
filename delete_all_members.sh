#!/bin/bash

# Set up environment variables
MAIL_LIST=$1
echo "Mailing list is" $MAIL_LIST

# Delete all members from mailing list
for member in $(blanche $MAIL_LIST -m); do blanche $MAIL_LIST -d $member; done
