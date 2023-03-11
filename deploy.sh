#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`


printf "${green}Fixing URLs for Zappa - AWS. ${reset}\n" 
cd backend
python fix_urls.py

printf "${green}Deploying using zappa. ${reset}\n" 
zappa update dev

printf "${green}Attaching EC2 role assuming to Lambda. ${reset}\n" 
python attach_ec2role_to_lambda.py

printf "${green}Clean Zappa changes. ${reset}\n" 
python clean_urls.py
cd ../frontend
npm run build