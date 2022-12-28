market=("kospi" "kosdaq")

# make stock historical data
python make_stocks.py -m ${market[@]}


cnn_name="224x224"
yolo_name="1800x650"

# make candlestick chart
python make_candlesticks -n ${yolo_name} -m ${market[@]} --yolo
python make_candlesticks -n ${cnn_name} -m ${market[@]} --cnn