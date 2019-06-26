import csv
import time
import requests

print("--------------------------------------")
print("| Generador de Release Packages v1.0 |")
print("--------------------------------------")

with open("/home/dba/Documents/EDCA/CSV/ocids_2018.csv","r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    with open("/home/dba/Documents/EDCA/2018/ocid_sefin_2018.json", "w") as WriteJson:
        for row in csv_reader:
            t1_start = time.perf_counter()
            t2_start = time.process_time()
            print('OCID a Generar: ' + str(row[0]))
            url = 'http://192.168.137.131:8006/SefinWebApi/api/releasePackage/' + str(row[0])
            req = requests.get(url)
            print("Response: " + str(req.status_code))
            # Convert bytes to string type and string type to dict
            req.encoding = 'utf-8'
            WriteJson.write(str(req.text) + "\n")
            line_count += 1
            t1_stop = time.perf_counter()
            t2_stop = time.process_time()
            print("Elapsed time: %.1f [segundos]" % (t1_stop - t1_start))
            print("CPU process time: %.1f [milisegundos]" % ((t2_stop - t2_start) * 1000))
            print(f'OCIDs procesados: --> {line_count}')
            print("\n")
        print(f'Cantidad de OCIDs {line_count} procesados.')
    WriteJson.close()
    print("Archivo JSON Finalizado.")

