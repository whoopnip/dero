
python setup.py sdist bdist_wheel
twine register dist\Dero-0.13.0*
twine upload dist\Dero-0.13.0*
pause
