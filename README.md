# EveMarketer
EveMarketer is an api interface that pulls and processes game data from Eve Online. Eventually this data will be used to conduct market analysis in-game.

Eve Online is known for its in-depth and extremely large in-game economy. I created this project
to gain experience with http networks, OAuth2 and MySQL databases. Currently the only existing portion of the project is the api. It is capable of authorizing itself via SSO and then storing the received access token in json. Eventually the api will then automatically update the MySQL database with daily game data. Market analyses will be produced automatically and sent to the user.
