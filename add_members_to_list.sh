#!/bin/bash

# Set up environment variables
MAIL_LIST=$1
FILE_TO_TRANSER=$2
echo "Mailing list is" $MAIL_LIST
echo "Name of text file is"  $FILE_TO_TRANSER

# Add new members to mailing list
blanche $MAIL_LIST -al $FILE_TO_TRANSER
