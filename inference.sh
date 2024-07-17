# export PYTHONPATH=./
python inference.py \
--model_path model_parameter/Qwen2_7b_instruct \
--dataset_name API_Bank \
--data_path data/api-bank/test_data/level-2-response.json \
--output_answer_file result/test.json \
