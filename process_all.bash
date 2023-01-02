market=("kospi" "kosdaq")

# make stock historical data
python make_stocks.py -m ${market[@]}


cnn_name="224x224"
yolo_name="1800x650"
number=5
start=2019
end=2022

# make candlestick chart
python make_candlesticks.py -n ${cnn_name} -m ${market[@]} --cnn -num ${number} -s ${start} -e ${end}
python make_candlesticks.py -n ${yolo_name} -m ${market[@]} --yolo -num ${number} -s ${start} -e ${end}


cnn_method="4%_01_2"
yolo_method=("MinMax" "Pattern" "Merge")
cnn_period=20
yolo_period=245
interval=5

# make labeling
python make_labeling.py -m ${market[@]} --cnn --method ${cnn_method} -interval ${interval} -num ${number} --period ${cnn_period} -s ${start} -e ${end}

for method in ${yolo_method[@]}
do
    python make_labeling.py -m ${market[@]} --yolo --method ${method} -n ${yolo_name} -num ${number} --period ${yolo_period} -s ${start} -e ${end}
done



name="Default"
train=(2019 2020)
valid=(2020 2021)
test=(2021 2022)
sample=(50 50 50)
prior_thres=5
pattern_thres=4


# make dataset
python make_dataset.py --n ${name} -m ${market[@]} --cnn -l ${cnn_method} -i ${cnn_name} -interval ${interval} --period ${cnn_period} --train ${train[@]} --valid ${valid[@]} --test ${test[@]} --sample ${sample[@]} -o 5

for method in ${yolo_method[@]}
do
    python make_dataset.py --n ${name} -m ${market[@]} --yolo -l ${yolo_method} -i ${yolo_name} --period ${cnn_period} --train ${train[@]} --valid ${valid[@]} --test ${test[@]} --sample ${sample[@]} -prior ${prior_thres} -pattern ${pattern_thres}
done



