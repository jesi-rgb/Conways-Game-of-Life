# Just some executable shell to automate the process of generating images.
for run in {1..10}
do
  python main.py
  echo Finished run ${run}
done