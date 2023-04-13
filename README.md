<p align="center">
<img src="https://github.com/theoelsti/binance-insider/blob/master/assets/binance-insider_logo.jpg" width="100" height="100">
</p>
<p align="center">
    <a href="https://github.com/theoelsti/binance-insider">Binance Insider</a>
    <br/>
    <sup><em>Python program to alert from binance futures traders trades.</em></sup>
</p>

<p align="center">
    <a>
        <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Python version">
    </a>
    <a href="https://deepsource.io/gh/theoelsti/binance-insider" target="_blank">
        <img src="https://deepsource.io/gh/theoelsti/binance-insider.svg/?label=active+issues" alt="DeepSource">
    </a>
    
</p>

## Features


- 📦 Direct use of the service, without restrictions
- ❤️ Forever FOSS!
- [Free Telegram Channel](https://t.me/+54diQijvA7xmMThk) to preview result


## Usage

> I highly recommend to run this bot on a Linux distribution. 
> It can either be a VPS or a simple Raspberry-Pi !

You can support me by using [Vultr](https://www.vultr.com/?ref=9298244) to create a VPS with cheap prices.
### 1. Clone this repo
```shell
git clone https://github.com/theoelsti/binance-insider
```
### 2. Edit config
Edit [config/config.ini](config/config.ini) with your values : 
```ini=
[telegram]
bot_api_key         = Your telegram bot api key
calls_channel_id    = The telegram channel you want alerts to be sent
public_channel_id   = The telegram channel you want summary to be sent
dev_channel_id      = The telegram channel you want to use for test & alerts
[database]
host                = Your database server IP adress
user                = Your SQL user
password            = Your SQL password
database            = Your SQL database
auth_plugin         = mysql_native_password

[settings]
profit_threshold    = (50) The profit percentage you want to wait before sending a profit notification
```
> Notes : 
- You can get your telegram bot api key by contacting [BotFather](https://t.me/BotFather) on telegram.
- You can get a channel id like this : 
1. Send a message in your channel (Change it to private)
2. Right Click on it -> Copy post link
3. Paste it in the chat, you should get something like this : 
`https://t.me/c/x/y`
the **x** refers to the channel ID. Add **-100** at the beginning, and you are good to go.

### 3. Execute [init.sh](init.sh)
`./init.sh`

### 4. Prepare the database

After changing your mysql root password, follow these following steps to create a mysql user 
```sh=
mysql -u root -p
CREATE USER 'binance_insider'@'{%|<localhost>}' IDENTIFIED WITH mysql_native_password BY '<YOUR_STRONG_PASSWORD>'; 
GRANT SELECT, UPDATE, DELETE,INSERT ON binance_insider.* TO 'binance_insider'@'{%|<localhost>}';
FLUSH PRIVILEGES;
```

> Notes
- Follow [ANSSI recommendations](https://www.ssi.gouv.fr/administration/precautions-elementaires/calculer-la-force-dun-mot-de-passe/) for passwords stength
- Use '%'  if you are planning to connect **remotely** from a device with **dynamic IP adress**, or 'localhost' if your database is **hosted on your server**. If you have a database on a **static IP server**, simply **set** your ip adress

### 5. Time to [launch](launch.sh) !
After adding traders to your database, launch the script ! 

`./launch.sh`

## License

[GNU General Public License, Version 3.0](LICENSE)
