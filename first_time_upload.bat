
python setup.py sdist bdist_wheel
twine register dist\Dero-0.11.0*
twine upload dist\Dero-0.11.0*
pause
