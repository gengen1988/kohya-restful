import argparse
import os
import torch
import time
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration


def load_model(model_id="Salesforce/blip2-opt-2.7b"):
    # Set the device to GPU if available, otherwise use CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Initialize the BLIP2 processor
    processor = Blip2Processor.from_pretrained(model_id)

    # Initialize the BLIP2 model
    model = Blip2ForConditionalGeneration.from_pretrained(model_id, torch_dtype=torch.bfloat16)

    # Move the model to the specified device
    model.to(device)

    return processor, model, device


def get_images_in_directory(directory_path):
    """
    Returns a list of image file paths found in the provided directory path.

    Parameters:
    - directory_path: A string representing the path to the directory to search for images.

    Returns:
    - A list of strings, where each string is the full path to an image file found in the specified directory.
    """

    # List of common image file extensions to look for
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]

    # Generate a list of image file paths in the directory
    image_files = [
        # constructs the full path to the file
        os.path.join(directory_path, file)
        # lists all files and directories in the given path
        for file in os.listdir(directory_path)
        # gets the file extension in lowercase
        if os.path.splitext(file)[1].lower() in image_extensions
    ]

    # Return the list of image file paths
    return image_files


def generate_caption(
    file_list,
    processor,
    model,
    device,
    caption_file_ext=".txt",
    max_new_tokens=40,
    min_new_tokens=20,
    temperature=1.0,
    top_k=40,
    repetition_penalty=1.0,
    top_p=1.0,
):
    """
    Fetches and processes each image in file_list, generates captions based on the image, and writes the generated captions to a file.

    Parameters:
    - file_list: A list of file paths pointing to the images to be captioned.
    - processor: The preprocessor for the BLIP2 model.
    - model: The BLIP2 model to be used for generating captions.
    - device: The device on which the computation is performed.
    - extension: The extension for the output text files.
    - num_beams: Number of beams for beam search. Default: 5.
    - repetition_penalty: Penalty for repeating tokens. Default: 1.5.
    - length_penalty: Penalty for sentence length. Default: 1.2.
    - max_new_tokens: Maximum number of new tokens to generate. Default: 40.
    - min_new_tokens: Minimum number of new tokens to generate. Default: 20.
    """
    for file_path in file_list:

        start_time = time.time()
        image = Image.open(file_path)
        inputs = processor(images=image, return_tensors="pt").to(device, torch.bfloat16)

        generated_ids = model.generate(
            **inputs,
            do_sample=True,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
            max_new_tokens=max_new_tokens,
            min_new_tokens=min_new_tokens,
        )

        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

        # Construct the output file path by replacing the original file extension with the specified extension
        output_file_path = os.path.splitext(file_path)[0] + caption_file_ext

        # Write the generated text to the output file
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(generated_text)

        # Log the image file path with a message about the fact that the caption was generated
        end_time = time.time()
        print(
            f"{file_path} caption was generated. elapsed time: {end_time - start_time:.2f} seconds"
        )


def main(
    directory_path,
    model_id,
    temperature,
    top_p,
    top_k,
    repetition_penalty,
    min_new_tokens,
    max_new_tokens,
    caption_file_ext,
):
    print("BLIP2 captionning...")

    if not os.path.isdir(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return

    processor, model, device = load_model(model_id)
    image_files = get_images_in_directory(directory_path)
    generate_caption(
        file_list=image_files,
        processor=processor,
        model=model,
        device=device,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        repetition_penalty=repetition_penalty,
        min_new_tokens=int(min_new_tokens),
        max_new_tokens=int(max_new_tokens),
        caption_file_ext=caption_file_ext,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate captions for images in a directory using BLIP2 model with nucleus sampling."
    )
    parser.add_argument("directory_path", type=str, help="Path to the directory containing images.")

    parser.add_argument(
        "--model_id",
        type=str,
        default="Salesforce/blip2-opt-2.7b",
        help="Id of the model to use for caption generation; defaults to Salesforce/blip2-opt-2.7b.",
    )

    parser.add_argument(
        "--temperature", type=float, default=1.0, help="Temperature for sampling; defaults to 1.0."
    )
    parser.add_argument(
        "--top_p", type=float, default=0.9, help="Top p for nucleus sampling; defaults to 0.9."
    )
    parser.add_argument("--top_k", type=int, default=50, help="Top k for sampling; defaults to 50.")
    parser.add_argument(
        "--repetition_penalty",
        type=float,
        default=1.0,
        help="Repetition penalty to discourage repetitive text; defaults to 1.0.",
    )
    parser.add_argument(
        "--min_new_tokens", type=int, default=20, help="Minimum new tokens; defaults to 20."
    )
    parser.add_argument(
        "--max_new_tokens", type=int, default=40, help="Maximum new tokens; defaults to 40."
    )
    parser.add_argument(
        "--caption_file_ext",
        type=str,
        default=".txt",
        help="File extension for saved captions; defaults to .txt.",
    )

    args = parser.parse_args()
    main(
        directory_path=args.directory_path,
        model_id=args.model_id,
        temperature=args.temperature,
        top_p=args.top_p,
        top_k=args.top_k,
        repetition_penalty=args.repetition_penalty,
        min_new_tokens=args.min_new_tokens,
        max_new_tokens=args.max_new_tokens,
        caption_file_ext=args.caption_file_ext,
    )
