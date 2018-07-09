
python setup.py sdist bdist_wheel
twine register dist\Dero-0.12.2*
twine upload dist\Dero-0.12.2*
pause
