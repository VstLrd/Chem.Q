<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo-cc.png" width='100%'>
  <source media="(prefers-color-scheme: light)" srcset="assets/logo-cc.png" width='100%'>
  <img alt="ChemCrow logo" src="/assets/" width="100%">
</picture>


<br></br>


#ChemQ?
A GUI version of [ChemCrow](https://github.com/ur-whitelab/chemcrow-public/tree/main) with ability to run on local LLMs. The credit belongs to them.


#GUI Usage
## Windows Usage

If you want to use gpt for first time:
Run "ChemQ.exe".  Enter your API key and run the app with no prompt. Let the app run cmd. Then reboot your system. <b>For next usages just pass 0 as API key.</b>

### Running using local LLMs.

Download a *.gguf model. Put your model in llm folder and run the app. Now you can choose your model in combo box and use it.
Which model? It`s on your own, but i tried Llama3:7B and it was great.

## General Usage (for any system with python)

Set up API key in environment variables:
```
export OPENAI_API_KEY = sk-***
```

You can optionally use Serp API:
```
export SERP_API_KEY=your-serpapi-api-key
```
Then run "ChemQ.py". Pass 0 to API key and ask your questions.


# CLI Usage
Just as like as ChemCrow:
```python
from chemcrow.agents import ChemCrow

chem_model = ChemCrow(model="gpt-4-0613", temp=0.1, streaming=False)
chem_model.run("What is the molecular weight of tylenol?")
```


##What`s next?
Maybe an image generation and image input. Also trying to add translation AI. UI improvments.

## Comments
app will crash if your API key is not valid. and also will do same if your API key is rate limited.
sometimes app ends task but no output is shown, please check log file to see the result.

These bugs will be fixed in next versions.