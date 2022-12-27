market=("kospi" "kosdaq")
names=("224x224" "1800x650")

for name in ${names[@]}
do
    python update.py -m ${market[@]} -n ${name}
done