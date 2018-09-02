
python setup.py sdist bdist_wheel
twine register dist\Dero-0.14.0*
twine upload dist\Dero-0.14.0*
pause
