import datetime

import adafruit_bme280
import board
import busio
import digitalio

from googleapiclient.discovery import build
from google.oauth2 import service_account

# prepare config
import config

# spiでbme280を操作する
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# D5は任意のGPIOピン
cs = digitalio.DigitalInOut(board.D5)
bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)

# google authの認証をしてAPIサービスの生成
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_RANGE_NAME = "A:D"
VALUE_INPUT_OPTION = "RAW"
INSERT_DATA_OPTION = "INSERT_ROWS"

credentials = service_account.Credentials.from_service_account_file(
    config.SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("sheets", "v4", credentials=credentials)


# 特定のシートで書き込みできるか調べる
sheet = service.spreadsheets()

print("time:{:%Y-%m-%d: %H:%M:%S}".format(datetime.datetime.now()))
print("Temperature: %0.1f C" % bme280.temperature)
print("Humidity: %0.1f %%" % bme280.humidity)
print("Pressure: %0.1f hPa\n" % bme280.pressure)

body = {
    "values": [
        [
            "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()),
            "{:0.1f}".format(bme280.temperature),
            "{:0.1f}".format(bme280.pressure),
            "{:0.1f}".format(bme280.humidity),
        ]
    ],
}
result = (
    service.spreadsheets()
    .values()
    .append(
        spreadsheetId=config.SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME,
        valueInputOption=VALUE_INPUT_OPTION,
        insertDataOption=INSERT_DATA_OPTION,
        body=body,
    )
    .execute()
)
