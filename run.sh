#!/bin/bash
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`


printf "\n\n ${green}Starting Docker...${reset} \n"
open -a Docker

printf "\n\n ${green}Activationg VENV...${reset} \n"
source .env/bin/activate

printf "\n\n ${green}Building React Front End...${reset} \n"
cd frontend
sudo chown -R $USER /usr/local/lib
npm update
npm update -g
npm install --loglevel=error
npm run build 

cd ..

# if [ -d ".env" ]; then
#     printf "${green}Directory .env exists. ${reset}\n" 
#     rm -rf .env
# fi

# python3 -m venv .env
# source .env/bin/activate

# printf "${green}Installing Flask Dependencies. ${reset}\n" 
cd backend
pip install -r requirements.txt


printf "\n\n ${green}Starting the app...${reset} \n"
export FLASK_APP=app.py
export FLASK_ENV=development

printf "${green}Setting up creds. ${reset}\n" 
python fix_creds.py

flask run --port 5000
