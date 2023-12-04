import serial
import pynmea2
from datetime import datetime
import pytz

def parse_nmea_sentence(sentence):
    try:
        nmea_sentence = pynmea2.parse(sentence)
        
        if isinstance(nmea_sentence, pynmea2.GGA):
            utc_time = datetime.combine(datetime.utcnow().date(), nmea_sentence.timestamp)
            sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(sao_paulo_tz)
            
            time_formatted = local_time.strftime('%H:%M:%S')
            date_formatted = local_time.strftime('%d/%m/%Y')  # Alteração no formato da data
            latitude = "{:.7f}".format(round(nmea_sentence.latitude, 7))
            latitude_dir = nmea_sentence.lat_dir
            longitude = "{:.7f}".format(round(nmea_sentence.longitude, 7))
            longitude_dir = nmea_sentence.lon_dir
            satellites = nmea_sentence.num_sats
            
            print(f"Data: {date_formatted}")
            print(f"Hora: {time_formatted}")
            print(f"Latitude: {latitude} {latitude_dir}")
            print(f"Longitude: {longitude} {longitude_dir}")
            print(f"Satélites: {satellites}")
    except pynmea2.ParseError:
        # Ignora sentenças NMEA inválidas
        pass

# Porta serial onde o módulo GPS u-blox 7 está conectado (ajuste para a porta correta)
serial_port = '/dev/ttyACM0'

# Configuração da conexão serial
ser = serial.Serial(serial_port, baudrate=4800, timeout=1)

try:
    while True:
        # Lê uma linha (sentença NMEA) da porta serial
        nmea_sentence = ser.readline().decode('utf-8').strip()

        # Verifica se a sentença NMEA começa com o caractere '$' (uma sentença válida)
        if nmea_sentence.startswith('$'):
            parse_nmea_sentence(nmea_sentence)
except KeyboardInterrupt:
    # Encerra o programa quando o usuário pressiona Ctrl+C
    ser.close()
    print("\nPrograma encerrado.")
