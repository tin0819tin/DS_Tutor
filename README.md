# DS_Tutor
<p align="center">
<img src="./public/logo.png" width="400" />
<br>
<a target="_blank"><img href="" src="https://img.shields.io/badge/python-%3E%3D3.7.0-brightgreen.svg"></a>
<a target="_blank"><img href="" src="https://img.shields.io/badge/flask-%3E%3D2.0.1-yellowgreen.svg"></a>
</p>

***
> :ok_man: A better web app for data structure visualization and tutoring.
***

## :checkered_flag: Getting start
**To learn more about this project please check this** [demo video](https://drive.google.com/file/d/1OoRhyeYP_Mw9_UDvZGIxbCY6F2WD0pVC/view?usp=sharing) and [slide](https://drive.google.com/file/d/1jeG6qTT1gPgXMh3XyxMr-YSsxXVh7_EL/view?usp=sharing).


## :hammer: Build from source
First clone the project to local.
```shell
$ git clone git@github.com:tin0819tin/DS_Tutor.git
```

### Setup Flask Server
1. Enable backend virtual environment
```shell
source api/bin/activate 
```

2. Set Flask variables
```shell
export FLASK_APP=main.py
```

3. Run DS_Tutor
```shell
flask run --reload --debugger
```
**It will open DS_Tutor on http://127.0.0.1:5000/**

4. Unable virtual environment
```shell
deactivate
```

## :gear: Deployed Version
**We have deployed our project on heroku, however since our budget is limited, our plan can't serve large traffic.
As a result, _we currently don't open the deployment link to public._**


## :bulb: Usage

### Flask api definition
For **developer**, if you are just using DS_Tutor, you could skip this table.

| Description | Methods | Binary Search Tree | Min Heap | Max Heap | Red Black Tree |
| --- | --- | --- | --- | --- | --- |
| The page showing the Data Structure | `root api` | `/bst` | `/minHeap` | `/maxHeap` | `/rbTree` |
| Insert the node with <value>| `/<DS>/insert/<value>` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| Delete the node with <value>| `/<DS>/delete/<value>` | :white_check_mark: | :x: | :x: | :white_check_mark: |
| Find the node with <value>| `/<DS>/find/<value>` | :white_check_mark: | :x: | :x: | :white_check_mark: |
| Print the DS inorderly | `/<DS>/print` | :white_check_mark: | :x: |:x: | :white_check_mark: |
| Remove minimum node| `/<DS>/rMin` | :x: | :white_check_mark: | :x: | :x: |
| Remove maximum node| `/<DS>/rMax` | :x: | :x: | :white_check_mark: | :x: |
| Clear the DS | `/<DS>/clear` | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: |


### :crayon: DIY mode
Check the DIY page on `/bst`, `minHeap`, `maxHeap` and `rbTree`.

<p align=center><img src="./public/DIY.gif" width="1000"/></p>

### :page_facing_up: Test your knowledge mode
Check the test your knowledge page on `/tutor`.

<p align=center><img src="./public/TYK.gif" width="1000"/></p>
