from typing import List

from transformers import AutoTokenizer, AutoModelForCausalLM

from src.otl._model import LocalLanguageModel

class LLaMA(LocalLanguageModel):
    def __init__(self, checkpoint_path: str) -> None:
        self.model_name = 'LLaMA'

        self.checkpoint_path = checkpoint_path

        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint_path, trust_remote_code=True)
        self.llm = AutoModelForCausalLM.from_pretrained(self.checkpoint_path, trust_remote_code=True, device_map="auto") # torch_dtype=torch.bfloat16,
        self.llm.eval()
        self.history = []

    def predict(self, prompt: str):
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        outputs = self.llm.generate(input_ids,do_sample=False, max_length=1024,pad_token_id=self.tokenizer.eos_token_id)
        output_text = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0][len(prompt):]
        return output_text

    def change_message(self,data_lst):
        self.history = data_lst

    def add_message(self, data):
        self.history.append(data)
    def parse(self):
        messages = self.history
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        response = self.predict(text)
        return response

    def __call__(self, input_text: str, max_new_length: int=256) -> str:
        inputs = self.tokenizer(input_text, return_tensors="pt")
        try:
            generate_ids = self.llm.generate(inputs.input_ids.cuda(), max_new_tokens=max_new_length)
        except:
            pass
        outputs = self.tokenizer.decode(generate_ids[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
        return outputs