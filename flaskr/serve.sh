#!/bin/bash
export FLASK_APP=page
export FLASK_ENV=development
thing=$(flask run) &
cd ../web
npm run start
kill $thing