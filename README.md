# Estudante
#### Video Demo:  https://youtu.be/hJdjAFrrKYY
#### Description:
run it with

python -m estudante

Estudante is my first app!
Initially, it was supposed to be a Python app to help people use the OpenAI API to make transcriptions of YouTube
videos or audio files.
My intention was threefold. First, I'd like to help a friend from work – a kind, but busy and not very 'computery' man, who
has no time or curiosity to learn  how to use the API). He was taking some online courses and used to ask me all the time
to make transcriptions of his
classes, which I did, using the OpenAI API – at a small cost to myself. So I'd like to help him and others like him, as
well as free myself from this little 'bill'. The user is linked to the OpenAI platform page and, after making his or her
own key, can just type it into the app's configurations. The app would then use this key to make its transcriptions.
Second, I wanted to be able to transcribe long videos and audios (say, transcribe a whole class or meeting and find the
useful parts using a CTRL + F word search). At the time, I hadn't seen any transcribing app that
had no limit on the length of the audio or video to be transcribed. So I used ffmpeg (a freely available command line
software) to divide the audio in smaller pieces that are accepted by the API. Then I'd combine the transcriptions of
these pieces into a single docx file. Using docx was a choice I made because it's a very common format among students
and office workers, like me and my friend. I'd download youtube media using the youtube-dl library.
Finally, I'd like to gain experience writing GUI apps. I used the Tkinter library for this. I had never written a GUI app
and for me it seemed like an important part of being a programmer (I know that probably sound pretty noob, but in me lives
a person who likes comfort).
Anyways, I eventually got really hooked on developing and started adding new features. Since I'm a student myself (I'm a writer
and a Law student), I thought of all the things that would be useful to me and my friends. I added the possibility of
summarizing PDFs and docxs, with default prompts that I have from my own academic experience (I have a masters in
History and Literature from Columbia University), as well as from study skills tips from books like Cal Newport's 'How
to be a Straight-A Student'.
I also added the possibility of converting photographed PDFs into docx files. I used the Tesseract library for this.
I also added a feature to help edit text. I used the spaCy library to help with this: it highlights adjectives and adverbs,
providing users with suggestions on where to cut or expand their argumentation (say show, not tell).
Finally, I added the possibility of reading text with RSVP (Rapid Serial Visual Presentation), a technique that supposedly
helps you reading faster. 
All of the output files are saved in a folder called 'saida' in the app's directory.
One thing that broke my heart about the experience was that I was never able to make a standalone app. Apparently, tkinter-based GUIs
are not very suitable for that. I tried to use PyInstaller, but it didn't work. I also tried to use Py2app and others, but I couldn't do it either.
I even tried to use this library based in Rust, a language I had never even heard about! Maybe I'll try harder in the future, or switch to another GUI library, or even language.
Another task that must be done is to improve the security of the user’s API key (it’s storaged in an env file).
That's not very safe, I guess, but I think this flaw can be forgiven since OpenAI has plenty of limits users can add to restrict abuse of their API keys.

#### System dependencies
Estudante needs a few command line tools besides Python:

- Python 3.12 or newer
- Git
- FFmpeg
- Tesseract OCR

You can install them with your system's package manager. Examples:
If you prefer, run `scripts/install_dependencies.sh` and confirm when prompted.

```bash
# macOS
brew install git ffmpeg tesseract

# Ubuntu / Debian
sudo apt update
sudo apt install git ffmpeg tesseract-ocr
```

```powershell
# Windows (PowerShell)
winget install Git.Git
winget install Gyan.FFmpeg
winget install UB-Mannheim.Tesseract-OCR
```

Make sure `ffmpeg` and `tesseract` are available in your `PATH` so the GUI can detect them.

#### Configuring `OPENAI_API_KEY`
This program reads your OpenAI key from the `OPENAI_API_KEY` environment variable.  
On Unix‑like systems, you can export it before running the app:

```bash
export OPENAI_API_KEY=your_key_here
```

On Windows CMD, use:

```cmd
set OPENAI_API_KEY=your_key_here
```

Or in PowerShell:

```powershell
$env:OPENAI_API_KEY='your_key_here'
```

You may also create a `.env` file in the project directory with the line `OPENAI_API_KEY=your_key_here`.  
Loading the key from a file is optional but keep in mind that plain text files can be read by anyone with access to your machine, so avoid committing `.env` to version control.

Well, I hope you enjoyed reading this as much as I enjoyed making the app. Thanks again for the course!
