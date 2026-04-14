@echo off
echo Running adversarial attacks on bank dataset...

python 2_generate_ae.py -t 1 -d True -c True -f True -p True -n 64

echo Attack generation complete!
pause