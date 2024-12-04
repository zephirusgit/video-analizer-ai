The idea came up while watching a conversation in which they were discussing a software to analyze videos like Gemini, 
and thinking about what tools could be used so that the LLM could access the video information. This could be improved
in many ways, even with some kind of summarization, but I haven't had any good results with what I've seen.
If anyone knows how to do something good, the contribution is welcome.


This source work with ollama server run in windows, u need ir working and instale first.
i use a rtx2060 with 12gb of vram and 48gb of ram, 
I have no idea if there is a minimum requirement but I assume you must have a motherboard and gpu capable of using Cudas-

I have used it with ollama on windows, I have no idea if it would work the same on linux... 
(but I think all the same libraries exist on linux)

https://ollama.com

how work?

1) use whisper to see if there is voice and text in the video and transcribe
2) use ffmpeg to decompress it into frames, you could skip seconds so you don't have to analyze them all if the video is long.
3) use moondream to see those frames and take notes.
4) perform an analysis of llava's responses to generate a log of events,
5) make a pdf with pngs,
6) analyze it with ocr, extract the text
7) process the 3 summaries with ollama (llama3) and generate a final report.
   If you have a preferred model in ollama, you can replace it (llama3) in the analyze video file with ia9_fix_Short_.py
   
You must download the file
https://www.mediafire.com/file/n85ny8eis0x2dwr/unpack_in_folder_models_from_moondream.zip/file

video example from Dotcsv
China LIBERA SU VERSIÓN OPEN SOURCE de o1 ¿Está OPENAI en RIESGO? | QwQ
https://www.youtube.com/watch?v=Jowgm934rvg

Example results:
https://www.mediafire.com/file/f1af14tkrx8n4kw/analiza_video%25282%2529.zip/file


and unzip it into the same folder as the project
This file contains a key model to analyze images from Moondream, without that it will only use Whisper, and it will give an error in that part of the process, without the OCR tools, it will not be able to analyze for texts either.

conda create -n videoanalizer python=3.10 pip -y
conda activate videoanalizer

pip install torch==2.4.0 torchvision torchaudio==2.4.0 xformers  --index-url https://download.pytorch.org/whl/cu121

pip install einops==0.7.0

pip install pypdf2

pip install ocrmypdf

In this same project I have included several files that are perhaps not necessary for this, such as for the use of gemini APIs,
and other things, so my pip list is longer than necessary, strangely, when creating a new env,
incompatibilities arose but I added separately what was causing problems, finally everything worked.
Therefore I recommend installing first those that go separately and then the requirements 1 2 3,
the envs will occupy approximately 2.5gb.
I asked gemini to try to tell me according to the source code what is really necessary to install
in the env, and it has detailed it, I will also include the original pip list, which seems extensive
because I use several other things, such as creating images with stable diffusion, moondream,
creating pdfs, performing ocr, extracting text, or using ctransformers, to use other models such as llama directly or zephyr etc.

pip install -r requirements.txt

pip install -r requirements2.txt

pip install -r requirements3.txt


python "analizar video con ia9_fix_Short_.py"

The input video must be named video.mp4

You can look in the frames folder, once the whisper is finished, 
which is usually fast with cuda, and there you can see how many frames it captured,
and based on that estimate how long it will take to finish.

as a final result there will be a video.txt file that will have the summary of whisper, a log.json 
file that will have the information of what you saw with moondream, a frames folder with the selected images in png,
depending on how many frames ffmpeg skips these can be more or less, but it will still take longer to process them,
a my_pdf.pdf file with the images, an adocr.pdf file with the ocr of the texts if there were any, an ocrmy_pdf.txt
file with the text, and a summary_final.txt file, with the summary in Spanish, I suppose that by changing the prompt,
you can expect a response from ollama in any language,




Based on the provided Python scripts, here's a list of the required Python packages:

    torch: For deep learning and tensor operations (used by Moondream).

    argparse: For command-line argument parsing.

    PIL (Pillow): For image processing.

    moondream: The specific library for the Moondream image captioning model. You'll likely
    need to install this from a specific source (e.g., GitHub repo) as it's not a standard 
    PyPI package. Make sure to install the dependencies of Moondream as well, which will likely include transformers.

    queue: For thread-safe queues (used for communication between threads).

    threading: For multithreading.

    transformers: For Hugging Face Transformers models (used by Moondream and the tokenizer).

    re: For regular expressions.

    subprocess: For running external commands (like ffmpeg, whisper, and ocrmypdf).

    datetime: For working with dates and times.

    json: For handling JSON data.

    requests: For making HTTP requests (to interact with Ollama).

    typing: For type hinting.

    PyPDF2: For working with PDF files.

    ocrmypdf: For Optical Character Recognition on PDFs. This is a system dependency,
    not a Python package, so you'll need to install it using your system's package manager 
    (e.g., apt-get install ocrmypdf on Debian/Ubuntu, brew install ocrmypdf on macOS with Homebrew).

    ffmpeg: For video processing. This is also a system dependency, so install it with your system's package manager.

    whisper: For audio transcription. Install this via pip: pip install 
    git+https://github.com/openai/whisper.git or through conda, see whisper docs.

How to create a requirements.txt file:

    (Recommended) Virtual Environment: Create a virtual environment to isolate your 
    project's dependencies: python3 -m venv .venv (or virtualenv .venv).

    Activate Virtual Environment:

        Linux/macOS: source .venv/bin/activate

        Windows: .venv\Scripts\activate

    Install Packages: pip install torch argparse Pillow transformers requests PyPDF2 
    (install moondream as per its instructions).

    Generate requirements.txt: pip freeze > requirements.txt

This will create a requirements.txt file containing all the Python packages installed
in your virtual environment, making it easy to reproduce your environment on other systems.
Remember that system dependencies like ffmpeg, whisper and ocrmypdf won't be in the requirements.txt
and must be installed separately. You might want to add a comment in your requirements.txt
or in a separate README file to document these system dependencies.

Important Notes:

    Moondream Installation: The moondream package is key. You'll need to find the correct
    installation instructions for it, as it's not a standard PyPI package.

    System Dependencies: ffmpeg, whisper and ocrmypdf require separate installation.
    Be sure to include clear instructions on how to install these in your project's documentation.

    Ollama: The code assumes Ollama is running locally. You'll need to install and run Ollama if you haven't already.

    GPU: If you want to use a GPU, ensure you have the appropriate CUDA drivers and PyTorch with CUDA support installed. The detect_device() function in sample.py helps with this, but the initial setup is still crucial.

By following these steps, you should be able to create a reproducible environment for your project. Remember to test thoroughly after setting up the environment to make sure everything works as expected.
