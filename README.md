

# Fine. Snake :snake:

#### team : Are You Okay?
- [Catherine Meng](https://github.com/MCatherine1994)
- [Chloe Yu](https://github.com/Chloeiii)
- [Licht Liu](https://github.com/xylliu)
- [Olivia Zhu](https://github.com/JJingg)

#### Our strat:
The Strategy of our Fine snake is based on DFS searching algorithm. We want to make sure our snake could always find a safe path from its head to tail on its way to the food. It turns out that the Fine snake performs outstanding when it runs alone on the board (achieved 3000+ turns on a 11x11 board), or during 1v1 battle with one other snake. During the BattleSnake 2019 event, we won 3 Bounty Snakes in total (snakes from Giftbit, TELMEDIQ, and Semaphore). 


Basically, based on the prediction of longer snakes' next steps, we have 3 DFS searching mode in totall. Mode C is the danger mode, in which we consider all the cells without considering other snakes' next steps. Mode B is the normal mode, in this case we consider longer snakes' one step ahead, we'll try to avoid those cells when we calculate the path. Mode A is the ...





#### heroku url: https://ccilosnake.herokuapp.com/
#### This is: A [Battlesnake AI](http://battlesnake.io) written in Python. 
- [Docs and APIs](https://docs.battlesnake.io/)  
- [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

----

#### Prerequests

* a working Python 2.7 development environment ([getting started guide](http://hackercodex.com/guide/python-development-environment-on-mac-osx/))
* [pip](https://pip.pypa.io/en/latest/installing.html) to install Python dependencies

----

### Running the Snake Locally:womans_hat:

1) [Fork this repo](https://github.com/battlesnakeio/starter-snake-python/fork).

2) Clone repo to your development environment:
```
git clone git@github.com:<your github username>/starter-snake-python.git
```

3) Install dependencies using [pip](https://pip.pypa.io/en/latest/installing.html):
```
pip install -r requirements.txt
```

4) Run local server:
```
python app/main.py
```

5) Test your snake by sending a curl to the running snake
```
curl -XPOST -H 'Content-Type: application/json' -d '{ "hello": "world"}' http://localhost:8080/start
```

### Deploying to Heroku:sushi:

1) Create a new Heroku app:
```
heroku create [APP_NAME]
```

2) Deploy code to Heroku servers:
```
git push heroku master
```

3) Open Heroku app in browser:
```
heroku open
```
or visit [http://APP_NAME.herokuapp.com](http://APP_NAME.herokuapp.com).

4) View server logs with the `heroku logs` command:
```
heroku logs --tail
```


### [Start the engine](https://docs.battlesnake.io/):sparkling_heart:

**MAC OS Example:**   
1. Install Brew

		/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

2. Install Git

		brew install git

3. Install Jq
	
	
		brew install jq

4. Install Wget

		brew install wget

5. Download the Engine

		mkdir battlesnake-engine
		cd battlesnake-engine
		wget -qO- `curl -s https://api.github.com/repos/battlesnakeio/engine/releases/latest \
		    | jq -r ".assets[] | select(.name) | .browser_download_url" | grep Darwin | grep 64` \
		    | bsdtar -xvf-

6. Run the engine in dev mode

		./engine dev

7. Open a browser and go to [http://localhost:3010/](http://localhost:3010/)
