
python setup.py sdist bdist_wheel
twine register dist\Dero-0.8.12*
twine upload dist\Dero-0.8.12*
pause
