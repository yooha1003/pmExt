# <font size=6><br>_**pmExt.py</br></font> <font size=2>(Pubmed Article Search and Download python script)**_</font>

## <font color=white>_Feature_</font>
<font size=4>Let's <font color=grean><b>_Search_</b></font> and <font color=yellow><b>_Download_</b> </font>Articles with <font color=red><b>_Keywords_ </b></font>!!</font>

## Description
+ Searching articles using Pubmed Engine
+ The script is very simple to use
+ Outputs are "_Summary of Articles_" and "_Article Figures_"
+ " _Automatic summary of abstract using [PyTextRank](https://pypi.org/project/pytextrank/)_ " added in version 0.2
+ The script supports <b>_python3_</b> and <b>_Chrome_</b>
+ _Progressbar_ is supporting in this version
![](assets/README-3b3d0f79.png)

## Install requirements
### &nbsp;&nbsp;&nbsp;_ChromeDriver_
&nbsp;&nbsp;&nbsp;&nbsp;You need to install [ChromeDriver](https://chromedriver.chromium.org/) to use this script.<br>
&nbsp;&nbsp;&nbsp;&nbsp;The installation instruction can be found [here](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/).

### &nbsp;&nbsp;&nbsp;_Modules_
&nbsp;&nbsp;&nbsp;&nbsp;
```python setup.py install```

### &nbsp;&nbsp;&nbsp;[_PyTextRank_](https://pypi.org/project/pytextrank/)
&nbsp;&nbsp;&nbsp;&nbsp;```python -m spacy download en_core_web_sm```

### &nbsp;&nbsp;&nbsp;_Before using this script_
##### &nbsp;&nbsp;&nbsp;You should input your own _'ChromeDriver'_ path in the following line of pmExt.py
&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp; For Windows,
```pathx = "your/chromeDriver/path/chromedriver.exe"```
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; For MacOS,
&nbsp;&nbsp;&nbsp;```pathx = "your/chromeDriver/path/chromedriver"```



## Usage
+ <b>Run in Terminal</b>
```
python pmExt.py
```
+ <b> Just type _keywords_ and _number of articles_</b>
![](assets/README-022c8f14.png)

+ <b>Tips</b>
```
(1) Can use multiple keywords with commas : A,B,C
(2) Use this script in a stable internet environment
```


+ <b>Help</b>
```
python pmExt.py --help
```

## Outputs
* <font size=4>_Summary of Articles (.txt)_</font>
```
(1) Title (2) Citation number (3) DOI (4) Abstract
```
![](assets/README-ecc77244.png)

* <font size=4>_Abstract Summary (.txt)_</font>
![](assets/README-c31fdb1f.png)

* <font size=4>_Article figures_</font>
![](assets/README-06318f08.png)

## Version history
+ Version 0.22: new version of output files (2020.08.04)
+ Version 0.21: bug fixed for duplicated articles over limits (2020.08.03)
+ Version 0.20: Added automatic summary of abstracts (2020.08.03)
+ Version 0.10: The script release (2020.08.01)

## _Contact for Feedback and Bug Reports_
_Uksu, Choi (qtwing@naver.com)_
