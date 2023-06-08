gallery-build

cp -r public/* ../gallery
cd ../gallery
git add .
git commit -m "update"
git push origin master
