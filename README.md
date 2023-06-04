# SettingConverter
 A small script to convert a Joplin folder export into 1 combined document. 

Used to convert a D&D Setting folder structure (Or any folder structure for that matter) into a single document.
* It will export a `combined.md` where all of the documents are now in 1 structure. 
* It cleans up headers and links. Folders and file names are H1 and H2 respectively, all others are extended by 1 levels
* Creates a ODT file for nice printing. Use the reference.odt as template for formatting

## How to use

### Installation
```
git clone https://github.com/schemen/SettingConverter.git && cd SettingConverter
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```

### Running

Move the exported folders into the SettingsCoverter project folder, rename it `toconvert`, leave `_resources` as is.

```
source venv/bin/activate
python /main.py
```