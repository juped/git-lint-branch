import os, subprocess, sys
import spacy


# NOTE: Preload the Spacy English File as it is used across
#       several linters
try:
    NLP = spacy.load('en_core_web_sm')
except OSError:
    print(
        f'"en_core_web_sm" not found!! Spacy will try to automatically'
        f' download it. If it fails please download it manually using the'
        f' command `python -m spacy download en_core_web_sm`'
    )
    subprocess.run([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'])
    NLP = spacy.load('en_core_web_sm')
