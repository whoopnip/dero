
python setup.py sdist bdist_wheel
twine register dist\Dero-0.11.2*
twine upload dist\Dero-0.11.2*
pause
