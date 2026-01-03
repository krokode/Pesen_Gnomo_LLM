from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

def generate(model_path, prompt, 
            length=500, results=1, 
            temperature=1.0, topic=0.95):
    """
    Generate text using a pre-trained GPT-2 model.
    """
    tokenizer = GPT2Tokenizer.from_pretrained(model_path)
    model = GPT2LMHeadModel.from_pretrained(model_path)
    
    # Check for GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    
    # Generate text
    out = model.generate(
        input_ids, 
        max_length=length, 
        num_return_sequences=results,
        # no_repeat_ngram_size=2,
        repetition_penalty=1.3,
        do_sample=True,
        top_k=50,
        top_p=topic,
        temperature=temperature,
    )

    generated_text = list(map(tokenizer.decode, out))[0]
    return generated_text

if __name__ == "__main__":
    model_path = "output/model"
    prompt = "Рождество"
    print(generate(model_path, prompt, length=1000, temperature=1.0, topic=0.5))
