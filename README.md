# Pesen_Gnomo LLM

A GPT-2 based language model trained on Russian poems and stories by Vyacheslav Soldatenko
and Olga Yudayeva. This project allows you to train and generate creative text in the style
of the author's works.

## Features

- **Text Generation**: Generate new poems, stories, or creative text based on trained models.
- **Custom Training**: Fine-tune GPT-2 models on custom datasets.
- **Data Processing**: Utilities for converting EPUB files to text and processing JSON data.
- **Markov Chain Generation**: Additional text generation using Markov chains for comparison.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/krokode/Pesen_Gnomo_LLM.git
   cd Pesen_Gnomo_LLM
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .PESEN_GNOMO_env
   source .PESEN_GNOMO_env/bin/activate  # On Windows: .PESEN_GNOMO_env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Training

To train the model on the provided dataset:

```bash
python train.py
```

The training script uses the `full_train_data.txt` file and saves the model to the `output/model/` directory.

### Text Generation

To generate text using the trained model:

```bash
python generate.py
```

This will generate text based on the prompt "Рождество" (Christmas). You can modify the prompt and parameters in the script.

### Data Processing

The `utils/` directory contains scripts for data manipulation:

- `epub_manupulations.py`: Convert EPUB files to text.
- `json_to_txt.py`: Convert JSON data to text format.
- `mimic_text.py`: Generate text using Markov chains.

## Data

The `data/` directory contains:

- `epub_pesen/`: Original EPUB files of Vyacheslav Soldatenko's works.
- `txt_pesen/`: Converted text files.
- `json_pesen_gnomo/`: JSON formatted data.
- `txt_gnomo/`: Additional text data.

## Model

The trained model is stored in `output/model/` and includes:

- GPT-2 model weights (`model.safetensors`)
- Tokenizer files
- Configuration files

## Requirements

- Python 3.8+
- PyTorch
- Transformers library
- Other dependencies listed in `requirements.txt`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Author

krokode