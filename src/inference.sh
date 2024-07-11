export PYTHONPATH=./
python src/otl/inference.py \
--dataset_name API_Bank \
--model_path model_parameter/Qwen2_7b_instruct \
--output_answer_file result/api.json \
--data_path data/api-bank/test_data/level-2-response.json












