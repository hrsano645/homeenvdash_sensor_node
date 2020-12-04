# Home Env Dashboard センサーノード

家の環境をグラフ、ダッシュボードで見る「Home Env Dashboard」のセンサー情報を取得し記録をするスクリプトです。

実行環境はRaspberry Pi 2以降を対象にしています。センサーは現在までBME280のみ対応しています。

ダッシュボードの構築はこちらを参考にしてください -> 

## 必要なもの

- Raspberry PI
  - 検証済み: 3B, zero w
- Raspberry Pi OS
  - 検証済み: 2020-08-20以降
- BME280: 現在はSPI接続で利用します
  - [AE-BME280（秋月電子通商）](https://akizukidenshi.com/catalog/g/gK-09421/)
- Raspberry Pi とセンサーをつなぐための部品
  - ブレットボード
  - ジャンプワイヤー

## 利用したPythonパッケージ

[Pipfile](./Pipfile)で確認出来ます。

## 使い方

### Google Sheet APIとサービスアカウント認証の設定

- Googleサービスアカウントでの認証の準備をします
- Google Sheet APIを有効化します
- Googleドライブでスプレッドシートのファイルを作成、サービスアカウントのユーザー（専用のメールアドレス）を登録します

サービスアカウントの鍵情報をこのプロジェクトのルートディレクトリに配置します。名称を`oauth_service_account_key.json`に変更するとわかりやすいです

### Raspberry Piセットアップとセンサー接続

[Raspberry Pi OS](https://www.raspberrypi.org/software/)のセットアップを行います。現在だとRaspberry Pi imagerの利用が手軽です。

次にSPIの有効化を行います。`sudo raspi-config` より `Interfacing Options > SPI` へ進み`Enable`か確認してください。`Disable`なら`Enable`へ変更します。

最後にraspberry piとセンサーを接続します。BME280とはSPIを使って通信を行うので、SPI通信向けの接続をしてください。

GPIO番号 | GPIOの種類 | AE-BME280 | 備考
-- | -- | -- | --
1 | 3V3 | VDD |  
6 | GND | GND |  
29 | GPIO 5 | CSB | curcitpythonのbme280ライブラリの例で利用
19 | GPIO 19(MOSI) | SDI |  
21 | GPIO 21(MOSO) | SDO |  
23 | GPIO 23(SLCK) | SCK |  

### Pythonで環境作成

システムのPython環境を設定します。このプロジェクトではPython3を利用しているので、python3のインストールを行い、`python`コマンドをpython3で起動できるようにします.

```bash
sudo update-alternatives --install /usr/bin/python python $(which python2) 1
sudo update-alternatives --install /usr/bin/python python $(which python3) 2
sudo update-alternatives --config python
```

システムのpythonにpipenvをインストールします

```bash
sudo apt-get install python3-pip
```

システムのPythonにpipenvでパッケージをインストールします

```bash
sudo pip3 install -r ./requirements.txt
```

### ライブラリの確認テスト

`blinka_test.py`を実行して、Raspberry PiのSPI有効とライブラリが正しく動作するか確認します。

```bash
sudo python blinka_test.py

Hello blinka!
Digital IO ok!
SPI ok!
done!
```

### センサーとの接続テスト

`test_bme280.py`を実行して、温度、湿度、気圧がそれぞれ表示されるか確認します。

```bash
sudo python test_bme280.py

Temperature: 22.7 C
Humidity: 38.3 %
Pressure: 1022.4 hPa
# 数字は実行時の状況で変わります
```

### 実行

`recode_bme280_to_gsheet.py`を実行してGoogle Sheetへ温度、湿度、気圧が記録されるか確認します。

```bash
sudo python ./recode_bme280_to_gsheet.py
```

<!-- TODO:2020-12-05 記録された画像を乗せる -->

### スクリプトを定期実行

スクリプトを定期実行させるにはcrontabを使います。

```cron
# 30分ごとの実行例
*/30 * * * * /usr/bin/python [/path/to/script]recode_bme280_to_gsheet.py
```

## 参考

- [サービス アカウントについて  |  Cloud IAM のドキュメント  |  Google Cloud](https://cloud.google.com/iam/docs/understanding-service-accounts?hl=ja#background)
- [Installing CircuitPython Libraries on Raspberry Pi | CircuitPython on Linux and Raspberry Pi | Adafruit Learning System](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
- [Python & CircuitPython Test | Adafruit BME280 Humidity + Barometric Pressure + Temperature Sensor Breakout | Adafruit Learning System](https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/python-circuitpython-test)
- [Raspberry Pi OS](https://www.raspberrypi.org/software/)
- [SPI - Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md)
- [raspi-config - Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)
- [GPIO - Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)
- [ＢＭＥ２８０使用　温湿度・気圧センサモジュールキット: センサ一般 秋月電子通商-電子部品・ネット通販](https://akizukidenshi.com/catalog/g/gK-09421/)
- [Crontab Generator - Generate crontab syntax](https://crontab-generator.org/)
